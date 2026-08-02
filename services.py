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
            
            # cálculo de padding dinámico ( 25% porprocional)
            pad_x = int(w * 0.25)
            pad_y = int(h * 0.25)
            
            # expansión de la caja, mayor margen superior para frente/cabello
            nuevo_x = max(0, x - pad_x)
            nuevo_y = max(0, int(y - (pad_y * 1.5)))
            
            # límite másximo anclado a la resolución del frame
            x_fin = min(iw, x + w + pad_x)
            y_fin = min(ih, x + h + pad_y)
            
            # se valida que la nea caja sea un área real
            if y_fin > nuevo_y and x_fin > nuevo_x:
                rostro = img[nuevo_y:y_fin, nuevo_x:x_fin]
                
                if rostro.size != 0:
                    rostro_blur = cv2.GaussianBlur(rostro, (99, 99), 30)
                    img[nuevo_y:y_fin, nuevo_x:x_fin] = rostro_blur
            
            
            
            
            
            
            
            

    _, buffer = cv2.imencode('.jpg', img)
    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')