import cv2
import easyocr
import re
import numpy as np

import os

# 📁 Create data folder path
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

os.makedirs(DATA_DIR, exist_ok=True)

from tkinter import Tk
from tkinter.filedialog import askopenfilename

# ✅ Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=False)

# -------------------------
# 🖼️ AADHAAR PHOTO EXTRACTOR
# -------------------------
def extract_aadhaar_photo(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # detect faces
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    # take first detected face
    x, y, w, h = faces[0]

    face_img = img[y:y+h, x:x+w]

    return face_img


# -------------------------
# 🔹 COMMON OCR FUNCTION
# -------------------------
def extract_text(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    result1 = reader.readtext(img, detail=1)
    result2 = reader.readtext(gray, detail=1)

    texts = []

    for res in result1 + result2:
        bbox, txt, conf = res

        # 🔥 Confidence filter (very important)
        if conf > 0.5:
            texts.append(txt)

    return "\n".join(texts).upper()


# -------------------------
# 🔵 AADHAAR EXTRACTION
# -------------------------
def extract_aadhaar(text):

    clean_text = re.sub(r'\b[6-9]\d{9}\b', '', text)

    # Aadhaar number
    aadhaar_match = re.findall(r'\d{4}\s?\d{4}\s?\d{4}', clean_text)
    aadhaar = aadhaar_match[0] if aadhaar_match else "Not Found"

    if aadhaar != "Not Found":
        aadhaar = re.sub(r'\D', '', aadhaar)  # remove spaces

    # DOB
    dob = re.findall(r'\d{2}[/\-]\d{2}[/\-]\d{4}', text)
    dob = dob[0] if dob else "Not Found"

    # -------------------------
    # 🚻 GENDER EXTRACTION (FINAL FIX)
    # -------------------------
    gender = "Not Found"

    # normalize text
    clean_text = re.sub(r'[^A-Z]', ' ', text.upper())

    words = clean_text.split()

    for w in words:
        # FEMALE patterns
        if re.match(r'F+E*M+A*L*E*', w):
            gender = "Female"
            break

        # MALE patterns (avoid matching inside FEMALE)
        elif re.match(r'M+A*L*E*', w):
            gender = "Male"
            break
    
    # 🔤 AGGRESSIVE NAME FILTER (AADHAAR)

    lines = text.split("\n")
    name = "Not Found"

    stopwords = [
        "MALE","FEMALE","INDIA","GOVERNMENT","AADHAAR",
        "DOB","YEAR","BIRTH","UNIQUE","IDENTIFICATION"
    ]

    candidates = []

    for i, line in enumerate(lines):
        clean = re.sub(r'[^A-Z ]', '', line).strip()
        words = clean.split()

        # strict rules
        if not (2 <= len(words) <= 3):
            continue

        if any(w in stopwords for w in words):
            continue

        if any(len(w) < 3 for w in words):
            continue

        # reject repeated chars (AAA, XXX)
        if re.search(r'(.)\1{2,}', clean):
            continue

        # position-based scoring (top = better)
        score = 100 - i * 5

        candidates.append((score, clean))

    if candidates:
        candidates.sort(reverse=True)
        name = candidates[0][1]

    # 🔥 HARD RULE: NAME IS ABOVE DOB (Aadhaar layout)
    for i, line in enumerate(lines):
        if re.search(r'\d{2}[/\-]\d{2}[/\-]\d{4}', line):
            if i > 0:
                possible = re.sub(r'[^A-Z ]', '', lines[i-1]).strip()
                words = possible.split()

                if 2 <= len(words) <= 3 and all(len(w) >= 3 for w in words):
                    name = possible
            break
    # fallback (above DOB)
    if name == "Not Found":
        for i, line in enumerate(lines):
            if "DOB" in line:
                if i > 0:
                    name = re.sub(r'[^A-Z ]', '', lines[i-1]).strip()
                    break

    return {
        "name": name,
        "dob": dob,
        "gender":gender,
        "aadhaar": aadhaar,
    }


# -------------------------
# 🟣 PAN EXTRACTION
# -------------------------
def extract_pan(text):

    # PAN number
    pan_match = re.findall(r'[A-Z]{5}[0-9]{4}[A-Z]', text)
    pan = pan_match[0] if pan_match else "Not Found"

    # Name (PAN usually ALL CAPS)
    lines = text.split("\n")
    # -------------------------
    # 👨 FATHER NAME DETECTION
    # -------------------------

    father_name = "Not Found"

    stopwords = [
        "INCOME", "TAX", "DEPARTMENT", "INDIA", "GOVT",
        "GOVERNMENT", "PERMANENT", "ACCOUNT", "NUMBER"
    ]

    valid_lines = []

    for line in lines:
        clean = re.sub(r'[^A-Z ]', '', line).strip()
        words = clean.split()

        # valid name-like line
        if 2 <= len(words) <= 4:
            if any(w in stopwords for w in words):
                continue
            if any(len(w) < 3 for w in words):
                continue

            valid_lines.append(clean)

    # PAN structure: name = first, father = second
    if len(valid_lines) >= 2:
        father_name = valid_lines[1]


    name = "Not Found"

    stopwords = [
        "INCOME", "TAX", "DEPARTMENT", "INDIA", "GOVT",
        "GOVERNMENT", "PERMANENT", "ACCOUNT", "NUMBER"
    ]

    candidates = []

    for i, line in enumerate(lines):
        clean = re.sub(r'[^A-Z ]', '', line).strip()
        words = clean.split()

        # strict rules
        if not (2 <= len(words) <= 4):
            continue

        if any(w in stopwords for w in words):
            continue

        if any(len(w) < 3 for w in words):
            continue

        # reject repeated garbage
        if re.search(r'(.)\1{2,}', clean):
            continue

        # 🔥 PAN name is usually near top-middle
        score = 100 - abs(i - 3) * 10

        candidates.append((score, clean))

    if candidates:
        candidates.sort(reverse=True)
        name = candidates[0][1]

    

    return {
        "name": name,
        "father_name": father_name, 
        "pan": pan
    }


# -------------------------
# 📤 MAIN FLOW
# -------------------------
if __name__ == "__main__":

    Tk().withdraw()

    # 🔵 Upload Aadhaar
    print("📤 Upload Aadhaar Card")
    aadhaar_path = askopenfilename(
        title="Select Aadhaar Card",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if not aadhaar_path:
        print("Aadhaar not selected ❌")
        exit()

    # 🔵 Upload PAN
    print("📤 Upload PAN Card")
    pan_path = askopenfilename(
        title="Select PAN Card",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if not pan_path:
        print("PAN not selected ❌")
        exit()

    # -------------------------
    # PROCESS AADHAAR
    # -------------------------
    img1 = cv2.imread(aadhaar_path)
    img1 = cv2.resize(img1, None, fx=2, fy=2)

   # ✅ Extract photo
    face = extract_aadhaar_photo(img1)

    if face is not None:
        face_path = os.path.join(DATA_DIR, "aadhaar_photo.jpg")
        cv2.imwrite(face_path, face)
        print("✅ Aadhaar face saved at:", face_path)
    else:
        print("❌ No face detected in Aadhaar")
    # ✅ Extract Aadhaar text (MISSING PART)
    text1 = extract_text(img1)
    aadhaar_data = extract_aadhaar(text1)

    # -------------------------
    # PROCESS PAN
    # -------------------------
    img2 = cv2.imread(pan_path)
    img2 = cv2.resize(img2, None, fx=2, fy=2)

    text2 = extract_text(img2)
    pan_data = extract_pan(text2)

    # -------------------------
    # 📦 FINAL OUTPUT
    # -------------------------
    print("\n🔵 Aadhaar Data:")
    for k, v in aadhaar_data.items():
        print(f"{k}: {v}")

    print("\n🟣 PAN Data:")
    for k, v in pan_data.items():
        print(f"{k}: {v}")