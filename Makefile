.PHONY: sync doctor lint test run clean format

# Đồng bộ hóa dependencies và workspace
sync:
	uv sync

# Chẩn đoán sức khỏe hệ thống qua tools/doctor
doctor:
	uv run python tools/doctor/main.py

# Kiểm tra chất lượng mã nguồn và typing
lint:
	uv run ruff check .
	uv run mypy apps/ kernel/ engine/ packages/ tools/ tests/

# Tự động định dạng mã nguồn theo chuẩn Ruff
format:
	uv run ruff format .

# Chạy toàn bộ bộ kiểm thử tự động
test:
	uv run pytest tests/

# Chạy thử nghiệm lõi Kernel thông qua module runtime
run:
	uv run python -m kernel.runtime.main

# Dọn dẹp các tệp tạm và bộ nhớ cache
clean:
	rm -rf .venv/ .pytest_cache/ __pycache__/ .ruff_cache/ .mypy_cache/