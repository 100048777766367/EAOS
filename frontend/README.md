# EAOS Frontend (Feature-Based Next.js Application)

Ứng dụng Giao diện Điều hành EAOS được tổ chức theo kiến trúc Feature-Based:
- `src/features/`: Gom nhóm components, hooks, types theo từng miền tính năng (`control-room`, `knowledge`).
- `src/services/`: Quản lý API Client và luồng dữ liệu thời gian thực Server-Sent Events (SSE).
- `src/layouts/`: Bố cục khung giao diện chung.
- `src/store/`: Quản lý trạng thái chung.
