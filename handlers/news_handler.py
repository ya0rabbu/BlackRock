import httpx
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

async def get_news(topic: str = "technology") -> str:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "apiKey": NEWS_API_KEY,
        "pageSize": 5,
        "sortBy": "publishedAt",
        "language": "en"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            return "কোনো news পাওয়া যায়নি।"
        result = f"📰 {topic} এর latest news:\n\n"
        for i, article in enumerate(articles[:5], 1):
            result += f"{i}. {article['title']}\n🔗 {article['url']}\n\n"
        return result