# EAOS Centralized Locales Package (`eaos-locales`)

Thư mục quản lý tập trung toàn bộ dữ liệu dịch đa ngôn ngữ (i18n) cho cả Backend Python và Frontend TypeScript:
- `translations/`: Chứa các tệp JSON từ điển chuẩn (`vi.json`, `en.json`, `ja.json`).
- `schema.py`: Pydantic v2 Schema kiểm toán tính toàn vẹn của tệp JSON.
- `manager.py`: Python i18n Manager hỗ trợ fallback và truyền tham số (`{name}`).
- `index.ts`: TypeScript i18n Loader dành cho Next.js / React Frontend.
