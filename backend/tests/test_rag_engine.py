# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 FoodSafe-DX-OS Contributors

def test_rag_query_offline_performance_under_50ms(client):
    """Kiểm thử Local RAG Engine: Tra cứu nội bộ cực nhanh dưới 50ms, không phụ thuộc Cloud LLM."""
    payload = {
        "query": "Nhiệt độ tâm nấu chín và giới hạn vi khuẩn Salmonella",
        "top_k": 2,
    }
    response = client.post("/api/v1/rag/query", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["engine_mode"] == "LOCAL_OFFLINE_ZERO_CLOUD"
    assert data["execution_time_ms"] < 50.0, f"RAG time {data['execution_time_ms']}ms vượt quá 50ms!"
    assert data["confidence_score"] >= 0.7


def test_rag_citations_accuracy(client):
    """Kiểm thử RAG trích dẫn chính xác quy chuẩn pháp luật và tiêu chuẩn kỹ thuật."""
    payload = {
        "query": "Quy định lưu mẫu thức ăn 24 giờ và mức phạt vi phạm theo nghị định 115",
        "top_k": 2,
    }
    response = client.post("/api/v1/rag/query", json=payload)
    assert response.status_code == 200
    data = response.json()

    citations_str = " ".join(data["citations"])
    assert "115" in citations_str or "1246" in citations_str
    assert len(data["relevant_chunks"]) >= 1


def test_rag_standards_and_pathogens_catalog(client):
    """Kiểm thử API danh mục quy chuẩn và bảng vi sinh."""
    standards_res = client.get("/api/v1/rag/standards")
    assert standards_res.status_code == 200
    standards_data = standards_res.json()
    assert standards_data["total_standards"] >= 4
    assert standards_data["cloud_independent"] is True

    pathogens_res = client.get("/api/v1/rag/pathogens")
    assert pathogens_res.status_code == 200
    pathogens = pathogens_res.json()
    assert len(pathogens) >= 4
    names = [p["pathogen"] for p in pathogens]
    assert any("Salmonella" in n for n in names)
    assert any("E. coli" in n for n in names)
    assert any("Histamine" in n for n in names)
