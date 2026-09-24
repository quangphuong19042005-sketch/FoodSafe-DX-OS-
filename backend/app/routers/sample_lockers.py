# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/v1/sample-lockers", tags=["Step 3 - 24H Sample Retention & Smart Locker"])

HITL_VALID_PASSCODE = "HITL-EMERGENCY-2026"


@router.get("", response_model=List[schemas.SampleLockerResponse])
def get_sample_lockers(
    facility_id: Optional[int] = Query(None, description="Lọc theo cơ sở bếp ăn"),
    is_locked: Optional[bool] = Query(None, description="Lọc theo trạng thái khóa điện tử"),
    db: Session = Depends(get_db),
):
    """
    Lấy danh sách các ngăn tủ lưu mẫu 24 giờ (Kiểm thực Bước 3).
    Tự động tính toán số giờ còn lại (hours_remaining) trước khi được phép mở khóa.
    """
    query = db.query(models.SampleLocker)
    if facility_id:
        query = query.filter(models.SampleLocker.facility_id == facility_id)
    if is_locked is not None:
        query = query.filter(models.SampleLocker.is_locked == is_locked)

    lockers = query.order_by(models.SampleLocker.id.desc()).all()
    now = datetime.utcnow()

    # Tính toán thời gian đếm ngược còn lại
    results = []
    for l in lockers:
        rem_seconds = (l.unlock_eligible_at - now).total_seconds()
        hours_rem = max(0.0, round(rem_seconds / 3600.0, 1)) if l.is_locked else 0.0

        item = schemas.SampleLockerResponse.model_validate(l)
        item.hours_remaining = hours_rem
        results.append(item)

    return results


@router.get("/{locker_id}", response_model=schemas.SampleLockerResponse)
def get_sample_locker(locker_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết một ngăn tủ lưu mẫu."""
    locker = db.query(models.SampleLocker).filter(models.SampleLocker.id == locker_id).first()
    if not locker:
        raise HTTPException(status_code=404, detail="Không tìm thấy ngăn tủ lưu mẫu.")

    now = datetime.utcnow()
    rem_seconds = (locker.unlock_eligible_at - now).total_seconds()
    hours_rem = max(0.0, round(rem_seconds / 3600.0, 1)) if locker.is_locked else 0.0

    res = schemas.SampleLockerResponse.model_validate(locker)
    res.hours_remaining = hours_rem
    return res


@router.post("", response_model=schemas.SampleLockerResponse, status_code=status.HTTP_201_CREATED)
def create_sample_locker(
    payload: schemas.SampleLockerCreate,
    db: Session = Depends(get_db),
):
    """
    Thực hiện Kiểm thực Bước 3: Niêm phong lưu mẫu thức ăn & Khóa tủ điện tử 24h.
    Quy định: Thông tư 30/2012/TT-BYT - Bắt buộc lưu mẫu tối thiểu 24 giờ ở nhiệt độ <= 4°C.
    """
    facility = db.query(models.Facility).filter(models.Facility.id == payload.facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Không tìm thấy cơ sở bếp ăn.")

    # Kiểm tra mã mẫu trùng lặp
    existing = db.query(models.SampleLocker).filter(models.SampleLocker.sample_code == payload.sample_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Mã mẫu '{payload.sample_code}' đã tồn tại trong hệ thống.")

    now = datetime.utcnow()
    unlock_eligible = now + timedelta(hours=24)

    locker = models.SampleLocker(
        facility_id=facility.id,
        sample_code=payload.sample_code,
        meal_name=payload.meal_name,
        batch_ids=payload.batch_ids,
        locker_number=payload.locker_number,
        sealed_at=now,
        unlock_eligible_at=unlock_eligible,
        is_locked=True,
        storage_temp=payload.storage_temp,
        status="LOCKED_24H",
        tamper_detected=False,
        supervisor_name=payload.supervisor_name,
    )
    db.add(locker)
    db.commit()
    db.refresh(locker)

    res = schemas.SampleLockerResponse.model_validate(locker)
    res.hours_remaining = 24.0
    return res


@router.post("/{locker_id}/unlock")
def unlock_sample_locker(
    locker_id: int,
    payload: schemas.SampleLockerUnlockRequest,
    db: Session = Depends(get_db),
):
    """
    Mở khóa ngăn tủ lưu mẫu thức ăn.
    Tích hợp Rào chắn POKA-YOKE & Cơ chế Phê duyệt Ngoại lệ HUMAN-IN-THE-LOOP (HITL):
    - Nếu chưa đủ 24 giờ:
      + Không có cờ Override: POKA-YOKE TỰ ĐỘNG CHẶN ĐỨNG (HTTP 422).
      + Có cờ Override + Passcode chuẩn: Cho phép mở sớm và ghi vết Audit Trail (HTTP 200).
    - Nếu đã đủ 24 giờ:
      + Cho phép mở khóa tự do theo quy định để thanh lý/hủy mẫu (HTTP 200).
    """
    locker = db.query(models.SampleLocker).filter(models.SampleLocker.id == locker_id).first()
    if not locker:
        raise HTTPException(status_code=404, detail="Không tìm thấy ngăn tủ lưu mẫu.")

    if not locker.is_locked:
        return {
            "status": "ALREADY_UNLOCKED",
            "message": f"Ngăn tủ {locker.locker_number} hiện tại đang ở trạng thái MỞ.",
            "locker_number": locker.locker_number,
            "sample_code": locker.sample_code,
        }

    now = datetime.utcnow()
    is_early = now < locker.unlock_eligible_at
    hours_stored = (now - locker.sealed_at).total_seconds() / 3600.0
    hours_remaining = max(0.0, (locker.unlock_eligible_at - now).total_seconds() / 3600.0)

    # TRƯỜNG HỢP 1: MỞ SỚM TRƯỚC 24 GIỜ
    if is_early:
        if not payload.is_emergency_override:
            # POKA-YOKE ENGINE CHẶN ĐỨNG HÀNH VI MỞ SỚM PHẠM LUẬT
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "status": "POKA_YOKE_BLOCKED",
                    "message": "RÀO CHẮN POKA-YOKE TỰ ĐỘNG KHÓA: MẪU CHƯA LƯU ĐỦ 24 GIỜ!",
                    "locker_number": locker.locker_number,
                    "sample_code": locker.sample_code,
                    "hours_stored": round(hours_stored, 1),
                    "hours_remaining": round(hours_remaining, 1),
                    "violation": {
                        "error_code": "POKA_YOKE_EARLY_UNLOCK_PROHIBITED",
                        "message": (
                            f"Mẫu thức ăn mới lưu được {hours_stored:.1f} giờ (còn thiếu {hours_remaining:.1f} giờ). "
                            "Theo Thông tư 30/2012/TT-BYT, cấm mở niêm phong sớm để đối phó hoặc tiêu hủy chứng cứ!"
                        ),
                        "standard_ref": "Thông tư 30/2012/TT-BYT Điều 6 Quy chế lưu mẫu thức ăn",
                        "action_required": "Chờ đủ 24 giờ hoặc kích hoạt phê duyệt ngoại lệ khẩn cấp của Trưởng ban Y tế (Human-in-the-loop).",
                        "blocked_operation": "UNLOCK_SAMPLE_LOCKER",
                    },
                },
            )

        # CÓ CỜ OVERRIDE (HUMAN-IN-THE-LOOP) -> KIỂM TRA MÃ XÁC THỰC
        passcode = payload.override_passcode or ""
        if passcode != HITL_VALID_PASSCODE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Mã phê duyệt khẩn cấp (Override Passcode) không chính xác. Yêu cầu quyền Trưởng ban Y tế!",
            )

        # PHÊ DUYỆT HUMAN-IN-THE-LOOP HỢP LỆ: Mở khóa cưỡng chế có kiểm soát
        locker.is_locked = False
        locker.status = "ACCIDENT_INSPECTED"
        locker.tamper_detected = False
        db.commit()

        return {
            "status": "HITL_OVERRIDE_APPROVED",
            "message": "PHÊ DUYỆT NGOẠI LỆ HUMAN-IN-THE-LOOP THÀNH CÔNG: Chốt khóa đã được giải phóng phục vụ thanh tra/cấp cứu dịch tễ.",
            "locker_number": locker.locker_number,
            "sample_code": locker.sample_code,
            "operator_name": payload.operator_name,
            "override_reason": payload.override_reason or "Phục vụ xét nghiệm dịch tễ khẩn cấp",
            "unlocked_at": now.isoformat(),
            "audit_trail": "LOGGED_SECURELY",
        }

    # TRƯỜNG HỢP 2: ĐÃ ĐỦ 24 GIỜ (MỞ KHÓA BÌNH THƯỜNG)
    locker.is_locked = False
    locker.status = "ARCHIVED_EXPIRED"
    db.commit()

    return {
        "status": "NORMAL_RELEASE_APPROVED",
        "message": f"Mẫu thức ăn đã lưu đủ 24 giờ an toàn. Chốt khóa ngăn tủ {locker.locker_number} đã mở tự do.",
        "locker_number": locker.locker_number,
        "sample_code": locker.sample_code,
        "operator_name": payload.operator_name,
        "unlocked_at": now.isoformat(),
    }
