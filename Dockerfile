FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Встановлюємо базові пакети + Python + OCR
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    python3 \
    python3-pip \
    tesseract-ocr \
    python3-tk \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Tailscale через офіційний скрипт
RUN curl -fsSL https://tailscale.com/install.sh | sh

# Python пакети
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Копіюємо головний скрипт
COPY main.py /app/main.py
WORKDIR /app

CMD ["python3", "main.py"]
