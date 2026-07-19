# ADR-006: Quy Chuẩn Biểu Quyết và Phản Biện Của Hội Đồng Kiến Trúc

## Status
Status: Accepted

## Context
Để ngăn chặn tình trạng rò rỉ kiến trúc và các AI Agents tự động sinh/sửa đổi code vô tội vạ, hệ thống bắt buộc phải có một rào cản quy trình rõ ràng. Mọi quyết định tiến hóa phải được kiểm duyệt thông qua sự phản biện đa chiều thay vì phê duyệt đồng bộ một chiều.

## Decision
Thiết lập quy trình 4 bước bắt buộc (Consensus and Rebuttal Protocol) cho mọi thay đổi cấu trúc:

```text
Kiến nghị (Proposal - PR) 
       │
       ▼
Ý kiến Phản biện (Objections / Rebuttals)
       │
       ▼
Biểu quyết Hội đồng (Council Voting)
       │
       ▼
Ghi sổ Ledger (Commit / Rollback)