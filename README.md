# FoodSafe-DX-OS
<!-- SPDX-License-Identifier: Apache-2.0 -->

> **Hệ Điều Hành Doanh Nghiệp Số Quản Trị Chuỗi Cung Ứng, Kiểm Thực 3 Bước & Phản Ứng Dịch Tễ Nhanh Cho Bếp Ăn Bán Trú & Doanh Nghiệp**  
> Dự án tham dự **Vòng Chung kết Cuộc thi "Xây dựng Hệ điều hành Doanh nghiệp số AI"** (02/10/2026 - HUTECH Thu Duc Campus).

---

## 🌟 Tổng Quan Dự Án

**FoodSafe-DX-OS** là nền tảng hệ điều hành doanh nghiệp số mở (Open-Core DX-OS) được thiết kế đặc thù cho các cơ sở chế biến suất ăn sẵn, bếp ăn tập thể khu công nghiệp và bếp ăn bán trú trường học.

Dự án giải quyết trực diện vấn đề nhức nhối trong xã hội Việt Nam (bóc tách từ dữ liệu thực tế 9.309 bài báo tháng 09/2026: vụ 254 ca ngộ độc Gia Lai, vụ 180 ca ngộ độc tại Scavi Huế, vụ tôm ươn thịt gà thối tại trường Tiểu học Lê Trọng Tấn):
- **Số hóa quy trình kiểm thực 3 bước** theo chuẩn Thông tư 30/2012/TT-BYT của Bộ Y tế.
- **Rào chắn an toàn Poka-yoke:** Khóa nghiệp vụ cứng từ chối tiếp nhận hoặc chế biến khi nhiệt độ bảo quản lạnh vi phạm ngưỡng an toàn ($\le 4^\circ\text{C}$) hoặc nhiệt độ tâm nấu chưa chín ($< 75^\circ\text{C}$).
- **Khóa thông minh Tủ lưu mẫu 24h (Smart Locker Guard):** Giám sát chu kỳ lưu mẫu 24 giờ bắt buộc và phát hiện can thiệp trái phép.
- **Agentic AI Incident Rapid Tracer:** Thuật toán đồ thị quét ngược chuỗi cung ứng chỉ trong **3 giây** khi có ca nghi ngộ độc, cảnh báo khẩn cấp các trường học/bếp ăn đang dùng chung lô nguyên liệu để thu hồi tức thời.

---

## 🏛️ Kiến Trúc 4 Không Gian DX-OS (VFOSSA)

1. **[H] Human Space (Không gian Nhân sự & Môi trường làm việc số):**
   - Cổng Bếp trưởng (Kitchen Staff App) thao tác nhanh trên máy tính bảng/di động.
   - Cổng Phụ huynh & Ban Giám sát kiểm tra nguồn gốc và thực đơn hàng ngày.
2. **[P] Process Space (Không gian Quy trình & Poka-yoke):**
   - Workflow kiểm thực 3 bước khép kín: Nhập hàng $\rightarrow$ Chế biến $\rightarrow$ Lưu mẫu 24h.
   - Cơ chế rào chắn kỹ thuật (Poka-yoke) và nút phê duyệt khẩn cấp có kiểm soát (Human-in-the-loop).
3. **[D] Data Space (Không gian Dữ liệu SSOT):**
   - Cơ sở dữ liệu PostgreSQL lưu trữ đầy đủ hồ sơ nhà cung cấp, lô nguyên liệu, nhật ký nhiệt độ và dữ liệu liên kết truy xuất nguồn gốc.
   - Bảng điều khiển BI thời gian thực giám sát tỷ lệ tuân thủ và độ an toàn chuỗi cung ứng.
4. **[I] Intelligence Space (Không gian Trí tuệ Nhân tạo):**
   - Module Agentic AI truy vết đồ thị lây nhiễm chéo (Graph Traceability Engine).
   - Module Local RAG tra cứu nhanh quy chuẩn kỹ thuật an toàn vi sinh y tế (Salmonella, E. coli, Histamine).

---

## 📋 Cấu Trúc Thư Mục

```text
FoodSafe-DX-OS/
├── backend/                  # Mã nguồn Backend FastAPI (Python 3.11)
├── frontend/                 # Mã nguồn Frontend Web SPA
├── docs/                     # Tài liệu thiết kế, thể lệ và thuyết minh
│   ├── agent-worklog/        # Bảng theo dõi tiến độ các Agent (TASK_BOARD.md)
│   ├── plans/                # Bản kế hoạch chi tiết (Master Plan)
│   └── ...                   # Báo cáo khảo sát báo chí & phân tích rubric
├── scripts/                  # Script nạp seed data & hỗ trợ kiểm thử
├── docker-compose.yml        # Cấu hình triển khai hệ thống 1 lệnh
├── LICENSE                   # Giấy phép nguồn mở Apache License 2.0
└── README.md                 # Tài liệu giới thiệu chính
```

---

## 🚀 Hướng Dẫn Khởi Động Nhanh (1 Lệnh Docker)

Yêu cầu môi trường: Docker và Docker Compose.

```bash
# Khởi động toàn bộ hệ thống
docker compose up --build
```

- **Frontend Portal:** `http://localhost:3000`
- **Backend API & Swagger Docs:** `http://localhost:8000/docs`
- **PostgreSQL Database:** `localhost:5432`

---

## 📜 Giấy Phép & Bản Quyền

Dự án được phát hành theo giấy phép nguồn mở **Apache License 2.0** (OSI-approved). Xem chi tiết tại tệp [LICENSE](file:///home/vanii/Documents/Workspace/olp/LICENSE).
