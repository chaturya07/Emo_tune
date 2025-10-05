import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./EmotionMusicApp.css";
import Chatbot from "./Chatbot";

const YOUTUBE_API_KEY = "AIzaSyAGICvnnV1VHFBgujNS6YXc-y2af66EScM";

function EmotionMusicApp() {
  const [emotion, setEmotion] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [preview, setPreview] = useState(null);
  const [songs, setSongs] = useState([]);
  const [username, setUsername] = useState(""); // 👈 for welcome banner
  const fileInputRef = useRef();
  const videoRef = useRef();
  const resultRef = useRef();

  // 🎥 Initialize webcam safely
  useEffect(() => {
    let stream;
    const startCamera = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (err) {
        console.error("Webcam error:", err);
      }
    };
    startCamera();
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  // 👋 Get username from localStorage
  useEffect(() => {
    const storedName = localStorage.getItem("username");
    if (storedName) setUsername(storedName);
  }, []);

  // 🎵 Fetch songs from YouTube
  const fetchSongs = async (emotion) => {
    try {
      const query = `${emotion} mood songs playlist`;
      const searchRes = await axios.get("https://www.googleapis.com/youtube/v3/search", {
        params: {
          part: "snippet",
          maxResults: 8,
          q: query,
          type: "video",
          videoEmbeddable: "true",
          key: YOUTUBE_API_KEY,
        },
      });

      const videoIds = searchRes.data.items
        .map((item) => item.id.videoId)
        .filter(Boolean)
        .join(",");

      if (!videoIds) {
        setSongs([
          {
            title: "Feel Good Songs Mix",
            videoId: "d-diB65scQU",
            channel: "YouTube Music",
            thumbnail: "https://img.youtube.com/vi/d-diB65scQU/hqdefault.jpg",
          },
        ]);
        return;
      }

      const detailsRes = await axios.get("https://www.googleapis.com/youtube/v3/videos", {
        params: {
          part: "snippet,contentDetails,status",
          id: videoIds,
          key: YOUTUBE_API_KEY,
        },
      });

      const playableVideos = detailsRes.data.items
        .filter((v) => v.status.embeddable && v.status.privacyStatus === "public")
        .map((v) => ({
          title: v.snippet.title,
          videoId: v.id,
          channel: v.snippet.channelTitle,
          thumbnail: v.snippet.thumbnails?.high?.url,
        }));

      setSongs(
        playableVideos.length > 0
          ? playableVideos
          : [
              {
                title: "Feel Good Songs Mix",
                videoId: "d-diB65scQU",
                channel: "YouTube Music",
                thumbnail: "https://img.youtube.com/vi/d-diB65scQU/hqdefault.jpg",
              },
            ]
      );
    } catch (err) {
      console.error("YouTube API Error:", err);
    }
  };

  const handleBackendResponse = (data) => {
    setEmotion(data.emotion);
    setConfidence((data.confidence * 100).toFixed(2));
    fetchSongs(data.emotion);

    setTimeout(() => {
      resultRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 500);
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      handleBackendResponse(data);
    } catch (err) {
      console.error("Backend error:", err);
    }
  };

  const handleCapture = async () => {
    const video = videoRef.current;
    if (!video) return;

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) {
        console.error("❌ Failed to capture image blob.");
        return;
      }

      const imageURL = URL.createObjectURL(blob);
      setPreview(imageURL);

      const formData = new FormData();
      formData.append("file", blob, "capture.jpg");

      try {
        const res = await fetch("http://127.0.0.1:5000/predict", {
          method: "POST",
          body: formData,
        });

        if (!res.ok) throw new Error("Failed to get prediction");
        const data = await res.json();
        handleBackendResponse(data);
      } catch (err) {
        console.error("Backend error:", err);
      }
    }, "image/jpeg");
  };

  return (
    <div className="app-container fade-in">
      {/* 👋 Welcome Banner */}
      <div className="welcome-banner">
        <h2>Welcome, {username || "Music Lover"}! 🎧</h2>
        <p>Let’s find the rhythm of your emotions 💫</p>
      </div>

      <h1 className="glow-text">🎵 Emo_Tune</h1>
      <p className="caption">Feel the rhythm of your emotions 💞</p>

      <div className="input-section">
        {/* 💖 Upload Section */}
        <div className="upload-section">
          <h3>✨ Upload your vibe ✨</h3>
          <p>Upload your selfie and let <b>Emo_Tune</b> feel your mood 🎭</p>

          <label htmlFor="fileUpload" className="custom-upload-label">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M12 2a10 10 0 1 0 10 10A10.011 10.011 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8 8.009 8.009 0 0 1-8 8ZM11 11V6h2v5h3l-4 4-4-4Z"/>
            </svg>
            Choose Image
          </label>
          <input
            type="file"
            id="fileUpload"
            accept="image/*"
            onChange={handleUpload}
            ref={fileInputRef}
          />
        </div>

        {/* 🎥 Webcam Section */}
        <div className="webcam-section">
          <h3>📷 Live Capture</h3>
          <video autoPlay playsInline width="300" height="200" ref={videoRef}></video>
          <button className="capture-btn" onClick={handleCapture}>📸 Capture Mood</button>
        </div>
      </div>

      <div ref={resultRef}>
        {preview && (
          <div className="result-section bounce">
            <h3>💫 Detected Emotion</h3>
            <img src={preview} alt="Preview" width="200" />
            <p>
              <strong>{emotion}</strong> ({confidence}% confidence)
            </p>
          </div>
        )}

        {songs.length > 0 && (
          <div className="songs-section fade-up">
            <h3>🎶 Songs for your {emotion} mood</h3>
            <div className="songs-grid">
              {songs.map((song) => (
                <div className="song-card shimmer" key={song.videoId}>
                  <a
                    href={`https://www.youtube.com/watch?v=${song.videoId}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <img
                      src={song.thumbnail}
                      alt={song.title}
                      style={{ width: "100%", borderRadius: "10px", marginBottom: "8px" }}
                    />
                  </a>
                  <div className="song-info">
                    <h4>{song.title}</h4>
                    <p>{song.channel}</p>
                    <a
                      href={`https://www.youtube.com/watch?v=${song.videoId}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="play-btn"
                    >
                      ▶️ Play on YouTube
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 🐼 Mickey the Chatbot */}
      <Chatbot />
    </div>
  );
}

export default EmotionMusicApp;
