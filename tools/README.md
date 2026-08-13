# Phân Hệ Công Cụ và Tiện Ích Hạ Tầng Doanh Nghiệp (EAOS Tools Engine v3.0)

## 1. Mục đích Kinh doanh
Quản trị toàn bộ tập công cụ CLI, chẩn đoán Doctor v2 (10/10 Checkers),
kiểm toán ranh giới Hexagonal, kịch bản Chaos Engineering, exporter Grafana,
tự vá lỗi không gian làm việc và đúc sổ cái bằng chứng thực thi công cụ.

## 2. Phân lớp Kiến trúc
- cli/: Giao diện dòng lệnh tập trung EAOS CLI Main.
- doctor/: Động cơ chẩn đoán sức khỏe Doctor v2 với Checkers & Reporters.
- alidate/: Động cơ kiểm toán ranh giới kiến trúc Hexagonal.
- chaos/: Động cơ Chaos Engineering và thử nghiệm độ chịu tải.
- itness/: Động cơ chấm điểm Architecture Fitness Functions.
- ootstrap/: Động cơ khởi tạo và tối ưu hóa môi trường dev.
- ops/: Bộ kịch bản tự động vá lỗi, seed dữ liệu MinIO/Neo4j.
- ledger/: Sổ cái lưu vết thực thi công cụ chống lượng tử.
- utomation/: Bộ mô phỏng Dry-Run & Tự phục hồi package.
