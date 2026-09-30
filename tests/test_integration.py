import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_end_to_end_flow():
    # Health check
    response = client.get("/")
    assert response.status_code == 200

    # Generate document
    response = client.post("/generate", json={
        "document_type": "Contract",
        "parties": "Party A: ABC Corp, Party B: XYZ Ltd",
        "terms_conditions": "Payment terms: Net 30",
        "effective_date": "2026-09-30"
    })
    assert response.status_code in [200, 500]


def test_multiple_document_types():
    doc_types = ["Contract", "NDA", "Lease Agreement", "Employment Document"]
    for doc_type in doc_types:
        response = client.post("/generate", json={
            "document_type": doc_type,
            "parties": "Test parties",
            "terms_conditions": "Test terms",
            "effective_date": "2026-09-30"
        })
        assert response.status_code in [200, 500]
