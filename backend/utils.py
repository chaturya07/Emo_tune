import numpy as np
from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image
from dotenv import load_dotenv
import os
import requests
from io import BytesIO
from PIL import Image

# Load environment variables (.env file)
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Emotion labels (adjust if changed during training)
CLASS_LABELS = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

def load_model(model_path):
    return keras_load_model(model_path)

async def predict_emotion(model, file):
    contents = await file.read()
    img = Image.open(BytesIO(contents)).convert("L").resize((48, 48))

    img_array = np.expand_dims(np.expand_dims(np.array(img), -1), 0)
    img_array = img_array.astype("float32") / 255.0

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    return CLASS_LABELS[predicted_class]

def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    )
    return response.json()["access_token"]

def get_recommendations(emotion):
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}

    mood_map = {
        "happy": "pop",
        "sad": "acoustic",
        "angry": "rock",
        "fear": "ambient",
        "disgust": "metal",
        "surprise": "dance",
        "neutral": "chill",
    }

    genre = mood_map.get(emotion, "pop")

    url = f"https://api.spotify.com/v1/recommendations?limit=5&seed_genres={genre}"
    response = requests.get(url, headers=headers)

    tracks = []
    if response.status_code == 200:
        data = response.json()
        for track in data["tracks"]:
            tracks.append({"name": track["name"], "artist": track["artists"][0]["name"]})
    else:
        tracks.append({"error": "Failed to fetch from Spotify"})

    return tracks
