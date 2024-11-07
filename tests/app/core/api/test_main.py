from fastapi.testclient import TestClient

from app.core.api.main import app


def test_read_main():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"New Phone": "Who Dis?"}
