import React, { useRef, useState } from "react";
import { motion } from "framer-motion";
import { PlayCircle, Music2, Camera } from "lucide-react";
import "./EmotionMusicApp.css";

export default function EmotionMusicApp() {
  const videoRef = useRef(null);
  const [emotion, setEmotion] = useState("Neutral");
  const [cameraOn, setCameraOn] = useState(false);

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
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
        videoRef.current.srcObject = null;
      }
      setCameraOn(false);
    }
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
          <button className="btn" onClick={toggleCamera}>
            {cameraOn ? "Stop Camera" : "Start Camera"}
          </button>
        </motion.div>
      </div>

      {/* Emotion + Music Side by Side */}
      <div className="side-by-side">
        <motion.div className="glass-card" whileHover={{ scale: 1.05 }}>
          <h2 className="card-title">Detected Emotion</h2>
          <p className="emotion-text">{emotion}</p>
        </motion.div>

        <motion.div className="glass-card" whileHover={{ scale: 1.05 }}>
          <h2 className="card-title">
            <Music2 /> Music Player
          </h2>
          <img
            src="https://via.placeholder.com/200"
            alt="Album Cover"
            className="album-cover"
          />
          <p className="song-title">Song Title</p>
          <p className="artist-name">Artist Name</p>
          <button className="btn play-btn">
            <PlayCircle /> Play Music
          </button>
        </motion.div>
      </div>

      <div className="footer">
        &copy; 2025 EmoTune. All rights reserved. 
      </div>
    </div>
  );
  <div className="side-by-side">
  {/* Emotion Card */}
  <motion.div className="glass-card" whileHover={{ scale: 1.05 }}>
    <h2 className="card-title">Detected Emotion</h2>
    <p className="emotion-text">{emotion}</p>
  </motion.div>

  {/* Music Player Card */}
  <motion.div className="glass-card" whileHover={{ scale: 1.05 }}>
    <h2 className="card-title">
      <Music2 /> Music Player
    </h2>
    <img
      src="https://via.placeholder.com/200"
      alt="Album Cover"
      className="album-cover"
    />
    <p className="song-title">Song Title</p>
    <p className="artist-name">Artist Name</p>
    <button className="btn play-btn">
      <PlayCircle /> Play Music
    </button>
  </motion.div>
</div>

}
