import asyncio
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["GEMINI_API_KEY"].strip()
MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest").strip()
MODEL = MODEL.removeprefix("models/")

URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:streamGenerateContent"

PAYLOAD = {
    "contents": [
        {
            "role": "user",
            "parts": [{"text": "Reply with exactly: EAOS_OK"}],
        }
    ],
    "generationConfig": {"maxOutputTokens": 4096},
}


async def main():
    async with (
        httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=15.0,
                read=180.0,
                write=30.0,
                pool=30.0,
            )
        ) as client,
        client.stream(
            "POST",
            URL,
            params={
                "key": API_KEY,
                "alt": "sse",
            },
            json=PAYLOAD,
        ) as response,
    ):
        print("HTTP:", response.status_code)

        if response.status_code >= 400:
            print(
                (await response.aread()).decode(
                    "utf-8",
                    errors="replace",
                )
            )
            return

        async for line in response.aiter_lines():
            if line:
                print(line)


asyncio.run(main())
