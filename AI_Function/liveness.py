import cv2
import os
import dlib
import numpy as np
from imutils import face_utils

# Load models
detector = dlib.get_frontal_face_detector()
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "shape_predictor_68_face_landmarks.dat")

predictor = dlib.shape_predictor(model_path)
# Eye aspect ratio
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

# Eye indexes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

cap = cv2.VideoCapture(0)

# Improve camera quality
cap.set(3, 640)
cap.set(4, 480)

# Steps
steps = ["BLINK", "RIGHT", "LEFT", "UP",]
current_step = 0

EAR_THRESHOLD = 0.26
CONSEC_FRAMES = 2
frame_counter = 0

initial_nose = None

print("Follow instructions on screen...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

        # Nose
        nose = shape[30]

        # Calibration
        if initial_nose is None:
            initial_nose = nose

        dx = nose[0] - initial_nose[0]
        dy = nose[1] - initial_nose[1]

        THRESH_X = 15
        THRESH_Y = 15

        step = steps[current_step]

        # -------- STEP LOGIC -------- #

        if step == "BLINK":
            if ear < EAR_THRESHOLD:
                frame_counter += 1
            else:
                if frame_counter >= CONSEC_FRAMES:
                    print("Blink detected ✅")
                    current_step += 1
                    initial_nose = None
                frame_counter = 0

        elif step == "RIGHT":
            if dx > THRESH_X:
                print("Right detected ✅")
                current_step += 1
                initial_nose = None

        elif step == "LEFT":
            if dx < -THRESH_X:
                print("Left detected ✅")
                current_step += 1
                initial_nose = None

        elif step == "UP":
            if dy < -THRESH_Y:
                print("Up detected ✅")
                current_step += 1
                initial_nose = None

    # -------- UI -------- #

    if current_step < len(steps):
        instruction = f"Do: {steps[current_step]}"
    else:
        instruction = "LIVENESS VERIFIED"

    cv2.putText(frame, instruction, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Liveness Check", frame)

    if current_step >= len(steps):
        print("✅ Liveness Verified")
        break

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
