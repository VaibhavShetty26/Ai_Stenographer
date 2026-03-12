from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import whisper
import os

from nlp_processing.nlp_pipeline import clean_text

app = Flask(__name__)
CORS(app)

# Load Whisper model
model = whisper.load_model("small")

# File where processed document will be stored
OUTPUT_FILE = "stenographer_output.txt"


@app.route("/process", methods=["POST"])
def process_audio():

    try:

        if "audio" not in request.files:
            return jsonify({"error": "No audio received"}), 400

        audio_file = request.files["audio"]

        audio_path = "temp_audio.webm"

        audio_file.save(audio_path)

        result = model.transcribe(audio_path)

        raw_text = result["text"]

        corrected_text = clean_text(raw_text)

        # Save processed text to file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(corrected_text)

        return jsonify({
            "raw_text": raw_text,
            "corrected_text": corrected_text
        })

    except Exception as e:

        print("PROCESS ERROR:", e)

        return jsonify({"error": "Error processing audio"}), 500


@app.route("/download", methods=["GET"])
def download_document():

    try:

        if not os.path.exists(OUTPUT_FILE):
            return jsonify({"error": "No document generated"}), 404

        return send_file(
            OUTPUT_FILE,
            as_attachment=True,
            download_name="AI_Stenographer_Output.txt",
            mimetype="text/plain"
        )

    except Exception as e:

        print("DOWNLOAD ERROR:", e)

        return jsonify({"error": "Download failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)