import httpx
from bs4 import BeautifulSoup

async def scrape_website(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        lines = [line for line in text.splitlines() if len(line) > 30]
        return "\n".join(lines[:20]) or "কোনো content পাওয়া যায়নি।"