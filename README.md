# EAOS (Enterprise Architecture Operating System)

## Tổng quan
Hệ thống kiến trúc doanh nghiệp tự động hóa, quản trị bởi mã nguồn và các nguyên tắc kiến trúc (Constitution).

## Cấu trúc Workspace
- `/services`: Các core services của hệ thống.
- `/libs`: Các thư viện chia sẻ.
- `/docs`: Tài liệu kiến trúc và quản trị.

## Bắt đầu (Quick Start)
1. Cài đặt phụ thuộc Python: `python -m pip install -r requirements.txt`
2. Chạy kiểm thử: `make test`
3. Khởi chạy web (local): `make run-web`

Thực hiện kiểm tra chất lượng: `make lint`

## Quản trị (Governance)
Mọi thay đổi kiến trúc phải tuân thủ `ARCHITECTURE_CONSTITUTION.md` và `ADR_INDEX.md`.

## License
Proprietary - EAOS Architecture Team