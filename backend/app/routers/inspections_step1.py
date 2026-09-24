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

router = APIRouter(prefix="/api/v1/inspections/step1", tags=["Step 1 - Receiving Inspection"])


@router.get("", response_model=List[schemas.InspectionStep1Response])
def get_step1_inspections(
    facility_id: Optional[int] = Query(None, description="Lọc theo cơ sở bếp ăn"),
    passed: Optional[bool] = Query(None, description="Lọc theo kết quả kiểm thực (đạt/không đạt)"),
    db: Session = Depends(get_db),
):
    """Lấy danh sách nhật ký kiểm thực Bước 1 (Giao nhận nguyên liệu)."""
    query = db.query(models.InspectionStep1)
    if facility_id:
        query = query.filter(models.InspectionStep1.facility_id == facility_id)
    if passed is not None:
        query = query.filter(models.InspectionStep1.passed == passed)
    return query.order_by(models.InspectionStep1.id.desc()).all()


@router.get("/{inspection_id}", response_model=schemas.InspectionStep1Response)
def get_step1_inspection(inspection_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết một phiếu kiểm thực Bước 1."""
    record = db.query(models.InspectionStep1).filter(models.InspectionStep1.id == inspection_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu kiểm thực Bước 1.")
    return record


@router.post("", status_code=status.HTTP_201_CREATED)
def create_step1_inspection(
    payload: schemas.InspectionStep1Create,
    db: Session = Depends(get_db),
):
    """
    Thực hiện Kiểm thực Bước 1: Tiếp nhận & Kiểm tra điều kiện bảo quản nguyên liệu.
    Tự động kích hoạt rào chắn an toàn POKA-YOKE:
    - Nếu vi phạm nhiệt độ chuỗi lạnh, tem rách, mùi lạ hoặc nhà cung cấp bị cấm:
      Hệ thống từ chối cấp quyền nhập kho và trả về mã lỗi HTTP 422 kèm biên bản Poka-yoke!
    """
    # 1. Kiểm tra tồn tại của Lô hàng và Cơ sở bếp ăn
    batch = db.query(models.IngredientBatch).filter(models.IngredientBatch.id == payload.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy lô nguyên liệu với ID {payload.batch_id}")

    facility = db.query(models.Facility).filter(models.Facility.id == payload.facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy cơ sở bếp ăn với ID {payload.facility_id}")

    # 2. Chạy rào chắn an toàn POKA-YOKE ENGINE
    is_safe, violation = PokaYokeEngine.validate_step1(batch=batch, data=payload)

    if not is_safe and violation:
        # POKA-YOKE KÍCH HOẠT: Tạo bản ghi từ chối & khóa lô hàng
        inspection = models.InspectionStep1(
            batch_id=batch.id,
            facility_id=facility.id,
            inspected_at=datetime.utcnow(),
            inspector_name=payload.inspector_name,
            delivery_temp=payload.delivery_temp,
            packaging_intact=payload.packaging_intact,
            sensory_status=payload.sensory_status,
            passed=False,
            poka_yoke_triggered=True,
            rejection_reason=f"[{violation.error_code}] {violation.message}",
            notes=payload.notes,
        )
        batch.status = "REJECTED"
        db.add(inspection)
        db.commit()
        db.refresh(inspection)

        # Trả về HTTP 422 Unprocessable Entity kèm payload vi phạm Poka-yoke chi tiết
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "POKA_YOKE_BLOCKED",
                "message": "RÀO CHẮN POKA-YOKE TỰ ĐỘNG KHÓA GIAO DỊCH NHẬP KHO!",
                "inspection_id": inspection.id,
                "batch_code": batch.batch_code,
                "facility_name": facility.name,
                "violation": violation.model_dump(),
            },
        )

    # 3. POKA-YOKE THÔNG QUA: Tiếp nhận thành công
    inspection = models.InspectionStep1(
        batch_id=batch.id,
        facility_id=facility.id,
        inspected_at=datetime.utcnow(),
        inspector_name=payload.inspector_name,
        delivery_temp=payload.delivery_temp,
        packaging_intact=payload.packaging_intact,
        sensory_status=payload.sensory_status,
        passed=True,
        poka_yoke_triggered=False,
        rejection_reason=None,
        notes=payload.notes,
    )
    batch.status = "APPROVED"
    db.add(inspection)
    db.commit()
    db.refresh(inspection)

    return {
        "status": "APPROVED",
        "message": "Kiểm thực Bước 1 ĐẠT CHUẨN. Lô hàng đủ điều kiện chuyển sang khu vực chế biến.",
        "inspection_id": inspection.id,
        "batch_code": batch.batch_code,
        "facility_name": facility.name,
        "delivery_temp": inspection.delivery_temp,
        "sensory_status": inspection.sensory_status,
        "passed": True,
    }
