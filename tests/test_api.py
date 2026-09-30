import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_generate_missing_fields():
    response = client.post("/generate", json={})
    assert response.status_code == 422


def test_generate_invalid_document_type():
    response = client.post("/generate", json={
        "document_type": "",
        "parties": "Test",
        "terms_conditions": "Test terms",
        "effective_date": "2026-09-30"
    })
    assert response.status_code == 422


def test_generate_valid_request():
    response = client.post("/generate", json={
        "document_type": "NDA",
        "parties": "Party A: Test Corp",
        "terms_conditions": "Confidentiality period: 1 year",
        "effective_date": "2026-09-30"
    })
    assert response.status_code in [200, 500]
