import httpx
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

async def test():
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        data = response.json()
        print("Available Claude models:")
        for model in data.get("data", []):
            if "claude" in model["id"].lower():
                print(" -", model["id"])

asyncio.run(test())
