import os
from pathlib import Path


def clean_yaml_files(directory="."):
    ignore_dirs = {".git", ".venv", "__pycache__", ".pytest_tmp"}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith((".yml", ".yaml")):
                filepath = Path(root) / file
                try:
                    with open(filepath, "rb") as f:
                        raw = f.read()
                    # Lọc bỏ ký tự không thuộc phạm vi in được hoặc mã độc/rác x008f
                    cleaned = bytes([b for b in raw if b == 9 or b == 10 or b == 13 or (b >= 32 and b != 143)])
                    if raw != cleaned:
                        with open(filepath, "wb") as f:
                            f.write(cleaned)
                        print(f"[✓] Đã làm sạch YAML: {filepath}")
                except Exception as e:
                    print(f"[!] Lỗi đọc file {filepath}: {e}")


if __name__ == "__main__":
    clean_yaml_files()
