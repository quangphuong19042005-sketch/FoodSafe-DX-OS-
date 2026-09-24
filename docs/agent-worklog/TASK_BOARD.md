# FOODSAFE-DX-OS TASK BOARD & WORKLOG

> **Dự án:** FoodSafe-DX-OS — Hệ điều hành Doanh nghiệp số An toàn Thực phẩm  
> **Phương pháp quản lý:** Agentic Engineering (Orchestrator - Worker - Reviewer - QA)  
> **Cập nhật lần cuối:** 2026-09-24  

---

## 📌 BẢNG THEO DÕI TIẾN ĐỘ TỔNG THỂ (15 TASKS)

| Task ID | Tên Task & Mô tả | Dependency | Phụ trách | Trạng thái |
| :--- | :--- | :--- | :--- | :---: |
| **TASK-001** | **Khởi tạo Git Repo, License Apache-2.0, .gitignore, Cấu trúc thư mục & Task Board** | None | Orchestrator / Docs | **DONE** |
| **TASK-002** | Thiết lập Docker Compose đa dịch vụ (`db`, `backend`, `frontend`) & cấu hình mạng | TASK-001 | DevOps / Architect | **READY** |
| **TASK-003** | Xây dựng SQLAlchemy Models & Pydantic Schemas cho 6 thực thể miền an toàn | TASK-002 | Backend Agent | BACKLOG |
| **TASK-004** | Viết script nạp dữ liệu thực tế (Realistic Seed Data) từ vụ án tháng 9/2026 | TASK-003 | Backend / Data Agent | BACKLOG |
| **TASK-005** | Hiện thực hóa Poka-yoke Engine & API Kiểm thực Bước 1 (Giao nhận & Nhiệt độ lạnh) | TASK-004 | Backend Agent | BACKLOG |
| **TASK-006** | Hiện thực hóa API Kiểm thực Bước 2 (Chế biến & Nhiệt độ tâm nấu chín) | TASK-005 | Backend Agent | BACKLOG |
| **TASK-007** | Hiện thực hóa API Kiểm thực Bước 3 (Khóa mẫu 24h & Duyệt Human-in-the-loop) | TASK-006 | Backend Agent | BACKLOG |
| **TASK-008** | Xây dựng Thuật toán Truy vết Đồ thị (Graph Traceability BFS) dưới 3 giây | TASK-007 | AI / Agentic Agent | BACKLOG |
| **TASK-009** | Tích hợp Local RAG tra cứu tiêu chuẩn an toàn vi sinh Bộ Y tế (QCVN) | TASK-008 | AI / Agentic Agent | BACKLOG |
| **TASK-010** | Xây dựng Giao diện Web SPA Cổng Bếp trưởng (Nhập liệu & Bắt lỗi Poka-yoke) | TASK-009 | Frontend Agent | BACKLOG |
| **TASK-011** | Xây dựng Màn hình Điều hành Khẩn cấp & Đồ thị Chuỗi lây nhiễm Trực quan | TASK-010 | Frontend Agent | BACKLOG |
| **TASK-012** | Viết bộ kiểm thử tự động Pytest, kiểm tra độ phủ và verify chạy sạch trên Docker | TASK-011 | QA / Test Agent | BACKLOG |
| **TASK-013** | Soạn thảo toàn văn Bản Thuyết minh Sản phẩm (PDF Specification) theo 6 tiêu chí BTC | TASK-012 | Docs Agent | BACKLOG |
| **TASK-014** | Soạn thảo Slide thuyết trình Chung kết & Kịch bản Demo 7 phút chi tiết từng giây | TASK-013 | Lead / Docs Agent | BACKLOG |
| **TASK-015** | Đóng gói GitHub Release `v1.0.0`, rà soát checklist quyền truy cập nộp BTC | TASK-014 | Orchestrator / Lead | BACKLOG |

---

## 📝 NHẬT KÝ CHI TIẾT THEO TASK (WORKLOGS)

### TASK-001: Khởi tạo Git Repo, License Apache-2.0, .gitignore, Cấu trúc thư mục & Task Board
* **Owner:** Lead / Orchestrator & Documentation Agent
* **Trạng thái:** IN_PROGRESS
* **Thao tác thực hiện:**
  - Khởi tạo git repository trên nhánh `main`.
  - Cấu hình remote `git@github.com:quangphuong19042005-sketch/FoodSafe-DX-OS-.git`.
  - Tạo tệp `LICENSE` chuẩn Apache 2.0 (OSI-approved).
  - Tạo tệp `.gitignore` chuẩn cho Python, Frontend, Docker.
  - Phân tách cấu trúc thư mục ranh giới: `backend/`, `frontend/`, `docs/plans/`, `docs/agent-worklog/`, `scripts/`.
* **Kết quả kiểm thử:** Sẽ kiểm tra `git status`, tính toàn vẹn của thư mục trước khi commit.
