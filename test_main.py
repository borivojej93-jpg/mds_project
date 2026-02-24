from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_sorting_logic():
    response = client.post("/do_balance")
    assert response.status_code == 200
