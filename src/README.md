# Phân Hệ Mã Nguồn Cốt Lõi (EAOS SRC Clean Architecture v3.0)

## 1. Mục đích Kinh doanh
Quản trị toàn bộ mã nguồn mô hình Domain Model, Use Cases, Application Ports
và Infrastructure Adapters theo nguyên lý Clean/Hexagonal Architecture.

## 2. Phân lớp Kiến trúc
- domain/: Lõi domain thuần khiết (Domain Models, Aggregates, Domain Services).
- pplication/: Lớp ứng dụng (Application Ports & Use Cases Orchestration).
- infrastructure/: Lớp hạ tầng (Persistence Adapters & Post-Quantum Ledger).
- utomation/: Bộ mô phỏng Dry-Run & Tự phục hồi package.
