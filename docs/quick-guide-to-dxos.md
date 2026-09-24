# HƯỚNG DẪN NHANH VỀ HỆ ĐIỀU HÀNH DOANH NGHIỆP SỐ (DX-OS) & CHỦ ĐỀ OLP PMNM 2026

> **Tài liệu tư liệu AI / Cẩm nang kiến trúc kỹ thuật DX-OS**  
> **Nguồn trích xuất từ:** `/home/vanii/Downloads/Quick-guide-to-DXOS.pdf`  
> **Tài liệu tham khảo toàn văn:** [Giáo trình DX-OS in Action](https://opendigitransform.gitbook.io/dx-os)  
> **Đơn vị chủ trì:** Hội Tin học Việt Nam & CLB Phần mềm Tự do Nguồn mở Việt Nam (VFOSSA)  

---

## 1. BÀI TOÁN CHUYỂN ĐỔI SỐ VÀ SỰ RA ĐỜI CỦA KIẾN TRÚC DX-OS

### 1.0. Bối cảnh và Thách thức Thực tiễn
- **Bối cảnh:** Trong "Kỷ nguyên vươn mình", Chuyển đổi số (CĐS) là tấm vé sinh tồn bắt buộc cho hơn 900.000 doanh nghiệp vừa và nhỏ (SME) cũng như các cơ quan nhà nước.
- **Cái bẫy "Ảo tưởng công nghệ":** Doanh nghiệp chi nhiều tiền mua phần mềm đắt đỏ nhưng nhân sự vẫn giữ thói quen cũ (nhắn tin trao đổi rải rác, nhập liệu thủ công, báo cáo thủ công qua bảng tính).
- **Hệ quả:** Dữ liệu bị giam cầm trong các "ốc đảo thông tin" (data silos), dẫn đến lỗi *"Rác đầu vào - Rác đầu ra"* (Garbage In - Garbage Out).
- **Bản chất của CĐS:** Là quá trình **chuyển giao quyền kiểm soát** từ thao tác thủ công của con người sang **các thuật toán tự động**.

---

## 1.1. CẤU TRÚC 4 KHÔNG GIAN CỦA HỆ ĐIỀU HÀNH DX-OS (MÔ HÌNH H-P-D-I)

Hệ thống vận hành doanh nghiệp số được phân rã thành 4 không gian chức năng chuyên biệt:

```
        ┌─────────────────────────────────────────────────────────────┐
        │  [I] Không gian Trí tuệ Nhân tạo (Intelligence Space)        │
        │  (Agentic AI, RAG, Tự động ra quyết định, Doanh nghiệp AI)  │
        └──────────────────────────────▲──────────────────────────────┘
                                       │ Kế thừa dữ liệu sạch & sự kiện
        ┌──────────────────────────────┴──────────────────────────────┐
        │  [D] Không gian Dữ liệu (Data Space)                         │
        │  (Single Source of Truth, Kho dữ liệu phẳng, Real-time BI)   │
        └──────────────────────────────▲──────────────────────────────┘
                                       │ Chuẩn hóa luồng dữ liệu
        ┌──────────────────────────────┴──────────────────────────────┐
        │  [P] Không gian Quy trình (Process Space)                    │
        │  (Event-driven, Tự động hóa luồng việc, Ràng buộc Poka-yoke) │
        └──────────────────────────────▲──────────────────────────────┘
                                       │ Chuyển giao quyền điều khiển
        ┌──────────────────────────────┴──────────────────────────────┐
        │  [H] Không gian Nhân sự (Human Space)                        │
        │  (Môi trường làm việc số khép kín, SSO, P.A.R.A, Cổng Wiki)  │
        └─────────────────────────────────────────────────────────────┘
```

### [H] - Không gian Nhân sự (Human Space)
*Kiến tạo Môi trường Làm việc Số Tích hợp*
- **Vị trí:** Phân tầng vận hành cơ sở.
- **Mục tiêu:** Thay vì để quy trình phụ thuộc vào trí nhớ, thói quen và thao tác thủ công rời rạc, kiến tạo một môi trường làm việc số khép kín.
- **Thành phần cốt lõi:**
  - Quản trị định danh tập trung (**SSO - Single Sign-On**).
  - Chuẩn hóa cấu trúc lưu trữ tệp tin vật lý theo phương pháp **P.A.R.A** (Projects, Areas, Resources, Archives).
  - Cổng thông tin nội bộ (**Wiki/CMS**) và kênh truyền thông tức thời nhằm kiểm soát tính chính xác của thông tin ngay từ khâu đầu vào.

### [P] - Không gian Quy trình (Process Space)
*Tự động hóa Luồng công việc (Workflow Automation)*
- **Vị trí:** Tầng tiếp nhận quyền điều khiển từ con người sang thuật toán.
- **Mục tiêu:** Tự động hóa quy trình dựa trên kiến trúc hướng sự kiện (**Event-driven architecture**), xử lý các bước luân chuyển thông tin liên phòng ban mà không cần thao tác thủ công.
- **Cơ chế kiểm soát chất lượng:**
  - Tích hợp các ràng buộc kỹ thuật khắt khe (**Poka-yoke / Mistake-proofing**) để ngăn chặn và giới hạn các thao tác không hợp lệ ngay tại điểm chạm đầu vào (input entrypoint).

### [D] - Không gian Dữ liệu (Data Space)
*Ra quyết định Dựa trên Sự thật (Data-Driven Decision Making)*
- **Vị trí:** Tầng lưu trữ, xử lý và trực quan hóa dữ liệu.
- **Mục tiêu:** Thu thập các tập dữ liệu phẳng có cấu trúc phát sinh tự động từ Không gian [P], làm sạch và đồng bộ hóa thành **Nguồn sự thật duy nhất** (*Single Source of Truth*), triệt tiêu hoàn toàn hiện tượng ốc đảo thông tin.
- **Công cụ đầu ra:** Các bảng điều khiển trực quan theo thời gian thực (**Real-time BI Dashboard**) giúp cấp quản trị theo dõi chỉ số đo lường hiệu năng và đưa ra quyết định định lượng.

### [I] - Không gian Trí tuệ Nhân tạo (Intelligence Space)
*Tiến đến Doanh nghiệp Tự hành (Autonomous / AI-Native Enterprise)*
- **Vị trí:** Tầng kiến trúc cấp cao nhất.
- **Mục tiêu:** Định vị doanh nghiệp ở mô hình AI-Native. AI không chỉ là chatbot thụ động mà vận hành dưới dạng **các tác tử tự hành (Agentic AI)**.
- **Cơ chế hoạt động:**
  - Tự động phân tích dữ liệu từ Không gian [D].
  - Tự động nhận diện sự kiện kích hoạt từ Không gian [P].
  - Tự động thực thi các hành động nghiệp vụ (Action Execution) theo cấu hình mà không cần con người nhấp chuột hay gửi lệnh thủ công.

---

## 1.2. SỰ TIẾN HÓA TUYẾN TÍNH VÀ NGUYÊN LÝ "HUMAN-IN-THE-LOOP"

1. **Tính tuyến tính bắt buộc (Linear Evolution):**
   - **Không thể nhảy cóc lên [I]** nếu chưa chuẩn hóa dữ liệu tại **[D]** và thiết lập ràng buộc kỹ thuật tại **[P]**.
   - Nếu áp dụng AI/LLM vào một quy trình hỗn loạn, chưa chuẩn hóa sẽ dẫn đến lỗi *Garbage In - Garbage Out* và hiện tượng ảo giác dữ liệu (AI Hallucination).

2. **Quy luật nghịch biến về quyền điều khiển:**
   - Khi năng lực xử lý của máy móc tại các trục **[P]**, **[D]**, **[I]** tăng lên:
   - Tỷ lệ thao tác thủ công của nhân sự (hằng số **[H]**) giảm từ **100%** xuống còn **10% - 20%**.

3. **Nguyên lý "Con người trong vòng lặp" (Human-in-the-loop):**
   - Con người không bị thay thế mà chuyển dịch vai trò lên tầng cao hơn:
     - Thiết kế luồng thuật toán và quy tắc nghiệp vụ.
     - Kiểm soát chất lượng và rào chắn an toàn/đạo đức.
     - Phê duyệt và xử lý các trường hợp ngoại lệ (Exceptions & Escalations).

---

## 2. CHỦ ĐỀ CUỘC THI OLP PMNM 2026: XÂY DỰNG DX-LAB

Mục tiêu cuộc thi: Sinh viên tự thiết kế và triển khai một **Trạm thực hành số (DX-Lab)** dựa trên kiến trúc **Lõi mở (Open-Core)**, mô phỏng đầy đủ 4 không gian H-P-D-I nhằm giải quyết các bài toán vận hành thực tế của doanh nghiệp.

### 2.1. Kế thừa Hệ sinh thái Công nghệ OLP các năm trước
Các đội thi cần chủ động tích hợp các nền tảng công nghệ nguồn mở từ các mùa OLP trước để cấu thành hệ thống:

| Kỳ thi OLP | Chủ đề công nghệ | Vai trò ứng dụng trong DX-OS 2026 |
|---|---|---|
| **OLP 2024** | **Nền tảng Low-code / No-code (LCDP)** | Xây dựng biểu mẫu nhập liệu (Forms), cơ sở dữ liệu quan hệ, tạo rào chắn Poka-yoke tại **Không gian [P]**. |
| **OLP 2025** | **Dữ liệu mở liên kết (Linked Open Data - LOD)** | Chuẩn hóa cấu trúc siêu dữ liệu (Metadata), xây dựng Single Source of Truth tại **Không gian [D]**. |
| **OLP 2023** | **Mô hình Ngôn ngữ Lớn (LLM) & RAG** | Triển khai mô hình ngôn ngữ lớn và kỹ thuật Retrieval-Augmented Generation (RAG) tạo Agent thông minh tại **Không gian [I]**. |

---

### 2.2. Quy hoạch Công cụ theo Bản đồ Công nghệ DX-OS (Technology Stack Mapping)

| Không gian | Nhóm chức năng cốt lõi | Gợi ý loại hình / Công nghệ nguồn mở tiêu biểu |
|:---:|---|---|
| **[H]<br>Human** | • Quản trị định danh tập trung (SSO)<br>• Quản trị lưu trữ đám mây nội bộ<br>• Quản trị tri thức (Wiki/CMS)<br>• Hệ thống truyền thông tức thời | Keycloak, Authentik, Nextcloud, OwnCloud, BookStack, Wiki.js, Mattermost, Matrix, Rocket.Chat |
| **[P]<br>Process** | • Giao diện Low-code / No-code (LCDP)<br>• Nền tảng tích hợp dịch vụ (iPaaS)<br>• Tự động hóa luồng việc (Workflow) | NocoDB, Appsmith, ToolJet, Directus, n8n, Activepieces, Node-RED, Apache Airflow |
| **[D]<br>Data** | • Cơ sở dữ liệu quan hệ / phi quan hệ<br>• Kinh doanh thông minh (BI)<br>• Trực quan hóa dữ liệu thời gian thực | PostgreSQL, MariaDB, ClickHouse, Apache Superset, Metabase, Grafana |
| **[I]<br>Intelligence** | • Khung phát triển LLM / Agentic AI<br>• Cơ sở dữ liệu Vector (Vector DB)<br>• Hệ thống RAG & Tác tử tự hành | LangChain, LlamaIndex, Flowise, Langflow, Dify, Qdrant, Chroma, PGvector, Ollama |

---

### 2.3. Phạm vi Khai thác DX-Lab (3 Nhóm Tác nhân Hưởng lợi)

1. **Ban lãnh đạo, Quản lý SME và Cơ quan Nhà nước:**
   - Sử dụng khung đo lường chẩn đoán thực trạng tổ chức.
   - Triệt tiêu lãng phí, rào cản vận hành.
   - Tối ưu hóa tỷ suất hoàn vốn đầu tư công nghệ (ROI).
2. **Chuyên gia Công nghệ và Tư vấn viên:**
   - Môi trường đóng gói và chia sẻ tri thức chuyên môn.
   - Kết nối đối tác kỹ thuật, xây dựng năng lực tham gia mạng lưới tư vấn CĐS quốc gia.
3. **Sinh viên và Giảng viên khối Kỹ thuật & Kinh tế số:**
   - Tiếp cận môi trường thực nghiệm giả lập (Hộp cát / Sandbox DX-Lab).
   - Thao tác trực tiếp trên dữ liệu và quy trình nghiệp vụ thực tế của doanh nghiệp.

---

## 3. CHIẾN LƯỢC DỰ THI OLP PMNM 2026

Thang điểm đánh giá: **100 điểm** (50 điểm PoF + 50 điểm Trình diễn Chung kết).

```
                            ┌───────────────────────────────────┐
                            │    TỔNG ĐIỂM DỰ THI: 100 ĐIỂM     │
                            └─────────────────┬─────────────────┘
                                              │
             ┌────────────────────────────────┴────────────────────────────────┐
             ▼                                                                 ▼
┌───────────────────────────────┐                             ┌───────────────────────────────┐
│     TIÊU CHÍ PoF (50 ĐIỂM)    │                             │ TIÊU CHÍ CHUNG KẾT (50 ĐIỂM)  │
│  (Chấm mã nguồn trước ngày thi│                             │   (Hackathon & Showcase tại   │
│        từ 07 - 09/12/2026)    │                             │       ngày 10/12/2026)        │
├───────────────────────────────┤                             ├───────────────────────────────┤
│ • Git Repo công khai (5đ)     │                             │ • Tính nguyên gốc giải pháp(10)│
│ • License OSI từng file (10đ) │                             │ • Mức độ hoàn thiện live (10đ)│
│ • Bản Release hợp lệ (5đ)     │                             │ • Độ thân thiện UX/UI (10đ)   │
│ • Build from Source sạch (10đ)│                             │ • Tính phát triển bền vững(10)│
│ • Quản lý Dependency (10đ)    │                             │ • Khả năng hút cộng đồng (10đ)│
│ • Tài liệu, Bug, Change (10đ) │                             └───────────────────────────────┘
└───────────────────────────────┘
```

### 3.1. Điểm cốt tử vòng PoF (50 điểm)
- **Bản quyền:** Bắt buộc dùng giấy phép mã nguồn mở OSI-approved. Khai báo header ở từng file mã nguồn và kèm file toàn văn `LICENSE`.
- **Hệ thống mã nguồn:** Repo công khai trên GitHub/GitLab, có Web viewer, có lịch sử commit thực chất từ ngày đầu làm bài.
- **Đóng gói & Cài đặt:**
  - Hỗ trợ biên dịch và cài đặt từ mã nguồn sạch.
  - Khuyến nghị sử dụng **Docker & Docker Compose** để đóng gói toàn bộ hệ sinh thái DX-Lab (giúp hội đồng chấm thi chạy `docker compose up` là hoạt động ngay).
  - Không hardcode đường dẫn tuyệt đối. Cấu hình qua `.env`.
- **Chất lượng dự án FOSS:** README chi tiết, CHANGELOG cập nhật, sử dụng GitHub Issues/Bug Tracker đầy đủ.

### 3.2. Điểm bứt phá vòng Chung kết (50 điểm)
- **Tính nguyên gốc & Tư duy Kiến trúc:** Cách ghép nối các module Open-Source thành một giải pháp vận hành mượt mà, sáng tạo, giải quyết đúng nỗi đau doanh nghiệp.
- **Hoàn thiện & UX:** Giao diện trực quan, dễ thao tác cho cả nhân viên nghiệp vụ lẫn cấp quản lý.
- **Showcase & Sức hút cộng đồng:** Kịch bản demo mạch lạc (theo luồng sự kiện end-to-end từ [H] -> [P] -> [D] -> [I]), tài liệu kỹ thuật chuẩn chỉ.

---

## 4. TÀI LIỆU TOÀN VĂN TRA CỨU
- Giáo trình toàn văn: **"Xây dựng Hệ điều hành Doanh nghiệp số: Từ Tư duy đến Hành động (DX-OS in Action)"**  
- Địa chỉ truy cập: [https://opendigitransform.gitbook.io/dx-os](https://opendigitransform.gitbook.io/dx-os)
