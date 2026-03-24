import cv2


def check_liveness(image_path):
    try:
        img = cv2.imread(image_path)

        if img is None:
            return {"live": False, "error": "Image not loaded"}

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blur_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        # brightness check
        brightness = gray.mean()

        if blur_var > 60 and brightness > 50:
            return {"live": True}
        else:
            return {
                "live": False,
                "reason": "Blurry or dark image"
            }

    except Exception as e:
        return {"live": False, "error": str(e)}