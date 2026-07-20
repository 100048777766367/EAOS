# ADR 002: Lựa Chọn PostgreSQL Làm Kho Lưu Trữ

## Status
Status: Draft

## Context
Chúng ta cần một cơ sở dữ liệu có cấu trúc ổn định và hỗ trợ tìm kiếm vector.

## Decision
Sử dụng PostgreSQL kết hợp phần mở rộng pgvector.

## Consequences
- **Ưu điểm:** Hợp nhất dữ liệu quan hệ, dữ liệu phi cấu trúc (JSONB) và dữ liệu vector vào cùng một thực thể duy nhất. Giảm tải tối đa việc đồng bộ dữ liệu chéo.
- **Nhược điểm:** Hiệu năng tìm kiếm vector quy mô lớn có thể chậm hơn các vector database chuyên dụng nếu không cấu hình tối ưu hóa chỉ mục HNSW.
