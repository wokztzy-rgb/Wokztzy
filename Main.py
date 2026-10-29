import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai
from google.genai import types

# Mengambil API Key dari Environment Variables (Secrets di Fly.io)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Setup Logging untuk memantau aktivitas bot
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inisialisasi Klien Gemini AI baru
client = genai.Client(api_key=GEMINI_KEY)

# Perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Halo! Saya adalah Web3 AI Agent Anda.\n\n"
        "Saya dapat menjawab pertanyaan dengan AI, mengecek saldo BNB dan token BEP-20, serta menyiapkan draft transfer unsigned.\n\n"
        "Perintah yang tersedia:\n"
        "/balance <alamat_wallet> - untuk saldo BNB\n"
        "/tokenbalance <alamat_wallet> <kontrak_token> - untuk saldo token\n\n"
        "Silakan kirim pesan atau tanyakan apa saja!"
    )
    await update.message.reply_text(welcome_text)

# Perintah /balance (Contoh fitur Web3 dasar)
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Format salah. Gunakan: /balance <alamat_wallet>")
        return
    wallet_address = args[0]
    # Placeholder logika pengecekan saldo
    await update.message.reply_text(f"Mengecek saldo untuk wallet: {wallet_address}\n(Fitur koneksi node blockchain siap dikonfigurasi).")

# Fitur Pesan Teks & AI (Gemini)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    if not GEMINI_KEY:
        await update.message.reply_text("AI belum dapat menjawab saat ini. Coba lagi nanti.")
        return

    try:
        # Memanggil Gemini AI menggunakan client terbaru
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Error AI: {e}")
        await update.message.reply_text("AI belum dapat menjawab saat ini. Coba lagi nanti.")

def main():
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_API_KEY belum diatur!")
        return

    # Membangun aplikasi bot Telegram
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Mendaftarkan handler perintah dan pesan
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot Telegram sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
