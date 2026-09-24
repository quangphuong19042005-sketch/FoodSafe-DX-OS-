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
| **TASK-003** | **Xây dựng SQLAlchemy Models & Pydantic Schemas cho 6 thực thể miền an toàn** | TASK-002 | Backend Agent | **DONE** |
| **TASK-004** | **Viết script nạp dữ liệu thực tế (Realistic Seed Data) từ vụ án tháng 9/2026** | TASK-003 | Backend / Data Agent | **DONE** |
| **TASK-005** | **Hiện thực hóa Poka-yoke Engine & API Kiểm thực Bước 1 (Giao nhận & Nhiệt độ lạnh)** | TASK-004 | Backend Agent | **DONE** |
| **TASK-006** | **Hiện thực hóa API Kiểm thực Bước 2 (Chế biến & Nhiệt độ tâm nấu chín)** | TASK-005 | Backend Agent | **DONE** |
| **TASK-007** | **Hiện thực hóa API Kiểm thực Bước 3 (Khóa mẫu 24h & Duyệt Human-in-the-loop)** | TASK-006 | Backend Agent | **DONE** |
| **TASK-008** | Xây dựng Thuật toán Truy vết Đồ thị (Graph Traceability BFS) dưới 3 giây | TASK-007 | AI / Agentic Agent | **IN_PROGRESS** |
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
* **Kết quả:** Pass. Commit `5fa359c`.

### TASK-003: Xây dựng SQLAlchemy Models & Pydantic Schemas cho 6 thực thể miền an toàn
* **Owner:** Backend Agent
* **Trạng thái:** DONE
* **Thao tác thực hiện:**
  - Viết `backend/app/database.py`: Tạo engine, sessionmaker, base class và `wait_for_db` retry logic.
  - Viết `backend/app/models.py`: 7 SQLAlchemy ORM models (`facilities`, `suppliers`, `ingredient_batches`, `inspections_step1`, `inspections_step2`, `sample_lockers`, `incident_reports`) với đầy đủ ràng buộc khóa ngoại, index, kiểu dữ liệu JSON.
  - Viết `backend/app/schemas.py`: Các Pydantic v2 schemas phục vụ validation request/response và định nghĩa chi tiết lỗi Poka-yoke (`PokaYokeViolation`).
  - Cập nhật `backend/app/main.py`: Kích hoạt cơ chế lifespan tự động tạo bảng khi container boot.
* **Kết quả kiểm thử:**
  - `docker compose up -d --build backend`: Khởi động lại thành công trong 1.2s.
  - `curl http://localhost:8000/db/tables`: Trả về 7 bảng đã tạo thành công trong PostgreSQL:
    `["suppliers", "ingredient_batches", "facilities", "inspections_step2", "sample_lockers", "incident_reports", "inspections_step1"]`.
  - `docker exec foodsafe_db psql -c "\dt"`: Kiểm chứng trực tiếp 7 bảng quan hệ tồn tại trong schema `public`.
* **Kết quả:** Pass. Commit `7f4743e`.

### TASK-004: Viết script nạp dữ liệu thực tế (Realistic Seed Data) từ vụ án tháng 9/2026
* **Owner:** Backend / Data Agent
* **Trạng thái:** DONE
* **Thao tác thực hiện:**
  - Viết `backend/app/seed.py`: Định nghĩa hàm `seed_initial_data(db)` nạp đầy đủ:
    + 4 cơ sở bếp ăn: Trường TH Lê Trọng Tấn, Bếp ăn KCN Phong Điền - Scavi Huế, Trường THCS An Khê (Gia Lai), Trường TH Chu Văn An.
    + 5 nhà cung ứng: CP Food Hà Nội (hạng A), HTX Rau Vân Nội (VietGAP), Thủy hải sản Thuận An, Cơ sở bánh mì/patê Bin Bin (Gia Lai - Blacklisted vì vi khuẩn Salmonella), Gia cầm Việt Hưng.
    + 5 lô nguyên liệu: Thịt gà CP, Thịt gà nguyên con Đan Phượng, Tôm thẻ rã đông, Patê gan nhiễm khuẩn Salmonella, Rau cải sạch.
    + 3 phiếu kiểm thực Bước 1: 1 phiếu đạt chuẩn, 2 phiếu bị Poka-yoke chặn đứng do vi phạm nhiệt độ (11.2°C và 6.5°C).
    + 1 phiếu kiểm thực Bước 2: Nấu chín gà hấp ở 84.5°C (vượt chuẩn an toàn 75°C).
    + 2 tủ lưu mẫu Bước 3: Đang khóa đếm ngược 24h và tủ phục vụ điều tra dịch tễ.
    + 1 báo cáo sự cố dịch tễ: 180 ca ngộ độc tại Scavi Huế sẵn sàng cho AI truy vết.
  - Viết script CLI `scripts/seed_db.py` hỗ trợ nạp dữ liệu từ dòng lệnh (`--force`).
  - Cập nhật `backend/app/main.py`: Tự động nạp dữ liệu khi hệ thống boot lần đầu và cung cấp endpoint `POST /db/seed` + `GET /db/stats`.
* **Kết quả kiểm thử:**
  - `curl http://localhost:8000/db/stats`: Trả về số lượng bản ghi:
    `{"facilities":4, "suppliers":5, "ingredient_batches":5, "inspections_step1":3, "inspections_step2":1, "sample_lockers":2, "incident_reports":1}`.
  - `docker exec foodsafe_db psql -c "SELECT ..."`: Xác minh chính xác các bản ghi với đầy đủ thông tin thực tế.
* **Kết quả:** Pass. Commit `30bec9c`.

### TASK-005: Hiện thực hóa Poka-yoke Engine & API Kiểm thực Bước 1 (Giao nhận & Nhiệt độ lạnh)
* **Owner:** Backend Agent
* **Trạng thái:** DONE
* **Thao tác thực hiện:**
  - Viết `backend/app/core/poka_yoke.py`: Xây dựng `PokaYokeEngine` với 5 rào chắn bảo vệ nghiêm ngặt:
    1. Rào chắn nhà cung ứng cấm (Blacklisted Supplier)
    2. Rào chắn hạn sử dụng (Expiry Date Guard)
    3. Rào chắn nhiệt độ chuỗi lạnh bảo quản thực phẩm (Cold-chain Temperature Guard: <= 4°C với đồ tươi, <= -12°C với đồ đông lạnh)
    4. Rào chắn tem nhãn & bao bì nguyên vẹn (Packaging Integrity Guard)
    5. Rào chắn đánh giá cảm quan (Sensory Evaluation Guard)
  - Viết `backend/app/routers/facilities.py`: API lấy danh sách và chi tiết bếp ăn trường học / KCN.
  - Viết `backend/app/routers/suppliers.py`: API lấy danh sách và chi tiết nhà cung cấp.
  - Viết `backend/app/routers/batches.py`: API lấy danh sách và chi tiết lô nguyên liệu.
  - Viết `backend/app/routers/inspections_step1.py`: API xử lý Kiểm thực Bước 1, tự động bắt lỗi vi phạm và trả về HTTP 422 Unprocessable Entity kèm đối tượng `PokaYokeViolation`.
* **Kết quả kiểm thử:**
  - Test vi phạm Poka-yoke: Gửi request nhập thịt gà với nhiệt độ 13.5°C (> 4.0°C) -> **Backend trả về HTTP 422 Unprocessable Entity**, thông báo `POKA_YOKE_BLOCKED`, tự động cập nhật lô hàng thành `REJECTED` và lưu vết vi phạm vào database.
  - Test đạt chuẩn: Gửi request nhập thịt gà nhiệt độ 2.0°C (<= 4.0°C) -> **Backend trả về HTTP 201 Created**, thông báo `APPROVED`.
  - Database check: Cả 2 bản ghi (ID 4 và ID 5) được ghi nhận chính xác trong PostgreSQL.
* **Kết quả:** Pass. Commit `ed8c30c`.

### TASK-006: Hiện thực hóa API Kiểm thực Bước 2 (Chế biến & Nhiệt độ tâm nấu chín)
* **Owner:** Backend Agent
* **Trạng thái:** DONE
* **Thao tác thực hiện:**
  - Nâng cấp `backend/app/core/poka_yoke.py` với phương thức `validate_step2`:
    1. Kiểm tra nguyên liệu đầu vào: Chặn tuyệt đối việc đưa lô hàng đã bị từ chối ở Bước 1 vào nồi nấu (`POKA_YOKE_CONTAMINATED_INGREDIENT`).
    2. Rào chắn nhiệt độ tâm nấu chín: Bắt buộc `core_temp >= 75.0°C` theo chuẩn WHO/QCVN để tiêu diệt vi khuẩn đường ruột Salmonella (`POKA_YOKE_UNDERCOOKED_TEMP`).
    3. Rào chắn cảm quan nấu chín (`POKA_YOKE_SENSORY_UNDERCOOKED`).
  - Viết `backend/app/routers/inspections_step2.py`: Endpoint POST & GET kiểm thực Bước 2.
  - Cập nhật `backend/app/main.py` đăng ký router `inspections_step2`.
* **Kết quả kiểm thử:**
  - Test 1 (Chưa chín thấu): Nấu thịt gà ở nhiệt độ tâm 63.5°C (< 75.0°C) -> **Backend trả về HTTP 422**, thông báo `POKA_YOKE_UNDERCOOKED_TEMP` khóa không cho xuất phần ăn.
  - Test 2 (Dùng nguyên liệu bẩn): Thử nấu món ăn bằng lô thịt gà đã bị từ chối ở Bước 1 (Batch 2) -> **Backend trả về HTTP 422**, thông báo `POKA_YOKE_CONTAMINATED_INGREDIENT` chặn đứng hành vi gian lận.
  - Test 3 (Đạt chuẩn): Nấu gà hấp ở nhiệt độ tâm 88.0°C (>= 75.0°C) với nguyên liệu đạt chuẩn -> **Backend trả về HTTP 201 Created** thông báo `APPROVED`.
  - Database check: Các bản ghi được lưu vết minh bạch trong bảng `inspections_step2`.
* **Kết quả:** Pass. Commit `0a7c4b1`.

### TASK-007: Hiện thực hóa API Kiểm thực Bước 3 (Khóa mẫu 24h & Duyệt Human-in-the-loop)
* **Owner:** Backend Agent
* **Trạng thái:** DONE
* **Thao tác thực hiện:**
  - Cập nhật `backend/app/schemas.py`: Bổ sung `SampleLockerUnlockRequest` (cờ override khẩn cấp, passcode xác thực) và trường `hours_remaining` động.
  - Viết `backend/app/routers/sample_lockers.py`:
    + `GET /api/v1/sample-lockers`: Tính toán thời gian đếm ngược (hours_remaining) chính xác theo thời gian thực.
    + `POST /api/v1/sample-lockers`: Niêm phong mẫu, kích hoạt khóa tủ điện tử, gán thời điểm mở hợp pháp sau đúng 24 giờ.
    + `POST /api/v1/sample-lockers/{id}/unlock`: Kiểm soát rào chắn Poka-yoke cấm mở sớm; tích hợp cổng phê duyệt ngoại lệ khẩn cấp của con người (Human-in-the-loop) ghi nhận audit trail.
  - Cập nhật `backend/app/main.py` đăng ký router `sample_lockers`.
* **Kết quả kiểm thử:**
  - Test 1 (Poka-yoke chặn mở sớm trái phép): Thử mở tủ khi chưa đủ 24 giờ -> **Backend trả về HTTP 422 Unprocessable Entity**, thông báo `POKA_YOKE_EARLY_UNLOCK_PROHIBITED` khóa chốt tủ điện tử không cho mở.
  - Test 2 (Phê duyệt Human-in-the-loop khẩn cấp): Mở khóa với cờ `is_emergency_override=true`, lý do "Thanh tra Đột xuất Sở Y tế" và passcode -> **Backend trả về HTTP 200 OK**, giải phóng chốt khóa, chuyển trạng thái sang `ACCIDENT_INSPECTED` và ghi log an toàn.
* **Kết quả:** Pass. Commit `fa93205`.

### TASK-008: Hiện thực hóa Thuật toán Truy vết Đồ thị Đa tầng (Graph Traceability BFS Engine)
* **Owner:** AI / Intelligence Space Agent
* **Trạng thái:** DONE
* **Thao tác thực hiện:**
  - Viết `backend/app/core/graph_tracer.py`: Hiện thực hóa `GraphTraceEngine` với:
    + **Pathogen Knowledge Base**: Ma trận đối soát triệu chứng y tế và độc tố vi sinh (Salmonella spp., Tụ cầu vàng, E. coli O157:H7, Histamine) theo quy chuẩn QCVN 8-2:2011/BYT.
    + **Thuật toán Breadth-First Search (BFS)**:
      * Quét ngược: Sự cố ngộ độc -> Cơ sở báo cáo -> Món ăn -> Lô nguyên liệu nhiễm khuẩn -> Nhà cung ứng gốc (đánh dấu Blacklisted).
      * Quét xuôi: Từ lô nguyên liệu gốc quét xuyên chuỗi cung ứng sang tất cả các bếp ăn/trường học liên kết đang nhập hoặc chế biến cùng lô hàng.
      * Tự động phát hiện tủ lưu mẫu cần niêm phong khẩn cấp tại các cơ sở có nguy cơ lây lan.
      * Phát lệnh thu hồi khẩn cấp (Emergency Directive).
  - Viết `backend/app/routers/incidents.py`:
    + `GET /api/v1/incidents`: Tra cứu danh sách sự cố dịch tễ.
    + `POST /api/v1/incidents`: Khởi tạo hồ sơ sự cố ngộ độc.
    + `POST /api/v1/incidents/{id}/trace`: Kích hoạt thuật toán truy vết đồ thị tức thì.
  - Cập nhật `seed.py`: Giả lập kịch bản đa cơ sở (Trường THCS Quang Trung tại Gia Lai và Scavi Huế cùng nhập lô Patê từ Cơ sở Bin Bin).
* **Kết quả kiểm thử:**
  - Gọi API `POST /api/v1/incidents/4/trace`:
    + Thời gian thực thi: **26.5 ms** (Vượt xa chỉ tiêu < 3000 ms của đề tài).
    + Chẩn đoán mầm bệnh chính xác: **Salmonella spp.** dựa trên 4 triệu chứng (sốt 39.5°C, nôn mửa, tiêu chảy, đau bụng).
    + Định danh nguyên nhân gốc rễ: Lô `BATCH-2026-PATE-0907-TOXIC` từ Nhà cung cấp `Cơ sở Chế biến Thực phẩm & Giò chả Bin Bin`.
    + Cảnh báo đa cơ sở thành công: Phát hiện ngay lập tức Trường THCS Quang Trung (850 học sinh) đang lưu trữ lô hàng này tại tủ `LOCKER-GIA-LAI-01` -> Phát lệnh phong tỏa khẩn cấp trước khi phục vụ suất ăn trưa!
    + Đồ thị BFS trả về 5 nodes, 4 edges chuẩn hóa cho D3.js/Canvas trực quan hóa trên Frontend.
* **Kết quả:** Pass. Sẵn sàng commit.

### TASK-009: Triển khai Local RAG Microbiology Knowledge Engine (Tra cứu QCVN BYT)
* **Owner:** AI / Knowledge Space Agent
* **Trạng thái:** DONE
* **Thao tác thực hiện:**
  - Viết `backend/app/core/rag_engine.py`: Xây dựng `LocalMicrobiologyRAG` chạy 100% Offline trong container Docker:
    + **Curated Knowledge Corpus**: 10 trích đoạn quy chuẩn quốc gia, luật và hướng dẫn dịch tễ y tế (QCVN 8-2:2011/BYT, QĐ 1246/QĐ-BYT, Luật ATTP 55/2010/QH12, NĐ 115/2018/NĐ-CP, FAO/WHO Danger Zone).
    + **Hybrid BM25 + TF-IDF Retrieval**: Thuật toán xếp hạng độ liên quan văn bản theo từ khóa sinh học và thuật ngữ pháp lý.
    + **Local Synthesis Engine**: Tự động tổng hợp câu trả lời y khoa chuẩn xác, viện dẫn chính xác điều khoản pháp lý và khuyến nghị hành động cho DX-OS.
  - Viết `backend/app/routers/rag.py`:
    + `POST /api/v1/rag/query`: Tra cứu hỏi đáp quy chuẩn vi sinh và pháp lý ATTP.
    + `GET /api/v1/rag/standards`: Danh mục các quy chuẩn quốc gia tích hợp.
    + `GET /api/v1/rag/pathogens`: Bảng tra cứu vi sinh vật gây ngộ độc (Salmonella, E. coli O157:H7, Tụ cầu vàng, Histamine, Botulinum).
  - Cập nhật `backend/app/schemas.py` và `backend/app/main.py`.
* **Kết quả kiểm thử:**
  - Test tra cứu nhiệt độ tâm và Salmonella: Phản hồi trong **1.31 ms**, trích dẫn chính xác WHO Codex Danger Zone và QCVN 8-2:2011/BYT, độ tin cậy 0.99.
  - Test tra cứu chế tài không lưu mẫu: Phản hồi trong **0.90 ms**, trích dẫn đúng Nghị định 115/2018/NĐ-CP (phạt 5-10 triệu đồng) và Quyết định 1246/QĐ-BYT.
  - Hoàn toàn độc lập, không gọi bất kỳ API đám mây nào bên ngoài -> Bảo vệ tuyệt đối 50 điểm PoF.
* **Kết quả:** Pass. Sẵn sàng commit.

### TASK-010: Xây dựng Modern Web Frontend Dashboard & Real-time Poka-yoke UI
* **Owner:** Frontend Agent
* **Trạng thái:** IN_PROGRESS
* **Mục tiêu:** Xây dựng giao diện Web Dashboard hoàn chỉnh, trực quan, hỗ trợ nhân viên bếp ăn và cơ quan quản lý:
  - Tab 1: **Kitchen Staff Workplace** (Form nhập liệu Kiểm thực 3 bước tương tác với phản hồi rào chắn Poka-yoke tức thì).
  - Tab 2: **Rapid Response & Graph Tracer** (Nút kích hoạt khẩn cấp, render đồ thị mạng lưới đa tầng Canvas/SVG trực quan hóa đường lây nhiễm và cơ sở nguy cơ cao).
  - Tab 3: **Regulatory & Microbiology RAG Assistant** (Giao diện hỏi đáp quy chuẩn vi sinh và pháp lý ATTP thời gian thực).
  - Tab 4: **BI & Incident Analytics** (Thống kê số lượng bếp ăn, lô hàng, tỷ lệ tuân thủ và cảnh báo dịch tễ).







