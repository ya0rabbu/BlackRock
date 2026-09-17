import httpx
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

async def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "en"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        if data.get("cod") != 200:
            return "শহরের নাম সঠিক দাও।"
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        return (
            f"🌤 {city} এর আবহাওয়া:\n"
            f"তাপমাত্রা: {temp}°C\n"
            f"অবস্থা: {weather}\n"
            f"আর্দ্রতা: {humidity}%\n"
            f"বাতাস: {wind} m/s"
        )