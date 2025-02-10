from flask import Flask, request, jsonify, send_from_directory
import os
import requests
import numpy as np
from werkzeug.utils import secure_filename
from urllib.parse import urlparse
from src.server.qrgen import final_qr_gen
from qr_decoder import return_message
from flask_cors import CORS


serve_folder = "src/server/host_files"
UPLOAD_FOLDER = "src/server/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__, static_folder=serve_folder)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def download_image(url):
    """Downloads an image from a given URL and saves it locally, handling headers and timeouts."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Accept": "image/png, image/jpeg, image/*",
        "Referer": url
    }

    try:
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()

        filename = os.path.basename(urlparse(url).path)
        if not filename or "." not in filename:
            filename = "downloaded_image.png"

        filename = secure_filename(filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        return file_path
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

@app.route("/")
def serve_index():
    return send_from_directory(serve_folder, "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(serve_folder, filename)

@app.route("/process", methods=["POST"])
def process_request():
    data = request.get_json()

    print(data)

    text = data["text"]
    error_char = data["errorchar"]
    if error_char == '':
        error_char = 'L'

    print(f"Received text: {text}, Error Char: {error_char}")  # Debugging


    return jsonify(final_qr_gen(text, error_char)), 200, {"Content-Type": "application/json"}

@app.route("/photo", methods=["POST"])
def process_photo():
    file_path = None

    if "file" in request.files:
        file = request.files["file"]
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

    elif request.is_json:
        data = request.get_json()
        image_url = data.get("url")

        file_path = download_image(image_url)

    qr_text = return_message(file_path)

    return qr_text, 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

