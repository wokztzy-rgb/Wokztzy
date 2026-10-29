FROM python:3.11-slim

# Install system dependencies, Git, dan Node.js (untuk 9router)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install 9router secara global sesuai panduan
RUN npm install -g 9router

# Install Hermes Agent dari Nous Research
RUN curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Set working directory
WORKDIR /app

# Salin konfigurasi atau file pendukung jika ada
COPY . /app

# Perintah default untuk menjalankan agent/gateway
CMD ["hermes", "gateway", "start"]
