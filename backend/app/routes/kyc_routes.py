from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.ocr_service import extract_ocr_data
from app.services.face_service import compare_faces
from app.services.liveness import check_liveness
from app.services.fraud_detection import calculate_risk

router = APIRouter()

UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_file(file: UploadFile, filename: str):
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path


@router.get("/test")
def test():
    return {"message": "API working"}


@router.post("/verify")
async def verify_kyc(
    id_image: UploadFile = File(...),
    selfie: UploadFile = File(...)
):
    id_path = save_file(id_image, "id.jpg")
    selfie_path = save_file(selfie, "selfie.jpg")

    # OCR
    ocr = extract_ocr_data(id_path)

    # Face match
    face = compare_faces(id_path, selfie_path)

    # Liveness
    live = check_liveness(selfie_path)

    # Fraud score
    risk = calculate_risk(face["match"], live, ocr["data"])

    return {
        "ocr": ocr,
        "face_match": face,
        "liveness": live,
        "risk_score": risk,
        "status": "Verified" if risk < 50 else "Rejected"
    }