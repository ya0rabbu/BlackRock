from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.news_handler import get_news
from handlers.weather_handler import get_weather
import os

scheduler = AsyncIOScheduler()

def start_scheduler(bot, chat_id: str):
    scheduler.add_job(
        send_daily_news,
        "cron",
        hour=8,
        minute=0,
        args=[bot, chat_id]
    )
    scheduler.add_job(
        send_daily_weather,
        "cron",
        hour=7,
        minute=0,
        args=[bot, chat_id]
    )
    scheduler.start()

async def send_daily_news(bot, chat_id: str):
    news = await get_news("technology")
    await bot.send_message(chat_id=chat_id, text=news)

async def send_daily_weather(bot, chat_id: str):
    weather = await get_weather("Dhaka")
    await bot.send_message(chat_id=chat_id, text=weather)