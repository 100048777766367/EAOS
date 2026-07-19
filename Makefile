# ==============================================================================
# EAOS OPERATING SYSTEM PLATFORM WORKSPACE ORCHESTRATOR
# ==============================================================================

.PHONY: help init install compose-up compose-down lint format test validate graph metrics time-machine twin compile-spec loop dlm clean

help:
	@echo "EAOS Platform Tasks:"
	@echo "  make init          - Khởi tạo tệp môi trường thực tế .env từ mẫu"
	@echo "  make install       - Cài đặt và đồng bộ hóa toàn bộ UV Workspace"
	@echo "  make compose-up    - Khởi chạy các container PostgreSQL, Redis, MinIO ngầm"
	@echo "  make compose-down  - Dừng và thu hồi các container cơ sở dữ liệu"
	@echo "  make lint          - Kiểm tra tĩnh chất lượng mã nguồn qua Ruff & MyPy"
	@echo "  make format        - Tự động hóa định dạng lại toàn bộ repo qua Ruff"
	@echo "  make test          - Thực thi toàn bộ bộ kiểm thử tự động Pytest"
	@echo "  make validate      - Chạy kiểm toán ranh giới kiến trúc & sáp nhập"
	@echo "  make graph         - Tự động sinh đồ thị dependencies giữa các packages"
	@echo "  make metrics       - Đo lường chỉ số Instability (I) hằng ngày"
	@echo "  make time-machine  - Chụp ảnh kiến trúc hoặc đối chiếu lịch sử"
	@echo "  make twin          - Chạy giả lập Bản sao số kiểm định đề xuất mới"
	@echo "  make compile-spec  - Biên dịch đặc tả thành mã nguồn Python & IaC"
	@echo "  make loop          - Khởi chạy Vòng lặp tiến hóa tự trị đóng kín"
	@echo "  make dlm           - Quản lý vòng đời tài liệu có mã hóa bảo mật"
	@echo "  make clean         - Dọn sạch các tệp cache phân giải"

init:
	@if [ ! -f .env ]; then cp .env.example .env; echo "Khởi tạo .env thành công."; else echo ".env đã tồn tại."; fi

install:
	uv sync

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

lint:
	uv run taskipy lint

format:
	uv run taskipy format

test:
	uv run taskipy test

validate:
	uv run taskipy validate

graph:
	uv run taskipy graph

metrics:
	uv run taskipy metrics

time-machine:
	uv run taskipy time-machine

twin:
	uv run taskipy twin

compile-spec:
	uv run taskipy compile

loop:
	uv run taskipy loop

dlm:
	uv run taskipy dlm

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf generated/