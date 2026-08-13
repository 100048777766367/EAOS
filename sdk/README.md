# Phân Hệ Bộ Công Cụ Phát Triển Phần Mềm (EAOS Polyglot SDK v3.0)

## 1. Mục đích Kinh doanh
Quản trị bộ công cụ SDK phát triển ứng dụng đa ngôn ngữ (Python, Go, TypeScript),
môi trường nhúng WebAssembly/Single-file engine, chữ ký xác thực API cuộc gọi
và sổ cái kiểm toán chống lượng tử SHA3-256.

## 2. Phân lớp Kiến trúc
- python/: SDK Client thuần Python (Sync & AsyncIO).
- go/: SDK Client bằng ngôn ngữ Go (package eaos_sdk).
- 	ypescript/: SDK Client bằng TypeScript / Node.js.
- embedded/: Động cơ nhúng đơn tệp không phụ thuộc ngoài.
- wasm/: Đặc tả định dạng bộ nhớ ABI WebAssembly.
- ledger/: Sổ cái lưu vết chữ ký cuộc gọi SDK chống lượng tử.
- utomation/: Bộ mô phỏng Dry-Run & Tự phục hồi package.
