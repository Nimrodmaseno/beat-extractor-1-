from flask import Flask, render_template, request, jsonify
import os
import librosa
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def extract_beats(file_path):
    y, sr = librosa.load(file_path, sr=None)

    # Beat tracking
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    # Convert frames → time
    beat_times = librosa.frames_to_time(beats, sr=sr)

    return {
        "tempo": float(tempo),
        "beats": beat_times.tolist()
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    filename = str(uuid.uuid4()) + "_" + file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    result = extract_beats(path)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)