import cv2
import easyocr
import re
import numpy as np

# =========================
# 🔥 INIT OCR
# =========================
reader = easyocr.Reader(['en'], gpu=False)


# =========================
# 🔥 ROTATION CORRECTION
# =========================
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


# =========================
# 🔥 SMART CROP
# =========================
def crop_id_region(img):
    h, w = img.shape[:2]
    return img[int(h * 0.2):int(h * 0.95), int(w * 0.05):int(w * 0.95)]


# =========================
# 🔥 ROI SPLIT
# =========================
def extract_roi(img):
    h, w = img.shape[:2]

    return {
        "top": img[0:int(h * 0.35), :],
        "middle": img[int(h * 0.3):int(h * 0.7), :],
        "bottom": img[int(h * 0.6):h, :]
    }


# =========================
# 🔥 PREPROCESS
# =========================
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


# =========================
# 🔥 OCR WITH CONFIDENCE
# =========================
def ocr_lines(img):
    processed = preprocess_image(img)

    results = reader.readtext(processed, detail=1)

    lines = []
    for (bbox, text, conf) in results:
        if conf > 0.55:  # strict filter
            lines.append(text.upper())

    # fallback
    if len(lines) < 2:
        results = reader.readtext(img, detail=1)
        lines = [text.upper() for (_, text, conf) in results if conf > 0.3]

    return lines


# =========================
# 🔥 CLEAN TEXT
# =========================
def clean_lines(lines):
    cleaned = []

    for line in lines:
        line = re.sub(r'[^A-Z0-9/\-\s]', ' ', line)
        line = re.sub(r'\s+', ' ', line).strip()

        if len(line) < 4:
            continue

        # remove garbage like "F I N C T"
        if re.search(r'[A-Z]\s[A-Z]\s[A-Z]', line):
            continue

        cleaned.append(line)

    return cleaned


# =========================
# 🔥 DOCUMENT DETECTION
# =========================
def detect_document_type(lines):
    text = " ".join(lines)

    if re.search(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', text):
        return "PAN"

    if "AADHAAR" in text or "GOVERNMENT OF INDIA" in text:
        return "AADHAAR"

    return "UNKNOWN"


# =========================
# 🔥 AADHAAR EXTRACTION
# =========================
def extract_aadhaar(lines):
    for line in lines:
        match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', line)
        if match:
            return match.group()
    return "Not Found"


def extract_dob(lines):
    for line in lines:
        match = re.search(r'\b\d{2}[-/]\d{2}[-/]\d{4}\b', line)
        if match:
            d, m, y = re.split(r'[-/]', match.group())
            if 1 <= int(d) <= 31 and 1 <= int(m) <= 12:
                return match.group()
    return "Not Found"


def extract_name(lines):
    blacklist = {
        "INDIA", "AADHAAR", "GOVERNMENT",
        "DOB", "MALE", "FEMALE"
    }

    candidates = []

    for line in lines:
        words = line.split()

        if 2 <= len(words) <= 4:
            if all(w.isalpha() for w in words):
                if not any(w in blacklist for w in words):
                    candidates.append(" ".join(words))

    return max(candidates, key=len) if candidates else "Not Found"


# =========================
# 🔥 PAN EXTRACTION
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
# 🔥 MAIN FUNCTION
# =========================
def extract_ocr_data(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return {"error": "Image not loaded"}

    # preprocessing
    img = correct_rotation(img)
    img = crop_id_region(img)
    img = cv2.resize(img, None, fx=2, fy=2)

    rois = extract_roi(img)

    all_lines = []

    for region in rois.values():
        lines = ocr_lines(region)
        all_lines.extend(lines)

    lines = clean_lines(all_lines)

    doc_type = detect_document_type(lines)

    if doc_type == "AADHAAR":
        name = extract_name(lines)
        dob = extract_dob(lines)
        aadhaar = extract_aadhaar(lines)

        confidence = sum([
            name != "Not Found",
            dob != "Not Found",
            aadhaar != "Not Found"
        ]) / 3

        return {
            "document_type": "AADHAAR",
            "confidence": confidence,
            "raw_lines": lines,
            "data": {
                "name": name,
                "dob": dob,
                "aadhaar": aadhaar
            }
        }

    elif doc_type == "PAN":
        text = " ".join(lines)

        return {
            "document_type": "PAN",
            "raw_lines": lines,
            "data": {
                "pan": extract_pan(text),
                "name": extract_pan_name(text),
                "dob": extract_pan_dob(text)
            }
        }

    else:
        return {
            "document_type": "UNKNOWN",
            "raw_lines": lines,
            "error": "Document not recognized"
        }