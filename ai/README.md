# Phân Hệ Trí Tuệ Nhân Tạo và Điều Tuyến LLM (EAOS AI Engine v3.0)

## 1. Mục đích Kinh doanh
Quản trị toàn bộ năng lực AI doanh nghiệp, điều tuyến mô hình LLM theo
chi phí/độ trễ, quản lý Prompt Templates (Jinja2), kiểm soát ảo giác
(Hallucination Guard), suy luận Chain-of-Thought và đúc sổ cái bằng chứng
suy luận AI chống lượng tử SHA3-256.

## 2. Phân lớp Kiến trúc
- evaluation/: Động cơ kiểm tra độ trung thực và rà soát ảo giác AI.
- memory/: Động cơ quản lý cửa sổ ngữ cảnh Token Context Window.
- models/: Động cơ kết nối các nhà cung cấp mô hình AI Providers.
- planner/: Động cơ phân rã mục tiêu phức tạp thành các sub-tasks.
- prompts/: Động cơ quản lý và tối ưu hóa Prompt Templates Jinja2.
- easoning/: Động cơ suy luận chuỗi tư duy Chain-of-Thought / Tree-of-Thought.
- outer/: Động cơ điều tuyến mô hình thông minh theo SLA.
- ledger/: Sổ cái chứng nhận bằng chứng suy luận AI chống lượng tử.
- utomation/: Bộ mô phỏng suy luận AI không tốn phí & Tự phục hồi package.
