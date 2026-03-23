import cv2
import numpy as np
from insightface.app import FaceAnalysis

# Load model
app = FaceAnalysis()
app.prepare(ctx_id=0)  # CPU=0, GPU=-1

# Load images
img1 = cv2.imread("aadhaar_photo.jpg")
img2 = cv2.imread("selfie.jpg")

# Detect faces
faces1 = app.get(img1)
faces2 = app.get(img2)

if len(faces1) == 0 or len(faces2) == 0:
    print("❌ No face detected")
    exit()

# Get embeddings
emb1 = faces1[0].embedding
emb2 = faces2[0].embedding

# Cosine similarity
similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

print(f"Similarity: {similarity:.4f}")

# Threshold (important)
if similarity > 0.5:
    print("✅ Same person")
else:
    print("❌ Different person")