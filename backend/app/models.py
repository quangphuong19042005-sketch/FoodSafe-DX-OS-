# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship
from .database import Base


class Facility(Base):
    """Bếp ăn bán trú trường học hoặc bếp ăn tập thể khu công nghiệp."""

    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    facility_type = Column(String(50), default="SCHOOL_CANTEEN")  # SCHOOL_CANTEEN, FACTORY_CANTEEN, HOSPITAL
    address = Column(String(255), nullable=False)
    manager_name = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=True)
    daily_meal_capacity = Column(Integer, default=500)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    inspections_step1 = relationship("InspectionStep1", back_populates="facility")
    inspections_step2 = relationship("InspectionStep2", back_populates="facility")
    sample_lockers = relationship("SampleLocker", back_populates="facility")
    incidents = relationship("IncidentReport", back_populates="facility")


class Supplier(Base):
    """Nhà cung ứng thực phẩm & nguyên liệu đầu vào."""

    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    tax_code = Column(String(50), nullable=False)
    license_no = Column(String(100), nullable=True)
    food_safety_cert = Column(String(100), nullable=True)
    cert_expiry_date = Column(DateTime, nullable=True)
    risk_level = Column(String(50), default="LOW")  # LOW, MEDIUM, HIGH, BLACKLISTED
    address = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    batches = relationship("IngredientBatch", back_populates="supplier")


class IngredientBatch(Base):
    """Lô nguyên liệu / thực phẩm nhập kho có mã truy xuất nguồn gốc."""

    __tablename__ = "ingredient_batches"

    id = Column(Integer, primary_key=True, index=True)
    batch_code = Column(String(100), unique=True, index=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # MEAT, POULTRY, SEAFOOD, VEGETABLE, DRY, DAIRY
    origin = Column(String(255), nullable=False)  # Địa phương / Nông trại nguồn
    quantity_kg = Column(Float, nullable=False)
    harvest_or_slaughter_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    storage_condition = Column(String(50), default="CHILLED")  # FROZEN, CHILLED, DRY
    max_safe_temp = Column(Float, default=4.0)  # Ngưỡng nhiệt độ an toàn Poka-yoke (<= 4°C cho đồ tươi sống)
    status = Column(String(50), default="PENDING_INSPECTION")  # PENDING_INSPECTION, APPROVED, REJECTED, CONSUMED
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    supplier = relationship("Supplier", back_populates="batches")
    inspections_step1 = relationship("InspectionStep1", back_populates="batch")

    __table_args__ = (
        Index("idx_batch_code_supplier", "batch_code", "supplier_id"),
    )


class InspectionStep1(Base):
    """Quy trình Kiểm thực Bước 1: Kiểm tra trước khi nhập kho / tiếp nhận."""

    __tablename__ = "inspections_step1"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("ingredient_batches.id"), nullable=False)
    facility_id = Column(Integer, ForeignKey("facilities.id"), nullable=False)
    inspected_at = Column(DateTime, default=datetime.utcnow)
    inspector_name = Column(String(100), nullable=False)
    delivery_temp = Column(Float, nullable=False)  # Đo nhiệt độ thực tế bằng nhiệt kế điện tử
    packaging_intact = Column(Boolean, default=True)  # Tem nhãn, bao bì còn nguyên vẹn
    sensory_status = Column(String(50), default="FRESH")  # FRESH, OFF_SMELL, DISCOLORED, SLIMY
    passed = Column(Boolean, default=False)
    poka_yoke_triggered = Column(Boolean, default=False)  # Hệ thống tự động khóa vi phạm
    rejection_reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    batch = relationship("IngredientBatch", back_populates="inspections_step1")
    facility = relationship("Facility", back_populates="inspections_step1")


class InspectionStep2(Base):
    """Quy trình Kiểm thực Bước 2: Kiểm tra trong quá trình chế biến."""

    __tablename__ = "inspections_step2"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id"), nullable=False)
    meal_name = Column(String(255), nullable=False)
    batch_ids = Column(JSON, nullable=False)  # Danh sách ID các lô nguyên liệu cấu thành món ăn
    cooking_method = Column(String(100), nullable=False)  # BOILING, FRYING, STEAMING, BRAISING
    cooking_started_at = Column(DateTime, default=datetime.utcnow)
    cooking_finished_at = Column(DateTime, nullable=True)
    core_temp = Column(Float, nullable=False)  # Nhiệt độ tâm thức ăn khi nấu chín (Poka-yoke: >= 75°C)
    sensory_check = Column(String(50), default="COOKED_THOROUGHLY")  # COOKED_THOROUGHLY, UNDERCOOKED
    cook_name = Column(String(100), nullable=False)
    passed = Column(Boolean, default=False)
    poka_yoke_triggered = Column(Boolean, default=False)
    rejection_reason = Column(Text, nullable=True)

    # Relationships
    facility = relationship("Facility", back_populates="inspections_step2")


class SampleLocker(Base):
    """Quy trình Kiểm thực Bước 3: Lưu mẫu thức ăn 24 giờ & Khóa tủ thông minh."""

    __tablename__ = "sample_lockers"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id"), nullable=False)
    sample_code = Column(String(100), unique=True, index=True, nullable=False)
    meal_name = Column(String(255), nullable=False)
    batch_ids = Column(JSON, nullable=False)
    locker_number = Column(String(50), nullable=False)  # Ngăn tủ số (Locker-01, Locker-02...)
    sealed_at = Column(DateTime, default=datetime.utcnow)
    unlock_eligible_at = Column(DateTime, nullable=False)  # sealed_at + 24 giờ
    is_locked = Column(Boolean, default=True)  # Trạng thái chốt khóa điện tử IoT
    storage_temp = Column(Float, default=2.5)  # Nhiệt độ tủ bảo quản mẫu (<= 4°C)
    status = Column(String(50), default="LOCKED_24H")  # LOCKED_24H, ARCHIVED_EXPIRED, ACCIDENT_INSPECTED
    tamper_detected = Column(Boolean, default=False)  # Phát hiện mở sớm trái phép
    supervisor_name = Column(String(100), nullable=False)

    # Relationships
    facility = relationship("Facility", back_populates="sample_lockers")


class IncidentReport(Base):
    """Báo cáo sự cố ngộ độc thực phẩm phục vụ kích hoạt AI truy vết thần tốc."""

    __tablename__ = "incident_reports"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id"), nullable=False)
    reported_at = Column(DateTime, default=datetime.utcnow)
    meal_name = Column(String(255), nullable=False)
    suspected_batches = Column(JSON, nullable=True)  # Danh sách lô nghi vấn
    symptoms = Column(JSON, nullable=False)  # ["Nôn mửa", "Sốt cao", "Tiêu chảy cấp", "Co giật"]
    affected_count = Column(Integer, default=1)
    severity = Column(String(50), default="SERIOUS")  # MILD, SERIOUS, CRITICAL
    status = Column(String(50), default="INVESTIGATING")  # INVESTIGATING, CONTAINED, RESOLVED
    investigation_log = Column(Text, nullable=True)

    # Relationships
    facility = relationship("Facility", back_populates="incidents")
