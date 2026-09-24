# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

def test_step3_early_unlock_prohibited(client):
    """Kiểm thử Bước 3: Mở tủ lưu mẫu khi chưa đủ 24 giờ -> Poka-yoke chặn đứng với HTTP 422."""
    lockers = client.get("/api/v1/sample-lockers").json()
    locked_locker = next((loc for loc in lockers if loc["is_locked"] and loc["hours_remaining"] > 0), None)
    if not locked_locker:
        return

    payload = {
        "operator_name": "Nhân viên Bếp ăn",
        "is_emergency_override": False,
    }
    response = client.post(f"/api/v1/sample-lockers/{locked_locker['id']}/unlock", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "POKA_YOKE_BLOCKED"
    assert data["violation"]["error_code"] == "POKA_YOKE_EARLY_UNLOCK_PROHIBITED"


def test_step3_emergency_override_with_wrong_passcode_forbidden(client):
    """Kiểm thử Bước 3: Mở khẩn cấp nhưng nhập sai passcode -> HTTP 403 Forbidden."""
    lockers = client.get("/api/v1/sample-lockers").json()
    locked_locker = next((loc for loc in lockers if loc["is_locked"] and loc["hours_remaining"] > 0), None)
    if not locked_locker:
        return

    payload = {
        "operator_name": "Nhân viên Bếp ăn",
        "is_emergency_override": True,
        "override_reason": "Thanh tra Đột xuất Sở Y tế",
        "override_passcode": "WRONG-PASSCODE-123",
    }
    response = client.post(f"/api/v1/sample-lockers/{locked_locker['id']}/unlock", json=payload)
    assert response.status_code == 403
    data = response.json()
    assert "Override Passcode" in data["detail"]


def test_step3_emergency_override_hitl_approved(client):
    """Kiểm thử Bước 3: Mở khẩn cấp Human-in-the-loop với passcode chuẩn HITL-EMERGENCY-2026 -> HTTP 200 OK."""
    # Tạo một mẫu mới để test mở khẩn cấp
    facilities = client.get("/api/v1/facilities").json()
    facility = facilities[0]
    import uuid
    unique_code = f"SMP-TEST-{uuid.uuid4().hex[:6].upper()}"

    create_payload = {
        "facility_id": facility["id"],
        "sample_code": unique_code,
        "meal_name": "Món ăn test mở khẩn cấp HITL",
        "batch_ids": [1],
        "locker_number": "LOCKER-TEST-99",
        "storage_temp": 3.0,
        "supervisor_name": "Cán bộ Y tế",
    }
    created = client.post("/api/v1/sample-lockers", json=create_payload).json()
    locker_id = created["id"]

    # Mở khóa khẩn cấp
    unlock_payload = {
        "operator_name": "Đoàn Thanh tra Sở Y tế",
        "is_emergency_override": True,
        "override_reason": "Phục vụ điều tra dịch tễ học khẩn cấp",
        "override_passcode": "HITL-EMERGENCY-2026",
    }
    response = client.post(f"/api/v1/sample-lockers/{locker_id}/unlock", json=unlock_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HITL_OVERRIDE_APPROVED"
    assert data["audit_trail"] == "LOGGED_SECURELY"
