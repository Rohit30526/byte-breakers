def calculate_risk(face_match, liveness, text_data):
    score = 0

    # Face mismatch
    if not face_match:
        score += 40

    # Liveness failed
    if not liveness:
        score += 30

    # Missing OCR data
    if text_data.get("name") == "Not Found":
        score += 20

    if text_data.get("aadhaar") == "Not Found":
        score += 10

    return score