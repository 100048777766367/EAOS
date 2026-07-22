# SỔ CÁI NHẬT KÝ SỰ CỐ VÀ PHƯƠNG PHÁP KHẮC PHỤC (POSTMORTEM LEDGER)

> **Tài liệu này được tự động cập nhật bởi EAOS Autonomic Self-Healing Engine.**

## INC-BLOCK-HASH-SIGNATURE-MISMATCH — packages/civilization/infrastructure/adapters.py | TypeError: calculate_block_hash() got unexpected keyword argument 'timestamp'
* **Số lần xuất hiện:** `3 lần`
* **Thời gian phát hiện đầu tiên:** `2026-07-22T16:10:00Z`
* **Thời gian cập nhật mới nhất:** `2026-07-22T09:19:43.523853+00:00`

### 1. Diễn biến sự cố (Timeline):
- 16:10:00 - Pytest ngắt tại khâu collect do TypeError hàm calculate_block_hash.
- 16:12:00 - Mypy phát hiện 17 lỗi liên quan đến thiếu trường trong models/ports.
- 16:15:00 - Cập nhật signature linh hoạt cho calculate_block_hash và bổ sung các phương thức thiếu.

### 2. Phân tích nguyên nhân gốc rễ (Root Cause Analysis):
Hàm calculate_block_hash chỉ nhận timestamp_str trong khi adapters truyền timestamp (dạng datetime). Đồng thời các Pydantic model thiếu các field alias.

### 3. Đánh giá các phương án (Proposed Options & Rationale):
- **[CHOSEN]** Cung cấp kwargs linh hoạt cho calculate_block_hash và bổ sung các trường alias vào models.py
  *Lý do:* Đảm bảo tính tương thích tuyệt đối cho cả 2 cách gọi hàm mà không làm vỡ các use cases hiện hữu.

### 4. Phương pháp sửa đổi (Remedy Method):
```text
Đồng bộ hóa signature hàm calculate_block_hash và định nghĩa đầy đủ phương thức save_block trên Port & Adapter.
```

### 5. Bằng chứng kiểm định (Verification Proof):
✔ `Pytest & Mypy PASS 100%.`

---
