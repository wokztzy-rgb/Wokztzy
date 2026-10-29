FROM python:3.11-slim

WORKDIR /app

# Salin semua file dari repository ke dalam folder app
COPY . /app

# Upgrade pip dan install langsung modul yang dibutuhkan tanpa file txt biar gak rewel
RUN pip install --no-cache-dir python-telegram-bot google-genai

# Jalankan bot utama
CMD ["python", "Main.py"]
