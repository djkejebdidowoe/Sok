from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "OCR API is running 🚀"

@app.route("/ocr", methods=["POST"])
def ocr_image():
    """
    Очікує JSON:
    {
        "url": "https://example.com/image.png"
    }
    """
    data = request.json
    if "url" not in data:
        return jsonify({"error": "Missing 'url'"}), 400

    img_url = data["url"]
    img_path = "/tmp/temp.png"

    # Завантажуємо зображення
    try:
        resp = requests.get(img_url)
        resp.raise_for_status()
        with open(img_path, "wb") as f:
            f.write(resp.content)
    except Exception as e:
        return jsonify({"error": f"Failed to download image: {e}"}), 400

    # OCR
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
    except Exception as e:
        return jsonify({"error": f"OCR failed: {e}"}), 500

    return jsonify({"text": text.strip()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
