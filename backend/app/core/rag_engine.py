# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

import re
import math
import time
import logging
from typing import Dict, Any, List, Tuple
from .. import schemas

logger = logging.getLogger("foodsafe.rag_engine")

# ==========================================
# CƠ SỞ TRI THỨC QUY CHUẨN VI SINH & PHÁP LÝ ATTP
# (Curated Vietnamese Food Safety Regulatory Corpus)
# ==========================================
KNOWLEDGE_CORPUS = [
    {
        "doc_id": "QCVN-8-2-SALMONELLA",
        "category": "MICROBIOLOGY",
        "standard_code": "QCVN 8-2:2011/BYT",
        "title": "Quy chuẩn kỹ thuật quốc gia đối với giới hạn ô nhiễm Salmonella trong thực phẩm",
        "content": (
            "Theo Quy chuẩn QCVN 8-2:2011/BYT của Bộ Y tế về giới hạn ô nhiễm độc tố vi sinh vật trong thực phẩm:\n"
            "- Vi khuẩn Salmonella spp. là vi khuẩn gây ngộ độc đường ruột cấp tính nguy hiểm (nhiễm trùng - nhiễm độc).\n"
            "- Giới hạn cho phép: KHÔNG ĐƯỢC PHÉP CÓ (0 / 25g hoặc 0 / 25ml) trong tất cả các nhóm thực phẩm ăn liền, "
            "thịt gia súc gia cầm chế biến sẵn, patê gan, giò chả, sữa và sản phẩm từ trứng.\n"
            "- Thời gian ủ bệnh: 6 đến 72 giờ (thông thường từ 12 đến 36 giờ sau khi ăn thực phẩm nhiễm khuẩn).\n"
            "- Triệu chứng lâm sàng: Sốt cao đột ngột (38.5°C - 40°C), đau quặn thắt vùng bụng, nôn mửa dữ dội, "
            "tiêu chảy nhiều lần trong ngày (phân lỏng, có thể lẫn chất nhầy).\n"
            "- Biện pháp kiểm soát: Nấu chín thực phẩm với nhiệt độ tâm đạt tối thiểu 75°C trong ít nhất 15 giây. "
            "Bảo quản thực phẩm chín riêng biệt với thực phẩm sống để tránh lây nhiễm chéo."
        ),
        "keywords": ["salmonella", "pate", "thịt gà", "trứng", "sốt cao", "tiêu chảy", "nhiễm khuẩn", "qcvn 8-2", "vi sinh"],
    },
    {
        "doc_id": "QCVN-8-2-ECOLI",
        "category": "MICROBIOLOGY",
        "standard_code": "QCVN 8-2:2011/BYT",
        "title": "Giới hạn vi khuẩn Escherichia coli (E. coli) và E. coli O157:H7 trong thực phẩm",
        "content": (
            "Quy chuẩn QCVN 8-2:2011/BYT quy định đối với Escherichia coli:\n"
            "- E. coli chỉ thị vệ sinh: Giới hạn tối đa trong thịt tươi và rau quả ăn liền thường là từ 10^1 đến 10^2 CFU/g.\n"
            "- Chủng độc tố E. coli O157:H7 (STEC): KHÔNG ĐƯỢC PHÉP CÓ trong 25g thực phẩm.\n"
            "- Độc lực: E. coli O157:H7 sinh độc tố Shiga gây viêm đại tràng xuất huyết và hội chứng tan máu urê huyết (HUS), "
            "có thể dẫn đến suy thận cấp ở trẻ em và người cao tuổi.\n"
            "- Nguồn lây: Thịt bò băm chưa nấu chín, phân gia súc nhiễm vào nguồn nước tưới rau sống, sữa chưa tiệt trùng.\n"
            "- Biện pháp phòng ngừa: Nấu chín thấu thịt bò, ngâm rửa rau củ bằng nước sạch nhiều lần, kiểm soát nguồn nước sinh hoạt."
        ),
        "keywords": ["e. coli", "o157", "shiga", "tan máu", "thịt bò", "rau sống", "tiêu chảy ra máu", "qcvn 8-2"],
    },
    {
        "doc_id": "QCVN-8-2-STAPHYLOCOCCUS",
        "category": "MICROBIOLOGY",
        "standard_code": "QCVN 8-2:2011/BYT",
        "title": "Giới hạn Tụ cầu vàng (Staphylococcus aureus) và độc tố Enterotoxin",
        "content": (
            "Quy chuẩn QCVN 8-2:2011/BYT và Hướng dẫn Dịch tễ học Bộ Y tế:\n"
            "- Staphylococcus aureus: Giới hạn tối đa không quá 10^2 CFU/g trong thực phẩm ăn liền.\n"
            "- Độc tố ruột Staphylococcal Enterotoxin: KHÔNG ĐƯỢC PHÉP CÓ (âm tính trong 25g).\n"
            "- Đặc điểm độc tố: Ngoại độc tố enterotoxin rất bền với nhiệt, không bị phá hủy hoàn toàn dù đun sôi ở 100°C trong 30 phút!\n"
            "- Thời gian khởi phát: Rất nhanh, chỉ từ 30 phút đến 6 giờ sau khi ăn.\n"
            "- Triệu chứng: Buồn nôn và nôn mửa dữ dội, co thắt bụng quằn quại, tụt huyết áp nhưng thường KHÔNG SỐT.\n"
            "- Nguồn ô nhiễm: Người chế biến có mụn nhọt, vết trầy xước ở bàn tay hoặc viêm họng xì mũi trực tiếp vào thức ăn."
        ),
        "keywords": ["tụ cầu vàng", "staphylococcus", "enterotoxin", "nôn dữ dội", "không sốt", "vết thương", "chế biến"],
    },
    {
        "doc_id": "QD-1246-KIEM-THUC-3-BUOC",
        "category": "PROCEDURE",
        "standard_code": "Quyết định 1246/QĐ-BYT",
        "title": "Quy trình thực hiện chế độ Kiểm thực 3 bước tại Bếp ăn tập thể",
        "content": (
            "Quyết định số 1246/QĐ-BYT ngày 31/03/2017 của Bộ Y tế ban hành Hướng dẫn thực hiện chế độ kiểm thực 3 bước:\n"
            "1. BƯỚC 1 - KIỂM TRA TRƯỚC KHI NHẬP THỰC PHẨM (Giao nhận):\n"
            "   - Kiểm tra giấy tờ xuất xứ, hóa đơn, chứng nhận kiểm dịch thú y.\n"
            "   - Kiểm tra cảm quan màu sắc, mùi vị, trạng thái vật lý.\n"
            "   - Đo nhiệt độ chuỗi lạnh: Thực phẩm tươi sống phải <= 4°C, thực phẩm đông lạnh phải <= -12°C.\n"
            "   - Lập sổ kiểm thực Bước 1 và ký biên bản giao nhận.\n"
            "2. BƯỚC 2 - KIỂM TRA TRƯỚC KHI CHẾ BIẾN & KHI NẤU XONG:\n"
            "   - Kiểm tra vệ sinh khu vực sơ chế, dụng cụ dao thớt riêng biệt cho đồ sống và đồ chín.\n"
            "   - Đo nhiệt độ tâm nấu chín: Phải đạt tối thiểu 75°C đối với tất cả món thịt, cá, gia cầm xào/kho/hấp.\n"
            "   - Kiểm tra cảm quan độ chín thấu của món ăn.\n"
            "3. BƯỚC 3 - KIỂM TRA TRƯỚC KHI ĂN & LƯU MẪU THỨC ĂN:\n"
            "   - Kiểm tra vệ sinh khay ăn, bát đĩa, bàn ăn.\n"
            "   - Thực hiện lưu mẫu thức ăn từng món riêng biệt vào hộp chuyên dụng vô trùng."
        ),
        "keywords": ["kiểm thực 3 bước", "quyết định 1246", "giao nhận", "sơ chế", "nấu chín", "nhiệt độ tâm", "lưu mẫu"],
    },
    {
        "doc_id": "QD-1246-LUU-MAU-24H",
        "category": "PROCEDURE",
        "standard_code": "Quyết định 1246/QĐ-BYT (Phụ lục 2)",
        "title": "Quy chuẩn kỹ thuật Lưu mẫu thức ăn 24 giờ bắt buộc tại Bếp ăn",
        "content": (
            "Quy định nghiêm ngặt về Lưu mẫu thức ăn theo Quyết định 1246/QĐ-BYT:\n"
            "- Đối tượng: Bắt buộc áp dụng cho tất cả các bữa ăn từ 30 suất ăn trở lên tại trường học, bệnh viện, nhà máy.\n"
            "- Lượng mẫu lưu tối thiểu: Món ăn đặc hoặc đặc biệt (thịt, cá, xôi...) tối thiểu 100g/món; Món ăn lỏng (canh, súp, cháo...) tối thiểu 150ml/món.\n"
            "- Dụng cụ lưu mẫu: Dụng cụ bằng thủy tinh hoặc inox hoặc nhựa an toàn thực phẩm, có nắp đậy kín và được khử trùng trước khi dùng.\n"
            "- Niêm phong nhãn mẫu: Phải ghi rõ Tên cơ sở, Tên món ăn, Bữa ăn (sáng/trưa/tối), Ngày giờ lấy mẫu, Người lấy mẫu.\n"
            "- Thời gian và điều kiện bảo quản: Lưu giữ tối thiểu ĐỦ 24 GIỜ trong tủ lạnh chuyên dụng ở nhiệt độ từ 2°C đến 8°C.\n"
            "- Nghiêm cấm: Nghiêm cấm hủy mẫu hoặc mở niêm phong trước 24 giờ trừ trường hợp có yêu cầu điều tra ngộ độc của cơ quan y tế có thẩm quyền."
        ),
        "keywords": ["lưu mẫu", "24 giờ", "100g", "150ml", "tủ lạnh 2-8 độ", "niêm phong", "hủy mẫu"],
    },
    {
        "doc_id": "LUAT-ATTP-55-DIEU-28",
        "category": "LEGAL",
        "standard_code": "Luật ATTP số 55/2010/QH12",
        "title": "Điều 28 & 29: Điều kiện bảo đảm an toàn thực phẩm đối với Bếp ăn tập thể",
        "content": (
            "Luật An toàn Thực phẩm số 55/2010/QH12 của Quốc hội:\n"
            "Điều 28 - Điều kiện đối với cơ sở kinh doanh dịch vụ ăn uống và bếp ăn tập thể:\n"
            "1. Bếp ăn được thiết kế và bố trí theo nguyên tắc một chiều: từ khu nguyên liệu đầu vào, sơ chế, chế biến, nấu nướng, chia suất ăn đến khu rửa dọn.\n"
            "2. Có dụng cụ bảo quản riêng biệt cho thực phẩm sống và thực phẩm chín.\n"
            "3. Dụng cụ ăn uống phải được rửa sạch và khử trùng khô ráo trước khi dùng.\n"
            "4. Có đủ nước đạt quy chuẩn kỹ thuật phục vụ chế biến và ăn uống.\n"
            "5. Có thiết bị bảo quản thực phẩm, nhà vệ sinh, nơi rửa tay và thu dọn rác thải cách biệt.\n"
            "6. Người trực tiếp tham gia chế biến thực phẩm phải được tập huấn kiến thức an toàn thực phẩm, khám sức khỏe định kỳ và không mắc các bệnh truyền nhiễm."
        ),
        "keywords": ["luật 55", "điều 28", "nguyên tắc một chiều", "bếp ăn tập thể", "dao thớt", "nước sạch", "khám sức khỏe"],
    },
    {
        "doc_id": "LUAT-ATTP-55-THU-HOI-KHAN-CAP",
        "category": "RECALL",
        "standard_code": "Luật ATTP số 55/2010/QH12",
        "title": "Điều 53, 54, 55: Thu hồi và xử lý thực phẩm không bảo đảm an toàn",
        "content": (
            "Theo Luật ATTP số 55/2010/QH12:\n"
            "- Cơ sở sản xuất, kinh doanh thực phẩm khi phát hiện thực phẩm thuộc diện không bảo đảm an toàn "
            "phải lập tức: DỪNG SẢN XUẤT, THÔNG BÁO CHO CÁC BÊN LIÊN QUAN, THU HỒI TOÀN BỘ LÔ HÀNG.\n"
            "- Trường hợp thu hồi khẩn cấp: Thực phẩm gây ngộ độc cấp tính hoặc chứa độc tố vi sinh nguy hiểm "
            "vượt ngưỡng cho phép, thời gian phát lệnh và thực hiện thu hồi phải hoàn thành trong vòng 24 GIỜ.\n"
            "- Trách nhiệm báo cáo: Lập tức thông báo cho Chi cục An toàn vệ sinh thực phẩm địa phương và Bộ Y tế.\n"
            "- Xử lý lô hàng bị thu hồi: Buộc tiêu hủy đối với thực phẩm nhiễm vi khuẩn gây bệnh không thể khắc phục."
        ),
        "keywords": ["thu hồi khẩn cấp", "điều 53", "luật 55", "dừng sản xuất", "tiêu hủy", "24 giờ", "chi cục attp"],
    },
    {
        "doc_id": "NGHI-DINH-115-XU-PHAT",
        "category": "LEGAL",
        "standard_code": "Nghị định 115/2018/NĐ-CP & 124/2021/NĐ-CP",
        "title": "Chế tài xử phạt vi phạm kiểm thực 3 bước và lưu mẫu tại trường học, bếp ăn",
        "content": (
            "Nghị định số 115/2018/NĐ-CP của Chính phủ quy định xử phạt vi phạm hành chính về an toàn thực phẩm:\n"
            "- Hành vi không thực hiện hoặc thực hiện không đúng chế độ kiểm thực 3 bước: Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng.\n"
            "- Hành vi không lưu mẫu thức ăn hoặc lưu mẫu không đúng quy chuẩn (không đủ 24 giờ, thiếu lượng mẫu, không ghi nhãn niêm phong): "
            "Phạt tiền từ 5.000.000 đồng đến 10.000.000 đồng.\n"
            "- Hành vi sử dụng nguyên liệu thực phẩm không rõ nguồn gốc, hết hạn hoặc nhiễm vi sinh gây hại: Phạt tiền từ 20.000.000 đồng đến 100.000.000 đồng, "
            "đình chỉ hoạt động bếp ăn từ 1 đến 3 tháng và buộc tiêu hủy toàn bộ nguyên liệu.\n"
            "- Nếu gây ngộ độc ảnh hưởng từ 5 người trở lên: Chuyển hồ sơ xử lý hình sự theo Điều 317 Bộ luật Hình sự 2015."
        ),
        "keywords": ["nghị định 115", "xử phạt", "phạt tiền", "không lưu mẫu", "đình chỉ", "hình sự", "điều 317"],
    },
    {
        "doc_id": "TEMPERATURE-DANGER-ZONE",
        "category": "PROCEDURE",
        "standard_code": "WHO & FAO Codex Alimentarius",
        "title": "Nguyên lý Vùng Nhiệt độ Nguy hiểm (The Temperature Danger Zone 5°C - 60°C)",
        "content": (
            "Nguyên tắc kiểm soát nhiệt độ an toàn thực phẩm chuẩn quốc tế Codex và Bộ Y tế:\n"
            "- VÙNG NGUY HIỂM (Danger Zone): Từ 5°C đến 60°C. Ở dải nhiệt độ này, các vi khuẩn như Salmonella, E. coli, "
            "Staphylococcus aureus nhân đôi số lượng mỗi 20 phút!\n"
            "- RÀO CHẮN LẠNH (Cold Storage): Thực phẩm tươi sống phải luôn bảo quản dưới 4°C; Thực phẩm đông lạnh dưới -18°C (hoặc tối thiểu -12°C).\n"
            "- RÀO CHẮN NÓNG (Hot Holding): Thức ăn sau khi nấu chín nếu chưa dùng ngay phải giữ nóng trên 60°C.\n"
            "- RÀO CHẮN NẤU CHÍN (Safe Cooking Core Temp): Nhiệt độ tâm món ăn phải đạt >= 75°C để tiêu diệt hầu hết tế bào vi khuẩn sinh dưỡng.\n"
            "- QUY TẮC 2 GIỜ: Thức ăn nấu chín để ở nhiệt độ phòng quá 2 giờ bắt buộc phải hâm nóng lại trên 75°C hoặc hủy bỏ."
        ),
        "keywords": ["nhiệt độ nguy hiểm", "danger zone", "5-60 độ", "nhiệt độ tâm", "75 độ", "bảo quản lạnh", "4 độ", "quy tắc 2 giờ"],
    },
    {
        "doc_id": "CLINICAL-HISTAMINE-TOXICITY",
        "category": "MICROBIOLOGY",
        "standard_code": "QCVN 8-2:2011/BYT",
        "title": "Ngộ độc Histamine do đứt gãy chuỗi lạnh thủy hải sản",
        "content": (
            "Tiêu chuẩn và hướng dẫn y tế về độc tố Histamine trong thủy hải sản (cá ngừ, cá thu, tôm, mực):\n"
            "- Cơ chế sinh độc tố: Khi cá bảo quản ở nhiệt độ > 4°C, vi khuẩn sinh enzyme histidine decarboxylase "
            "chuyển hóa amino acid histidine thành độc tố Histamine.\n"
            "- Giới hạn tối đa cho phép theo QCVN 8-2:2011/BYT: 100 mg/kg đến tối đa 200 mg/kg.\n"
            "- Khởi phát: Cực kỳ nhanh, từ 10 đến 60 phút sau khi ăn.\n"
            "- Dấu hiệu nhận biết: Đỏ bừng mặt, nổi mề đay ngứa ngáy dữ dội vùng cổ và ngực, nóng rát họng, hạ huyết áp, đau đầu chóng mặt.\n"
            "- Lưu ý đặc biệt: Histamine chịu nhiệt rất cao, một khi đã sinh ra trong thịt cá thì nấu chín không thể phân hủy được!"
        ),
        "keywords": ["histamine", "cá ngừ", "cá thu", "tôm cá", "chuỗi lạnh", "đỏ bừng mặt", "dị ứng", "qcvn 8-2"],
    },
]


class LocalMicrobiologyRAG:
    """
    Local RAG Engine chạy 100% Offline trong container Docker.
    Không phụ thuộc bất kỳ Cloud LLM API nào (Zero Cloud Dependency).
    Sử dụng thuật toán Hybrid Token Retrieval + Term Weighting (TF-IDF/BM25)
    kết hợp với bộ sinh câu trả lời có cấu trúc pháp lý & y khoa chuẩn xác.
    """

    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        """Chuẩn hóa và tách từ (tokenization) hỗ trợ tiếng Việt."""
        text = text.lower()
        # Chuẩn hóa các ký tự đặc biệt nhưng giữ lại số và dấu chấm cho tên chuẩn/nhiệt độ
        tokens = re.findall(r"[a-z0-9àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ\.\-\/]+", text)
        return [t for t in tokens if len(t) > 1]

    @classmethod
    def search(cls, query: str, category: str = "ALL", top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """Tìm kiếm các trích đoạn văn bản quy chuẩn phù hợp nhất với câu hỏi."""
        query_tokens = cls.tokenize(query)
        if not query_tokens:
            return []

        results = []
        filtered_corpus = KNOWLEDGE_CORPUS
        if category and category.upper() != "ALL":
            filtered_corpus = [doc for doc in KNOWLEDGE_CORPUS if doc["category"] == category.upper()]
            if not filtered_corpus:
                filtered_corpus = KNOWLEDGE_CORPUS

        total_docs = len(filtered_corpus)

        for doc in filtered_corpus:
            doc_text = f"{doc['title']} {doc['content']} {' '.join(doc['keywords'])}"
            doc_tokens = cls.tokenize(doc_text)
            doc_token_counts = {}
            for t in doc_tokens:
                doc_token_counts[t] = doc_token_counts.get(t, 0) + 1

            doc_len = len(doc_tokens)
            score = 0.0

            # Tính điểm BM25 / Term Overlap
            for q_token in query_tokens:
                count = doc_token_counts.get(q_token, 0)
                if count > 0:
                    tf = count / (doc_len + 1e-5)
                    # Tính IDF sơ bộ
                    idf = math.log((total_docs + 1) / (1 + 1)) + 1
                    score += tf * idf * 10.0

                # Keyword exact boost
                for kw in doc["keywords"]:
                    if q_token in kw or kw in q_token:
                        score += 3.0

            # Title exact match boost
            if any(t in doc["title"].lower() for t in query_tokens):
                score += 2.0

            if score > 0:
                results.append((doc, round(score, 3)))

        # Sắp xếp theo độ liên quan giảm dần
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    @classmethod
    def synthesize_answer(cls, query: str, retrieved_docs: List[Tuple[Dict[str, Any], float]]) -> Tuple[str, List[str], float]:
        """Tổng hợp câu trả lời chuyên môn y tế & viện dẫn quy chuẩn chính xác."""
        if not retrieved_docs:
            answer = (
                "Hệ thống không tìm thấy quy chuẩn kỹ thuật hoặc điều khoản trực tiếp khớp với câu hỏi của bạn. "
                "Vui lòng tham khảo trực tiếp QCVN 8-2:2011/BYT hoặc Quyết định 1246/QĐ-BYT của Bộ Y tế."
            )
            return answer, ["QCVN BYT"], 0.3

        citations = []
        for doc, _ in retrieved_docs:
            cite = f"{doc['standard_code']} - {doc['title']}"
            if cite not in citations:
                citations.append(cite)

        top_doc, top_score = retrieved_docs[0]
        confidence = min(0.99, max(0.65, round(0.6 + (top_score / 20.0), 2)))

        # Tạo câu trả lời cấu trúc rõ ràng
        summary_points = []
        for doc, score in retrieved_docs:
            summary_points.append(f"### 📋 {doc['title']} ({doc['standard_code']})\n{doc['content']}\n")

        answer = (
            f"## KẾT QUẢ TRA CỨU QUY CHUẨN AN TOÀN THỰC PHẨM\n\n"
            f"**Câu hỏi:** *{query}*\n\n"
            f"**Căn cứ pháp lý & Y khoa áp dụng:**\n"
            + "\n".join([f"- **{c}**" for c in citations])
            + "\n\n---\n\n"
            + "\n".join(summary_points)
            + "\n---\n\n"
            f"**Khuyến nghị vận hành DX-OS:**\n"
            f"1. Đối soát ngay thông số đo đạc thực tế với ngưỡng giới hạn quy định nêu trên.\n"
            f"2. Nếu có dấu hiệu vi phạm (vượt nhiệt độ, nhiễm khuẩn, không lưu mẫu), rào chắn Poka-yoke của FoodSafe-DX-OS sẽ tự động khóa chốt quy trình để bảo đảm an toàn tính mạng cho người dùng.\n"
            f"3. Trong trường hợp khẩn cấp, phối hợp ngay với Cơ quan Y tế địa phương theo Luật ATTP 55/2010/QH12."
        )

        return answer, citations, confidence

    @classmethod
    def query(cls, request: schemas.RAGQueryRequest) -> schemas.RAGQueryResponse:
        start_time = time.perf_counter()

        retrieved = cls.search(query=request.query, category=request.category or "ALL", top_k=request.top_k or 3)
        answer, citations, confidence = cls.synthesize_answer(request.query, retrieved)

        chunks = [
            schemas.RAGChunk(
                doc_id=doc["doc_id"],
                title=doc["title"],
                standard_code=doc["standard_code"],
                content=doc["content"],
                relevance_score=score,
            )
            for doc, score in retrieved
        ]

        exec_time = round((time.perf_counter() - start_time) * 1000, 2)

        return schemas.RAGQueryResponse(
            query=request.query,
            category=request.category or "ALL",
            answer=answer,
            confidence_score=confidence,
            citations=citations,
            relevant_chunks=chunks,
            execution_time_ms=exec_time,
            engine_mode="LOCAL_OFFLINE_ZERO_CLOUD",
        )
