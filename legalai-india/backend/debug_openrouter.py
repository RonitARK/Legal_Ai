import httpx
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

async def test():
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4.5",
                "max_tokens": 100,
                "messages": [{"role": "user", "content": "Say hello in one word."}]
            }
        )
        print("Status:", response.status_code)
        print("Response:", response.text)

asyncio.run(test())
