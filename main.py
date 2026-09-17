import os
import logging
import threading
import tempfile
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)
from database.db import init_db
from handlers.ai_handler import ai_chat
from handlers.weather_handler import get_weather
from handlers.news_handler import get_news
from handlers.scraper_handler import scrape_website
from handlers.translation_handler import translate_text
from handlers.document_handler import process_pdf, process_excel

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# FastAPI health check
web_app = FastAPI()

@web_app.get("/")
def health_check():
    return {"status": "Bot is running!"}

def run_web():
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(web_app, host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 আমি তোমার Advanced Bot!\n\n"
        "📌 Commands:\n"
        "/ai [message] — AI Chat\n"
        "/weather [city] — আবহাওয়া\n"
        "/news [topic] — News\n"
        "/scrape [url] — Website Scrape\n"
        "/translate [text] — Translation\n"
        "/analyze — File Analyze (PDF/Excel পাঠাও)\n"
        "/help — সব commands"
    )

async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ai তোমার প্রশ্ন লেখো")
        return
    message = " ".join(context.args)
    await update.message.reply_text("🤔 AI ভাবছে...")
    response = await ai_chat(message)
    await update.message.reply_text(f"🤖 {response}")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args) if context.args else "Dhaka"
    await update.message.reply_text("🌤 আবহাওয়া দেখছি...")
    result = await get_weather(city)
    await update.message.reply_text(result)

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else "Bangladesh"
    await update.message.reply_text("📰 News খুঁজছি...")
    result = await get_news(topic)
    await update.message.reply_text(result)

async def scrape_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /scrape https://example.com")
        return
    url = context.args[0]
    await update.message.reply_text("🔍 Scraping করছি...")
    result = await scrape_website(url)
    await update.message.reply_text(result[:4000])

async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /translate Hello World")
        return
    text = " ".join(context.args)
    result = translate_text(text, "en", "bn")
    await update.message.reply_text(f"🌍 Translation:\n{result}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc:
        return
    file = await context.bot.get_file(doc.file_id)
    with tempfile.NamedTemporaryFile(suffix=f".{doc.file_name.split('.')[-1]}", delete=False) as tmp:
        await file.download_to_drive(tmp.name)
        if doc.file_name.endswith(".pdf"):
            result = await process_pdf(tmp.name)
        elif doc.file_name.endswith((".xlsx", ".xls")):
            result = await process_excel(tmp.name)
        else:
            result = "শুধু PDF বা Excel file support করা হয়।"
    await update.message.reply_text(result[:4000])

def main():
    init_db()

    # Web server background এ চালাও
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    logger.info("Web server চালু হয়েছে!")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ai", ai_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("news", news_command))
    app.add_handler(CommandHandler("scrape", scrape_command))
    app.add_handler(CommandHandler("translate", translate_command))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    logger.info("Bot চালু হয়েছে!")
    app.run_polling()

if __name__ == "__main__":
    main()