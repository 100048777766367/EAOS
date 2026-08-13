import json

import httpx

API_KEY = "AIzaSyBt91rKgX4kROC5BvwgyjI63vi1DDmYa8s"  # dán key thật vào đây

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    resp = httpx.get(url, timeout=20.0)
    print("👉 Status Code:", resp.status_code)
    print("👉 Raw Response:")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print("❌ Lỗi:", e)
