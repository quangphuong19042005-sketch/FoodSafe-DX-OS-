# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/v1/batches", tags=["Ingredient Batches"])


@router.get("", response_model=List[schemas.IngredientBatchResponse])
def get_batches(
    status: Optional[str] = Query(None, description="Lọc theo trạng thái lô hàng"),
    db: Session = Depends(get_db),
):
    """Lấy danh sách các lô nguyên liệu thực phẩm nhập kho."""
    query = db.query(models.IngredientBatch)
    if status:
        query = query.filter(models.IngredientBatch.status == status)
    return query.order_by(models.IngredientBatch.id.desc()).all()


@router.get("/{batch_id}", response_model=schemas.IngredientBatchResponse)
def get_batch(batch_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết một lô nguyên liệu."""
    batch = db.query(models.IngredientBatch).filter(models.IngredientBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Không tìm thấy lô nguyên liệu.")
    return batch
