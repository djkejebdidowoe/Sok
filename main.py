from flask import Flask
from PIL import Image
import pytesseract
import requests
import os

app = Flask(__name__)

# ===== Telegram настройки =====
# ⚠️ Не добавляй сюда свои реальные токены напрямую в код, но для теста можно так
TELEGRAM_TOKEN = "5713086959:AAEsY9YIe4bkBE_VIYorOvBkXgsp-5XR_Og"
CHAT_ID = "1047092792"

# ===== Ссылка на скриншот Avica =====
SCREENSHOT_URL = "https://example.com/avica_screenshot.png"  # замени на реальный URL

# ===== Функция отправки скрина в Telegram =====
def send_to_telegram(file_path, caption="Avica Screenshot"):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(file_path, "rb") as f:
        resp = requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": f})
    if resp.status_code == 200:
        print("[+] Screenshot sent to Telegram!")
    else:
        print("[!] Telegram upload failed:", resp.text)

@app.route("/")
def home():
    return "Avica OCR Telegram sender running 🚀"

# ===== Запуск отправки сразу после старта =====
@app.before_first_request
def send_screenshot():
    img_path = "/tmp/screenshot.png"

    try:
        print("[*] Загружаем скриншот...")
        resp = requests.get(SCREENSHOT_URL, verify=False)  # отключаем проверку SSL
        resp.raise_for_status()
        with open(img_path, "wb") as f:
            f.write(resp.content)
        print("[*] Скриншот загружен!")
    except Exception as e:
        print("[!] Failed to download image:", e)
        return

    try:
        send_to_telegram(img_path)
    except Exception as e:
        print("[!] Telegram send failed:", e)

    # OCR (для интереса)
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        print("[*] OCR Result:\n", text)
    except Exception as e:
        print("[!] OCR failed:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
