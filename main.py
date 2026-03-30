from flask import Flask
import os
import requests
import time

app = Flask(__name__)

# Telegram настройки (можеш вставити прямо або через Secrets Railway)
TELEGRAM_TOKEN = "5713086959:AAEsY9YIe4bkBE_VIYorOvBkXgsp-5XR_Og"
CHAT_ID = "1047092792"

def send_to_telegram(text, caption="Avica Terminal Screenshot"):
    """Отправляем текст как фото в Telegram"""
    # Создаем временный файл
    file_path = "/tmp/avica_screenshot.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    # Отправляем как документ
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(file_path, "rb") as f:
        resp = requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"document": f})
    if resp.status_code == 200:
        print("[+] Screenshot sent to Telegram!")
    else:
        print("[!] Telegram upload failed:", resp.text)

def make_avica_screenshot():
    """Эмуляция скриншота Avica в текстовом виде"""
    demo_output = """
    ===========================
        AVICA LITE TERMINAL
    ===========================
    User: DemoUser
    Password: DemoPass
    ===========================
    Connection Status: OK
    """
    return demo_output

# === Автоматическая отправка при старте контейнера ===
@app.before_first_request
def auto_send():
    print("[*] Generating Avica screenshot...")
    screenshot = make_avica_screenshot()
    send_to_telegram(screenshot)

@app.route("/")
def home():
    return "Avica OCR API is running 🚀"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
