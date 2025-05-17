import { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [text, setText] = useState("");
  const [videoUrl, setVideoUrl] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);

  const [inputMode, setInputMode] = useState("text");
const [isListening, setIsListening] = useState(false);

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

const handleMicClick = () => {
  if (!recognition) {
    alert("Speech Recognition not supported in this browser.");
    return;
  }

  setIsListening(true);
  recognition.start();

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    setText(transcript);
    setIsListening(false);
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error", event);
    setIsListening(false);
  };

  recognition.onend = () => {
    setIsListening(false);
  };
};


  const handleTranslate = async () => {
    setError("");
    setVideoUrl(null);
    
    if (!text.trim()) {
      setError("Please enter some text.");
      return;
    }

    setIsLoading(true);
    
    try {
      const response = await axios.post("http://127.0.0.1:8000/translate", 
        { text }, 
        { responseType: "blob" } // Handle video response
      );

      const videoBlob = new Blob([response.data], { type: "video/mp4" });
      const videoObjectUrl = URL.createObjectURL(videoBlob);
      setVideoUrl(videoObjectUrl);
    } catch (err) {
      console.error("❌ API Error:", err);
      setError("Failed to fetch sign language video. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">ISL Sign Language Translator</h1>
      
      <div className="content-container">
        <div className="input-section">
        <div className="mode-switch">
          <button 
            className={inputMode === "text" ? "mode-button active" : "mode-button"} 
            onClick={() => setInputMode("text")}
          >
            Text
          </button>
          <button 
            className={inputMode === "speech" ? "mode-button active" : "mode-button"} 
            onClick={() => setInputMode("speech")}
          >
            Speech
          </button>
        </div>

          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text to translate..."
            className="input-textarea"
          />
          {inputMode === "speech" && (
          <button 
            className={`mic-button ${isListening ? "listening" : ""}`} 
            onClick={handleMicClick}
            title="Click to speak"
          >
            🎤
          </button>
        )}

          <button
            onClick={handleTranslate}
            className="translate-button"
          >
            Translate to ISL
          </button>
          <div className="speed-slider-container">
            <label htmlFor="speedSlider">Playback Speed: {playbackSpeed.toFixed(1)}x</label>
            <input
              type="range"
              id="speedSlider"
              min="0.5"
              max="2"
              step="0.1"
              value={playbackSpeed}
              onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
              className="speed-slider"
            />
          </div>

          {error && <p className="error-message">{error}</p>}
        </div>
        
        <div className="output-section">
          <h2 className="section-title">Sign Language Output</h2>
          
          {isLoading && (
            <div className="loader-container">
              <div className="loader"></div>
              <p>Generating sign language video...</p>
            </div>
          )}
          
          {videoUrl && !isLoading && (
            <div className="video-container">
              <video 
                autoPlay 
                loop 
                muted 
                playsInline
                className="output-video"
                playbackRate={playbackSpeed}
                ref={(video) => {
                  if (video) video.playbackRate = playbackSpeed;
                }}
                >
                <source src={videoUrl} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          )}
          
          {!videoUrl && !isLoading && (
            <div className="placeholder-message">
              <p>Translated video will appear here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
