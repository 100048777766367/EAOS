# ADR 001: Sử Dụng Hexagonal Architecture

## Status
Status: Accepted

## Context
Chúng ta cần xây dựng một kiến trúc linh hoạt, dễ nâng cấp và thay thế công nghệ trong tương lai mà không ảnh hưởng trực tiếp đến logic nghiệp vụ lõi.

## Decision
Sử dụng kiến trúc Ports & Adapters làm nền tảng chính.

## Consequences
Logic nghiệp vụ sẽ cực kỳ độc lập, tuy nhiên số lượng code mẫu (boilerplate code) sẽ tăng nhẹ ở giai đoạn đầu.
