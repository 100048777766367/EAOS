import asyncio
import json

import websockets


async def main() -> None:
    print("Connecting...")

    async with websockets.connect(
        "ws://127.0.0.1:8000/ws/chat",
        open_timeout=10,
        close_timeout=10,
    ) as ws:
        print("CONNECTED")

        payload = {
            "conversation_id": "debug-001",
            "message": "hello",
            "agent_role": "coder",
            "system_instruction": "",
            "active_file": "",
            "temperature": 0.7,
            "max_output_tokens": 100,
            "json_mode": False,
        }

        print("Sending...")
        await ws.send(json.dumps(payload))
        print("SENT")

        try:
            while True:
                message = await asyncio.wait_for(
                    ws.recv(),
                    timeout=120,
                )

                print("RECV:", message)

                try:
                    event = json.loads(message)
                except json.JSONDecodeError:
                    continue

                if event.get("type") == "task_lifecycle":
                    state = event.get("state")

                    if state in {"COMPLETED", "FAILED"}:
                        print(f"FINAL STATE: {state}")
                        break

                if event.get("type") == "verification_result":
                    status = event.get("status")
                    print(f"VERIFICATION STATUS: {status}")

        except TimeoutError:
            print("TIMEOUT: no WebSocket event received for 120 seconds")

        except websockets.ConnectionClosed as exc:
            print(f"CLOSED: code={exc.code} reason={exc.reason}")


if __name__ == "__main__":
    asyncio.run(main())
