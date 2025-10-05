import React, { useState } from "react";
import EmotionMusicApp from "./EmotionMusicApp";
import LoginPage from "./LoginPage";

function App() {
  const [user, setUser] = useState(null);
  return user ? (
    <EmotionMusicApp username={user} />
  ) : (
    <LoginPage onLogin={setUser} />
  );
}
export default App;
