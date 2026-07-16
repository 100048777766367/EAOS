# EAOS (Enterprise Architecture Operating System)

## Tổng quan
Hệ thống kiến trúc doanh nghiệp tự động hóa, quản trị bởi mã nguồn và các nguyên tắc kiến trúc (Constitution).

## Cấu trúc Workspace
- `/services`: Các core services của hệ thống.
- `/libs`: Các thư viện chia sẻ.
- `/docs`: Tài liệu kiến trúc và quản trị.

## Bắt đầu (Quick Start)
1. Cài đặt `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Khởi tạo môi trường: `make setup`
3. Chạy kiểm thử: `make test`

## Quản trị (Governance)
Mọi thay đổi kiến trúc phải tuân thủ `ARCHITECTURE_CONSTITUTION.md` và `ADR_INDEX.md`.

## License
Proprietary - EAOS Architecture Team