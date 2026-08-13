import os
from pathlib import Path


def sanitize_codebase(directory="."):
    # Ma trận thay thế: Ký tự gây hỏng AST -> Ký tự chuẩn
    CHAR_MAP = {
        "\xa0": " ",  # Non-breaking space -> Khoảng trắng chuẩn
        "\ufeff": "",  # Xóa BOM
        "\u200b": "",  # Xóa Zero-width space
        "\u200c": "",  # Xóa Zero-width non-joiner
        "\u200d": "",  # Xóa Zero-width joiner
        "\u3000": " ",  # Ideographic space -> Khoảng trắng chuẩn
    }

    ignore_dirs = {".git", ".venv", "__pycache__", ".pytest_tmp"}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if not file.endswith(".py"):
                continue

            filepath = Path(root) / file
            try:
                # Đọc byte thô, decode bỏ qua byte lỗi (tránh crash với non-UTF8)
                with open(filepath, "rb") as f:
                    raw_content = f.read().decode("utf-8", errors="ignore")

                cleaned_content = raw_content
                for bad_char, good_char in CHAR_MAP.items():
                    cleaned_content = cleaned_content.replace(bad_char, good_char)

                # Chuẩn hóa line-ending thành LF và xóa khoảng trắng rác cuối dòng
                lines = [line.rstrip() for line in cleaned_content.splitlines()]
                final_content = "\n".join(lines) + "\n"

                if raw_content != final_content:
                    # Ép ghi lại bằng UTF-8 No BOM
                    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
                        f.write(final_content)
                    print(f"[✓] Đã làm sạch: {filepath}")
            except Exception as e:
                print(f"[!] Bỏ qua {filepath}: {e}")


if __name__ == "__main__":
    sanitize_codebase()
