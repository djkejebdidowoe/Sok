import os
import subprocess
import time

# === 1. Підключення до Tailscale ===
TAILSCALE_AUTHKEY = os.environ.get("tskey-auth-kHFFEd2Qw511CNTRL-anq4osFo2u2wxWmxuidHu2kpbax5GhmVB")  # треба задати у Railway Secrets
HOSTNAME = "railway-server"

print("[*] Піднімаємо Tailscale...")
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
print("[*] Тепер ти можеш підключатися через SSH/тунель до цього IP, якщо Tailscale дозволяє")

# === 2. Headless OCR (якщо треба) ===
from PIL import Image
import pytesseract

# Приклад: обробка картинки з інтернету
import urllib.request
img_url = "https://example.com/screenshot.png"
urllib.request.urlretrieve(img_url, "/tmp/screenshot.png")
img = Image.open("/tmp/screenshot.png")
text = pytesseract.image_to_string(img)
print("[*] OCR Result:")
print(text)

# === 3. Тримати процес живим (як у GitHub workflow) ===
print("[*] Сервер живий. Тунель працює...")
while True:
    time.sleep(60)
