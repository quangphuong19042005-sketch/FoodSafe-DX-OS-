# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

from datetime import datetime
from typing import Tuple, Optional
from .. import models
from ..schemas import PokaYokeViolation, InspectionStep1Create, InspectionStep2Create


class PokaYokeEngine:
    """
    Rào chắn an toàn kỹ thuật (Poka-yoke Engine) cho hệ thống FoodSafe-DX-OS.
    Thiết kế theo nguyên lý Fail-Safe: Mặc định từ chối (Deny by Default)
    nếu bất kỳ chỉ số an toàn thực phẩm nào vi phạm ngưỡng cho phép của Bộ Y tế.
    """

    @staticmethod
    def validate_step1(
        batch: models.IngredientBatch,
        data: InspectionStep1Create,
    ) -> Tuple[bool, Optional[PokaYokeViolation]]:
        """
        Kiểm tra rào chắn Poka-yoke Bước 1: Giao nhận & Nhập kho nguyên liệu.
        Quy chuẩn đối chiếu: Thông tư 30/2012/TT-BYT & QCVN 12-1:2011/BYT.
        """
        now = datetime.utcnow()

        # 1. Rào chắn Nhà cung ứng bị cấm (Blacklisted Supplier)
        if batch.supplier and batch.supplier.risk_level == "BLACKLISTED":
            return False, PokaYokeViolation(
                error_code="POKA_YOKE_BLACKLISTED_SUPPLIER",
                message=f"Nhà cung ứng '{batch.supplier.name}' đang thuộc danh sách đen bị đình chỉ. Khóa tiếp nhận toàn bộ lô hàng!",
                standard_ref="Nghị định 115/2018/NĐ-CP về xử phạt vi phạm ATVSTP",
                action_required="Từ chối nhập kho và lập biên bản trả hàng ngay lập tức.",
                blocked_operation="IMPORT_TO_KITCHEN",
            )

        # 2. Rào chắn Hạn sử dụng (Expiry Date Guard)
        if batch.expiry_date and batch.expiry_date < now:
            return False, PokaYokeViolation(
                error_code="POKA_YOKE_EXPIRED_BATCH",
                message=f"Lô hàng '{batch.name}' ({batch.batch_code}) đã hết hạn sử dụng vào ngày {batch.expiry_date.strftime('%d/%m/%Y')}.",
                standard_ref="Điều 5 Luật An toàn thực phẩm số 55/2010/QH12",
                action_required="Tiêu hủy hoặc lập biên bản hoàn trả nhà cung cấp.",
                blocked_operation="IMPORT_TO_KITCHEN",
            )

        # 3. Rào chắn Nhiệt độ Giao nhận (Cold-chain Temperature Guard) - ĐIỂM CỐT LÕI
        max_safe = batch.max_safe_temp
        if data.delivery_temp > max_safe:
            delta = data.delivery_temp - max_safe
            return False, PokaYokeViolation(
                error_code="POKA_YOKE_TEMP_VIOLATION",
                message=(
                    f"Nhiệt độ đo thực tế {data.delivery_temp:.1f}°C vượt ngưỡng an toàn {max_safe:.1f}°C "
                    f"(vượt +{delta:.1f}°C). Vi phạm đứt gãy chuỗi lạnh bảo quản thực phẩm!"
                ),
                standard_ref="QCVN 12-1:2011/BYT Quy chuẩn kỹ thuật quốc gia về ATVSTP",
                action_required="Khóa mã lô hàng, cấm đưa vào khu vực sơ chế/chế biến.",
                blocked_operation="IMPORT_TO_KITCHEN",
            )

        # 4. Rào chắn Tem nhãn & Bao bì (Packaging Integrity Guard)
        if not data.packaging_intact:
            return False, PokaYokeViolation(
                error_code="POKA_YOKE_PACKAGING_DAMAGED",
                message="Bao bì bị rách vỡ hoặc tem niêm phong truy xuất nguồn gốc bị rách rời, không bảo đảm vô trùng.",
                standard_ref="Thông tư 30/2012/TT-BYT Điều 4 Mục a",
                action_required="Yêu cầu bên giao hàng cung cấp lại lô nguyên vẹn hoặc từ chối.",
                blocked_operation="IMPORT_TO_KITCHEN",
            )

        # 5. Rào chắn Đánh giá Cảm quan (Sensory Evaluation Guard)
        if data.sensory_status in ["OFF_SMELL", "SLIMY", "DISCOLORED"]:
            sensory_map = {
                "OFF_SMELL": "Thực phẩm bốc mùi ôi thiu / mùi lạ",
                "SLIMY": "Bề mặt nhớt dính, rã đông nhũn nát",
                "DISCOLORED": "Biến đổi màu sắc bất thường (thâm tím, tái nhợt)",
            }
            violation_desc = sensory_map.get(data.sensory_status, data.sensory_status)
            return False, PokaYokeViolation(
                error_code="POKA_YOKE_SENSORY_FAILED",
                message=f"Đánh giá cảm quan không đạt: {violation_desc}. Có dấu hiệu phân hủy sinh học.",
                standard_ref="Thông tư 30/2012/TT-BYT Kiểm thực 3 bước",
                action_required="Niêm phong lô hàng và không cho phép chuyển sang Bước 2 (Chế biến).",
                blocked_operation="COOKING_STEP_2",
            )

        # Tất cả điều kiện Poka-yoke đều thỏa mãn
        return True, None

    @staticmethod
    def validate_step2(
        data: InspectionStep2Create,
    ) -> Tuple[bool, Optional[PokaYokeViolation]]:
        """
        Kiểm tra rào chắn Poka-yoke Bước 2: Trong quá trình chế biến.
        Quy chuẩn đối chiếu: Nhiệt độ tâm nấu chín thức ăn tối thiểu 75°C.
        """
        # Rào chắn Nhiệt độ tâm thức ăn (Core Cooking Temperature Guard)
        if data.core_temp < 75.0:
            return False, PokaYokeViolation(
                error_code="POKA_YOKE_UNDERCOOKED_TEMP",
                message=(
                    f"Nhiệt độ tâm thức ăn đo được là {data.core_temp:.1f}°C (thấp hơn ngưỡng an toàn 75.0°C). "
                    f"Không đủ tiêu diệt vi khuẩn đường ruột (Salmonella, E. coli, Clostridium)!"
                ),
                standard_ref="QCVN 8-2:2011/BYT & Hướng dẫn kỹ thuật WHO Food Safety",
                action_required="Tiếp tục gia nhiệt cho đến khi nhiệt độ tâm đạt tối thiểu 75°C mới được xuất chia phần.",
                blocked_operation="MEAL_DISTRIBUTION",
            )

        if data.sensory_check != "COOKED_THOROUGHLY":
            return False, PokaYokeViolation(
                error_code="POKA_YOKE_SENSORY_UNDERCOOKED",
                message="Thức ăn chưa chín kỹ đều ở các phần (chưa đạt cảm quan COOKED_THOROUGHLY).",
                standard_ref="Thông tư 30/2012/TT-BYT Bước 2 Chế biến",
                action_required="Nấu lại thức ăn bảo đảm chín thấu hoàn toàn.",
                blocked_operation="MEAL_DISTRIBUTION",
            )

        return True, None
