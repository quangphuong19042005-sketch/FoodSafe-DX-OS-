# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..core.graph_tracer import GraphTraceEngine

router = APIRouter(prefix="/api/v1/incidents", tags=["Intelligence Space - Incident Rapid Tracer"])


@router.get("", response_model=List[schemas.IncidentReportResponse])
def get_incidents(
    facility_id: Optional[int] = Query(None, description="Lọc theo cơ sở bếp ăn"),
    status: Optional[str] = Query(None, description="Lọc theo trạng thái sự cố"),
    db: Session = Depends(get_db),
):
    """Lấy danh sách các sự cố an toàn thực phẩm / nghi ngờ ngộ độc."""
    query = db.query(models.IncidentReport)
    if facility_id:
        query = query.filter(models.IncidentReport.facility_id == facility_id)
    if status:
        query = query.filter(models.IncidentReport.status == status)
    return query.order_by(models.IncidentReport.id.desc()).all()


@router.get("/{incident_id}", response_model=schemas.IncidentReportResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết một báo cáo sự cố an toàn thực phẩm."""
    incident = db.query(models.IncidentReport).filter(models.IncidentReport.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Không tìm thấy báo cáo sự cố.")
    return incident


@router.post("", response_model=schemas.IncidentReportResponse, status_code=status.HTTP_201_CREATED)
def create_incident(
    payload: schemas.IncidentReportCreate,
    db: Session = Depends(get_db),
):
    """Tạo mới một báo cáo sự cố ngộ độc thực phẩm."""
    facility = db.query(models.Facility).filter(models.Facility.id == payload.facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Không tìm thấy cơ sở bếp ăn.")

    incident = models.IncidentReport(
        facility_id=facility.id,
        reported_at=datetime.utcnow(),
        meal_name=payload.meal_name,
        suspected_batches=payload.suspected_batches,
        symptoms=payload.symptoms,
        affected_count=payload.affected_count,
        severity=payload.severity,
        status="INVESTIGATING",
        investigation_log=f"Khởi tạo sự cố lúc {datetime.utcnow().strftime('%H:%M:%S %d/%m/%Y')}. Ghi nhận {payload.affected_count} ca có triệu chứng {', '.join(payload.symptoms)}.",
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@router.post("/{incident_id}/trace")
def trigger_rapid_graph_trace(
    incident_id: int,
    db: Session = Depends(get_db),
):
    """
    KÍCH HOẠT THUẬT TOÁN TRUY VẾT ĐỒ THỊ THẦN TỐC (DƯỚI 3 GIÂY).
    - Quét ngược: Tìm lô nguyên liệu độc hại và nhà cung ứng gốc.
    - Quét xuôi: Phát hiện tất cả các trường học / bếp ăn khác đang chia sẻ chung lô hàng đó.
    - Chẩn đoán mầm bệnh (Salmonella, E. coli, Histamine...) và phát lệnh thu hồi khẩn cấp.
    """
    result = GraphTraceEngine.trace_incident(db=db, incident_id=incident_id)
    if result.get("status") == "NOT_FOUND":
        raise HTTPException(status_code=404, detail=result.get("message"))
    return result
