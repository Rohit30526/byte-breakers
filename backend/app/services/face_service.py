import face_recognition
import cv2
import numpy as np


# 🔥 IMAGE ENHANCEMENT
def enhance_image(img):
    # Resize for better detection
    img = cv2.resize(img, None, fx=1.5, fy=1.5)

    # Convert to RGB (important)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


# 🔥 EXTRACT BEST FACE ENCODING
def get_face_encoding(image):
    locations = face_recognition.face_locations(image, model="hog")

    if len(locations) == 0:
        return None, 0

    encodings = face_recognition.face_encodings(image, locations)

    # Use average encoding (better stability)
    encoding = np.mean(encodings, axis=0)

    return encoding, len(locations)


# 🔥 MAIN FUNCTION
def compare_faces(id_path, selfie_path):
    try:
        # Load images
        id_img = cv2.imread(id_path)
        selfie_img = cv2.imread(selfie_path)

        if id_img is None or selfie_img is None:
            return {
                "match": False,
                "confidence": 0,
                "error": "Image not loaded"
            }

        # Enhance
        id_img = enhance_image(id_img)
        selfie_img = enhance_image(selfie_img)

        # Get encodings
        id_encoding, id_faces = get_face_encoding(id_img)
        selfie_encoding, selfie_faces = get_face_encoding(selfie_img)

        # ❌ No face detected
        if id_encoding is None or selfie_encoding is None:
            return {
                "match": False,
                "confidence": 0,
                "error": "Face not detected"
            }

        # ❌ Multiple faces (fraud)
        if id_faces > 1 or selfie_faces > 1:
            return {
                "match": False,
                "confidence": 0,
                "error": "Multiple faces detected"
            }

        # 🔥 FACE DISTANCE
        distance = face_recognition.face_distance(
            [id_encoding],
            selfie_encoding
        )[0]

        # 🔥 ADAPTIVE THRESHOLD
        if distance < 0.45:
            match = True
        elif distance < 0.6:
            match = True
        else:
            match = False

        # 🔥 CONFIDENCE SCORE
        confidence = (1 - distance) * 100
        confidence = round(float(confidence), 2)

        return {
            "match": match,
            "confidence": confidence,
            "distance": round(float(distance), 4),
            "faces_detected": {
                "id": id_faces,
                "selfie": selfie_faces
            }
        }

    except Exception as e:
        return {
            "match": False,
            "confidence": 0,
            "error": str(e)
        }