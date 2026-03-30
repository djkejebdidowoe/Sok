FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# 1️⃣ Встановлюємо базові пакети
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    gnupg \
    lsb-release \
    python3 \
    python3-pip \
    tesseract-ocr \
    python3-tk \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# 2️⃣ Встановлюємо Tailscale CLI
RUN curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.gpg | sudo gpg --dearmor -o /usr/share/keyrings/tailscale-archive-keyring.gpg \
    && curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.list | sudo tee /etc/apt/sources.list.d/tailscale.list \
    && apt-get update && apt-get install -y tailscale \
    && rm -rf /var/lib/apt/lists/*

# 3️⃣ Python пакети
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# 4️⃣ Копіюємо скрипт
COPY main.py /app/main.py
WORKDIR /app

CMD ["python3", "main.py"]
