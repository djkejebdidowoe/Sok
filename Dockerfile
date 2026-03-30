# Use Ubuntu base image
FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    python3 \
    python3-pip \
    tesseract-ocr \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy the main Python script
COPY main.py /app/main.py

WORKDIR /app

# Run the script
CMD ["python3", "main.py"]
