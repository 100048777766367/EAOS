import asyncio
from pathlib import Path

from apps.api.app.services.chat.verification_pipeline import (
    VerificationPipeline,
)


async def main():
    pipeline = VerificationPipeline(Path.cwd())
    print("START")
    result = await pipeline.run_checks_async()
    print("RESULT")
    print(result)


asyncio.run(main())
