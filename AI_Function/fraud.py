def calculate_fraud_score(num_faces, blink_count, eye_closed_frames):
    fraud_score = 0

    # No face
    if num_faces == 0:
        fraud_score += 30

    # Multiple faces
    if num_faces > 1:
        fraud_score += 40

    # No blink
    if blink_count == 0:
        fraud_score += 20

    # Eyes closed too long
    if eye_closed_frames > 15:
        fraud_score += 25

    fraud_score = min(fraud_score, 100)

    # Risk level
    if fraud_score < 30:
        risk = "LOW"
    elif fraud_score < 70:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return fraud_score, risk