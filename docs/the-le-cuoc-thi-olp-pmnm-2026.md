# THỂ LỆ CUỘC THI PHẦN MỀM NGUỒN MỞ - OLP 2026

> **Tài liệu tư liệu AI / Cẩm nang tra cứu quy chế thi PMNM OLP 2026**  
> **Nguồn trích xuất từ:** `/home/vanii/Downloads/Thể lệ cuộc thi phần mềm nguồn mở - OLP 2026.pdf`  
> **Cơ quan tổ chức:** Hội Tin học Việt Nam  
> **Đơn vị thường trực:** Câu lạc bộ Phần mềm Tự do Nguồn mở Việt Nam (VFOSSA)  

---

## 1. THÔNG TIN CHUNG

Căn cứ theo Quy chế Olympic Tin học Sinh viên Việt Nam:

- **Đối tượng tham dự:** Sinh viên chuyên hoặc không chuyên về Công nghệ Thông tin (CNTT) của các trường đại học, cao đẳng trên toàn quốc.
- **Hình thức cuộc thi:** Lập trình hackathon theo đội tuyển với đề thi do Ban Tổ chức (BTC) đưa ra.
- **Yêu cầu tham gia:**
  - Các trường đăng ký các đội tuyển tham gia nội dung Phần mềm Nguồn mở (PMNM).
  - Mỗi đội thi bao gồm **không quá 3 thí sinh** và được dẫn dắt bởi **một giảng viên** của trường tham dự.
  - Mỗi trường chỉ được đăng ký **tối đa 2 đội tuyển** tham gia nội dung PMNM.
- **Giải thưởng:** Theo quy chế của cuộc thi OLP 2026.

---

## 2. PHƯƠNG THỨC RA ĐỀ VÀ LÀM BÀI THI

1. **Ra đề:** Đề thi lập trình do các chuyên gia của VFOSSA xây dựng dựa trên chủ đề của năm.
2. **Thời gian công bố đề:** Đề thi được công bố **trước 1 tháng** tính đến ngày chấm thi chung kết.
3. **Quá trình làm bài:** Sau khi đề thi được công bố, các đội tiến hành lập trình theo các yêu cầu của đề bài. Toàn bộ kết quả sản phẩm của các đội thi **phải được công bố trên một kho mã nguồn mở**.
4. **Trình diễn sản phẩm:** Các đội thi chuẩn bị bài trình bày và nội dung trình diễn sản phẩm kết quả tại buổi chấm thi của BTC OLP.
5. **Đánh giá & xếp hạng:** BTC chấm điểm bài thi và sắp xếp phân hạng dựa trên:
   - Sản phẩm đã được công bố trên kho nguồn mở (chấm trước chung kết - PoF).
   - Kết quả trình diễn tại buổi chung kết.

---

## 3. CHỦ ĐỀ VÀ LỊCH TRÌNH NĂM 2026

### Chủ đề chính thức:
> **“Xây dựng hệ điều hành doanh nghiệp số (DX-OS)”**

### Lịch trình tổ chức:
| Mốc thời gian | Sự kiện |
|---|---|
| **Tháng 7/2026** | Công bố chủ đề và phát động cuộc thi PMNM - OLP 2026 |
| **Tháng 11/2026** | BTC công bố đề thi và tiếp nhận thông tin danh sách đăng ký thi |
| **Ngày 07 - 09/12/2026** | Chấm thi kho mã nguồn của sản phẩm dự thi (Tiêu chí PoF) |
| **Ngày 10/12/2026** | Trình diễn sản phẩm và chấm thi chung kết |
| **Ngày 11/12/2026** | Công bố trao giải |

---

## 4. TIÊU CHÍ CHẤM ĐIỂM (TỔNG ĐIỂM: 100 ĐIỂM)

### Yêu cầu bắt buộc tiên quyết:
- Dự án tham gia dự thi **bắt buộc phải là phần mềm nguồn mở** được phát hành theo **giấy phép OSI-approved** ([Danh mục giấy phép OSI](http://opensource.org/licenses)).
- Mã nguồn phải được **truy cập tự do trên Internet**.
- **Chỉ các dự án đáp ứng được yêu cầu là phần mềm nguồn mở mới được BTC chấm điểm xếp hạng.**

---

### PHẦN I: TIÊU CHÍ DỰA TRÊN PoF (Point of Failure) - 50 ĐIỂM
*(Được chấm trước buổi chung kết, từ ngày 07 - 09/12/2026)*

| STT | Tiêu chí | Điểm tối đa | Điểm trừ (Vi phạm) | Ghi chú & Diễn giải |
|:---:|---|:---:|---|---|
| **1** | **Sử dụng hệ thống quản lý mã nguồn trên Internet** | **5** | | Có thể truy cập kho mã nguồn của sản phẩm từ Internet |
| | - Có hệ thống quản lý mã nguồn công khai, nhưng không có web viewer | | **-3** | Phải xem được mã nguồn trực tiếp qua giao diện web (như GitHub, GitLab, Gitea...) |
| | - Có hệ thống quản lý mã nguồn nhưng không được truy cập mở | | **-3** | Bị khóa quyền truy cập hoặc đòi hỏi xác thực/phân quyền khép kín |
| | - Có hệ thống quản lý mã nguồn nhưng trên thực tế không được sử dụng | | **-5** | Chỉ upload 1 commit cuối cùng hoặc không sử dụng VCS trong quá trình phát triển |
| **2** | **Cấp phép PMNM theo giấy phép OSI-approved** | **10** | | Sản phẩm có giấy phép mở và giải quyết đúng đầu bài của đề thi |
| | - Giấy phép không được ghi trong từng tệp mã | | **-5** | Mỗi tệp mã nguồn (source code header) phải có license header |
| | - Mã nguồn tự thân chứa sự không tương thích của các giấy phép | | **-5** | Tránh trộn lẫn các license xung đột (ví dụ GPL-2.0 và Apache-2.0 không tương thích) |
| | - Mã nguồn không có thông báo về mục đích của giấy phép | | **-5** | Thiếu NOTICE hoặc văn bản nêu rõ mục đích cấp phép |
| | - Mã nguồn không bao gồm một bản sao toàn văn giấy phép | | **-5** | Kho lưu trữ phải chứa tệp `LICENSE` / `COPYING` toàn văn |
| **3** | **Có ít nhất một bản phát hành (release) để làm sản phẩm dự thi** | **5** | | Bản release đầu tiên phải được tạo trước thời điểm nộp bài thi |
| | - Dự án không có phát hành | | **-5** | Không tạo GitHub/GitLab Release hoặc tag phiên bản |
| | - Dự án không thực hiện phát hành theo phiên bản | | **-3** | Không đánh số phiên bản chuẩn (ví dụ Semantic Versioning `v1.0.0`) |
| | - Sử dụng các định dạng không phải là mở cho bản phát hành | | **-3** | Dùng `.rar`, `.arj` thay vì `.tar.gz`, `.tar.bz2`, `.zip` |
| **4** | **Cài đặt, dịch từ mã nguồn (Building From Source)** | **10** | | Sản phẩm phải cho phép cài đặt, biên dịch được từ mã nguồn |
| | - Không có hướng dẫn dịch từ mã nguồn | | **-5** | Thiếu file README hướng dẫn build chi tiết từng bước |
| | - Mã nguồn được cấu hình bằng cách sửa thủ công vào các tệp header | | **-5** | Cần dùng biến môi trường `.env`, cờ cấu hình thay vì hardcode sửa header |
| | - Mã nguồn không cấu hình được trước khi dịch | | **-5** | Không hỗ trợ file config / options trước build |
| | - Mã nguồn được dịch bằng công cụ nguồn đóng hoặc tự tạo | | **-5** | Phải dùng công cụ build chuẩn nguồn mở (npm/yarn/pnpm, make, cmake, gcc, docker...) |
| | - Chương trình không thể hoạt động nếu nằm ngoài thư mục mã nguồn | | **-5** | Bị hardcode đường dẫn cục bộ (absolute path máy dev) |
| **5** | **Sử dụng thư viện và gói đính kèm (bundling)** | **10** | | Có thông tin làm rõ các thư viện, gói đính kèm được sử dụng |
| | - Không cố gắng sử dụng các thư viện sẵn có trong hệ thống | | **-5** | Bỏ qua package manager chuẩn mà tự copy paste thư viện vào source |
| | - Phát hành cùng với gói đính kèm của các dự án khác mà nó phụ thuộc vào | | **-5** | Vendor bundle không cần thiết thay vì khai báo dependency (`package.json`, `go.mod`, `requirements.txt`...) |
| | - Mã nguồn của gói đính kèm đã bị chỉnh sửa | | **-5** | Tự ý sửa mã thư viện ngoài mà không đóng góp/fork tách bạch |
| **6** | **Tài liệu và giao tiếp** | **10** | | Tài liệu rõ ràng, thực hiện được |
| | - Không có ghi nhận quản lý lỗi phần mềm (bug tracker) | | **-5** | Không sử dụng GitHub/GitLab Issues |
| | - Không có lịch sử thay đổi mã nguồn (changelog) | | **-5** | Thiếu file `CHANGELOG.md` ghi nhận lịch sử các bản cập nhật |
| | - Không có tài liệu readme và hướng dẫn | | **-5** | Thiếu file `README.md` hoặc tài liệu sơ sài |

---

### PHẦN II: TIÊU CHÍ DỰA TRÊN SẢN PHẨM - 50 ĐIỂM
*(Được chấm trong buổi thi chung kết ngày 10/12/2026)*

| STT | Tiêu chí | Điểm tối đa | Ghi chú & Diễn giải |
|:---:|---|:---:|---|
| **7** | **Tính nguyên gốc của giải pháp kĩ thuật** | **10** | Dựa trên kết quả trình bày về sự sáng tạo của đội thi trong cách giải quyết bài toán |
| **8** | **Mức độ hoàn thiện của sản phẩm** | **10** | Dựa trên kết quả chạy trình diễn thực tế (live demo mượt mà, hạn chế lỗi/crash) |
| **9** | **Mức độ sử dụng thân thiện của sản phẩm** | **10** | Dựa trên trải nghiệm người dùng (UX/UI), tiện ích thực tế cho doanh nghiệp/người dùng cuối |
| **10** | **Mức độ phát triển bền vững của sản phẩm** | **10** | Dựa trên tài liệu kĩ thuật (architecture, API docs), công cụ hỗ trợ công bố kèm theo, khả năng duy trì lâu dài |
| **11** | **Phong cách trình diễn và khả năng thu hút cộng đồng nguồn mở** | **10** | Dựa trên showcase trình diễn tại cuộc thi, sức hấp dẫn và tiềm năng phát triển cộng đồng |

---

## 5. NGUỒN THAM KHẢO VỀ TIÊU CHÍ CHẤM ĐIỂM PoF

1. **How you know your Free or Open Source Software Project is doomed to FAIL (or at least, held back from success)**  
   - Tác giả: Tom Callaway  
   - Xuất bản trên Livejournal (29/05/2009): [http://spot.livejournal.com/308370.html](http://spot.livejournal.com/308370.html)
2. **Đánh giá khả năng phát triển của một dự án PMTDNM (Bản dịch tiếng Việt)**  
   - Người dịch: Trương Anh Tuấn  
   - Link: [http://blog.iwayvietnam.com/tuanta/2013/04/danh-gia-kha-nang-phat-trien-cua-mot-du-an-foss/](http://blog.iwayvietnam.com/tuanta/2013/04/danh-gia-kha-nang-phat-trien-cua-mot-du-an-foss/)

---

## 6. CHECKLIST CHECKPOINT NHANH DÀNH CHO AI / DEVELOPER (CHỐNG TRỪ ĐIỂM PoF)

- [ ] **Mã nguồn công khai:** Repo công khai trên GitHub/GitLab, có web viewer, có commit history đầy đủ trong suốt quá trình làm.
- [ ] **Giấy phép OSI-approved:**
  - [ ] File `LICENSE` hoặc `COPYING` toàn văn ở root repo.
  - [ ] Header bản quyền và license xuất hiện ở đầu tất cả các file mã nguồn.
  - [ ] Kiểm tra tương thích license giữa các package/dependencies.
- [ ] **Release:**
  - [ ] Tạo ít nhất 1 GitHub Release (hoặc tag release `v1.0.0`) trước giờ nộp bài.
  - [ ] File nén đính kèm dùng định dạng mở chuẩn (`.tar.gz`, `.zip`).
- [ ] **Build từ mã nguồn:**
  - [ ] File `README.md` hướng dẫn build step-by-step rõ ràng từ môi trường sạch.
  - [ ] Hỗ trợ cấu hình qua file `.env` / config flags, không hardcode path hay sửa header file.
  - [ ] Build bằng công cụ mã nguồn mở tiêu chuẩn hoặc đóng gói bằng Docker / Docker Compose.
  - [ ] Chạy độc lập, không phụ thuộc vào thư mục gốc code máy cục bộ.
- [ ] **Quản lý dependencies:**
  - [ ] Sử dụng file quản lý phụ thuộc chuẩn (`package.json`, `pnpm-lock.yaml`, `go.mod`, v.v.).
  - [ ] Không commit vendored binary hay file code thư viện bị chỉnh sửa.
- [ ] **Tài liệu & giao tiếp:**
  - [ ] Có `README.md` hoàn chỉnh (kiến trúc, cài đặt, chạy demo, API).
  - [ ] Có `CHANGELOG.md` ghi lại lịch sử các phiên bản.
  - [ ] Kích hoạt và có issue/bug tracker ghi nhận task và xử lý lỗi trên GitHub/GitLab.
