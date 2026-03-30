from PIL import Image
import pytesseract
import requests
import re
import os
import time

# =========================
# Telegram настройки (прямо)
# =========================
TELEGRAM_TOKEN = "5713086959:AAEsY9YIe4bkBE_VIYorOvBkXgsp-5XR_Og"
CHAT_ID = 1047092792  # число, не строка

# URL скрина Avica
SCREENSHOT_URL = "https://example.com/avica_screenshot.png"  # <-- сюда твой реальный скриншот

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

def main():
    img_path = "/tmp/screenshot.png"

    # 1️⃣ Скачиваем скриншот
    try:
        resp = requests.get(SCREENSHOT_URL)
        resp.raise_for_status()
        with open(img_path, "wb") as f:
            f.write(resp.content)
        print("[+] Screenshot downloaded")
    except Exception as e:
        print("[!] Failed to download image:", e)
        return

    # 2️⃣ Отправляем скрин в Telegram
    try:
        send_to_telegram(img_path)
    except Exception as e:
        print("[!] Telegram send failed:", e)

    # 3️⃣ OCR
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        print("[+] OCR done:")
        print(text)
    except Exception as e:
        print("[!] OCR failed:", e)
        return

    # 4️⃣ Ищем ID и Password через регулярку
    id_match = re.search(r"(ID|Login|User)[\s:]*([A-Za-z0-9]+)", text, re.IGNORECASE)
    pass_match = re.search(r"(Pass|Password)[\s:]*([A-Za-z0-9]+)", text, re.IGNORECASE)

    avica_id = id_match.group(2) if id_match else None
    avica_pass = pass_match.group(2) if pass_match else None

    print("[+] Parsed credentials:")
    print("ID:", avica_id)
    print("Password:", avica_pass)

if __name__ == "__main__":
    # Даем контейнеру немного прогрузиться
    time.sleep(5)
    main()
