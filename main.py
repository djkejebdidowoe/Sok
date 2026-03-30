import os
import subprocess
import time
from PIL import Image
import pytesseract
import requests

# ============================
# 1️⃣ Підключення до Tailscale
# ============================
TAILSCALE_AUTHKEY = os.environ.get("TAILSCALE_AUTHKEY")  # потрібно додати у Railway Secrets
HOSTNAME = "railway-server"

print("[*] Піднімаємо Tailscale...")
# Запускаємо Tailscale CLI
subprocess.run(f"tailscale up --authkey={TAILSCALE_AUTHKEY} --hostname={HOSTNAME}", shell=True)

# Отримуємо Tailscale IP
ts_ip = None
retries = 0
while not ts_ip and retries < 10:
    try:
        ts_ip = subprocess.check_output("tailscale ip -4", shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        pass
    if not ts_ip:
        time.sleep(5)
        retries += 1

print(f"[+] Tailscale IP: {ts_ip}")
print("[*] Тепер ти можеш підключатися через SSH/тунель до цього IP")

# ============================
# 2️⃣ Headless OCR на прикладі
# ============================
img_url = "https://example.com/screenshot.png"  # заміни на потрібне
img_path = "/tmp/screenshot.png"

print(f"[*] Завантажуємо зображення з {img_url}")
response = requests.get(img_url)
with open(img_path, "wb") as f:
    f.write(response.content)

img = Image.open(img_path)
text = pytesseract.image_to_string(img)

print("[*] OCR Result:")
print(text)

# ============================
# 3️⃣ Тримаємо контейнер живим
# ============================
print("[*] Сервер живий. Тунель працює...")
while True:
    time.sleep(60)
