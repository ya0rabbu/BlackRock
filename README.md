# 🤖 BlackRock Bot

An advanced Telegram bot with AI, scraping, weather, news, and more!

## ✨ Features

- 🤖 AI Chat (HuggingFace)
- 🌐 Web Scraping
- 📰 News Alert
- 🌤 Weather Info
- 📄 Document Processing (PDF/Excel)
- 🌍 Multi-language Translation
- 📊 Data Analytics & Report
- 🔗 Webhook System
- ⏰ Task Scheduler

## 🚀 Commands

| Command           | Description           |
| ----------------- | --------------------- |
| /start            | Bot শুরু করো          |
| /ai [message]     | AI Chat               |
| /weather [city]   | আবহাওয়া দেখো         |
| /news [topic]     | News দেখো             |
| /scrape [url]     | Website Scrape করো    |
| /translate [text] | Translation করো       |
| /analyze          | PDF/Excel analyze করো |
| /help             | সব commands           |

## ⚙️ Setup

1. Clone the repository
2. Create `.env` file
3. Add your API keys
4. Run `pip install -r requirements.txt`
5. Run `python main.py`

## 🔑 Required API Keys

- Telegram Bot Token (t.me/BotFather)
- HuggingFace Token (huggingface.co)
- OpenWeather API (openweathermap.org)
- News API (newsapi.org)

## 📦 Tech Stack

- Python 3.10+
- python-telegram-bot
- FastAPI
- PostgreSQL
- HuggingFace API
