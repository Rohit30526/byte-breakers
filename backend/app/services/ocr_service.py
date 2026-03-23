import cv2
import easyocr
import re
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)


# 🔥 SUPER PREPROCESSING
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # Noise removal
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # Adaptive threshold (better than normal)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Sharpen
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpen = cv2.filter2D(thresh, -1, kernel)

    return sharpen


# 🔥 MULTI OCR PASS
def extract_text(img):
    processed = preprocess_image(img)

    result1 = reader.readtext(processed, detail=0)
    result2 = reader.readtext(img, detail=0)

    text = " ".join(result1 + result2)

    return text.upper()


# 🔥 CLEAN TEXT
def clean_text(text):
    text = re.sub(r'[^A-Z0-9/\-\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# 🔥 AADHAAR (STRICT + FORMAT FIX)
def extract_aadhaar(text):
    matches = re.findall(r'\b\d{4}\s?\d{4}\s?\d{4}\b', text)

    if matches:
        aadhaar = matches[0]
        # format nicely
        aadhaar = re.sub(r'\s+', ' ', aadhaar)
        return aadhaar

    return "Not Found"


# 🔥 DOB (MULTIPLE PATTERNS)
def extract_dob(text):
    patterns = [
        r'\b\d{2}/\d{2}/\d{4}\b',
        r'\b\d{2}-\d{2}-\d{4}\b'
    ]

    for p in patterns:
        match = re.search(p, text)
        if match:
            return match.group()

    return "Not Found"


# 🔥 NAME (STRUCTURED DETECTION)
def extract_name(text):
    lines = text.split()

    blacklist = [
        "GOVERNMENT", "INDIA", "AADHAAR", "DOB",
        "MALE", "FEMALE", "YEAR", "UNIQUE",
        "IDENTIFICATION", "AUTHORITY"
    ]

    candidates = []

    for i in range(len(lines) - 1):
        w1, w2 = lines[i], lines[i+1]

        if (
            w1.isalpha() and w2.isalpha()
            and w1 not in blacklist
            and w2 not in blacklist
            and len(w1) > 2 and len(w2) > 2
        ):
            candidates.append(w1 + " " + w2)

    # Prefer longer names (more realistic)
    candidates = sorted(candidates, key=len, reverse=True)

    return candidates[0] if candidates else "Not Found"


# 🔥 FINAL FUNCTION
def extract_ocr_data(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return {
            "raw_text": "",
            "data": {
                "name": "Not Found",
                "dob": "Not Found",
                "aadhaar": "Not Found"
            }
        }

    # Resize for clarity
    img = cv2.resize(img, None, fx=2, fy=2)

    text = extract_text(img)
    text = clean_text(text)

    name = extract_name(text)
    dob = extract_dob(text)
    aadhaar = extract_aadhaar(text)

    return {
        "raw_text": text,
        "data": {
            "name": name,
            "dob": dob,
            "aadhaar": aadhaar
        }
    }