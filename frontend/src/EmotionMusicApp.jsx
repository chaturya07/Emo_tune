import React, { useRef, useState } from "react";
import { motion } from "framer-motion";
import { PlayCircle, Music2, Camera } from "lucide-react";
import "./EmotionMusicApp.css";

export default function EmotionMusicApp() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const [emotion, setEmotion] = useState("Neutral");
  const [songs, setSongs] = useState([]);
  const [cameraOn, setCameraOn] = useState(false);
  const [loading, setLoading] = useState(false);

  const BACKEND_URL = "http://127.0.0.1:8000"; // change to deployed backend later

  // Toggle webcam on/off
  const toggleCamera = async () => {
    if (!cameraOn) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
        setCameraOn(true);
      } catch (err) {
        console.error("Error accessing camera:", err);
      }
    } else {
      if (videoRef.current?.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
        videoRef.current.srcObject = null;
      }
      setCameraOn(false);
    }
  };

  // Capture frame & send to backend
  const captureAndDetect = async () => {
    if (!videoRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");

    // Draw current frame from video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to blob
    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append("file", blob, "frame.jpg");

      setLoading(true);
      try {
        // Detect emotion
        const res = await fetch(`${BACKEND_URL}/detect-emotion`, {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        setEmotion(data.emotion);

        // Get songs
        const recRes = await fetch(`${BACKEND_URL}/recommendations/${data.emotion}`);
        const recData = await recRes.json();
        setSongs(recData.songs);
      } catch (err) {
        console.error("Error detecting emotion:", err);
        setEmotion("Error");
        setSongs([]);
      } finally {
        setLoading(false);
      }
    }, "image/jpeg");
  };

  return (
    <div className="app-container">
      <motion.h1
        className="app-title"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
      >
        EmoTune – Feel the Music
      </motion.h1>

      {/* Camera Card */}
      <div className="card-grid">
        <motion.div className="glass-card" whileHover={{ scale: 1.05 }}>
          <h2 className="card-title">
            <Camera /> Live Camera
          </h2>
          <video ref={videoRef} autoPlay muted playsInline className="camera-preview"></video>
          <canvas ref={canvasRef} style={{ display: "none" }}></canvas>
          <div>
            <button className="btn" onClick={toggleCamera}>
              {cameraOn ? "Stop Camera" : "Start Camera"}
            </button>
            {cameraOn && (
              <button className="btn" onClick={captureAndDetect} disabled={loading}>
                {loading ? "Detecting..." : "Capture & Detect"}
              </button>
            )}
          </div>
        </motion.div>
      </div>

      {/* Emotion + Music */}
      <div className="side-by-side">
        <motion.div className="glass-card" whileHover={{ scale: 1.05 }}>
          <h2 className="card-title">Detected Emotion</h2>
          <p className="emotion-text">{emotion}</p>
        </motion.div>

        <motion.div className="glass-card" whileHover={{ scale: 1.05 }}>
          <h2 className="card-title">
            <Music2 /> Music Recommendations
          </h2>
          {songs.length > 0 ? (
            <ul className="song-list">
              {songs.map((song, idx) => (
                <li key={idx} className="song-item">
                  <p className="song-title">{song.name}</p>
                  <p className="artist-name">{song.artist}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p>No songs yet. Capture to detect!</p>
          )}
        </motion.div>
      </div>

      <div className="footer">&copy; 2025 EmoTune. All rights reserved.</div>
    </div>
  );
}
