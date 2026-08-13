# EAOS Delivery Applications (`apps/`)

Thư mục cấp cao quản lý 7 Kênh Giao tiếp & Phân phối (Delivery Edge Channels) của EAOS:

## Danh mục 7 Ứng dụng Delivery
1. `apps/api`: Pure Data REST/gRPC/SSE API Gateway (`:8000`).
2. `apps/web`: Web Control Room Dashboard UI (`:3000`).
3. `apps/cli`: Typer/Rich Command Line Interface.
4. `apps/agent`: Đội ngũ AI Agent thực thi tự trị.
5. `apps/desktop`: Native Desktop Application.
6. `apps/automation`: Kịch bản mô phỏng Dry-Run & Tự chữa lỗi.
7. `apps/ledger`: Sổ cái đúc khối bất biến Quantum Apps Ledger.

## Quy ước Phát triển (DX Rules)
- **Tên Packages**: Sử dụng `snake_case` (ví dụ `apps/agent`, `apps/api`).
- **Docstrings**: Tuân thủ chuẩn Google-style Docstrings cho Sphinx/Typedoc.
- **Biến môi trường**: Cấu hình `HOST` (mặc định `127.0.0.1`), `API_PORT` qua `.env`. Không bao giờ hardcode `0.0.0.0`.
