import React, { useState } from "react";
import EmotionMusicApp from "./EmotionMusicApp";
import LoginPage from "./LoginPage";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  return isLoggedIn ? (
    <EmotionMusicApp />
  ) : (
    <LoginPage onLogin={() => setIsLoggedIn(true)} />
  );
}
export default App;
