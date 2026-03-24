import cv2
import easyocr
import re
import numpy as np

# Initialize OCR reader
reader = easyocr.Reader(['en'], gpu=False)


# 🔥 ROTATION CORRECTION
def correct_rotation(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = np.column_stack(np.where(gray > 0))

    if len(coords) == 0:
        return img

    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h),
                          flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)


# 🔥 SMART CROP
def crop_id_region(img):
    h, w = img.shape[:2]
    return img[int(h * 0.2):int(h * 0.9), int(w * 0.05):int(w * 0.95)]


# 🔥 PREPROCESS
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return thresh


# 🔥 OCR
def extract_text(img):
    processed = preprocess_image(img)

    result = reader.readtext(processed, detail=0)

    if len(result) < 3:
        result += reader.readtext(img, detail=0)

    return " ".join(result).upper()


# 🔥 CLEAN TEXT
def clean_text(text):
    text = re.sub(r'[^A-Z0-9/\-\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


# =========================
# 🔥 DOCUMENT DETECTION
# =========================
def detect_document_type(text):
    text = text.upper()

    pan_pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'

    if re.search(pan_pattern, text):
        return "PAN"

    if "AADHAAR" in text or "GOVERNMENT OF INDIA" in text:
        return "AADHAAR"

    return "UNKNOWN"


# =========================
# 🔥 AADHAAR (UNCHANGED)
# =========================
def extract_aadhaar(text):
    match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', text)
    return match.group() if match else "Not Found"


def extract_dob(text):
    match = re.search(r'\b\d{2}[-/]\d{2}[-/]\d{4}\b', text)
    return match.group() if match else "Not Found"


def extract_name(text):
    words = text.split()
    blacklist = {"GOVERNMENT", "INDIA", "AADHAAR", "DOB"}

    candidates = [
        f"{words[i]} {words[i+1]}"
        for i in range(len(words)-1)
        if words[i].isalpha() and words[i+1].isalpha()
        and words[i] not in blacklist
        and words[i+1] not in blacklist
    ]

    return max(candidates, key=len) if candidates else "Not Found"


# =========================
# 🔥 PAN LOGIC
# =========================
def extract_pan(text):
    match = re.search(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', text)
    return match.group() if match else "Not Found"


def extract_pan_name(text):
    words = text.split()

    blacklist = {
        "INCOME", "TAX", "DEPARTMENT", "INDIA",
        "PERMANENT", "ACCOUNT", "NUMBER"
    }

    candidates = []

    for i in range(len(words)-1):
        w1, w2 = words[i], words[i+1]

        if (
            w1.isalpha() and w2.isalpha()
            and w1 not in blacklist
            and w2 not in blacklist
        ):
            candidates.append(w1 + " " + w2)

    return max(candidates, key=len) if candidates else "Not Found"


def extract_pan_dob(text):
    match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', text)
    return match.group() if match else "Not Found"


# =========================
# 🔥 MAIN FUNCTION (ROUTING)
# =========================
def extract_ocr_data(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return {"error": "Image not loaded"}

    # Preprocessing
    img = correct_rotation(img)
    img = crop_id_region(img)
    img = cv2.resize(img, None, fx=2, fy=2)

    text = clean_text(extract_text(img))

    # 🔥 DETECT DOCUMENT TYPE
    doc_type = detect_document_type(text)

    # 🔥 ROUTE
    if doc_type == "AADHAAR":
        return {
            "document_type": "AADHAAR",
            "raw_text": text,
            "data": {
                "name": extract_name(text),
                "dob": extract_dob(text),
                "aadhaar": extract_aadhaar(text)
            }
        }

    elif doc_type == "PAN":
        return {
            "document_type": "PAN",
            "raw_text": text,
            "data": {
                "name": extract_pan_name(text),
                "dob": extract_pan_dob(text),
                "pan": extract_pan(text)
            }
        }

    else:
        return {
            "document_type": "UNKNOWN",
            "raw_text": text,
            "error": "Document not recognized"
        }