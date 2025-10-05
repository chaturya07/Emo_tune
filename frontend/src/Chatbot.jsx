import React, { useState } from "react";
import "./Chatbot.css";

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hey there 🐼 I'm Mickey! How are you feeling today?" },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const toggleChat = () => setIsOpen(!isOpen);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { from: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();

      setTimeout(() => {
        setMessages((prev) => [...prev, { from: "bot", text: data.reply }]);
        setIsTyping(false);
      }, 800);
    } catch (err) {
      console.error("Chatbot error:", err);
      setIsTyping(false);
    }
  };

  return (
    <>
      {/* 🐼 Floating Mickey Icon */}
      <div className="panda-icon" onClick={toggleChat}>
        <img
          src="https://cdn-icons-png.flaticon.com/512/616/616408.png"
          alt="mickey bot"
        />
        {!isOpen && <p className="help-text">Need help?</p>}
      </div>

      {/* 💬 Chat Window */}
      {isOpen && (
        <div className="chatbot-container">
          <div className="chat-header">
            🐼 Mickey – Your Support Bot
            <button className="close-btn" onClick={toggleChat}>
              ✕
            </button>
          </div>

          <div className="chat-body">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`chat-msg ${msg.from === "user" ? "user-msg" : "bot-msg"}`}
              >
                {msg.from === "bot" && (
                  <img
                    src="https://cdn-icons-png.flaticon.com/512/616/616408.png"
                    alt="bot"
                    className="avatar"
                  />
                )}
                <p>{msg.text}</p>
              </div>
            ))}

            {isTyping && (
              <div className="typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            )}
          </div>

          <div className="chat-input">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your thoughts..."
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      )}
    </>
  );
}

export default Chatbot;
