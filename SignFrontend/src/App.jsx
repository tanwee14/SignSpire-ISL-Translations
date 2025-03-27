import { useState } from "react";
import axios from "axios";
import './App.css'
function App() {
  const [text, setText] = useState("");
  const [videoUrl, setVideoUrl] = useState(null);
  const [error, setError] = useState("");

  const handleTranslate = async () => {
    setError("");
    setVideoUrl(null);

    if (!text.trim()) {
      setError("Please enter some text.");
      return;
    }

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
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-4">ISL Sign Language Translator</h1>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to translate..."
        className="w-full max-w-lg p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <button
        onClick={handleTranslate}
        className="mt-4 px-6 py-2 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600"
      >
        Translate to ISL
      </button>

      {error && <p className="mt-3 text-red-500">{error}</p>}

      {videoUrl && (
        <div className="mt-6">
          <h2 className="text-lg font-semibold">Generated Sign Language Video:</h2>
          <video controls className="mt-2 rounded-lg shadow-lg">
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}

export default App;
