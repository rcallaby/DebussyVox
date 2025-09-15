import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from stt import transcribe_file
from tts import synthesize_text
from debussy_client import query_debussy

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "static/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder="static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

@app.route("/voice", methods=["POST"])
def voice_endpoint():
    """
    Accepts multipart/form-data with file field "audio".
    Returns JSON: { text: "...", reply: "...", audio_url: "/static/audio/..." }
    """
    if "audio" not in request.files:
        return jsonify({"error": "no audio file provided"}), 400

    f = request.files["audio"]
    filename = f"{uuid.uuid4().hex}_{f.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(filepath)

    # Transcribe
    try:
        text = transcribe_file(filepath)
    except Exception as e:
        return jsonify({"error": "stt failed", "details": str(e)}), 500

    # Send to DebussyOps
    try:
        reply_text = query_debussy(text)
    except Exception as e:
        return jsonify({"error": "debussy call failed", "details": str(e)}), 500

    # Synthesize reply
    try:
        out_name = f"{uuid.uuid4().hex}.mp3"
        out_path = os.path.join(app.config['AUDIO_FOLDER'], out_name)
        synthesize_text(reply_text, out_path)
        audio_url = f"/static/audio/{out_name}"
    except Exception as e:
        return jsonify({"error": "tts failed", "details": str(e)}), 500

    return jsonify({
        "text": text,
        "reply": reply_text,
        "audio_url": audio_url
    })


# Serve generated audio files (Flask static can handle but explicit route okay)
@app.route("/static/audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

if __name__ == "__main__":
    # Allow host override with env
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
