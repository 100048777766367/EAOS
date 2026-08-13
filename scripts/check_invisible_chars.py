# scripts/check_invisible_chars.py
import sys
from pathlib import Path

# Danh sách các ký tự ẩn / homograph nguy hiểm cần chặn tuyệt đối
FORBIDDEN_CHARS = {
    "\xa0": "Non-breaking space",
    "\ufeff": "Byte Order Mark (BOM)",
    "\u200b": "Zero-width space",
    "\u200c": "Zero-width non-joiner",
    "\u200d": "Zero-width joiner",
    "\u3000": "Ideographic space",
}


def main():
    has_error = False
    # Duyệt qua các file được git staging chuẩn bị commit
    for filename in sys.argv[1:]:
        path = Path(filename)
        if not path.exists() or path.suffix != ".py":
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            for char, name in FORBIDDEN_CHARS.items():
                if char in content:
                    print(f"[!] BẢO MẬT: Phát hiện ký tự cấm [{name}] trong tệp: {path}")
                    has_error = True
        except Exception as e:
            print(f"[!] Không thể quét tệp {path}: {e}")
            has_error = True

    if has_error:
        print("[!] Commit bị từ chối. Vui lòng làm sạch mã nguồn trước khi đẩy lên hệ thống.")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
