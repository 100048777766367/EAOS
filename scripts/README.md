# Phân Hệ Kịch Bản Tự Động Hóa Doanh Nghiệp (EAOS Scripts Engine v3.0)

## 1. Mục đích Kinh doanh
Quản trị toàn bộ tập kịch bản tự động hóa vận hành, bảo trì, phục hồi tự động,
CI/CD Quality Gates, khởi chạy Control Room và môi trường sản xuất.

## 2. Phân lớp Kiến trúc
- powershell/: Động cơ điều phối kịch bản PowerShell (.ps1).
- ash/: Động cơ điều phối kịch bản Bash/POSIX (.sh).
- python_tasks/: Động cơ điều phối kịch bản bảo trì Python (.py).
- cicd/: Động cơ quản lý cổng kiểm soát tích hợp liên tục.
- healing/: Động cơ phục hồi đa chiến lược hệ thống.
- ledger/: Sổ cái lưu vết thực thi kịch bản chống lượng tử.
- utomation/: Bộ mô phỏng Dry-Run & Tự phục hồi package.
