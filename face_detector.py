import cv2
import numpy as np
import requests

def detect_face(image_url):
    try:
        resp = requests.get(image_url, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        return len(faces) > 0
    except Exception as e:
        print(f"Error detecting face: {e}")
        return False

if __name__ == "__main__":
    test_url = "https://example.com/sample.jpg"
    print(detect_face(test_url))
