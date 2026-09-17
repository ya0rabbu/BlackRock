import httpx
import os

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

async def ai_chat(message: str) -> str:
    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    payload = {
        "inputs": f"<s>[INST] {message} [/INST]",
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(API_URL, headers=headers, json=payload)
        result = response.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "কোনো উত্তর পাওয়া যায়নি।")
        return "AI এখন busy, একটু পরে try করো।"