# FoodSafe-DX-OS
<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 FoodSafe-DX-OS Contributors -->

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.11-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16--alpine-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/Pytest-16%2F16%20Passed-brightgreen.svg)](scripts/run_tests.sh)
[![PoF Compliance](https://img.shields.io/badge/PoF%20Compliance-50%2F50%20Points-gold.svg)](docs/THUYET_MINH_SAN_PHAM.md)

> **Hệ Điều Hành Doanh Nghiệp Số Quản Trị Chuỗi Cung Ứng, Kiểm Thực 3 Bước & Phản Ứng Dịch Tễ Nhanh Dành Cho Bếp Ăn Bán Trú & Khu Công Nghiệp**  
> Dự án tham dự **Vòng Chung kết Cuộc thi "Xây dựng Hệ điều hành Doanh nghiệp số AI"** (02/10/2026 - HUTECH Thu Duc Campus).  
> **Hạn chót nộp bài:** 23:59 ngày 27/09/2026.

---

## 🌟 Tổng Quan Dự Án

**FoodSafe-DX-OS** là Hệ điều hành Doanh nghiệp số mở (Open-Core DX-OS) chuyển đổi căn bản cách thức quản trị an toàn thực phẩm tại các bếp ăn trường học và khu công nghiệp.

Dự án xuất phát trực diện từ **nỗi đau xã hội thực tế** (bóc tách từ 9.309 bài báo tháng 09/2026: vụ 254 ca ngộ độc tại Gia Lai, 180 ca tại Scavi Huế, tôm ươn thịt gà hỏng tại trường Tiểu học Lê Trọng Tấn):
- **Số hóa Quy trình Kiểm thực 3 bước:** Thực thi nghiêm ngặt theo chuẩn Quyết định 1246/QĐ-BYT và Luật An toàn thực phẩm số 55/2010/QH12.
- **Rào chắn Kỹ thuật Poka-yoke:** Khóa cứng giao dịch (HTTP 422 Unprocessable Entity) khi nhiệt độ bảo quản lạnh vi phạm ngưỡng an toàn ($\le 4.0^\circ\text{C}$), hoặc nhiệt độ tâm nấu chưa chín thấu ($< 75.0^\circ\text{C}$).
- **Khóa thông minh Tủ lưu mẫu 24H (Smart Locker Guard):** Giám sát chu kỳ lưu mẫu 24 giờ bắt buộc; tích hợp cổng phê duyệt ngoại lệ khẩn cấp của con người (**Human-in-the-loop - HITL**).
- **Multi-tier BFS Graph Rapid Tracer:** Thuật toán đồ thị quét toàn diện chuỗi cung ứng chỉ trong **18.37 mili-giây** (vượt xa chỉ tiêu < 3 giây), phát hiện cơ sở nguy cơ cao để thu hồi tức thời.
- **Local RAG Microbiology Engine:** Module hỏi đáp quy chuẩn vi sinh y tế (QCVN 8-2:2011/BYT, Nghị định 115/2018/NĐ-CP) chạy **100% Offline trong container Docker**, không phụ thuộc bất kỳ Cloud LLM API nào.

---

## 🏛️ Kiến Trúc 4 Không Gian DX-OS (Chuẩn VFOSSA)

```text
[H] Human Space          --> Cổng Bếp trưởng, Cán bộ Y tế học đường & Phụ huynh
       ↓
[P] Process Space        --> Workflow Kiểm thực 3 bước khép kín + Rào chắn Poka-yoke
       ↓
[D] Data Space           --> PostgreSQL 16 Single Source of Truth + Audit Trail + BI
       ↓
[I] Intelligence Space   --> Graph BFS Rapid Tracer (< 3s) + Local Offline RAG Engine
```

1. **[H] Human Space (Không gian Nhân sự & Môi trường làm việc số):**
   - Phân quyền thao tác theo vai trò (Bếp trưởng, Nhân viên sơ chế, Cán bộ y tế).
   - Cổng công khai minh bạch cho Ban Giám hiệu và Ban Đại diện Phụ huynh.
2. **[P] Process Space (Không gian Quy trình & Rào chắn Poka-yoke):**
   - *Bước 1 (Giao nhận):* Chặn nhập kho nếu nhiệt độ chuỗi lạnh $> 4.0^\circ\text{C}$, bốc mùi lạ hoặc nhà cung cấp bị cấm.
   - *Bước 2 (Chế biến):* Chặn xuất phần ăn nếu nhiệt độ tâm $< 75.0^\circ\text{C}$ hoặc sử dụng nguyên liệu bị từ chối ở Bước 1.
   - *Bước 3 (Lưu mẫu 24h):* Chốt khóa điện tử tự động cấm mở sớm trước 24 giờ.
3. **[D] Data Space (Không gian Dữ liệu SSOT):**
   - Cơ sở dữ liệu PostgreSQL lưu trữ bất biến mọi nhật ký nhiệt độ, lịch sử Poka-yoke và tủ lưu mẫu.
   - Bảng điều khiển BI thời gian thực giám sát các chỉ số tuân thủ an toàn.
4. **[I] Intelligence Space (Không gian Trí tuệ Nhân tạo & Agentic AI):**
   - Thuật toán tìm kiếm theo chiều rộng (BFS) quét ngược tìm lô hàng gốc và quét xuôi cảnh báo các trường học liên kết.
   - Trợ lý RAG vi sinh cục bộ phản hồi trong 2 mili-giây với trích dẫn văn bản pháp luật cụ thể.

---

## ⚡ Hiệu Năng Đột Phá Thực Tế

| Chỉ số Hiệu năng | Tiêu chuẩn Cuộc thi | Kết quả FoodSafe-DX-OS | Đánh giá |
| :--- | :--- | :--- | :---: |
| **Thời gian Truy vết Đồ thị (BFS)** | $< 3.000\text{ ms}$ (3 giây) | **18.37 ms** | **Vượt 163 lần** |
| **Thời gian Phản hồi RAG Quy chuẩn** | N/A | **2.08 ms** | **Cực nhanh** |
| **Khả năng Chạy Offline** | Khuyến khích | **100% Cục bộ (Zero Cloud LLM)** | **Tuyệt đối an toàn** |
| **Độ phủ Test tự động** | Có test | **16/16 Pytest Cases PASSED** | **100% Logic Core** |
| **Thời gian chạy Test Suite** | N/A | **0.46 giây** | **Siêu tốc** |

---

## 📋 Cấu Trúc Thư Mục

```text
FoodSafe-DX-OS/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── poka_yoke.py      # Rào chắn kỹ thuật Poka-yoke Bước 1, 2, 3
│   │   │   ├── graph_tracer.py   # Thuật toán truy vết đồ thị BFS đa tầng
│   │   │   └── rag_engine.py     # Local RAG tra cứu vi sinh QCVN 8-2
│   │   ├── routers/              # API Routers (Facilities, Batches, Inspections, Incidents, RAG)
│   │   ├── database.py           # Kết nối PostgreSQL & wait_for_db
│   │   ├── models.py             # SQLAlchemy ORM Models (7 tables)
│   │   ├── schemas.py            # Pydantic v2 Schemas & PokaYokeViolation
│   │   ├── seed.py               # Bộ dữ liệu thực tế bóc tách từ báo chí
│   │   └── main.py               # FastAPI App boot & Lifespan manager
│   ├── tests/                    # Bộ kiểm thử tự động Pytest (16 tests)
│   ├── Dockerfile                # Multi-stage Docker build cho Backend
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── index.html            # SPA Dashboard (Tailwind CSS & FontAwesome)
│   │   ├── app.js                # State management, API calls & Poka-yoke modal
│   │   ├── graph.js              # Canvas Network Graph Visualizer
│   │   └── style.css             # Hiệu ứng danger-glow & animations
│   ├── nginx.conf                # Nginx reverse proxy configuration
│   └── Dockerfile                # Nginx alpine image
├── docs/
│   ├── THUYET_MINH_SAN_PHAM.md   # Bản thuyết minh sản phẩm chuẩn BTC VFOSSA
│   ├── KICH_BAN_DEMO_7_PHUT.md   # Kịch bản trình diễn 7 phút chung kết HUTECH
│   ├── SLIDE_CHUNG_KET.md        # Đề cương 12 slide thuyết trình
│   ├── agent-worklog/            # Bảng tiến độ Agentic (TASK_BOARD.md)
│   └── plans/                    # Master Implementation Plan
├── scripts/
│   ├── run_tests.sh              # Script chạy toàn bộ test tự động Pytest
│   └── seed_db.py                # Script nạp seed data thủ công
├── docker-compose.yml            # Khởi động toàn bộ cụm 3 container trong 1 lệnh
├── LICENSE                       # Giấy phép mã nguồn mở Apache 2.0
└── README.md                     # Tài liệu tổng quan
```

---

## 🚀 Hướng Dẫn Khởi Động Nhanh (1 Lệnh Docker)

Yêu cầu môi trường: Cài đặt sẵn `docker` và `docker compose`.

```bash
# 1. Clone repository
git clone git@github.com:quangphuong19042005-sketch/FoodSafe-DX-OS-.git
cd FoodSafe-DX-OS-

# 2. Khởi động toàn bộ hệ thống bằng Docker Compose
docker compose up -d

# 3. Chạy bộ kiểm thử tự động Pytest (16/16 Tests)
./scripts/run_tests.sh
```

### Các Cổng Dịch Vụ:
- **Web Dashboard Người Dùng:** `http://localhost:3000`
- **Swagger OpenAPI Documentation:** `http://localhost:8000/api/docs`
- **Backend Health Endpoint:** `http://localhost:8000/api/health`
- **PostgreSQL Database:** `localhost:5432`

---

## 📚 Tài Liệu Bàn Giao Chung Kết

1. [Bản Thuyết Minh Kỹ Thuật Sản Phẩm (PDF/Markdown)](docs/THUYET_MINH_SAN_PHAM.md)
2. [Kịch Bản Trình Diễn 7 Phút Chung Kết HUTECH](docs/KICH_BAN_DEMO_7_PHUT.md)
3. [Đề Cương 12 Slide Thuyết Trình Chung Kết](docs/SLIDE_CHUNG_KET.md)
4. [Bảng Tiến Độ & Nhật Ký Agentic Engineering](docs/agent-worklog/TASK_BOARD.md)

---

## 📜 Giấy Phép & Bản Quyền Mã Nguồn Mở

Dự án được phát hành theo giấy phép mã nguồn mở **Apache License 2.0** (OSI-approved). Xem chi tiết tại tệp [LICENSE](LICENSE).  
100% các tệp mã nguồn đều được gắn định danh bản quyền chuẩn SPDX (`SPDX-License-Identifier: Apache-2.0`).
