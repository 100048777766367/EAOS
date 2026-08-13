# Phân Hệ Đặc Tả Thực Thi Doanh Nghiệp (EAOS Specifications Engine v3.0)

## 1. Mục đích Kinh doanh
Quản trị toàn bộ các tệp đặc tả kiến trúc doanh nghiệp (Executable Specifications),
kiểm tra tính tuân thủ của codebase theo quy định kiến trúc và ngăn ngừa
hiện tượng trôi dạt kiến trúc (Architecture Drift).

## 2. Phân lớp Kiến trúc
- pis/: Động cơ kiểm tra đặc tả cổng giao diện API.
- usiness/: Động cơ kiểm tra đặc tả quy trình nghiệp vụ.
- capabilities/: Động cơ kiểm tra đặc tả năng lực kinh doanh.
- domains/: Động cơ kiểm tra đặc tả miền Bounded Context.
- services/: Động cơ kiểm tra đặc tả vi dịch vụ hạ tầng.
- workflows/: Động cơ kiểm tra đặc tả luồng tự động phục hồi.
- parser/: Trình đọc và phân tích cấu trúc Markdown/YAML Specs.
- ledger/: Sổ cái lưu vết bằng chứng đặc tả chống lượng tử.
- utomation/: Bộ mô phỏng Drift & Tự phục hồi package.
