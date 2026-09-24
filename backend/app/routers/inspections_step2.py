# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..core.poka_yoke import PokaYokeEngine

router = APIRouter(prefix="/api/v1/inspections/step2", tags=["Step 2 - Cooking Inspection"])


@router.get("", response_model=List[schemas.InspectionStep2Response])
def get_step2_inspections(
    facility_id: Optional[int] = Query(None, description="Lọc theo cơ sở bếp ăn"),
    passed: Optional[bool] = Query(None, description="Lọc theo kết quả kiểm thực chế biến"),
    db: Session = Depends(get_db),
):
    """Lấy danh sách nhật ký kiểm thực Bước 2 (Trong quá trình chế biến)."""
    query = db.query(models.InspectionStep2)
    if facility_id:
        query = query.filter(models.InspectionStep2.facility_id == facility_id)
    if passed is not None:
        query = query.filter(models.InspectionStep2.passed == passed)
    return query.order_by(models.InspectionStep2.id.desc()).all()


@router.get("/{inspection_id}", response_model=schemas.InspectionStep2Response)
def get_step2_inspection(inspection_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết một phiếu kiểm thực Bước 2."""
    record = db.query(models.InspectionStep2).filter(models.InspectionStep2.id == inspection_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu kiểm thực Bước 2.")
    return record


@router.post("", status_code=status.HTTP_201_CREATED)
def create_step2_inspection(
    payload: schemas.InspectionStep2Create,
    db: Session = Depends(get_db),
):
    """
    Thực hiện Kiểm thực Bước 2: Kiểm soát quá trình chế biến & Đo nhiệt độ tâm thức ăn.
    Tự động kích hoạt rào chắn an toàn POKA-YOKE:
    - Nếu sử dụng lô nguyên liệu bị TỪ CHỐI ở Bước 1 -> KHÓA NGAY LẬP TỨC!
    - Nếu nhiệt độ tâm thức ăn < 75.0°C (chưa chín thấu) -> KHÓA KHÔNG CHO XUẤT ĂN!
    - Nếu cảm quan chưa chín kỹ -> KHÓA VÀ YÊU CẦU NẤU LẠI!
    """
    # 1. Kiểm tra tồn tại cơ sở bếp ăn
    facility = db.query(models.Facility).filter(models.Facility.id == payload.facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy cơ sở bếp ăn với ID {payload.facility_id}")

    # 2. Truy xuất các lô nguyên liệu cấu thành món ăn
    batches = db.query(models.IngredientBatch).filter(models.IngredientBatch.id.in_(payload.batch_ids)).all()
    if len(batches) != len(payload.batch_ids):
        raise HTTPException(
            status_code=400,
            detail="Một hoặc nhiều ID lô nguyên liệu không tồn tại trong hệ thống.",
        )

    # 3. Kích hoạt rào chắn an toàn POKA-YOKE BƯỚC 2
    is_safe, violation = PokaYokeEngine.validate_step2(batches=batches, data=payload)

    if not is_safe and violation:
        # POKA-YOKE KÍCH HOẠT: Tạo bản ghi từ chối & chặn xuất ăn
        inspection = models.InspectionStep2(
            facility_id=facility.id,
            meal_name=payload.meal_name,
            batch_ids=payload.batch_ids,
            cooking_method=payload.cooking_method,
            cooking_started_at=datetime.utcnow(),
            cooking_finished_at=datetime.utcnow(),
            core_temp=payload.core_temp,
            sensory_check=payload.sensory_check,
            cook_name=payload.cook_name,
            passed=False,
            poka_yoke_triggered=True,
            rejection_reason=f"[{violation.error_code}] {violation.message}",
        )
        db.add(inspection)
        db.commit()
        db.refresh(inspection)

        # Trả về HTTP 422 Unprocessable Entity kèm chi tiết Poka-yoke
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "POKA_YOKE_BLOCKED",
                "message": "RÀO CHẮN POKA-YOKE BƯỚC 2 ĐÃ KHÓA: MÓN ĂN KHÔNG ĐỦ TIÊU CHUẨN XUẤT BÁN / CHIA PHẦN!",
                "inspection_id": inspection.id,
                "meal_name": payload.meal_name,
                "facility_name": facility.name,
                "violation": violation.model_dump(),
            },
        )

    # 4. POKA-YOKE THÔNG QUA: Món ăn nấu chín đạt chuẩn
    inspection = models.InspectionStep2(
        facility_id=facility.id,
        meal_name=payload.meal_name,
        batch_ids=payload.batch_ids,
        cooking_method=payload.cooking_method,
        cooking_started_at=datetime.utcnow(),
        cooking_finished_at=datetime.utcnow(),
        core_temp=payload.core_temp,
        sensory_check=payload.sensory_check,
        cook_name=payload.cook_name,
        passed=True,
        poka_yoke_triggered=False,
        rejection_reason=None,
    )
    db.add(inspection)
    db.commit()
    db.refresh(inspection)

    return {
        "status": "APPROVED",
        "message": "Kiểm thực Bước 2 ĐẠT CHUẨN. Món ăn đã chín thấu, đủ điều kiện chuyển sang chia phần & Lưu mẫu 24h.",
        "inspection_id": inspection.id,
        "meal_name": payload.meal_name,
        "facility_name": facility.name,
        "core_temp": inspection.core_temp,
        "passed": True,
    }
