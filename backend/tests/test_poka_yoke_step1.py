# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

def test_step1_valid_delivery_approved(client):
    """Kiểm thử Bước 1: Giao nhận thịt tươi nhiệt độ 2.5°C đạt chuẩn (<= 4.0°C) -> HTTP 201 Created."""
    batches = client.get("/api/v1/batches").json()
    valid_batch = next((b for b in batches if b["category"] == "POULTRY" and b["status"] != "REJECTED"), batches[0])
    facilities = client.get("/api/v1/facilities").json()
    facility = facilities[0]

    payload = {
        "batch_id": valid_batch["id"],
        "facility_id": facility["id"],
        "inspector_name": "Cán bộ Y tế Kiểm thử",
        "delivery_temp": 2.5,
        "packaging_intact": True,
        "sensory_status": "FRESH",
        "notes": "Kiểm tra nhiệt độ đạt chuẩn an toàn",
    }
    response = client.post("/api/v1/inspections/step1", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["passed"] is True
    assert data["status"] == "APPROVED"
    assert data["delivery_temp"] == 2.5


def test_step1_temperature_violation_blocked_by_poka_yoke(client):
    """Kiểm thử Bước 1: Giao hàng thịt gà ở 12.5°C (> 4.0°C) -> Poka-yoke chặn đứng với HTTP 422."""
    batches = client.get("/api/v1/batches").json()
    batch = batches[0]
    facilities = client.get("/api/v1/facilities").json()
    facility = facilities[0]

    payload = {
        "batch_id": batch["id"],
        "facility_id": facility["id"],
        "inspector_name": "Cán bộ Y tế Kiểm thử",
        "delivery_temp": 12.5,  # Vi phạm nghiêm trọng chuỗi lạnh!
        "packaging_intact": True,
        "sensory_status": "FRESH",
        "notes": "Thử nghiệm kích hoạt rào chắn Poka-yoke",
    }
    response = client.post("/api/v1/inspections/step1", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "POKA_YOKE_BLOCKED"
    assert "violation" in data
    assert data["violation"]["error_code"] == "POKA_YOKE_TEMP_VIOLATION"
    assert "QCVN" in data["violation"]["standard_ref"]


def test_step1_sensory_violation_blocked(client):
    """Kiểm thử Bước 1: Thực phẩm bốc mùi lạ (OFF_SMELL) -> Poka-yoke chặn đứng với HTTP 422."""
    batches = client.get("/api/v1/batches").json()
    batch = batches[0]
    facilities = client.get("/api/v1/facilities").json()
    facility = facilities[0]

    payload = {
        "batch_id": batch["id"],
        "facility_id": facility["id"],
        "inspector_name": "Cán bộ Y tế Kiểm thử",
        "delivery_temp": 3.0,
        "packaging_intact": True,
        "sensory_status": "OFF_SMELL",  # Bốc mùi lạ!
        "notes": "Mùi ươn chua bất thường",
    }
    response = client.post("/api/v1/inspections/step1", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["violation"]["error_code"] == "POKA_YOKE_SENSORY_FAILED"


def test_step1_broken_packaging_blocked(client):
    """Kiểm thử Bước 1: Bao bì rách, mất niêm phong -> Poka-yoke chặn đứng với HTTP 422."""
    batches = client.get("/api/v1/batches").json()
    batch = batches[0]
    facilities = client.get("/api/v1/facilities").json()
    facility = facilities[0]

    payload = {
        "batch_id": batch["id"],
        "facility_id": facility["id"],
        "inspector_name": "Cán bộ Y tế Kiểm thử",
        "delivery_temp": 2.0,
        "packaging_intact": False,  # Bao bì rách hở!
        "sensory_status": "FRESH",
        "notes": "Tem niêm phong bị xé rách",
    }
    response = client.post("/api/v1/inspections/step1", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["violation"]["error_code"] == "POKA_YOKE_PACKAGING_DAMAGED"
