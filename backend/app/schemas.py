# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict


# ==========================================
# POKA-YOKE ERROR SCHEMAS
# ==========================================
class PokaYokeViolation(BaseModel):
    """Chi tiết lỗi rào chắn an toàn kỹ thuật Poka-yoke."""
    error_code: str
    message: str
    standard_ref: str
    action_required: str
    blocked_operation: str


# ==========================================
# FACILITY SCHEMAS
# ==========================================
class FacilityBase(BaseModel):
    code: str
    name: str
    facility_type: str = "SCHOOL_CANTEEN"
    address: str
    manager_name: str
    phone: Optional[str] = None
    daily_meal_capacity: int = 500


class FacilityCreate(FacilityBase):
    pass


class FacilityResponse(FacilityBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# SUPPLIER SCHEMAS
# ==========================================
class SupplierBase(BaseModel):
    code: str
    name: str
    tax_code: str
    license_no: Optional[str] = None
    food_safety_cert: Optional[str] = None
    cert_expiry_date: Optional[datetime] = None
    risk_level: str = "LOW"
    address: Optional[str] = None
    is_active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# INGREDIENT BATCH SCHEMAS
# ==========================================
class IngredientBatchBase(BaseModel):
    batch_code: str
    supplier_id: int
    name: str
    category: str
    origin: str
    quantity_kg: float
    harvest_or_slaughter_date: datetime
    expiry_date: datetime
    storage_condition: str = "CHILLED"
    max_safe_temp: float = 4.0
    status: str = "PENDING_INSPECTION"


class IngredientBatchCreate(IngredientBatchBase):
    pass


class IngredientBatchResponse(IngredientBatchBase):
    id: int
    created_at: datetime
    supplier: Optional[SupplierResponse] = None
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# INSPECTION STEP 1 SCHEMAS
# ==========================================
class InspectionStep1Create(BaseModel):
    batch_id: int
    facility_id: int
    delivery_temp: float = Field(..., description="Nhiệt độ đo thực tế khi nhận hàng (°C)")
    packaging_intact: bool = Field(True, description="Bao bì, tem nhãn nguyên vẹn không rách rời")
    sensory_status: str = Field("FRESH", description="Đánh giá cảm quan (FRESH, OFF_SMELL, DISCOLORED, SLIMY)")
    inspector_name: str
    notes: Optional[str] = None


class InspectionStep1Response(BaseModel):
    id: int
    batch_id: int
    facility_id: int
    inspected_at: datetime
    inspector_name: str
    delivery_temp: float
    packaging_intact: bool
    sensory_status: str
    passed: bool
    poka_yoke_triggered: bool
    rejection_reason: Optional[str] = None
    notes: Optional[str] = None
    batch: Optional[IngredientBatchResponse] = None
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# INSPECTION STEP 2 SCHEMAS
# ==========================================
class InspectionStep2Create(BaseModel):
    facility_id: int
    meal_name: str
    batch_ids: List[int]
    cooking_method: str = "BOILING"
    core_temp: float = Field(..., description="Nhiệt độ tâm thực phẩm (°C, tối thiểu 75°C)")
    sensory_check: str = "COOKED_THOROUGHLY"
    cook_name: str


class InspectionStep2Response(BaseModel):
    id: int
    facility_id: int
    meal_name: str
    batch_ids: List[int]
    cooking_method: str
    cooking_started_at: datetime
    cooking_finished_at: Optional[datetime] = None
    core_temp: float
    sensory_check: str
    cook_name: str
    passed: bool
    poka_yoke_triggered: bool
    rejection_reason: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# SAMPLE LOCKER STEP 3 SCHEMAS
# ==========================================
class SampleLockerCreate(BaseModel):
    facility_id: int
    meal_name: str
    batch_ids: List[int]
    sample_code: str
    locker_number: str
    storage_temp: float = Field(2.5, description="Nhiệt độ tủ lưu mẫu (°C, tối đa 4°C)")
    supervisor_name: str


class SampleLockerResponse(BaseModel):
    id: int
    facility_id: int
    sample_code: str
    meal_name: str
    batch_ids: List[int]
    locker_number: str
    sealed_at: datetime
    unlock_eligible_at: datetime
    is_locked: bool
    storage_temp: float
    status: str
    tamper_detected: bool
    supervisor_name: str
    hours_remaining: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)


class SampleLockerUnlockRequest(BaseModel):
    """Yêu cầu mở khóa tủ lưu mẫu 24h kèm cơ chế duyệt Human-in-the-loop."""
    operator_name: str = Field(..., description="Tên cán bộ thực hiện thao tác")
    is_emergency_override: bool = Field(False, description="Kích hoạt phê duyệt khẩn cấp (Human-in-the-loop)")
    override_reason: Optional[str] = Field(None, description="Lý do phê duyệt khẩn cấp (Thanh tra Sở Y tế / Cấp cứu dịch tễ)")
    override_passcode: Optional[str] = Field(None, description="Mã xác thực quyền Trưởng ban (Mặc định: HITL-EMERGENCY-2026)")



# ==========================================
# INCIDENT & TRACEABILITY SCHEMAS
# ==========================================
class IncidentReportCreate(BaseModel):
    facility_id: int
    meal_name: str
    suspected_batches: Optional[List[int]] = None
    symptoms: List[str]
    affected_count: int = 1
    severity: str = "SERIOUS"
    notes: Optional[str] = None


class IncidentReportResponse(BaseModel):
    id: int
    facility_id: int
    reported_at: datetime
    meal_name: str
    suspected_batches: Optional[List[int]] = None
    symptoms: List[str]
    affected_count: int
    severity: str
    status: str
    investigation_log: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class TraceAffectedFacility(BaseModel):
    facility_id: int
    facility_name: str
    facility_address: str
    manager_phone: Optional[str] = None
    meal_name: str
    consumed_batch_code: str
    emergency_action: str


class TraceResultResponse(BaseModel):
    status: str
    incident_id: int
    detected_pathogen_risk: str
    root_cause_batch: str
    supplier_name: str
    supplier_tax_code: str
    affected_facilities_count: int
    affected_facilities: List[TraceAffectedFacility]
    execution_time_ms: float
    immediate_recall_order: str


# ==========================================
# LOCAL RAG & MICROBIOLOGY ENGINE SCHEMAS
# ==========================================
class RAGQueryRequest(BaseModel):
    query: str = Field(..., description="Câu hỏi hoặc từ khóa tra cứu quy chuẩn/vi sinh/pháp lý ATTP")
    category: Optional[str] = Field("ALL", description="Phân loại: ALL, MICROBIOLOGY, LEGAL, PROCEDURE, RECALL")
    top_k: Optional[int] = Field(3, description="Số lượng trích đoạn quy chuẩn đối chiếu cao nhất")


class RAGChunk(BaseModel):
    doc_id: str
    title: str
    standard_code: str
    content: str
    relevance_score: float


class RAGQueryResponse(BaseModel):
    query: str
    category: str
    answer: str
    confidence_score: float
    citations: List[str]
    relevant_chunks: List[RAGChunk]
    execution_time_ms: float
    engine_mode: str = "LOCAL_OFFLINE_ZERO_CLOUD"
