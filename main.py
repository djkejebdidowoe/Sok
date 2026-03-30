from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import requests
import re
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Avica OCR API is running 🚀"

@app.route("/ocr", methods=["POST"])
def ocr_avica():
    """
    JSON пример:
    {
        "url": "https://example.com/avica_screenshot.png"
    }
    """
    data = request.json
    if "url" not in data:
        return jsonify({"error": "Missing 'url'"}), 400

    img_url = data["url"]
    img_path = "/tmp/screenshot.png"

    # 1️⃣ Скачиваем скриншот
    try:
        resp = requests.get(img_url)
        resp.raise_for_status()
        with open(img_path, "wb") as f:
            f.write(resp.content)
    except Exception as e:
        return jsonify({"error": f"Failed to download image: {e}"}), 400

    # 2️⃣ OCR
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
    except Exception as e:
        return jsonify({"error": f"OCR failed: {e}"}), 500

    # 3️⃣ Ищем ID и Password через регулярку
    # Предполагаем, что ID — цифры или буквы, Password — рядом с ID
    id_match = re.search(r"(ID|Login|User)[\s:]*([A-Za-z0-9]+)", text, re.IGNORECASE)
    pass_match = re.search(r"(Pass|Password)[\s:]*([A-Za-z0-9]+)", text, re.IGNORECASE)

    avica_id = id_match.group(2) if id_match else None
    avica_pass = pass_match.group(2) if pass_match else None

    return jsonify({
        "id": avica_id,
        "password": avica_pass,
        "raw_text": text
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
