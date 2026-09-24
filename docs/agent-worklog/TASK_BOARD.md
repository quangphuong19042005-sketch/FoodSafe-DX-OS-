# FOODSAFE-DX-OS TASK BOARD & WORKLOG

> **Dự án:** FoodSafe-DX-OS — Hệ điều hành Doanh nghiệp số An toàn Thực phẩm  
> **Phương pháp quản lý:** Agentic Engineering (Orchestrator - Worker - Reviewer - QA)  
> **Cập nhật lần cuối:** 2026-09-24  

---

## 📌 BẢNG THEO DÕI TIẾN ĐỘ TỔNG THỂ (15 TASKS)

| Task ID | Tên Task & Mô tả | Dependency | Phụ trách | Trạng thái |
| :--- | :--- | :--- | :--- | :---: |
| **TASK-001** | **Khởi tạo Git Repo, License Apache-2.0, .gitignore, Cấu trúc thư mục & Task Board** | None | Orchestrator / Docs | **DONE** |
| **TASK-002** | **Thiết lập Docker Compose đa dịch vụ (`db`, `backend`, `frontend`) & cấu hình mạng** | TASK-001 | DevOps / Architect | **DONE** |
| **TASK-003** | Xây dựng SQLAlchemy Models & Pydantic Schemas cho 6 thực thể miền an toàn | TASK-002 | Backend Agent | **READY** |
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
* **Trạng thái:** DONE
* **Thao tác thực hiện:**
  - Khởi tạo git repository trên nhánh `main`.
  - Cấu hình remote `git@github.com:quangphuong19042005-sketch/FoodSafe-DX-OS-.git`.
  - Tạo tệp `LICENSE` chuẩn Apache 2.0 (OSI-approved).
  - Tạo tệp `.gitignore` chuẩn cho Python, Frontend, Docker.
  - Phân tách cấu trúc thư mục ranh giới: `backend/`, `frontend/`, `docs/plans/`, `docs/agent-worklog/`, `scripts/`.
* **Kết quả:** Pass. Commit `14c673c`.

### TASK-002: Thiết lập Docker Compose đa dịch vụ (db, backend, frontend) & Cấu hình mạng
* **Owner:** DevOps / Architect
* **Trạng thái:** DONE
* **Thao tác thực hiện:**
  - Viết `backend/Dockerfile` (Python 3.11-slim, curl healthcheck).
  - Viết `backend/requirements.txt` cố định phiên bản các thư viện lõi.
  - Viết `backend/app/main.py` khởi tạo FastAPI với `/health` và CORS.
  - Viết `frontend/Dockerfile` (Nginx 1.25-alpine).
  - Viết `frontend/nginx.conf` với reverse proxy `/api/` tới backend container.
  - Viết `frontend/src/index.html` giao diện Web SPA ban đầu.
  - Viết `docker-compose.yml` định nghĩa 3 services: `db`, `backend`, `frontend`, bridge network và persistent volume.
  - Viết `.env.example` cấu hình tham số.
* **Kết quả kiểm thử:**
  - `docker compose build`: Cả 2 image build thành công (exit code 0).
  - `docker compose up -d`: Cả 3 container khởi động và chuyển sang trạng thái `healthy`.
  - `curl http://localhost:8000/`: Trả về HTTP 200 JSON hệ thống.
  - `curl http://localhost:3000/api/health`: Reverse proxy hoạt động chuẩn xác (`healthy`, `database: connected`).
  - `curl http://localhost:3000/`: Trả về Web SPA HTML 10.891 bytes.

