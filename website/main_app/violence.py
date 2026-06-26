import os
import cv2
from datetime import datetime
from django.conf import settings
from ultralytics import YOLO

# Load YOLO model ONCE
model = YOLO("yolov8violence_final.pt")


def detect_violence(video_path):
    cap = cv2.VideoCapture(video_path)
    violence_detected = False
    screenshot_path = None

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)

        if len(results[0].boxes) > 0:
            violence_detected = True

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(
                settings.MEDIA_ROOT, f"violence_{ts}.jpg"
            )

            cv2.imwrite(screenshot_path, frame)
            break

    cap.release()
    return violence_detected, screenshot_path


VIOLENCE_FRAME_COUNT = 0
REQUIRED_FRAMES = 3      
TRIGGER_CONFIDENCE = 0.40  



def detect_frame_violence(frame):
    global VIOLENCE_FRAME_COUNT

    if frame is None or frame.size == 0:
        return False, frame, None

    results = model(frame)
    frame_with_boxes = frame.copy()

    screenshot_path = None
    violence_in_this_frame = False

    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        label = results[0].names[cls].lower()

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if label == "violence" and conf >= 0.60:
            color = (0, 0, 255)  # RED
            text = f"VIOLENCE {conf:.2f}"
            violence_in_this_frame = True


        else:
            color = (0, 255, 0)  
            text = f"NON-VIOLENCE {conf:.2f}"

        # Draw box
        cv2.rectangle(frame_with_boxes, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            frame_with_boxes,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    if violence_in_this_frame:
        VIOLENCE_FRAME_COUNT += 1
    else:
        VIOLENCE_FRAME_COUNT = 0

    violence_detected = VIOLENCE_FRAME_COUNT >= REQUIRED_FRAMES

    if violence_detected:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        screenshot_path = os.path.join(
            settings.MEDIA_ROOT, f"violence_live_{ts}.jpg"
        )
        cv2.imwrite(screenshot_path, frame_with_boxes)

    return violence_detected, frame_with_boxes, screenshot_path


