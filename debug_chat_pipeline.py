"""Diagnostic script to test end-to-end EAOS Chat Pipeline FOR REAL."""

import asyncio
import os
from pathlib import Path

import httpx

# 1. Tự động nạp file .env
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip("'").strip('"')
            if k and v:
                os.environ[k] = v

print("=" * 60)
print("EAOS REAL CHAT PIPELINE DIAGNOSTIC")
print("=" * 60)

# Check Environment Variables
gemini_keys = os.getenv("GEMINI_API_KEYS", "") or os.getenv("GEMINI_API_KEY", "")
ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

print("[1] KIỂM TRA BIẾN MÔI TRƯỜNG (.env):")
print(f"    - Co Gemini API Key: {bool(gemini_keys)}")
print(f"    - Ollama URL: {ollama_url}")
print(f"    - Gemini Model: {gemini_model}")


# 2. Test kết nối trực tiếp đến Google Gemini API
async def test_gemini():
    print("\n[2] KIỂM TRA KẾT NỐI GEMINI API THẬT...")
    if not gemini_keys:
        print("    ❌ FAIL: Khong tim thay GEMINI_API_KEY trong file .env!")
        return False

    key = gemini_keys.split(",")[0].strip().strip("'").strip('"')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": "Xin chao"}]}]}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.post(url, json=payload)
            print(f"    - Gemini Response Status: {res.status_code}")
            if res.status_code == 200:
                print("    ✅ SUCCESS: Gemini API Key HOẠT ĐỘNG TỐT!")
                return True
            print(f"    ❌ FAIL: Gemini phan hoi loi: {res.text[:200]}")
            return False
    except Exception as exc:
        print(f"    ❌ FAIL: Loi ket noi Gemini: {exc}")
        return False


# 3. Test kết nối Container Ollama Local
async def test_ollama():
    print("\n[3] KIỂM TRA CONTAINER OLLAMA LOCAL THẬT...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.get(f"{ollama_url}/api/tags")
            print(f"    - Ollama Status: {res.status_code}")
            if res.status_code == 200:
                models = res.json().get("models", [])
                model_names = [m.get("name") for m in models]
                print(f"    - Cac Model Ollama da cai dat: {model_names}")
                if model_names:
                    print("    ✅ SUCCESS: Ollama dang chay va DA CO MODEL!")
                    return True
                print("    ⚠️ FAIL: Ollama dang chay nhung CHƯA CÓ MODEL!")
                print("       Huong dan: Chay 'docker exec -it eaos-ollama ollama pull llama3'")
                return False
            print("    ❌ FAIL: Ollama phan hoi status xau")
            return False
    except Exception as exc:
        print(f"    ❌ FAIL: Khong the ket noi den Ollama tai {ollama_url}: {exc}")
        return False


# 4. Test WebSocket Server
async def test_websocket():
    print("\n[4] KIỂM TRA KẾT NỐI WEBSOCKET THẬT (ws://127.0.0.1:8000/ws/chat)...")
    url = "http://127.0.0.1:8000/v1/chat/completions"
    payload = {"model": "ollama", "messages": [{"role": "user", "content": "Test diagnostic"}]}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.post(url, json=payload)
            print(f"    - REST API Gateway Status: {res.status_code}")
            if res.status_code == 200:
                print(f"    - Response: {res.text[:150]}")
                print("    ✅ SUCCESS: REST API Gateway phan hoi thanh cong!")
                return True
            print(f"    ❌ FAIL: REST API Status {res.status_code}")
            return False
    except Exception as exc:
        print(f"    ❌ FAIL: Loi ket noi Server: {exc}")
        return False


async def main():
    has_gemini = await test_gemini()
    has_ollama = await test_ollama()
    has_ws = await test_websocket()

    print("\n" + "=" * 60)
    print("TỔNG KẾT BẢNG CHẨN ĐOÁN:")
    print(f"  - Kết nối Gemini API:   {'✅ HOẠT ĐỘNG' if has_gemini else '❌ LỖI / CHƯA CÓ KEY'}")
    print(f"  - Kết nối Ollama Local: {'✅ HOẠT ĐỘNG' if has_ollama else '❌ LỖI / CHƯA PULL MODEL'}")
    print(f"  - Kết nối Server API:   {'✅ HOẠT ĐỘNG' if has_ws else '❌ LỖI SERVER'}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
