from fastapi.testclient import TestClient

from app import repository
from app.main import app

client = TestClient(app)


def test_sorting_logic():
    response = client.post("/do_balance")
    print(response)
    assert response.status_code == 404
    # print("oi")
    # print(response)
    # print(response.json())
    # print(repository.rack_dict)
    # assert response.json() == {"msg": "balance finished"}
