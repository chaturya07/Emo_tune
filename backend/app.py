from auth import router as auth_router
app.include_router(auth_router)
from fastapi import FastAPI, UploadFile, File
from utils import load_model, predict_emotion, get_recommendations
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


# Initialize FastAPI app
app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
model = load_model("ml/models/baseline_v1/baseline_final.h5")

@app.post("/detect-emotion")
async def detect_emotion(file: UploadFile = File(...)):
    emotion = await predict_emotion(model, file)
    return {"emotion": emotion}

@app.get("/recommendations/{emotion}")
async def recommendations(emotion: str):
    songs = get_recommendations(emotion)
    return {"emotion": emotion, "songs": songs}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")
@app.post("/detect-emotion")
async def detect_emotion(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)  # 🔒 protected
):
    emotion = await predict_emotion(model, file)
    return {"emotion": emotion}

@app.get("/recommendations/{emotion}")
async def recommendations(
    emotion: str,
    current_user: str = Depends(get_current_user)  # 🔒 protected
):
    songs = get_recommendations(emotion)
    return {"emotion": emotion, "songs": songs}
