# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

def get_or_create_approved_batch(client):
    """Helper đảm bảo có ít nhất một lô hàng đã được duyệt APPROVED ở Bước 1."""
    batches = client.get("/api/v1/batches").json()
    approved = next((b for b in batches if b["status"] == "APPROVED"), None)
    if approved:
        return approved

    # Nếu chưa có lô APPROVED, thực hiện duyệt Bước 1 cho lô đầu tiên
    facilities = client.get("/api/v1/facilities").json()
    target_batch = batches[0]
    client.post("/api/v1/inspections/step1", json={
        "batch_id": target_batch["id"],
        "facility_id": facilities[0]["id"],
        "inspector_name": "Cán bộ Y tế",
        "delivery_temp": 2.0,
        "packaging_intact": True,
        "sensory_status": "FRESH",
    })
    updated_batches = client.get("/api/v1/batches").json()
    return next((b for b in updated_batches if b["id"] == target_batch["id"]), target_batch)


def test_step2_safe_cooking_temp_approved(client):
    """Kiểm thử Bước 2: Nấu chín món ăn ở 85.0°C (>= 75.0°C) với lô đã duyệt Bước 1 -> HTTP 201 Created."""
    valid_batch = get_or_create_approved_batch(client)
    facilities = client.get("/api/v1/facilities").json()
    facility = facilities[0]

    payload = {
        "facility_id": facility["id"],
        "meal_name": "Gà hấp lá chanh đạt chuẩn chín thấu",
        "batch_ids": [valid_batch["id"]],
        "cooking_method": "STEAMING",
        "core_temp": 85.0,  # >= 75.0°C chuẩn WHO/Codex
        "sensory_check": "COOKED_THOROUGHLY",
        "cook_name": "Bếp trưởng Kiểm thử",
    }
    response = client.post("/api/v1/inspections/step2", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["passed"] is True
    assert data["core_temp"] == 85.0


def test_step2_undercooked_temp_blocked(client):
    """Kiểm thử Bước 2: Nấu ở 62.0°C (< 75.0°C) -> Poka-yoke chặn đứng với HTTP 422."""
    valid_batch = get_or_create_approved_batch(client)
    facilities = client.get("/api/v1/facilities").json()
    facility = facilities[0]

    payload = {
        "facility_id": facility["id"],
        "meal_name": "Gà luộc còn lòng đào nguy hiểm",
        "batch_ids": [valid_batch["id"]],
        "cooking_method": "BOILING",
        "core_temp": 62.0,  # Chưa đủ 75.0°C diệt khuẩn!
        "sensory_check": "UNDERCOOKED_RAW_INSIDE",
        "cook_name": "Bếp trưởng Kiểm thử",
    }
    response = client.post("/api/v1/inspections/step2", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "POKA_YOKE_BLOCKED"
    assert data["violation"]["error_code"] == "POKA_YOKE_UNDERCOOKED_TEMP"


def test_step2_contaminated_ingredient_blocked(client):
    """Kiểm thử Bước 2: Cố tình sử dụng lô nguyên liệu đã bị REJECTED -> Poka-yoke chặn đứng với HTTP 422."""
    batches = client.get("/api/v1/batches").json()
    rejected_batch = next((b for b in batches if b["status"] == "REJECTED"), None)
    if not rejected_batch:
        # Nếu chưa có lô REJECTED, kích hoạt 1 lô vi phạm ở Bước 1
        facilities = client.get("/api/v1/facilities").json()
        client.post("/api/v1/inspections/step1", json={
            "batch_id": batches[-1]["id"],
            "facility_id": facilities[0]["id"],
            "inspector_name": "Cán bộ Y tế",
            "delivery_temp": 15.0,  # Bị REJECTED
            "packaging_intact": False,
            "sensory_status": "OFF_SMELL",
        })
        batches = client.get("/api/v1/batches").json()
        rejected_batch = next((b for b in batches if b["status"] == "REJECTED"), batches[-1])

    facilities = client.get("/api/v1/facilities").json()
    facility = facilities[0]

    payload = {
        "facility_id": facility["id"],
        "meal_name": "Món ăn gian lận dùng nguyên liệu hỏng",
        "batch_ids": [rejected_batch["id"]],
        "cooking_method": "STIR_FRY",
        "core_temp": 88.0,
        "sensory_check": "COOKED_THOROUGHLY",
        "cook_name": "Bếp trưởng Kiểm thử",
    }
    response = client.post("/api/v1/inspections/step2", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["violation"]["error_code"] in ["POKA_YOKE_CONTAMINATED_INGREDIENT", "POKA_YOKE_UNAPPROVED_INGREDIENT"]
