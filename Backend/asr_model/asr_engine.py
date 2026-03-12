import whisper
import os

# Load Whisper model (better accuracy than tiny/base)
model = whisper.load_model("small")

def speech_to_text(audio_path):

    try:

        if not os.path.exists(audio_path):
            return ""

        result = model.transcribe(
            audio_path,
            language="en",
            temperature=0,
            fp16=False
        )

        text = result.get("text", "").strip()

        return text

    except Exception as e:

        print("ASR ERROR:", e)
        return ""