from deepface import DeepFace
import cv2
import os
import uuid


# 🔥 EXTRACT FACE FROM IMAGE
def extract_face(image_path):
    try:
        faces = DeepFace.extract_faces(
            img_path=image_path,
            detector_backend="retinaface",   # best accuracy
            enforce_detection=True
        )

        if not faces:
            return None

        # ✅ Pick largest face (important improvement)
        largest_face = max(faces, key=lambda x: x["facial_area"]["w"] * x["facial_area"]["h"])

        face = largest_face["face"]

        # Convert from float (0–1) → uint8 (0–255)
        face = (face * 255).astype("uint8")

        # Save temp file
        temp_path = f"temp_{uuid.uuid4().hex}.jpg"
        cv2.imwrite(temp_path, face)

        return temp_path

    except Exception as e:
        print("Face extraction error:", e)
        return None


# 🔥 MAIN FUNCTION (ID vs SELFIE)
def compare_id_with_selfie(id_path, selfie_path):
    id_face_path = None
    selfie_face_path = None

    try:
        # 🔹 Extract face from ID
        id_face_path = extract_face(id_path)
        if id_face_path is None:
            return {
                "match": False,
                "error": "No face found in ID card"
            }

        # 🔹 Extract face from selfie
        selfie_face_path = extract_face(selfie_path)
        if selfie_face_path is None:
            return {
                "match": False,
                "error": "No face found in selfie"
            }

        # 🔥 Face comparison
        result = DeepFace.verify(
            img1_path=id_face_path,
            img2_path=selfie_face_path,
            model_name="ArcFace",           # 🔥 best accuracy
            detector_backend="retinaface",
            enforce_detection=True
        )

        distance = result["distance"]
        confidence = round((1 - distance) * 100, 2)

        return {
            "match": result["verified"],
            "confidence": confidence,
            "distance": round(distance, 4)
        }

    except Exception as e:
        return {
            "match": False,
            "error": str(e)
        }

    finally:
        # 🔥 Cleanup temp files (VERY IMPORTANT)
        if id_face_path and os.path.exists(id_face_path):
            os.remove(id_face_path)

        if selfie_face_path and os.path.exists(selfie_face_path):
            os.remove(selfie_face_path)