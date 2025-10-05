import React, { useState } from "react";
import "./LoginPage.css";
export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmedName = username.trim();
    if (trimmedName) {
      //Save user info to localStorage
      localStorage.setItem("username", trimmedName);
      localStorage.setItem("token", "true");
      //Call parent to navigate to main app
      onLogin(trimmedName);
    }
  };
  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">🎵 Emo_Tune</h1>
        <p className="login-caption">Feel your emotions. Find your rhythm 💫</p>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter your name..."
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="login-input"
          />
          <button type="submit" className="login-btn">
            Let’s Go 🎶
          </button>
        </form>
      </div>
    </div>
  );
}
