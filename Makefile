.PHONY: setup lock sync lint test clean

# Thiết lập môi trường phát triển
setup:
	@echo "Initializing EAOS workspace..."
	uv sync

# Khóa dependencies
lock:
	@echo "Generating lockfile..."
	uv lock

# Đồng bộ môi trường
sync:
	@echo "Syncing dependencies..."
	uv sync --frozen

# Linting và Format
lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .

# Kiểm thử hệ thống
test:
	uv run pytest tests/

# Vệ sinh workspace
clean:
	rm -rf .venv/ .pytest_cache/ __pycache__/ .ruff_cache/