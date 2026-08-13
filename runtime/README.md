# Phân Hệ Vận Hành Thời Gian Thực Doanh Nghiệp (EAOS Runtime Engine v3.0)

## 1. Mục đích Kinh doanh
Quản trị trạng thái vận hành thời gian thực của hệ điều hành doanh nghiệp,
bao gồm bộ nhớ đệm Splay Cache, Event Mesh Queue, Khám phá dịch vụ (Service Discovery),
State Machine (FSM), Prometheus Metrics, Phiên làm việc và Sổ cái vết thực thi chống lượng tử.

## 2. Phân lớp Kiến trúc
- cache/: Động cơ quản lý bộ nhớ đệm Splay Cache.
- events/: Động cơ Event Mesh Queue chuẩn NDJSON.
- governance/: Động cơ kiểm tra lịch sử kiểm toán vận hành.
- inventory/: Động cơ quét và ghi nhận tài sản hạ tầng.
- logs/: Hệ thống ghi nhật ký tập trung có Correlation ID.
- metrics/: Động cơ thu thập chỉ số Prometheus Realtime.
- policies/: Động cơ thực thi chính sách runtime chủ động.
- egistry/: Động cơ đăng ký và kiểm tra sức khỏe dịch vụ.
- sessions/: Động cơ quản lý phiên đăng nhập và TTL Token.
- state/: Động cơ chuyển trạng thái hữu hạn FSM Machine.
- 	mp/: Vùng làm việc tạm thời tự dọn dẹp xoay vòng.
- 	races/: Sổ cái vết thực thi mã hóa SHA3-256 chống lượng tử.
- utomation/: Bộ mô phỏng Failover & Tự phục hồi dọn rác package.
