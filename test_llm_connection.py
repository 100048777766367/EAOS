import asyncio

from apps.api.app.adapters.llm.gemini import GeminiAdapter
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    adapter = GeminiAdapter()

    print("TESTING LLM...")

    try:
        chunks = [
            token
            async for token in adapter.generate_stream(
                messages=[
                    {
                        "role": "user",
                        "content": "Reply with exactly: EAOS_OK",
                    }
                ],
                temperature=0,
                max_output_tokens=20,
            )
        ]

        response = "".join(chunks)

        print("STATUS: SUCCESS")
        print("RESPONSE:", response)

    except Exception as exc:
        print("STATUS: FAILED")
        print("ERROR:", type(exc).__name__)
        print("DETAIL:", exc)


if __name__ == "__main__":
    asyncio.run(main())
