import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from model_def import build_emotion_model
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Path to model weights
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "model.h5")

# Build model and load weights
model = build_emotion_model()
model.load_weights(MODEL_PATH)

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(gray, (48, 48))
    face = face.astype("float") / 255.0
    face = np.expand_dims(face, axis=0)
    face = np.expand_dims(face, axis=-1)
    return face


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files['file']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    face = preprocess_image(img)
    preds = model.predict(face)[0]
    emotion = emotion_labels[np.argmax(preds)]
    confidence = float(np.max(preds))
    return jsonify({"emotion": emotion, "confidence": confidence})


# 🧠 Emotional Support Chatbot Route
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "")

    # Friendly and safe personality prompt
    system_prompt = (
        "You are a compassionate emotional support companion. "
        "Always reply kindly, warmly, and gently. "
        "Avoid medical or clinical advice. "
        "Use empathy, short paragraphs, and encouraging tone."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.8,
            max_tokens=150,
        )

        ai_reply = response.choices[0].message.content.strip()
        return jsonify({"reply": ai_reply})

    except Exception as e:
        print("Chatbot error:", e)
        return jsonify({"reply": "I'm here for you, but I'm having trouble responding right now 💛"})


if __name__ == "__main__":
    app.run(debug=True)
