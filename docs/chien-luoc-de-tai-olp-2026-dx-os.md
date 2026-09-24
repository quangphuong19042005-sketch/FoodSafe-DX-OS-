# CHIẾN LƯỢC KIẾN TRÚC & ĐỀ XUẤT ĐỀ TÀI XUẤT SẮC OLP PMNM 2026
## CHỦ ĐỀ: XÂY DỰNG HỆ ĐIỀU HÀNH DOANH NGHIỆP SỐ (DX-OS)

> **Tài liệu Chiến lược Độc quyền**  
> **Chuyên gia:** Kiến trúc Hệ thống & Chiến lược DX-OS (DX-OS Strategist)  
> **Mục tiêu:** Định hướng giành Giải Nhất Khối Phần mềm Nguồn mở (PMNM) - Olympic Tin học Sinh viên Việt Nam (OLP) 2026  
> **Cơ quan tổ chức:** Hội Tin học Việt Nam & CLB Phần mềm Tự do Nguồn mở Việt Nam (VFOSSA)

---

## MỤC LỤC
1. **Phân tích Chuyên sâu Bối cảnh & Yêu cầu Kỹ thuật của Ban Tổ chức**
   - 1.1. Bản chất CĐS và Sự phá vỡ bẫy "Ảo tưởng công nghệ"
   - 1.2. Mô hình Kiến trúc Phân tầng H-P-D-I
   - 1.3. Nguyên lý Tiến hóa Tuyến tính & "Human-in-the-loop"
   - 1.4. Trục Kế thừa Tam giác Công nghệ OLP (2023 - 2024 - 2025)
   - 1.5. Cấu trúc Điểm số 100 điểm: Chiến lược "Thủ vững PoF (50đ) - Công phá Showcase (50đ)"
2. **Bản đồ Đánh giá So sánh 3 Hướng Đề tài Tiềm năng**
3. **Đề tài 1 (Trọng tâm / Khuyến nghị số 1): ProcureOS - DX-OS Vận hành Mua sắm & Chuỗi cung ứng Tự hành**
4. **Đề tài 2 (Hướng đi Thay thế 1): OmniCare DX-OS - DX-OS Vận hành Dịch vụ Khách hàng Đa kênh & Bảo hành Hậu mãi**
5. **Đề tài 3 (Hướng đi Thay thế 2): CampusDX-OS - DX-OS Vận hành Đào tạo & Quản trị Đề tài Nghiên cứu Học thuật**
6. **Chiến lược Thực thi Kỹ thuật "Không điểm chết" (Zero-PoF Checklist) & Kịch bản Thuyết trình Đỉnh cao**

---

# PHẦN 1: PHÂN TÍCH BỐI CẢNH & YÊU CẦU KỸ THUẬT CỦA BAN TỔ CHỨC

### 1.1. Bản chất Chuyển đổi số và Sự phá vỡ bẫy "Ảo tưởng công nghệ"
Trong nền kinh tế số Việt Nam với hơn 900.000 doanh nghiệp vừa và nhỏ (SME), đại đa số đang mắc kẹt trong **"Ảo tưởng công nghệ" (Technology Illusion)**:
- **Thực trạng đau đớn:** Doanh nghiệp chi tiền mua sắm các phần mềm ERP, CRM đắt đỏ hoặc cồng kềnh, nhưng nhân viên vẫn dùng Zalo/Telegram để giao việc, dùng Excel cá nhân để tính toán, và chốt báo cáo bằng bản in giấy.
- **Hậu quả:** Xuất hiện các **"Ốc đảo thông tin" (Data Silos)**. Khi dữ liệu đầu vào là sự chắp vá, cảm tính và rời rạc, bất kỳ hệ thống phân tích hay AI nào được áp vào cũng đều gánh chịu hội chứng **"Rác đầu vào - Rác đầu ra" (Garbage In - Garbage Out)**.
- **Tư tưởng cốt lõi của VFOSSA:** Chuyển đổi số thực chất là **cuộc chuyển giao quyền kiểm soát** từ các thao tác thủ công phân mảnh của con người sang **các thuật toán tự động và có cấu trúc**.

### 1.2. Cấu trúc 4 Không gian Vận hành DX-OS (Mô hình H-P-D-I)
DX-OS không phải là một "phần mềm đơn khối" (monolith app) mà là một **Hệ điều hành tích hợp mở (Open-Core DX-Lab Ecosystem)** gồm 4 không gian tương hỗ:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ [I] INTELLIGENCE SPACE (Trí tuệ Nhân tạo Tự hành)                       │
│ • Multi-Agent Autonomous Systems • Local RAG Tri thức Đặc thù           │
│ • Anomaly Detection • Auto Action Execution (Human-in-the-loop Guard)   │
└────────────────────────────────────▲────────────────────────────────────┘
                                     │ Dữ liệu sạch + Sự kiện chuẩn hóa
┌────────────────────────────────────┴────────────────────────────────────┐
│ [D] DATA SPACE (Không gian Dữ liệu & Sự thật Duy nhất)                  │
│ • Single Source of Truth (SSOT) • Flat Tabular Datasets                 │
│ • Linked Open Data (LOD) Graph Ontology • Real-time BI Dashboards       │
└────────────────────────────────────▲────────────────────────────────────┘
                                     │ Dữ liệu phát sinh không sai lệch
┌────────────────────────────────────┴────────────────────────────────────┐
│ [P] PROCESS SPACE (Không gian Quy trình & Rào chắn Kỹ thuật)            │
│ • Event-Driven Workflow Automation • Low-code/No-code Dynamic UI Forms  │
│ • Rào chắn Poka-yoke (Mistake-Proofing Validation at Input)             │
└────────────────────────────────────▲────────────────────────────────────┘
                                     │ Giao diện số hóa thay thao tác rời rạc
┌────────────────────────────────────┴────────────────────────────────────┐
│ [H] HUMAN SPACE (Không gian Nhân sự & Môi trường Làm việc Số)           │
│ • Single Sign-On (SSO / OIDC) • Quản trị Tài liệu Chuẩn P.A.R.A         │
│ • Cổng Tri thức Doanh nghiệp (Wiki/CMS) • Kênh Truyền thông Tức thời    │
└─────────────────────────────────────────────────────────────────────────┘
```

1. **[H] Human Space:** Tạo ra "nơi làm việc số khép kín". Nhân sự chỉ cần 1 tài khoản duy nhất (SSO) để truy cập mọi tài nguyên, tài liệu lưu trữ khoa học theo P.A.R.A (Projects, Areas, Resources, Archives), và giao tiếp có ngữ cảnh, xóa bỏ văn hóa chat nhóm trôi việc.
2. **[P] Process Space:** Chuyển dịch quyền điều khiển sang thuật toán. Mọi quy trình nghiệp vụ được mô hình hóa bằng workflow hướng sự kiện (Event-driven). Đặc biệt, phải áp dụng triết lý **Poka-yoke** (rào chắn chống sai sót của Toyota): Hệ thống từ chối nhận dữ liệu nếu không thỏa mãn các điều kiện tiên quyết (ví dụ: Không cho duyệt đơn nếu thiếu mã số thuế hợp lệ, không cho tạo PO vượt định mức ngân sách).
3. **[D] Data Space:** Thu thập dữ liệu phẳng tự động từ Không gian [P]. Dữ liệu được chuẩn hóa thành **Nguồn sự thật duy nhất (Single Source of Truth)**. Liên kết dữ liệu với các chuẩn quốc tế (Linked Open Data - LOD) để phá vỡ hoàn toàn định dạng cô lập, hiển thị trên Real-time BI Dashboard giúp lãnh đạo "nhìn thấy nhịp thở doanh nghiệp".
4. **[I] Intelligence Space:** Đỉnh cao của hệ thống - Doanh nghiệp AI-Native. AI ở đây là **Tác tử tự hành (Agentic AI)** có khả năng suy luận, truy vấn tri thức cục bộ (Local RAG) từ [D], lắng nghe sự kiện từ [P] và chủ động thực thi lệnh (Tool Calling/Action Execution).

### 1.3. Nguyên lý Tiến hóa Tuyến tính & Cơ chế "Human-in-the-loop"
- **Quy luật bất biến:** Tuyệt đối không thể "nhảy cóc" từ [H] thẳng lên [I]. Doanh nghiệp không thể ứng dụng AI/LLM hiệu quả nếu dữ liệu tại [D] chưa sạch và quy trình tại [P] chưa có rào chắn Poka-yoke.
- **Biến thiên quyền kiểm soát:** 
  - Giai đoạn sơ khai: [H] chiếm 100% thao tác thủ công.
  - Giai đoạn DX-OS chuẩn hóa: [P], [D], [I] gánh 80-90% công việc xử lý; tỷ lệ can thiệp thủ công của [H] giảm xuống 10-20%.
- **Human-in-the-loop:** Con người không bị đào thải mà trở thành người kiểm duyệt cấp cao: AI phân tích và chuẩn bị hành động -> Con người nhấn 1-click xác nhận (Escalation & Approval) -> Workflow tự động kích hoạt.

### 1.4. Trục Kế thừa Tam giác Công nghệ OLP (2023 - 2024 - 2025)
Đề bài yêu cầu thể hiện tính liên tục và kế thừa sâu sắc nền tảng công nghệ của 3 mùa thi OLP PMNM gần nhất:
- **Kế thừa OLP 2024 (Low-code / No-code LCDP):** Đóng vai trò hạt nhân xây dựng giao diện nghiệp vụ và form nhập liệu tại **Không gian [P]**. Cho phép người dùng nghiệp vụ tự cấu hình bảng biểu, tự động tạo API CRUD và áp đặt ràng buộc Poka-yoke tức thì.
- **Kế thừa OLP 2025 (Linked Open Data - LOD):** Đóng vai trò xương sống cho **Không gian [D]**. Sử dụng các bộ từ vựng chuẩn thế giới (Schema.org, Dublin Core, FOAF, GS1 EPCIS) để mô tả thực thể dữ liệu doanh nghiệp dưới dạng đồ thị RDF/JSON-LD, sẵn sàng mở rộng và liên thông liên hệ thống.
- **Kế thừa OLP 2023 (LLM & RAG):** Đóng vai trò bộ não tư duy tại **Không gian [I]**. Kết hợp kỹ thuật Vector Search (Embedding) trên kho tri thức cục bộ và cơ chế Function Calling/Tool Use để biến LLM từ "kẻ chỉ biết trò chuyện" thành "trợ lý tác tử tự hành hành động".

### 1.5. Thấu hiểu Thang điểm: "Thủ vững 50đ PoF - Công phá 50đ Chung kết"
- **50 điểm PoF (Point of Failure) - Chấm tự động 07-09/12:**
  - *Bẫy nguy hiểm nhất:* Thiếu license header ở đầu từng file nguồn (-5đ), xung đột license giữa các package (-5đ), hardcode đường dẫn máy dev (-5đ), build thất bại từ git sạch (-5đ).
  - *Biện pháp hạ gục PoF:* 100% mã nguồn dùng giấy phép OSI-approved (ưu tiên MIT / Apache-2.0 / AGPL-3.0 đồng nhất); Docker Compose 1-click (`docker compose up -d`); script tự động chèn bản quyền SPDX header; Semantic Versioning release có `.tar.gz`; README và CHANGELOG chuẩn chỉ.
- **50 điểm Trình diễn Chung kết (10/12):**
  - Đòi hỏi: Live Demo mượt mà (10đ), Giải pháp nguyên gốc và giải quyết đúng nỗi đau (10đ), UX mượt mà trực quan (10đ), Tài liệu kỹ thuật bền vững (10đ), Phong cách truyền cảm hứng cộng đồng (10đ).

---

# PHẦN 2: BẢN ĐỒ SO SÁNH CHIẾN LƯỢC 3 HƯỚNG ĐỀ TÀI

| Tiêu chí Đánh giá | Đề tài 1 (Trọng tâm): **ProcureOS** (Mua sắm & Chuỗi cung ứng Tự hành) | Đề tài 2 (Thay thế): **OmniCare DX-OS** (Vận hành CSKH Đa kênh & Bảo hành) | Đề tài 3 (Thay thế): **CampusDX-OS** (Vận hành Học thuật & Dự án R&D) |
|---|---|---|---|
| **Lĩnh vực ứng dụng** | Sản xuất, Bán lẻ, Thương mại, Phân phối | Điện tử - Gia dụng, D2C, Chuỗi dịch vụ kỹ thuật | Đại học, Viện nghiên cứu, EdTech, DevShop |
| **Mức độ đau đớn thực tế (Pain-Point)** | ⭐⭐⭐⭐⭐ (Thất thoát dòng tiền trực tiếp, maverick spend, sai hóa đơn 3 bên) | ⭐⭐⭐⭐ (Khách hàng phàn nàn Zalo/FB, mất dấu ticket, trễ hẹn bảo hành) | ⭐⭐⭐⭐ (Thất thoát tri thức khi SV ra trường, phê duyệt giấy tờ hành chính chậm) |
| **Độ hoàn hảo với mô hình H-P-D-I** | 100% (Khớp hoàn hảo mọi không gian, đặc biệt Poka-yoke 3-Way Matching) | 95% (Rất mạnh ở [H] và [P], [D] quy mô CRM vừa) | 90% (Rất mạnh ở [H] P.A.R.A và LOD [D], [P] quy trình hành chính) |
| **Độ sâu kế thừa OLP (23-24-25)** | ⭐⭐⭐⭐⭐ (LOD chuẩn GS1/Schema.org, Low-code PO form, RAG hợp đồng nhà cung cấp) | ⭐⭐⭐⭐ (Schema.org Customer, Low-code CRM, RAG tài liệu sửa chữa linh kiện) | ⭐⭐⭐⭐⭐ (LOD Dublin Core/BIBO, Low-code đề tài, RAG đồ án/bài báo) |
| **Sức hút Trình diễn Showcase (7 phút)** | **Cực cao**: Demo dòng tiền, AI phát hiện lệch giá hóa đơn & tự đàm phán tức thì | **Cao**: Demo chat đa kênh từ Zalo/FB sang ticket điều phối kỹ thuật viên | **Khá**: Demo duyệt đồ án và ghép hội đồng phản biện học thuật |
| **Độ phức tạp triển khai & Đóng gói Docker** | Trung bình - Cao (Đã quy hoạch module tối ưu, Docker ổn định) | Trung bình (Tích hợp Webhook mạng xã hội cần sandbox giả lập) | Trung bình (Các module CMS/Wiki nhẹ nhàng, dễ đóng gói) |
| **Khuyến nghị Chiến lược** | 🏆 **KHUYẾN NGHỊ SỐ 1 ĐỂ GIÀNH GIẢI NHẤT** | **LỰA CHỌN DỰ PHÒNG XUẤT SẮC SỐ 2** | **LỰA CHỌN DỰ PHÒNG HỌC THUẬT SỐ 3** |

---

# PHẦN 3: ĐỀ TÀI 1 (TRỌNG TÂM / KHUYẾN NGHỊ SỐ 1)
## ProcureOS - Hệ điều hành Vận hành Mua sắm & Chuỗi Cung ứng Tự hành cho SME (Autonomous Procurement & Supply Chain DX-OS)

### 3.1. Tên đề tài & Đối tượng Người dùng Mục tiêu
- **Tên thương mại mã nguồn mở:** **ProcureOS (DX-Lab Procurement Engine)**
- **Slogan:** *"Từ Đề xuất Mua sắm đến Đối soát Thanh toán: Chuẩn hóa Quy trình, Dữ liệu Hợp nhất, Tác tử Tự hành"*
- **Đối tượng thụ hưởng:**
  - Doanh nghiệp sản xuất, chế biến, chuỗi bán lẻ, xây dựng công trình (50 - 500 nhân sự).
  - Trưởng phòng Mua hàng (Procurement Manager), Kế toán kho & Kế toán công nợ, Thủ kho, Giám đốc điều hành (CEO/CFO).

### 3.2. Nỗi đau Vận hành Thực tế tại các Doanh nghiệp Việt Nam
1. **Mua sắm phân mảnh, tùy tiện (Maverick Buying):** Nhân viên tự ý gọi nhà cung ứng quen qua Zalo/điện thoại, không có phê duyệt ngân sách trước, dẫn đến việc mua giá cao, vượt hạn mức chi tiêu của phòng ban.
2. **"Địa ngục" Đối soát 3 bên (The 3-Way Matching Nightmare):** Kế toán mất hàng tuần lễ để cầm hóa đơn VAT điện tử (XML/PDF) so sánh từng dòng với Phiếu nhập kho (Goods Receipt Note) và Đơn đặt hàng (PO). Sai lệch số lượng, đơn giá, chiết khấu thường xuyên xảy ra gây thất thoát dòng tiền nghiêm trọng.
3. **Đứt gãy chuỗi cung ứng hoặc Đọng vốn tồn kho (Stockout vs. Deadstock):** Thủ kho ghi sổ tay hoặc file Excel riêng, phòng Mua hàng không biết lượng tồn thực tế để đặt hàng kịp thời, dẫn tới việc lúc thì thiếu nguyên vật liệu sản xuất, lúc thì tồn kho quá hạn hàng trăm triệu đồng.

### 3.3. Thiết kế Ánh xạ Chi tiết vào 4 Không gian H-P-D-I

#### 🏢 [H] Human Space (Không gian Nhân sự & Môi trường Làm việc Số)
- **Định danh tập trung (SSO):** Cài đặt **Keycloak** (hoặc **Authentik**) làm Identity Provider (IdP). Một tài khoản duy nhất phân quyền RBAC (Role-Based Access Control) cho: Nhân viên yêu cầu, Trưởng phòng duyệt, Nhân viên mua sắm, Thủ kho, Kế toán, Ban Giám đốc.
- **Quản trị Tài liệu Chuẩn P.A.R.A trên Nextcloud:**
  - `Projects/`: Thư mục hồ sơ thầu các dự án mua sắm lớn đang triển khai.
  - `Areas/`: Hồ sơ danh bạ nhà cung cấp (Vendor Profiles), Báo cáo kiểm định chất lượng định kỳ.
  - `Resources/`: Bảng báo giá tiêu chuẩn, Catalogue sản phẩm của nhà cung cấp, Hợp đồng khung nguyên tắc.
  - `Archives/`: Hợp đồng đã hoàn thành, chứng từ mua bán các năm trước.
- **Cổng Tri thức & Giao tiếp (Wiki & Team Chat):**
  - **BookStack**: Lưu trữ Quy chế Chi tiêu Nội bộ, Tiêu chuẩn Kỹ thuật vật tư mua sắm, Hướng dẫn kiểm tra chất lượng (QC).
  - **Mattermost**: Hệ thống kênh liên lạc tức thời (Channel `#procure-alerts`, `#warehouse-inbound`). Mọi sự kiện từ hệ thống đều bắn notification có liên kết trực tiếp tới chứng từ liên quan.

#### ⚙️ [P] Process Space (Không gian Quy trình & Rào chắn Kỹ thuật Poka-yoke)
- **Giao diện Low-code Nghiệp vụ (NocoDB & Appsmith):**
  - Giao diện tạo Yêu cầu mua sắm (Purchase Requisition - PR) và Đơn đặt hàng (Purchase Order - PO) thân thiện, tự động gợi ý giá lịch sử gần nhất.
- **Workflow Automation Engine (n8n):**
  - Điều phối luồng phê duyệt đa cấp theo giá trị: PR < 10 triệu (Trưởng phòng duyệt tự động), PR >= 10 triệu (Giám đốc duyệt qua Mattermost Interactive Button).
- **Rào chắn Kỹ thuật Poka-yoke (Bảo đảm Zero-Error tại điểm chạm đầu vào):**
  - *Poka-yoke Ngân sách:* Form từ chối gửi PR nếu tổng tiền vượt định mức ngân sách khả dụng của phòng ban trong tháng đó.
  - *Poka-yoke Nhà cung cấp:* Khóa chức năng chọn nhà cung cấp nếu trạng thái trong hệ thống là "Blacklist" hoặc "Hết hạn chứng nhận năng lực".
  - *Poka-yoke 3-Way Matching:* Hệ thống tự động khóa lệnh duyệt thanh toán nếu: Số lượng xuất hóa đơn > Số lượng thực nhập kho, hoặc Đơn giá trên hóa đơn chênh lệch > 1% so với Đơn đặt hàng PO đã chốt.

#### 📊 [D] Data Space (Không gian Dữ liệu & Nguồn Sự thật Duy nhất)
- **Single Source of Truth (SSOT):**
  - Cơ sở dữ liệu hạt nhân **PostgreSQL** lưu trữ mô hình dữ liệu quan hệ phẳng: `Vendors`, `Products`, `Purchase_Orders`, `Inventory_Transactions`, `Invoices`.
- **Ứng dụng Dữ liệu Mở Liên kết (LOD - Kế thừa OLP 2025):**
  - Định nghĩa dữ liệu sản phẩm và nhà cung cấp theo chuẩn **Schema.org** (`schema:Product`, `schema:Offer`, `schema:Organization`) và **GS1 EPCIS Ontology**.
  - Tích hợp pipeline xuất bản JSON-LD API: Cho phép liên kết mã định danh nhà cung ứng với Cơ sở dữ liệu Thuế Quốc gia (kiểm tra MST doanh nghiệp) và chia sẻ danh mục vật tư liên thông giữa các chi nhánh nhà máy.
- **Real-time BI Dashboard (Apache Superset):**
  - Bảng điều khiển tài chính & chuỗi cung ứng thời gian thực:
    - Chỉ số Giao hàng Đúng hạn & Đủ số lượng (OTIF - On-Time In-Full Rate).
    - Ma trận Phân tích Chi tiêu (Spend Analysis theo danh mục & phòng ban).
    - Biểu đồ Cảnh báo Điểm Đặt hàng lại (Reorder Point Alert) dựa trên tốc độ xuất kho 30 ngày gần nhất.

#### 🧠 [I] Intelligence Space (Không gian Trí tuệ Nhân tạo Tự hành)
- **Hạ tầng AI Cục bộ (Kế thừa OLP 2023):**
  - **Ollama** chạy mô hình mã nguồn mở thế hệ mới (ví dụ: `Qwen2.5-7B-Instruct` hoặc `Llama-3.1-8B-Instruct`) bảo đảm an toàn dữ liệu nội bộ 100%, không rò rỉ giá mua ra ngoài.
  - **Vector DB (Qdrant / PGvector)**: Nhúng toàn bộ kho tài liệu hợp đồng khung, điều khoản thanh toán, và biên bản báo giá từ Không gian [H] & [D].
- **Hệ thống Multi-Agent Tự hành (Agentic AI - Dify / LangGraph):**
  1. *Quote Intelligence Agent (Tác tử Đọc hiểu Báo giá):* Tự động trích xuất bảng giá từ các file chào hàng (PDF/Excel), chuẩn hóa về cùng đơn vị tính và xếp hạng so sánh nhà cung ứng theo ma trận: Giá - Thời gian giao - Điều khoản công nợ.
  2. *Invoice Audit Agent (Tác tử Đối soát Hóa đơn Tự động):* OCR hóa đơn điện tử đầu vào, tự động đối soát 3 chiều (PO - Phiếu kho - Hóa đơn), phát hiện sai lệch chỉ trong 2 giây và cảnh báo tới Kế toán.
  3. *Autonomous Reorder Agent (Tác tử Đề xuất Tái đặt hàng):* Lắng nghe sự kiện tồn kho chạm ngưỡng an toàn từ [P], tự động tính toán số lượng kinh tế (EOQ - Economic Order Quantity), tự tạo bản nháp PR và gửi đề xuất phê duyệt 1-click kèm tóm tắt nguyên nhân đến Giám đốc qua Mattermost.

### 3.4. Tech-Stack Nguồn mở Đề xuất (100% OSI-Approved, Docker-Ready)

```
┌────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                  │
│   Appsmith / NocoDB (Apache 2.0 / AGPL v3) + React Custom Components   │
├────────────────────────────────────────────────────────────────────────┤
│                       ORCHESTRATION & API                              │
│   n8n (Sustainable Core / Fair-code hoặc Activepieces - MIT)           │
│   FastAPI (MIT) làm DX-OS Semantic Gateway & LOD JSON-LD Middleware    │
├────────────────────────────────────────────────────────────────────────┤
│                     DATA & KNOWLEDGE LAYER                             │
│   PostgreSQL 16 (PostgreSQL License) + PGvector Extension (PostgreSQL) │
│   Apache Superset (Apache 2.0)                                         │
│   Nextcloud (AGPL v3) + BookStack (MIT)                                │
├────────────────────────────────────────────────────────────────────────┤
│                    IDENTITY & COMMUNICATION                            │
│   Keycloak (Apache 2.0)                                                │
│   Mattermost Team Edition (AGPL v3 / MIT)                              │
├────────────────────────────────────────────────────────────────────────┤
│                       AI & AGENTIC STACK                               │
│   Dify Community Edition (Apache 2.0) / Langflow (Astra)               │
│   Ollama (MIT) + Qdrant (Apache 2.0)                                   │
└────────────────────────────────────────────────────────────────────────┘
```

> **Ghi chú về Giấy phép:** Toàn bộ các phần mềm và thư viện đều đạt chứng chỉ OSI-approved hoặc tương thích hoàn toàn khi triển khai đóng gói container độc lập, cam kết điểm số tuyệt đối ở phần kiểm tra PoF.

### 3.5. Kịch bản Trình diễn 7 Phút (Live Demo Showcase) Đốn tim Giám khảo
- **Phút 00:00 - 01:00 (Mở màn & [H] Human Space):**
  - Thí sinh 1 trình chiếu slide 1 trang: Nỗi đau SME Việt Nam mất 12% chi phí do mua sắm sai lệch.
  - Đăng nhập vào cổng DX-OS Portal thông qua **Keycloak SSO**.
  - Show nhanh cây thư mục **Nextcloud P.A.R.A** lưu trữ hợp đồng và **BookStack** chứa cẩm nang mua sắm.
- **Phút 01:00 - 02:30 (Quy trình & Rào chắn Poka-yoke tại [P]):**
  - Thí sinh 2 thao tác trên giao diện **Appsmith**: Tạo một Yêu cầu Mua hàng (PR) trị giá 50 triệu cho phòng IT.
  - *Demo Poka-yoke số 1:* Nhập vượt ngân sách phòng ban -> Form lập tức chuyển màu đỏ, nút "Submit" bị khóa cứng, hiển thị cảnh báo: *"Vượt ngân sách tháng còn lại: 15.000.000 VNĐ"*.
  - Sửa lại số lượng hợp lệ -> Submit -> **n8n** kích hoạt luồng sự kiện bắn tin nhắn phê duyệt tương tác vào **Mattermost** của Giám đốc. Giám đốc bấm nút "Phê duyệt" trực tiếp trên khung chat.
- **Phút 02:30 - 04:00 ([D] Data Space & Chuẩn hóa LOD):**
  - Hệ thống tự động chuyển PR thành PO chuẩn. Dữ liệu phẳng được đẩy vào **PostgreSQL**.
  - Bật endpoint LOD: Xem dữ liệu PO được xuất bản dưới dạng **JSON-LD (Schema.org)** liên kết ngữ nghĩa.
  - Mở **Apache Superset**: Dashboard nhảy số tức thì theo thời gian thực (Real-time update) phản ánh cam kết dòng tiền phải trả trong tuần tới.
- **Phút 04:00 - 06:00 ([I] Intelligence Space - Cú hích Tác tử Tự hành):**
  - Kịch bản kịch tính: Nhà cung ứng gửi hóa đơn điện tử PDF qua email/hệ thống. Hóa đơn bị cố tình kê tăng giá mỗi chiếc màn hình lên 200.000đ.
  - **Invoice Audit Agent (Dify + Ollama)** chạy ngầm, bóc tách OCR trong 2 giây.
  - Màn hình bật popup cảnh báo từ Agent: *"Phát hiện sai lệch 3-Way Matching: Đơn giá PO = 3.500.000đ, Đơn giá Hóa đơn = 3.700.000đ. Đã kích hoạt Poka-yoke: Khóa thanh toán!"*
  - Tiếp theo, Agent tự động dự thảo email phản hồi đối soát nhà cung ứng kèm trích dẫn điều khoản hợp đồng được tìm kiếm từ Vector DB.
- **Phút 06:00 - 07:00 (Tổng kết Kiến trúc & Đóng góp Nguồn mở):**
  - Thí sinh 3 show terminal chạy `docker compose ps` (100% services healthy).
  - Tóm tắt giá trị: Tối ưu 80% thời gian mua hàng, loại bỏ 100% sai sót đối soát, minh bạch dòng tiền.
  - Dẫn link GitHub Repository: Đầy đủ license SPDX header, CI/CD pass, Semantic Release `v1.0.0`.

---

# PHẦN 4: ĐỀ TÀI 2 (HƯỚNG ĐI THAY THẾ 1)
## OmniCare DX-OS - Hệ điều hành Vận hành Dịch vụ Khách hàng Đa kênh & Bảo hành Tự hành (Unified Customer Operations & Autonomous After-Sales DX-OS)

### 4.1. Tên đề tài & Đối tượng Người dùng Mục tiêu
- **Tên thương mại mã nguồn mở:** **OmniCare DX-OS**
- **Slogan:** *"Hợp nhất Đa kênh, Tự động hóa Dịch vụ, Trí tuệ hóa Trải nghiệm Khách hàng"*
- **Đối tượng:** Doanh nghiệp kinh doanh thiết bị công nghệ, điện gia dụng tử tế, chuỗi bán lẻ D2C, các trung tâm bảo hành và bảo trì kỹ thuật (Field Services).

### 4.2. Nỗi đau Vận hành Thực tế
1. **Phân mảnh kênh tiếp nhận (Channel Chaos):** Khách nhắn qua Zalo OA, Fanpage Facebook, Shopee, hotline gọi điện... Nhân viên CSKH trả lời chồng chéo, sót tin nhắn, không nắm được lịch sử mua hàng của khách.
2. **Quy trình Bảo hành - Sửa chữa thủ công, thất lạc linh kiện:** Tiếp nhận phiếu bảo hành giấy, khách gọi hỏi tiến độ thì nhân viên phải chạy xuống xưởng hỏi thợ. Linh kiện thay thế không được đồng bộ trừ kho, dẫn đến thất thoát.
3. **Vi phạm SLA (Service Level Agreement):** Không có hệ thống theo dõi thời hạn cam kết với khách hàng, các ca khiếu nại phức tạp bị bỏ quên dẫn đến khủng hoảng truyền thông.

### 4.3. Thiết kế Ánh xạ 4 Không gian H-P-D-I
- **[H] Human Space:**
  - **Authentik SSO**: Định danh nhân viên CSKH, kỹ thuật viên sửa chữa, quản trị viên.
  - **Chatwoot**: Nền tảng giao tiếp khách hàng đa kênh nguồn mở (gom Facebook, Zalo qua Webhook, Website Livechat vào 1 hộp thư chung).
  - **BookStack**: Sổ tay tra cứu mã lỗi kỹ thuật, quy trình an toàn lao động, chính sách đổi trả sản phẩm.
- **[P] Process Space:**
  - **Appsmith**: Bàn làm việc số của Kỹ thuật viên (Service Workbench) - nhận ticket, cập nhật trạng thái sửa chữa, chọn linh kiện thay thế.
  - **n8n**: Điều phối vòng đời ticket bảo hành (Tiếp nhận -> Kiểm tra -> Báo giá -> Sửa chữa -> Bàn giao).
  - **Rào chắn Poka-yoke:**
    - Không thể tạo phiếu bảo hành nếu số Serial Number/IMEI không tồn tại trên hệ thống hoặc đã hết hạn bảo hành (trừ khi chuyển sang luồng sửa chữa dịch vụ tính phí).
    - Khóa không cho đóng ticket (Resolve) nếu chưa có chữ ký số điện tử của khách hàng hoặc ảnh chụp biên bản bàn giao thiết bị.
- **[D] Data Space:**
  - **PostgreSQL**: Customer 360 Database lưu trữ toàn bộ lịch sử mua sắm, khiếu nại, sửa chữa.
  - **Linked Open Data (LOD):** Mô hình hóa thông tin theo **Schema.org/Product**, **Schema.org/WarrantyPromise**, cung cấp trang tra cứu tiến độ bảo hành công khai qua giao diện web chuẩn SEO Semantic (khách tự nhập mã tra cứu không cần gọi hotline).
  - **Metabase BI Dashboard:** Đo lường thời gian xử lý trung bình (MTTR), Tỷ lệ giải quyết cuộc gọi đầu tiên (FCR), Chỉ số hài lòng khách hàng (CSAT) theo thời gian thực.
- **[I] Intelligence Space:**
  - **Agentic Diagnostic Assistant (Ollama + Qdrant + Dify):**
    - Tự động phân tích triệu chứng hư hỏng khách mô tả qua đoạn chat, tra cứu RAG trong sổ tay kỹ thuật để gợi ý nguyên nhân hỏng hóc và danh sách linh kiện cần thay kèm báo giá dự kiến.
  - **SLA Sentinel Agent:**
    - Lắng nghe các ticket sắp chạm trễ hạn (còn 2 tiếng là quá SLA), tự động đẩy độ ưu tiên (Escalation) và tag Trưởng bộ phận vào nhóm xử lý khẩn cấp.

### 4.4. Tech-Stack Đề xuất
- **Chatwoot** (MIT), **Appsmith** (Apache 2.0), **n8n** (Fair-code/Community), **PostgreSQL** + **Metabase** (AGPL v3), **Dify** + **Ollama** + **Qdrant** (Apache 2.0).
- 100% Docker-ready, chạy mượt mà trên máy tính tiêu chuẩn phục vụ hội đồng chấm thi.

### 4.5. Kịch bản Demo 7 Phút
- **0 - 2p:** Khách hàng nhắn tin vào Chatwoot báo quạt thông minh kêu to và bốc mùi khét.
- **2 - 4p:** AI Agent lập tức trích xuất thông tin khách hàng từ [D], nhận diện mã sản phẩm, chẩn đoán lỗi hỏng tụ điện, tự động tạo Ticket trên Appsmith kèm rào chắn Poka-yoke chỉ định kỹ thuật viên chuyên ngành điện tử gia dụng.
- **4 - 5p:** Kỹ thuật viên thao tác đổi trạng thái, hệ thống kích hoạt trừ kho linh kiện tự động và xuất bản link tra cứu tiến độ LOD JSON-LD cho khách.
- **5 - 7p:** Metabase cập nhật SLA live; Tóm tắt mô hình Open-Core và giá trị kinh tế cho doanh nghiệp bán lẻ.

---

# PHẦN 5: ĐỀ TÀI 3 (HƯỚNG ĐI THAY THẾ 2)
## CampusDX-OS - Hệ điều hành Vận hành Đào tạo & Quản trị Đề tài Nghiên cứu Khoa học (Academic & Institutional Operations DX-OS)

### 5.1. Tên đề tài & Đối tượng Người dùng Mục tiêu
- **Tên thương mại mã nguồn mở:** **CampusDX-OS**
- **Slogan:** *"Số hóa Vận hành Học thuật, Liên kết Tri thức Mở, Tự hành Đánh giá Nghiên cứu"*
- **Đối tượng:** Các Khoa/Viện trường Đại học, Cao đẳng, Trung tâm Ươm tạo khởi nghiệp công nghệ, Viện nghiên cứu & R&D của doanh nghiệp.

### 5.2. Nỗi đau Vận hành Thực tế
1. **Quy trình nộp - duyệt - phản biện đồ án/đề tài thủ công:** Sử dụng email cá nhân, biểu mẫu giấy tờ rườm rà; sinh viên và giảng viên mất nhiều thời gian xếp lịch họp hội đồng.
2. **Thất thoát tài sản học thuật và mã nguồn:** Khi sinh viên tốt nghiệp, mã nguồn đồ án, dữ liệu nghiên cứu và tài liệu báo cáo phân tán, người đi sau không kế thừa được, dẫn đến việc nghiên cứu trùng lặp, lãng phí tài nguyên.
3. **Phân mảnh dữ liệu chuyên gia & Giảng viên:** Khó khăn trong việc tìm kiếm chuyên gia phản biện đúng chuyên môn hẹp; dữ liệu công bố khoa học không được liên kết chuẩn hóa.

### 5.3. Thiết kế Ánh xạ 4 Không gian H-P-D-I
- **[H] Human Space:**
  - **Keycloak SSO**: Phân quyền Sinh viên, Cán bộ Hướng dẫn, Cán bộ Phản biện, Trưởng Khoa.
  - **Nextcloud P.A.R.A**: Lưu trữ toàn bộ mã nguồn bài nộp, dataset thực nghiệm, tài liệu hướng dẫn theo cấu trúc phân tầng khoa học.
  - **Wiki.js**: Cổng tri thức nghiên cứu, quy chuẩn trình bày luận văn tốt nghiệp, quy định liêm chính học thuật.
- **[P] Process Space:**
  - **Directus / NocoDB**: Giao diện đăng ký tên đề tài, nộp đề cương, chấm điểm online.
  - **n8n**: Quản trị luồng thẩm định: Đăng ký đề cương -> Duyệt đề cương -> Nộp báo cáo tiến độ -> Thẩm định phản biện -> Ra Hội đồng bảo vệ.
  - **Poka-yoke Rào chắn:**
    - Khóa không cho nộp bản báo cáo nếu không có đính kèm repo mã nguồn và link dataset kiểm chứng.
    - Chặn đăng ký đề tài nếu trùng lặp ngữ nghĩa trên 80% với đề tài đã bảo vệ trong vòng 3 năm gần nhất.
- **[D] Data Space:**
  - **PostgreSQL**: Cơ sở dữ liệu học thuật trung tâm.
  - **Linked Open Data (LOD):** Kế thừa OLP 2025 triệt để thông qua việc chuẩn hóa dữ liệu công trình theo **Dublin Core Metadata (DCMI)** và **Bibliographic Ontology (BIBO)**. Mở cổng SPARQL/JSON-LD endpoint để kết nối liên thông với các kho lưu trữ mở quốc tế (OpenAlex, CrossRef, arXiv).
  - **Apache Superset Dashboard:** Theo dõi tỷ lệ hoàn thành tiến độ đồ án, phân bổ đề tài theo xu hướng công nghệ, ma trận năng suất nghiên cứu của các lab.
- **[I] Intelligence Space:**
  - **Academic Peer-Review Matcher Agent (Dify + Qdrant):**
    - Đọc tóm tắt và từ khóa của đề tài, thực hiện semantic search trên hồ sơ lý lịch khoa học (LOD) của các giảng viên để tự động đề xuất 3 phản biện có độ tương thích cao nhất.
  - **Integrity & Formatting Agent (Ollama):**
    - Kiểm tra sơ bộ cấu trúc bài báo cáo theo mẫu quy định của trường, phát hiện các đoạn văn bản thiếu trích dẫn khoa học hợp lệ trước khi cho phép nộp chính thức.

### 5.4. Tech-Stack Đề xuất
- **Keycloak** (Apache 2.0), **Nextcloud** (AGPL v3), **Directus** (GPL v3 / BSL -> thay thế bằng **NocoDB** AGPL v3 để bảo đảm 100% OSI-approved), **n8n**, **PostgreSQL**, **Apache Superset**, **Dify** + **Ollama**.

### 5.5. Kịch bản Demo 7 Phút
- Sinh viên đăng nhập Keycloak nộp đề tài tốt nghiệp OLP 2026 -> Poka-yoke chặn vì thiếu cam kết bản quyền -> Nộp lại thành công -> Agent tự động tóm tắt và đối sánh tìm giảng viên phản biện trên kho dữ liệu mở LOD -> Trưởng khoa duyệt 1-click -> Superset cập nhật biểu đồ phân bổ đề tài toàn trường.

---

# PHẦN 6: CHIẾN LƯỢC THỰC THI "KHÔNG ĐIỂM CHẾT" (ZERO-PoF CHECKLIST) & CẨM NANG THUYẾT TRÌNH ĐỈNH CAO

### 6.1. Bộ Quy tắc Bất Khả Xâm Phạm Vượt Ải PoF (50 Điểm Tuyệt Đối)
Ban Giám khảo VFOSSA rất nghiêm khắc về văn hóa nguồn mở. Dưới đây là các biện pháp kỹ thuật bắt buộc phải thiết lập ngay từ commit đầu tiên:

1. **Giấy phép Bản quyền (10 điểm):**
   - Chọn giấy phép chuẩn: Khuyến nghị sử dụng **Apache-2.0** hoặc **MIT** cho toàn bộ phần mã nguồn đội thi tự viết.
   - Bắt buộc có file `LICENSE` toàn văn ở thư mục gốc.
   - Dùng công cụ tự động (như `addlicense` của Google hoặc GitHub Action `fsfe/reuse-action`) để chèn License Header chuẩn SPDX vào **100% tệp mã nguồn** (`.ts`, `.py`, `.go`, `.sh`, `.sql`).
2. **Hệ thống Quản lý Mã nguồn (5 điểm):**
   - Kho lưu trữ public trên GitHub/GitLab.
   - Commit liên tục trong suốt 1 tháng làm bài (từ tháng 11 đến tháng 12/2026). Tuyệt đối cấm hành vi code máy cá nhân rồi chỉ đẩy 1 commit duy nhất trước ngày thi.
3. **Bản Phát hành Release (5 điểm):**
   - Tạo GitHub Release chính thức với tag Semantic Versioning: `v1.0.0`.
   - File đính kèm phải là định dạng nén mở tiêu chuẩn: `.tar.gz` hoặc `.zip`.
4. **Cài đặt & Biên dịch Sạch từ Mã nguồn (10 điểm):**
   - Đóng gói toàn bộ hệ thống bằng **Docker & Docker Compose**.
   - Cung cấp file `.env.example` rõ ràng; không hardcode bất kỳ IP, port hay đường dẫn tuyệt đối nào của máy tính cá nhân.
   - Test kiểm thử kịch bản: Trên một máy ảo Ubuntu hoàn toàn sạch, chỉ cần gõ:
     ```bash
     git clone <repo-url>
     cd dx-os-procure
     cp .env.example .env
     docker compose up -d
     ```
     Toàn bộ 4 không gian H-P-D-I phải khởi động thành công và liên thông với nhau trong vòng dưới 5 phút!
5. **Quản lý Thư viện Phụ thuộc (10 điểm):**
   - Không commit file nhị phân (binary) hay các thư mục thư viện (`node_modules/`, `venv/`, `vendor/`) vào git.
   - Luôn sử dụng lockfile chuẩn (`package-lock.json`, `pnpm-lock.yaml`, `requirements.txt`, `poetry.lock`).
6. **Tài liệu & Bug Tracker (10 điểm):**
   - `README.md` chuyên nghiệp: Đầy đủ sơ đồ kiến trúc Mermaid, giải thích mô hình 4 không gian, hướng dẫn cấu hình chi tiết, API docs.
   - `CHANGELOG.md` ghi nhận từng mốc thay đổi theo chuẩn Keep a Changelog.
   - Kích hoạt **GitHub Issues**, tạo các issue mô tả task, gán nhãn bug/feature và liên kết với các Pull Request thực tế.

---

### 6.2. Kỹ năng Thuyết trình & Trình diễn Sân khấu Chung kết (50 Điểm Thăng Hoa)

1. **Công thức Cấu trúc Thuyết trình 7 Phút (The 7-Minute Pitch Formula):**
   - **00:00 - 01:00 (Hook & Problem):** Mở đầu bằng nỗi đau nhức nhối thực tế tại Việt Nam (không đọc lý thuyết giáo điều, dùng số liệu trực quan).
   - **01:00 - 02:00 (The DX-OS Architecture):** Giới thiệu kiến trúc H-P-D-I, khẳng định tính kế thừa trọn vẹn OLP 2023 - 2024 - 2025.
   - **02:00 - 05:30 (Live End-to-End Action):** Trình diễn dòng dữ liệu xuyên suốt 1 kịch bản nghiệp vụ duy nhất từ [H] -> [P] -> [D] -> [I]. Tuyệt đối không trình chiếu slide chụp màn hình; Ban Giám khảo muốn thấy hệ thống sống đang chạy!
   - **05:30 - 06:30 (The WOW Factor):** Kích hoạt tính năng Agentic AI tự hành giải quyết bài toán phức tạp và cơ chế Human-in-the-loop bảo đảm an toàn.
   - **06:30 - 07:00 (FOSS Spirit & Call to Action):** Trưng bày kho mã nguồn, chỉ số PoF hoàn hảo, tài liệu mở và tiềm năng đóng góp cho cộng đồng doanh nghiệp Việt Nam.

2. **Quy tắc An toàn Sân khấu (Live Demo Fail-Safe):**
   - Chuẩn bị sẵn một video quay màn hình chất lượng cao 4K lưu ở máy cục bộ (Offline Backup) phòng khi hội trường mất mạng Internet hoặc máy chủ quá tải.
   - Toàn bộ mô hình LLM (Ollama) phải chạy offline cục bộ trên GPU máy trạm của đội thi, không phụ thuộc vào API OpenAI/Claude bên ngoài để tránh nghẽn mạng hay lỗi quota giữa buổi thuyết trình.

---

### KẾT LUẬN & ĐỀ XUẤT HÀNH ĐỘNG
Để tối đa hóa cơ hội đạt **Giải Nhất Khối Phần mềm Nguồn mở OLP 2026**, đội tuyển nên tập trung 100% nguồn lực vào **Đề tài 1: ProcureOS**. Đây là đề tài hội tụ đầy đủ nhất tính thời sự kinh tế, độ sâu kiến trúc H-P-D-I, tính răn đe chống lỗi Poka-yoke, và phô diễn sức mạnh vượt trội của Agentic AI kết hợp Dữ liệu mở liên kết (LOD).
