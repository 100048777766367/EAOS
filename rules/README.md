# Phân Hệ Quản Trị Quy Tắc Doanh Nghiệp (EAOS Rules Engine v3.0)

## 1. Mục đích Kinh doanh
Quản trị toàn bộ tập quy tắc chính sách doanh nghiệp (Governance Policy as Code),
đánh giá tuân thủ tự động theo thời gian thực cho 8 miền cốt lõi.

## 2. Phân lớp Kiến trúc
- i/: Quy tắc kiểm soát độ trôi mô hình AI Drift.
- rchitecture/: Quy tắc ranh giới cô lập Hexagonal.
- usiness/: Quy tắc quyết định giá trị đơn hàng.
- compliance/: Quy tắc thời gian lưu trữ GDPR.
- engineering/: Quy tắc giới hạn dòng code < 80 chars.
- quality/: Quy tắc cổng kiểm soát MyPy Strict.
- untime/: Quy tắc chịu lỗi Circuit Breaker.
- security/: Quy tắc quét lộ Secret.
- evaluator/: Trình phân tích YAML & Biên dịch OPA Rego.
- ledger/: Sổ cái kiểm toán chống lượng tử.
- utomation/: Bộ mô phỏng Dry-Run & Tự phục hồi.
