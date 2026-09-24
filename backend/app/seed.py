# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models

logger = logging.getLogger("foodsafe.seed")


def seed_initial_data(db: Session, force: bool = False):
    """
    Nạp bộ dữ liệu thực tế (Realistic Seed Data) vào cơ sở dữ liệu.
    Dữ liệu được bóc tách từ các sự kiện an toàn thực phẩm thực tế tháng 09/2026:
    - Vụ 254 ca ngộ độc Salmonella tại Gia Lai (07/09/2026)
    - Vụ 180 công nhân dệt may Scavi Huế nhập viện tại KCN Phong Điền (12/09/2026)
    - Vụ phát hiện tôm ươn, gà bốc mùi tại trường Tiểu học Lê Trọng Tấn (11/09/2026)
    """
    existing_facilities = db.query(models.Facility).count()
    if existing_facilities > 0 and not force:
        logger.info(f"Database already contains {existing_facilities} facilities. Skipping seed.")
        return {"status": "skipped", "message": "Database already seeded."}

    if force:
        logger.warning("Force seeding: Clearing existing transaction data...")
        db.query(models.IncidentReport).delete()
        db.query(models.SampleLocker).delete()
        db.query(models.InspectionStep2).delete()
        db.query(models.InspectionStep1).delete()
        db.query(models.IngredientBatch).delete()
        db.query(models.Supplier).delete()
        db.query(models.Facility).delete()
        db.commit()

    logger.info("Starting realistic data ingestion...")

    now = datetime(2026, 9, 24, 8, 0, 0)

    # ==========================================
    # 1. FACILITIES (BẾP ĂN BÁN TRÚ & DOANH NGHIỆP)
    # ==========================================
    fac_le_trong_tan = models.Facility(
        code="FAC-TH-LTRONGTAN",
        name="Trường Tiểu học Lê Trọng Tấn (Hà Đông, Hà Nội)",
        facility_type="SCHOOL_CANTEEN",
        address="Khu Đô Thị Geleximco, Dương Nội, Hà Đông, Hà Nội",
        manager_name="Nguyễn Thị Mai (Hiệu trưởng)",
        phone="024-3388-9922",
        daily_meal_capacity=1400,
        created_at=now - timedelta(days=30),
    )
    fac_scavi_hue = models.Facility(
        code="FAC-KCN-SCAVIHUE",
        name="Bếp ăn KCN Phong Điền - Cty May Scavi Huế",
        facility_type="FACTORY_CANTEEN",
        address="Khu Công nghiệp Phong Điền, Huyện Phong Điền, Thừa Thiên Huế",
        manager_name="Trần Văn Hưng (Trưởng ban Hậu cần)",
        phone="0234-377-1122",
        daily_meal_capacity=2200,
        created_at=now - timedelta(days=60),
    )
    fac_an_khe = models.Facility(
        code="FAC-THCS-ANKHE",
        name="Trường THCS Quang Trung (Thị xã An Khê, Gia Lai)",
        facility_type="SCHOOL_CANTEEN",
        address="Phường An Bình, Thị xã An Khê, Tỉnh Gia Lai",
        manager_name="Lê Đình Phúc (Bếp trưởng)",
        phone="0269-383-4455",
        daily_meal_capacity=850,
        created_at=now - timedelta(days=45),
    )
    fac_chu_van_an = models.Facility(
        code="FAC-TH-CHUVANAN",
        name="Trường Tiểu học Chu Văn An (Tây Hồ, Hà Nội)",
        facility_type="SCHOOL_CANTEEN",
        address="Số 260 Thụy Khuê, Tây Hồ, Hà Nội",
        manager_name="Phạm Thanh Thảo (Quản trị Bếp ăn)",
        phone="024-3829-1144",
        daily_meal_capacity=1600,
        created_at=now - timedelta(days=90),
    )

    db.add_all([fac_le_trong_tan, fac_scavi_hue, fac_an_khe, fac_chu_van_an])
    db.flush()

    # ==========================================
    # 2. SUPPLIERS (NHÀ CUNG CẤP NGUYÊN LIỆU)
    # ==========================================
    sup_cp_food = models.Supplier(
        code="SUP-CP-FOOD-HN",
        name="Công ty Cổ phần Thực phẩm Sạch CP Hà Nội",
        tax_code="0102938475",
        license_no="DKKD-01029384-HN",
        food_safety_cert="ISO-22000:2018 / HACCP Gold",
        cert_expiry_date=now + timedelta(days=365),
        risk_level="LOW",
        address="Lô B4, KCN Thạch Thất - Quốc Oai, Hà Nội",
        is_active=True,
    )
    sup_rau_vannoi = models.Supplier(
        code="SUP-HTX-VANNOI",
        name="Hợp tác xã Rau an toàn Vân Nội (Đông Anh)",
        tax_code="0108746392",
        license_no="HTX-VANNOI-092",
        food_safety_cert="VietGAP Số 88/2025/NNPTNT",
        cert_expiry_date=now + timedelta(days=180),
        risk_level="LOW",
        address="Xã Vân Nội, Huyện Đông Anh, Hà Nội",
        is_active=True,
    )
    sup_thuan_an = models.Supplier(
        code="SUP-THUANAN-HUE",
        name="Hợp tác xã Thủy hải sản Cửa Biển Thuận An",
        tax_code="3301827461",
        license_no="DKKD-330182-HUE",
        food_safety_cert="VSATTP-HUE-2024",
        cert_expiry_date=now + timedelta(days=90),
        risk_level="MEDIUM",
        address="Thị trấn Thuận An, Thành phố Huế",
        is_active=True,
    )
    sup_bin_bin = models.Supplier(
        code="SUP-BINBIN-GL",
        name="Cơ sở Chế biến Thực phẩm & Giò chả Bin Bin",
        tax_code="5900192837",
        license_no="HKD-ANKHE-5900",
        food_safety_cert="Đã bị đình chỉ sau sự cố Salmonella (17/09/2026)",
        cert_expiry_date=now - timedelta(days=7),
        risk_level="BLACKLISTED",
        address="Đường Quang Trung, Phường An Khê, Tỉnh Gia Lai",
        is_active=False,
    )
    sup_viet_poultry = models.Supplier(
        code="SUP-POULTRY-NORTH",
        name="Công ty TNHH Cung ứng Gia cầm Việt Hưng",
        tax_code="0105432198",
        license_no="DKKD-010543-HN",
        food_safety_cert="HACCP-2025-HN",
        cert_expiry_date=now + timedelta(days=200),
        risk_level="MEDIUM",
        address="Thị trấn Phùng, Đan Phượng, Hà Nội",
        is_active=True,
    )

    db.add_all([sup_cp_food, sup_rau_vannoi, sup_thuan_an, sup_bin_bin, sup_viet_poultry])
    db.flush()

    # ==========================================
    # 3. INGREDIENT BATCHES (LÔ HÀNG NGUYÊN LIỆU)
    # ==========================================
    # Lô 1: Thịt gà công nghiệp an toàn từ CP Food (giao cho trường Chu Văn An)
    batch_ga_cva = models.IngredientBatch(
        batch_code="BATCH-2026-GA-0923-CVA",
        supplier_id=sup_cp_food.id,
        name="Thịt gà ức phi lê tươi CP",
        category="POULTRY",
        origin="Trang trại CP Ba Vì, Hà Nội",
        quantity_kg=120.0,
        harvest_or_slaughter_date=now - timedelta(days=1),
        expiry_date=now + timedelta(days=3),
        storage_condition="CHILLED",
        max_safe_temp=4.0,
        status="APPROVED",
    )
    # Lô 2: Lô thịt gà nghi vấn (liên quan vụ Lê Trọng Tấn)
    batch_ga_ltt = models.IngredientBatch(
        batch_code="BATCH-2026-GA-0911-LTT",
        supplier_id=sup_viet_poultry.id,
        name="Thịt gà công nghiệp nguyên con sơ chế",
        category="POULTRY",
        origin="Cơ sở giết mổ vệ tinh Đan Phượng",
        quantity_kg=150.0,
        harvest_or_slaughter_date=now - timedelta(days=3),
        expiry_date=now + timedelta(days=1),
        storage_condition="CHILLED",
        max_safe_temp=4.0,
        status="REJECTED",
    )
    # Lô 3: Lô tôm đông lạnh quá nhiệt độ (bị Poka-yoke bắt giữ)
    batch_tom_ltt = models.IngredientBatch(
        batch_code="BATCH-2026-TOM-0911-LTT",
        supplier_id=sup_thuan_an.id,
        name="Tôm thẻ chân trắng đông lạnh",
        category="SEAFOOD",
        origin="Vùng nuôi Thừa Thiên Huế",
        quantity_kg=80.0,
        harvest_or_slaughter_date=now - timedelta(days=10),
        expiry_date=now + timedelta(days=30),
        storage_condition="FROZEN",
        max_safe_temp=-12.0,
        status="REJECTED",
    )
    # Lô 4: Lô Patê gan nhiễm khuẩn Salmonella (vụ Gia Lai & Scavi Huế)
    batch_pate_toxic = models.IngredientBatch(
        batch_code="BATCH-2026-PATE-0907-TOXIC",
        supplier_id=sup_bin_bin.id,
        name="Patê gan heo đặc biệt đóng khay",
        category="MEAT",
        origin="Xưởng chế biến Bin Bin, An Khê, Gia Lai",
        quantity_kg=65.0,
        harvest_or_slaughter_date=now - timedelta(days=15),
        expiry_date=now + timedelta(days=5),
        storage_condition="CHILLED",
        max_safe_temp=4.0,
        status="CONSUMED",
    )
    # Lô 5: Rau cải xanh VietGAP
    batch_rau_cai = models.IngredientBatch(
        batch_code="BATCH-2026-RAU-0924",
        supplier_id=sup_rau_vannoi.id,
        name="Rau cải ngọt canh VietGAP",
        category="VEGETABLE",
        origin="Cánh đồng mẫu lớn Vân Nội, Đông Anh",
        quantity_kg=200.0,
        harvest_or_slaughter_date=now - timedelta(hours=8),
        expiry_date=now + timedelta(days=2),
        storage_condition="CHILLED",
        max_safe_temp=10.0,
        status="APPROVED",
    )

    db.add_all([batch_ga_cva, batch_ga_ltt, batch_tom_ltt, batch_pate_toxic, batch_rau_cai])
    db.flush()

    # ==========================================
    # 4. INSPECTIONS STEP 1 (KIỂM THỰC BƯỚC 1: GIAO NHẬN)
    # ==========================================
    # Record 1: Đạt chuẩn (Chu Văn An)
    insp1_cva = models.InspectionStep1(
        batch_id=batch_ga_cva.id,
        facility_id=fac_chu_van_an.id,
        inspected_at=now - timedelta(hours=3),
        inspector_name="Trần Thị Bích (Y tế học đường)",
        delivery_temp=2.8,  # <= 4.0 °C -> Đạt chuẩn
        packaging_intact=True,
        sensory_status="FRESH",
        passed=True,
        poka_yoke_triggered=False,
        rejection_reason=None,
        notes="Thịt gà tươi hồng, độ đàn hồi tốt, tem niêm phong nguyên vẹn.",
    )
    # Record 2: BỊ POKA-YOKE TỰ ĐỘNG CHẶN ĐỨNG (Lê Trọng Tấn phát hiện gà hỏng)
    insp1_ltt_ga = models.InspectionStep1(
        batch_id=batch_ga_ltt.id,
        facility_id=fac_le_trong_tan.id,
        inspected_at=now - timedelta(days=1, hours=2),
        inspector_name="Ban Phụ huynh & Bếp trưởng LTT",
        delivery_temp=11.2,  # > 4.0°C -> VI PHẠM NGHIÊM TRỌNG!
        packaging_intact=False,
        sensory_status="OFF_SMELL",  # Bốc mùi lạ
        passed=False,
        poka_yoke_triggered=True,  # POKA-YOKE KÍCH HOẠT
        rejection_reason="POKA_YOKE_TRIGGERED: Nhiệt độ 11.2°C vượt ngưỡng 4.0°C và phát hiện mùi lạ. Hệ thống lập tức KHÓA CHẶN không cho nhập kho.",
        notes="Phụ huynh kiểm tra lúc 5h sáng, lập biên bản trả lại toàn bộ lô hàng.",
    )
    # Record 3: BỊ POKA-YOKE CHẶN (Tôm đông lạnh bị rã đông chảy nhớt)
    insp1_ltt_tom = models.InspectionStep1(
        batch_id=batch_tom_ltt.id,
        facility_id=fac_le_trong_tan.id,
        inspected_at=now - timedelta(days=1, hours=2),
        inspector_name="Ban Phụ huynh & Bếp trưởng LTT",
        delivery_temp=6.5,  # Đông lạnh nhưng đo được 6.5°C -> Hỏng lạnh hoàn toàn!
        packaging_intact=False,
        sensory_status="SLIMY",
        passed=False,
        poka_yoke_triggered=True,
        rejection_reason="POKA_YOKE_TRIGGERED: Tôm đông lạnh rã đông chảy nước (6.5°C). Chặn nhập kho theo QCVN 12-1:2011/BYT.",
        notes="Tôm có dấu hiệu ươn nhũn.",
    )

    db.add_all([insp1_cva, insp1_ltt_ga, insp1_ltt_tom])
    db.flush()

    # ==========================================
    # 5. INSPECTIONS STEP 2 (KIỂM THỰC BƯỚC 2: CHẾ BIẾN)
    # ==========================================
    insp2_cva_ga = models.InspectionStep2(
        facility_id=fac_chu_van_an.id,
        meal_name="Gà hấp lá chanh & Canh rau cải thịt nạc",
        batch_ids=[batch_ga_cva.id, batch_rau_cai.id],
        cooking_method="STEAMING",
        cooking_started_at=now - timedelta(hours=2),
        cooking_finished_at=now - timedelta(hours=1),
        core_temp=84.5,  # >= 75.0°C -> Đạt chuẩn chín hoàn toàn!
        sensory_check="COOKED_THOROUGHLY",
        cook_name="Bếp trưởng Nguyễn Văn Tuấn",
        passed=True,
        poka_yoke_triggered=False,
        rejection_reason=None,
    )
    db.add(insp2_cva_ga)
    db.flush()

    # ==========================================
    # 6. SAMPLE LOCKERS (KIỂM THỰC BƯỚC 3: LƯU MẪU 24H)
    # ==========================================
    sample_cva = models.SampleLocker(
        facility_id=fac_chu_van_an.id,
        sample_code="SMP-CVA-20260924-01",
        meal_name="Gà hấp lá chanh & Canh cải",
        batch_ids=[batch_ga_cva.id, batch_rau_cai.id],
        locker_number="LOCKER-A01",
        sealed_at=now - timedelta(hours=1),
        unlock_eligible_at=now + timedelta(hours=23),  # 24h sau mới được mở
        is_locked=True,
        storage_temp=2.2,
        status="LOCKED_24H",
        tamper_detected=False,
        supervisor_name="Cán bộ Y tế Phạm Thị Hoa",
    )
    sample_scavi = models.SampleLocker(
        facility_id=fac_scavi_hue.id,
        sample_code="SMP-SCAVI-20260911-03",
        meal_name="Bánh mì patê & Giò lụa ăn ca trưa",
        batch_ids=[batch_pate_toxic.id],
        locker_number="LOCKER-B04",
        sealed_at=now - timedelta(days=2),
        unlock_eligible_at=now - timedelta(days=1),
        is_locked=False,
        storage_temp=3.5,
        status="ACCIDENT_INSPECTED",
        tamper_detected=False,
        supervisor_name="Lê Văn Thành (KCN Phong Điền)",
    )
    db.add_all([sample_cva, sample_scavi])
    db.flush()

    # ==========================================
    # 7. INCIDENT REPORT (SỰ CỐ DỊCH TỄ NGỘ ĐỘC THẬT ĐỂ DEMO TRUY VẾT)
    # ==========================================
    incident_scavi = models.IncidentReport(
        facility_id=fac_scavi_hue.id,
        reported_at=now - timedelta(hours=4),
        meal_name="Bánh mì kẹp Patê gan & Giò lụa",
        suspected_batches=[batch_pate_toxic.id],
        symptoms=["Sốt cao 39.5°C", "Nôn mửa dữ dội", "Tiêu chảy cấp", "Đau thắt bụng dưới"],
        affected_count=180,
        severity="CRITICAL",
        status="INVESTIGATING",
        investigation_log="Ngày 12/09/2026: Phát hiện hơn 180 công nhân Scavi Huế có triệu chứng nhiễm khuẩn đường ruột cấp. Cần truy vết tức thì nhà cung cấp lô patê gan BATCH-2026-PATE-0907-TOXIC và các cơ sở khác đã tiêu thụ lô hàng này.",
    )
    db.add(incident_scavi)
    db.commit()

    logger.info("Successfully loaded 100% Realistic Seed Data into PostgreSQL!")
    return {
        "status": "success",
        "facilities": 4,
        "suppliers": 5,
        "batches": 5,
        "inspections_step1": 3,
        "inspections_step2": 1,
        "sample_lockers": 2,
        "incidents": 1,
    }
