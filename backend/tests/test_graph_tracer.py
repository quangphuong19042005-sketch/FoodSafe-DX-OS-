# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

def test_graph_trace_performance_under_100ms(client):
    """Kiểm thử Thuật toán Truy vết Đồ thị Đa tầng (BFS): Phải hoàn thành dưới 100ms (chỉ tiêu chung kết < 3000ms)."""
    incidents = client.get("/api/v1/incidents").json()
    assert len(incidents) > 0, "Cần có ít nhất 1 sự cố để kiểm thử truy vết."
    incident = incidents[0]

    response = client.post(f"/api/v1/incidents/{incident['id']}/trace")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "EMERGENCY_RECALL_ACTIVATED"
    # Thời gian thực thi cực nhanh: < 100ms
    assert data["execution_time_ms"] < 100.0, f"Execution time {data['execution_time_ms']}ms vượt quá 100ms!"


def test_graph_trace_pathogen_diagnosis(client):
    """Kiểm thử Chẩn đoán Mầm bệnh dựa trên triệu chứng lâm sàng."""
    incidents = client.get("/api/v1/incidents").json()
    incident = incidents[0]

    response = client.post(f"/api/v1/incidents/{incident['id']}/trace")
    data = response.json()

    pathogen_analysis = data["pathogen_analysis"]
    assert "Salmonella" in pathogen_analysis["likely_pathogen"]
    assert "QCVN 8-2" in pathogen_analysis["standard_reference"]
    assert pathogen_analysis["risk_level"] == "CRITICAL"


def test_graph_trace_root_cause_and_imminent_risk(client):
    """Kiểm thử Xác định Lô hàng & Nhà cung ứng gốc, đồng thời phát hiện Cơ sở nguy cơ cao."""
    incidents = client.get("/api/v1/incidents").json()
    incident = incidents[0]

    response = client.post(f"/api/v1/incidents/{incident['id']}/trace")
    data = response.json()

    # Nguyên nhân gốc
    root = data["root_cause_analysis"]
    assert "BATCH-2026-PATE-0907-TOXIC" in root["batch_code"]
    assert "Bin Bin" in root["supplier_name"]
    assert root["supplier_status"] == "BLACKLISTED"

    # Cơ sở nguy cơ lây nhiễm cận kề (THCS Quang Trung)
    assert data["imminent_risk_facilities_count"] >= 1
    imminent = data["imminent_risk_facilities"][0]
    assert "Quang Trung" in imminent["facility_name"]
    assert "LOCKER-GIA-LAI-01" in imminent["locker_to_seal"]

    # Cấu trúc đồ thị cho trực quan hóa
    graph = data["graph"]
    assert graph["nodes_count"] >= 4
    assert graph["edges_count"] >= 3
    assert len(graph["nodes"]) == graph["nodes_count"]
    assert len(graph["links"]) == graph["edges_count"]
