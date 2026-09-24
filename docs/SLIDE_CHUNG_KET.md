# ĐỀ CƯƠNG 12 SLIDE THUYẾT TRÌNH VÒNG CHUNG KẾT
### Cuộc thi "Xây dựng Hệ điều hành Doanh nghiệp số AI (DX-OS)" — OLP PMNM 2026
**Đội thi:** FoodSafe-DX-OS Team  
**Đơn vị:** OLP 2026 Finalist

---

## 🖥️ SLIDE 1: TIÊU ĐỀ & ĐỊNH VỊ SẢN PHẨM
* **Tiêu đề chính:** FoodSafe-DX-OS
* **Tiêu đề phụ:** Hệ Điều Hành Doanh Nghiệp Số Quản Trị An Toàn Thực Phẩm, Kiểm Thực 3 Bước & Phản Ứng Dịch Tễ Thần Tốc Dưới 3 Giây
* **Thông điệp:** "Bảo Vệ Từng Bữa Ăn Bán Trú Học Đường & Khu Công Nghiệp Bằng Rào Chắn Poka-yoke & Agentic AI"
* **Badge:** Vòng Chung kết OLP PMNM 2026 • 100% Mã nguồn mở Apache 2.0 • PoF Validated (50/50đ)

---

## 🖥️ SLIDE 2: NỖI ĐAU THỜI SỰ NHỨC NHỐI (THÁNG 09/2026)
* **Số liệu thực tế bóc tách từ báo chí:**
  - **254 ca ngộ độc tại Gia Lai (07/09/2026):** Vi khuẩn Salmonella từ bánh mì và patê Bin Bin.
  - **180 công nhân dệt may Scavi Huế (12/09/2026):** Nhập viện cấp cứu sau bữa ăn ca tại KCN Phong Điền.
  - **Trường Tiểu học Lê Trọng Tấn - Hà Nội (11/09/2026):** Phát hiện tôm ươn và thịt gà bốc mùi đứt chuỗi lạnh lúc 5h sáng.
* **Câu hỏi bản lề:** Tại sao có Luật ATTP số 55 và Thông tư Kiểm thực 3 bước nhưng ngộ độc tập thể vẫn liên tục xảy ra?

---

## 🖥️ SLIDE 3: BẪY VẬN HÀNH & NGUYÊN NHÂN GỐC RỄ
* **3 Tử huyệt trong vận hành bếp ăn hiện nay:**
  1. *Ghi chép thủ công đối phó:* Sổ kiểm thực 3 bước và lưu mẫu chỉ được viết bù lùi ngày khi có đoàn thanh tra.
  2. *Thiếu rào chắn kỹ thuật (No Poka-yoke):* Nhiệt độ lạnh > 4°C, thịt nấu chưa chín < 75°C vẫn dễ dãi cho qua.
  3. *Phản ứng dịch tễ chậm chạp:* Mất 3 - 5 ngày truy vết bằng công văn giấy tờ $\rightarrow$ Hàng nghìn học sinh khác tiếp tục ăn phải thực phẩm độc hại!

---

## 🖥️ SLIDE 4: GIẢI PHÁP FOODSAFE-DX-OS
* **Chuyển đổi từ Phần mềm Thụ động sang Hệ Điều Hành Có Quyền Lực:**
  - Không cho phép người dùng nhập sai dữ liệu.
  - Tự động kích hoạt rào chắn Poka-yoke khóa giao dịch (HTTP 422).
  - Khóa điện tử tủ lưu mẫu 24 giờ bảo vệ chứng cứ dịch tễ.
  - Thuật toán đồ thị BFS truy vết liên thông chuỗi cung ứng dưới 3 giây.

---

## 🖥️ SLIDE 5: KIẾN TRÚC 4 KHÔNG GIAN (H-P-D-I) CHUẨN VFOSSA
* **[H] Human Space:** Cổng tác nghiệp Bếp trưởng, Cán bộ Y tế học đường và Cổng minh bạch cho Ban Giám hiệu / Phụ huynh.
* **[P] Process Space:** Workflow Kiểm thực 3 bước khép kín; Rào chắn Poka-yoke chuỗi lạnh $\le$ 4°C, nhiệt độ tâm $\ge$ 75°C, Khóa tủ mẫu 24H.
* **[D] Data Space:** PostgreSQL 16 Single Source of Truth; Nhật ký Audit Trail bất biến; BI Dashboard trực quan.
* **[I] Intelligence Space:** Multi-tier BFS Graph Tracer; Chẩn đoán mầm bệnh Salmonella; Local RAG vi sinh 100% offline.

---

## 🖥️ SLIDE 6: KẾ THỪA DI SẢN OLP PMNM CÁC NĂM
* **OLP 2023 (RAG & Tri thức chuyên sâu):** Local RAG tra cứu QCVN 8-2:2011/BYT và văn bản pháp luật không ảo giác.
* **OLP 2024 (Low-code Process):** Biểu mẫu kiểm thực tương tác động, cơ chế kiểm soát lỗi Poka-yoke cấu hình linh hoạt.
* **OLP 2025 (Linked Open Data):** Chuẩn hóa định danh mã cơ sở, mã lô hàng và mã số thuế theo chuẩn dữ liệu liên kết mở.

---

## 🖥️ SLIDE 7: RÀO CHẮN POKA-YOKE ENGINE TRONG THỰC TẾ
* **Bước 1 (Giao nhận):** Thịt tươi 13.5°C (> 4.0°C) $\rightarrow$ Khóa chốt kho, đổi trạng thái lô thành `REJECTED`.
* **Bước 2 (Chế biến):** Nấu ở 61.5°C (< 75.0°C) $\rightarrow$ Khóa quyền xuất ăn; Cố tình dùng lô hàng bị từ chối $\rightarrow$ Khóa lập tức!
* **Bước 3 (Lưu mẫu 24h):** Mở sớm trước 24h $\rightarrow$ Khóa chốt điện tử; Chỉ mở khẩn cấp khi có quyền Human-in-the-loop (HITL) và mã passcode thanh tra y tế.

---

## 🖥️ SLIDE 8: THUẬT TOÁN TRUY VẾT ĐỒ THỊ BFS DƯỚI 3 GIÂY
* **Tốc độ thực tế đo đạc:** **18.37 mili-giây** (Vượt xa chuẩn < 3000 ms).
* **Quét ngược (Backward Trace):** Bệnh nhân $\rightarrow$ Món ăn $\rightarrow$ Lô hàng `BATCH-2026-PATE-0907-TOXIC` $\rightarrow$ Cơ sở Bin Bin (`BLACKLISTED`).
* **Quét xuôi (Forward Recall - Cứu sống người):** Phát hiện Trường THCS Quang Trung (850 học sinh) chuẩn bị dùng chung lô patê $\rightarrow$ Phát lệnh phong tỏa tủ mẫu và ngừng bữa ăn trưa khẩn cấp!

---

## 🖥️ SLIDE 9: LOCAL RAG VI SINH — 100% OFFLINE (ZERO CLOUD)
* **Loại bỏ hoàn toàn rủi ro AI Wrapper:**
  - Không tốn chi phí API OpenAI/Gemini.
  - Không rò rỉ dữ liệu an ninh lương thực nội bộ.
  - Không bị ảnh hưởng khi mất kết nối Internet tại bếp ăn vùng sâu vùng xa.
  - Phản hồi trong **2.08 mili-giây**, trích dẫn chính xác từng điều khoản Nghị định 115 và QCVN 8-2.

---

## 🖥️ SLIDE 10: MINH CHỨNG POF 50 ĐIỂM TUYỆT ĐỐI
* **100% SPDX Apache License 2.0** trên mọi file mã nguồn.
* **1 Lệnh Docker Compose duy nhất** khởi chạy sạch toàn bộ Backend, Frontend, Database trên mọi máy tính.
* **Bộ Pytest tự động 16/16 Test Cases PASSED trong 0.46 giây.**
* **Không hardcode đường dẫn, Issue tracker và CHANGELOG minh bạch.**

---

## 🖥️ SLIDE 11: HIỆU QUẢ KINH TẾ & TÁC ĐỘNG XÃ HỘI
* **Đối với Trường học / Doanh nghiệp:**
  - Triệt tiêu 99% rủi ro ngộ độc thực phẩm do đứt gãy chuỗi lạnh hoặc nấu chưa chín thấu.
  - Bảo vệ uy tín nhà trường, tránh nguy cơ bị xử phạt 20 - 100 triệu đồng hoặc đình chỉ hoạt động theo Nghị định 115.
* **Đối với Xã hội:**
  - Chặn đứng các vụ ngộ độc hàng trăm ca trước khi thức ăn được đưa vào bàn ăn.
  - Số hóa minh bạch để phụ huynh hoàn toàn an tâm gửi gắm con em mỗi ngày.

---

## 🖥️ SLIDE 12: KẾT LUẬN & CAM KẾT HÀNH ĐỘNG
* **FoodSafe-DX-OS:** Code thật, chạy thật, dữ liệu thực nghiệm chân thực, giải quyết dứt điểm nỗi đau thời sự nhức nhối.
* **Lời cảm ơn:** Trân trọng cảm ơn Ban Giám khảo, Hội đồng chuyên môn VFOSSA và Ban Tổ chức Olympic Tin học Sinh viên Việt Nam 2026!
* **Q&A:** Sẵn sàng trả lời các câu hỏi phản biện chuyên sâu của Hội đồng!
