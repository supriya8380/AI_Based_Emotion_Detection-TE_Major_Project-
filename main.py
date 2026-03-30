import cv2
import numpy as np
from ultralytics import YOLO
from tensorflow.keras.models import load_model

# Load YOLOv8 model (face detection)
yolo_model = YOLO("yolov8n.pt")  # make sure file exists

# Load Emotion Model
emotion_model = load_model("emotion_model.hdf5")

# Emotion labels
emotions = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO detection
    results = yolo_model(frame)

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()

        for box in boxes:
            x1, y1, x2, y2 = map(int, box)

            # Crop face
            face = frame[y1:y2, x1:x2]

            if face.size == 0:
                continue

            # Preprocess for emotion model
            face = cv2.resize(face, (48, 48))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            face = face / 255.0
            face = np.reshape(face, (1, 48, 48, 1))

            # Predict emotion
            preds = emotion_model.predict(face)
            emotion_index = np.argmax(preds)
            emotion = emotions[emotion_index]

            # Draw bounding box + label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, emotion, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Show output
    cv2.imshow("Emotion Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
