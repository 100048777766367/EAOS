# ENTERPRISE EVIDENCE & DECISION GOVERNANCE LEDGER

> **Tài liệu này ghi nhận toàn bộ Bằng chứng (Evidence), Quyết định (Decision) và Vòng lặp Học tập (Learning Loop) của EAOS.**

## [VERIFIED_AND_LEARNED] EV-20260722-001 — architecture_test_failed
* **Nguồn phát hiện:** `CI/CD Pipeline & Architecture Validator`
* **Số lần xuất hiện (Occurrence Count):** `3 lần`
* **Thời gian ghi nhận:** `2026-07-22T16:10:00Z`

### 1. Bằng chứng Đo lường (Observed Evidence):
- **Metric:** `Domain Separation & Signature Compliance`
- **Giá trị quan sát:** `TypeError: calculate_block_hash() got unexpected keyword 'timestamp'`

### 2. Định tuyến Quy tắc & Hiến pháp (Rule & Policy Traceability):
- **Mã Rule:** `R-ARCH-001` (Domain Isolation Protection Rule)
- **Capability liên kết:** `capability.architecture_governance`
- **Nguyên tắc Hiến pháp:** `P5 — Stable Core, Flexible Edge`
- **Sổ cái ADR:** `ADR-004`

### 3. Đánh giá Quản trị & Quyết định (Governance & Decision):
- **Trạng thái phê duyệt:** `AUTOMATICALLY_APPROVED` (Bởi `Autonomous Self-Healing Engine`)
- **Hành động chốt:** `AUTO_REMEDY_CODE_PATCH`
- **Cơ sở lý giải (Rationale):** Cung cấp kwargs linh hoạt cho calculate_block_hash để đảm bảo tính tương thích 100%.

### 4. Bằng chứng Kiểm định Khôi phục (Verification Proof):
✔ `Ruff & Mypy PASS 100% - 17/17 tests passed`

---

## [VERIFIED_AND_LEARNED] EV-20260722-002 — backwards_compatibility_violation
* **Nguồn phát hiện:** `Evolution Engine & Policy Validator`
* **Số lần xuất hiện (Occurrence Count):** `2 lần`
* **Thời gian ghi nhận:** `2026-07-22T16:20:00Z`

### 1. Bằng chứng Đo lường (Observed Evidence):
- **Metric:** `Type Schema Consistency`
- **Giá trị quan sát:** `Migration rule default:5 assigned string '5' to int field max_retry_loops`

### 2. Định tuyến Quy tắc & Hiến pháp (Rule & Policy Traceability):
- **Mã Rule:** `R-EVO-002` (Backwards Compatibility Rule)
- **Capability liên kết:** `capability.evolution_management`
- **Nguyên tắc Hiến pháp:** `P4 — Evolution Over Convenience`
- **Sổ cái ADR:** `ADR-006`

### 3. Đánh giá Quản trị & Quyết định (Governance & Decision):
- **Trạng thái phê duyệt:** `AUTOMATICALLY_APPROVED` (Bởi `Policy Engine`)
- **Hành động chốt:** `AUTO_CAST_DATA_TYPES`
- **Cơ sở lý giải (Rationale):** Ép kiểu tự động int/float trong migrate_payload để giữ nguyên kiểu dữ liệu nguyên thủy.

### 4. Bằng chứng Kiểm định Khôi phục (Verification Proof):
✔ `Autonomous closed loop cycle status == 201 Created`

---
