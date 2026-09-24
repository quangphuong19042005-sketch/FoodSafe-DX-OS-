# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/v1/facilities", tags=["Facilities"])


@router.get("", response_model=List[schemas.FacilityResponse])
def get_facilities(db: Session = Depends(get_db)):
    """Lấy danh sách các cơ sở bếp ăn bán trú & doanh nghiệp."""
    return db.query(models.Facility).order_by(models.Facility.id.asc()).all()


@router.get("/{facility_id}", response_model=schemas.FacilityResponse)
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết một cơ sở bếp ăn."""
    facility = db.query(models.Facility).filter(models.Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Không tìm thấy cơ sở bếp ăn.")
    return facility
