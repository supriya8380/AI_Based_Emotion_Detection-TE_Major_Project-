from flask import Flask, render_template, request
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

# ✅ Load trained model
model = load_model('model_file.keras')

# ✅ Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Class labels
class_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Upload folder
UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')  # Home page

@app.route('/detection')
def detection():
    return render_template('detection.html')  # Detection page

@app.route('/resources')
def resources():
    return render_template('resources.html')


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('image')

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # ✅ Read image
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ✅ Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) == 0:
            return render_template(
                'result.html',
                prediction="No Face Detected",
                img_path=filepath,
                confidence=0,
                message="No face found in the image",
                probs={}
            )

        # ✅ Take largest face
        faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
        (x, y, w, h) = faces[0]

        face = gray[y:y+h, x:x+w]

        # ✅ Preprocessing
        face = cv2.resize(face, (48, 48))
        face = cv2.equalizeHist(face)
        face = face / 255.0
        face = np.reshape(face, (1, 48, 48, 1))

        # ✅ Prediction
        prediction = model.predict(face, verbose=0)[0]
        predicted_class = np.argmax(prediction)
        result = class_labels[predicted_class]
        confidence = round(float(np.max(prediction) * 100), 2)

        if confidence < 60:
            result = "Not Sure"

        top_indices = prediction.argsort()[-4:][::-1]
        probs = {class_labels[i]: round(float(prediction[i] * 100), 2) for i in top_indices}

        messages = {
            'Angry': "You seem angry. Try to relax!",
            'Happy': "You seem happy today! 😊",
            'Sad': "You look a bit sad. Stay strong 💙",
            'Fear': "You seem scared. It's okay!",
            'Neutral': "You look calm and neutral.",
            'Surprise': "You look surprised!",
            'Disgust': "That expression shows discomfort.",
            'Not Sure': "I'm not fully confident. Try another image."
        }

        message = messages.get(result, "")

        return render_template(
            'result.html',
            prediction=result,
            confidence=confidence,
            message=message,
            img_path=filepath,
            probs=probs
        )

    return "Error: No image uploaded"


if __name__ == '__main__':
    app.run(debug=True)