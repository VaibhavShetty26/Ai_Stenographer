import React, { useState, useRef } from "react";
import "./App.css";

function App() {

  const [isRecording, setIsRecording] = useState(false);
  const [status, setStatus] = useState("Idle");
  const [processedText, setProcessedText] = useState("");

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    const mediaRecorder = new MediaRecorder(stream);

    mediaRecorderRef.current = mediaRecorder;
    audioChunksRef.current = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorder.onstop = async () => {

      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });

      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      setStatus("Processing...");

      try {

        const response = await fetch("http://localhost:5000/process", {
          method: "POST",
          body: formData
        });

        const data = await response.json();

        setProcessedText(data.corrected_text || "No processed text returned");

        setStatus("Document ready");

      } catch (error) {

        console.error(error);
        setProcessedText("Error processing audio.");
        setStatus("Idle");

      }

    };

    mediaRecorder.start();

    setIsRecording(true);
    setStatus("Listening...");
  };

  const stopRecording = () => {

    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }

    setIsRecording(false);
  };

  const downloadDocument = () => {

    window.open("http://localhost:5000/download");

  };

  return (
    <div className="app-container">

      <h1 className="title">AI Stenographer</h1>

      <div className="main-card">

        <div className="mic-section">
          <div className="mic-button">🎤</div>
        </div>

        <div className="controls">

          {!isRecording ? (
            <button className="start-btn" onClick={startRecording}>
              Start Recording
            </button>
          ) : (
            <button className="stop-btn" onClick={stopRecording}>
              Stop Recording
            </button>
          )}

          <button className="download-btn" onClick={downloadDocument}>
            Download Document
          </button>

        </div>

        <p className="status-text">{status}</p>

        <div className="processed-container">

          <h3 className="processed-title">Processed Text</h3>

          <textarea
            value={processedText}
            readOnly
            className="processed-box"
            placeholder="Corrected speech transcript will appear here..."
          />

        </div>

      </div>

    </div>
  );
}

export default App;