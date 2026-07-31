import base64
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

base_options = python.BaseOptions(model_asset_path='detector.tflite')
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

def process_frame(data_url: str) -> str:
    encoded_data = data_url.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    
    detection_result = detector.detect(mp_image)

    if detection_result.detections:
        ih, iw, _ = img.shape
        for detection in detection_result.detections:
            bbox = detection.bounding_box
            x, y = bbox.origin_x, bbox.origin_y
            w, h = bbox.width, bbox.height
            
            x, y = max(0, x), max(0, y)
            
            if y + h <= ih and x + w <= iw:
                rostro = img[y:y+h, x:x+w]
                if rostro.size != 0:
                    rostro_blur = cv2.GaussianBlur(rostro, (99, 99), 30)
                    img[y:y+h, x:x+w] = rostro_blur

    _, buffer = cv2.imencode('.jpg', img)
    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')