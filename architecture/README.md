# Phân Hệ Kiến Trúc Doanh Nghiệp Cốt Lõi (EAOS Architecture Engine v3.0)

## 1. Mục đích Kinh doanh
Quản trị toàn bộ mô hình C4 Metamodel (Context, Container, Component, Code),
Ma trận 52 Tầng Kiến trúc Canonical, động cơ quản lý quyết định kiến trúc (ADRs),
xuất sơ đồ Mermaid/SVG và đúc sổ cái bằng chứng kiến trúc chống lượng tử SHA3-256.

## 2. Phân lớp Kiến trúc
- decisions/: Động cơ quản lý và đánh giá quyết định kiến trúc (ADR Manager).
- models/: Động cơ C4 Metamodel và kiểm toán 52 Canonical Layers Matrix.
- iews/: Động cơ xuất chiếu sơ đồ Mermaid và View Renderer.
- ledger/: Sổ cái chứng nhận bằng chứng quyết định kiến trúc chống lượng tử.
- utomation/: Bộ mô phỏng thay đổi kiến trúc & Tự phục hồi package.
