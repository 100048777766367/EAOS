from fastapi.testclient import TestClient
from apps.api.app.main import app

client = TestClient(app)

print("=== WS TEXT MESSAGE TEST ===")

with client.websocket_connect("/ws/chat") as ws:
    print("CONNECTED = YES")
    ws.send_text("hello")
    print("SENT = hello")

    try:
        response = ws.receive_text()
        print("RECEIVED TEXT =", response)
    except Exception as e:
        print("RECEIVE ERROR =", type(e).__name__, str(e))
