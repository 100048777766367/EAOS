# Phân Hệ Bộ Máy Tự Trị Đa Agent Swarm (EAOS Agents Engine v3.0)

## 1. Mục đích Kinh doanh
Quản trị mạng lưới các Agent tự trị (Architect, Coder, Operator, Planner,
Reviewer, Security, Tester), điều phối Swarm Message Bus, phân bổ công việc
và đúc sổ cái bằng chứng quyết định Agent chống lượng tử SHA3-256.

## 2. Phân lớp Kiến trúc
- rchitect/: Agent chuyên trách thiết kế C4 Metamodels & ADRs.
- coder/: Agent chuyên trách tổng hợp mã nguồn & tạo bản vá minimal diff.
- operator/: Agent chuyên trách vận hành SRE runbooks & Docker/K8s.
- planner/: Agent chuyên trách lập kế hoạch sprint & phân rã DAG tasks.
- eviewer/: Agent chuyên trách kiểm duyệt chất lượng Ruff/MyPy code.
- security/: Agent chuyên trách rà quét lỗ hổng & Threat Modeling.
- 	ester/: Agent chuyên trách sinh bài test Pytest & xác minh coverage.
- swarm/: Giao thức truyền thông điệp liên Agent Swarm Message Bus.
- ledger/: Sổ cái chứng nhận vết quyết định Agent chống lượng tử.
- utomation/: Bộ mô phỏng phân phối task Agent & Tự phục hồi package.
