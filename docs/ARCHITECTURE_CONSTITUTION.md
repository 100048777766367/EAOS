# Hiến Pháp Kiến Trúc EAOS (Architecture Constitution)

Mọi thay đổi cấu trúc mã nguồn và quyết định kỹ thuật phải tuân thủ nghiêm ngặt các điều luật dưới đây:

## 1. Cấu trúc Phân Lớp (Hexagonal Architecture)
* Các Module thuộc tầng **Domain** không được phép import bất kỳ phần tử nào từ **Application** hoặc **Infrastructure**.
* Tầng **Application** (Use Cases, Core Engines) chỉ được tương tác với **Domain**, không biết đến sự hiện diện của **Infrastructure**.

## 2. Tiêu chuẩn Hồ sơ Quyết Định (ADR Template)
Mọi tài liệu quyết định kỹ thuật (.md) nằm trong `docs/adrs/` bắt buộc phải có đầy đủ 4 đề mục:
1. `# Status`
2. `# Context`
3. `# Decision`
4. `# Consequences`
