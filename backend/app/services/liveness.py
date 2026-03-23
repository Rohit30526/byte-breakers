import cv2

def check_liveness(image_path):
    try:
        img = cv2.imread(image_path)

        if img is None:
            return False

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Blur detection (simple liveness)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()

        if variance > 50:
            return True
        else:
            return False

    except Exception as e:
        print("Liveness error:", e)
        return False