from fastapi.testclient import TestClient

from app.main import app


def test_login_and_fetch_recommendations() -> None:
    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"phone": "13800000000", "password": "12345678"},
        )
        assert login_response.status_code == 200
        token = login_response.json()["data"]["token"]

        recommendation_response = client.get(
            "/api/v1/recipes/recommendations",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert recommendation_response.status_code == 200
        groups = recommendation_response.json()["data"]["groups"]
        assert len(groups) == 3
