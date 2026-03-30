
from flask import Flask, jsonify
import subprocess
import os
import requests

app = Flask(__name__)

# Telegram настройки
TELEGRAM_TOKEN = "5713086959:AAEsY9YIe4bkBE_VIYorOvBkXgsp-5XR_Og"  # можна пізніше в Secrets
CHAT_ID = "1047092792"

def send_text_to_telegram(text, caption="Avica Terminal Output"):
    """Відправляємо текст у Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    resp = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": f"{caption}:\n```\n{text}\n```",
        "parse_mode": "Markdown"
    })
    if resp.status_code == 200:
        print("[+] Terminal output sent to Telegram!")
    else:
        print("[!] Telegram send failed:", resp.text)

@app.route("/")
def home():
    return "Avica CLI Text Screenshot API 🚀"

@app.route("/run_avica")
def run_avica():
    """Запускаємо Avica CLI і відправляємо текст"""
    try:
        # Тут заміни команду на реальну Avica CLI
        result = subprocess.run(
            ["echo", "This is a demo Avica terminal output"], 
            capture_output=True, text=True, check=True
        )
        output = result.stdout
    except Exception as e:
        output = f"Failed to run Avica CLI: {e}"

    # Відправляємо у Telegram
    send_text_to_telegram(output)

    return jsonify({"status": "sent", "output": output})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
