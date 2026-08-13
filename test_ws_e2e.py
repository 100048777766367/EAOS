import asyncio
import json

import websockets


async def main():
    uri = "ws://localhost:8000/ws/chat"

    async with websockets.connect(uri) as ws:
        request = {
            "conversation_id": "e2e-test-001",
            "message": "Reply with exactly: EAOS_E2E_OK",
            "agent_role": "coder",
            "system_instruction": "",
            "active_file": "apps/api/app/routers/chat.py",
            "temperature": 0.0,
            "max_output_tokens": 64,
            "json_mode": False,
        }

        await ws.send(json.dumps(request))

        while True:
            raw = await ws.recv()
            event = json.loads(raw)

            print(json.dumps(event, indent=2, ensure_ascii=False))

            if event.get("type") in {
                "response_complete",
                "stream_error",
            }:
                break


asyncio.run(main())
