# Business Capability Specification: Content Management

1. Capability Name: Digital Content Asset Creation
2. Business Objective: Tu dong sang tao, bien tap va quan ly tai san so (Articles, Videos, Ebooks).
3. Business Value: Tich luy tai san so doc quyen, giam 95% chi phi sang tao noi dung.
4. Stakeholders: Chief Content Officer, Solopreneur, Media Team.
5. Actors: Content Manager, Writing Agent, Video Script Agent, Reviewer.
6. Business Workflow: Research Topic -> Draft Markdown -> AI Quality Audit -> Store Repository.
7. Business Rules: Noi dung phai nguyen ban, qua AI Audit score > 85/100, dinh dang Markdown chuan.
8. Information Model: DigitalContentAsset, ContentCategory, MediaAttachment.
9. KPIs: 100 Content Assets/thang, 0% Plagiarism, 100% Repurposable.
10. UI Requirements: Content Studio UI, Asset Library Viewer, Markdown Editor.
11. API Requirements: POST /v1/content/assets/create, GET /v1/content/assets/search.
12. Data Requirements: PostgreSQL pgvector for semantic content RAG.
13. AI Requirements: Claude 3.5 Sonnet for writing, SDXL for thumbnail generation.
14. Security Requirements: Author authentication, OPA content policy guard.
15. Acceptance Criteria: Tu dong tao, danh chi muc vector va luu kho tai san so.
16. Out of Scope: Direct ad campaign management (handled by Marketing).
