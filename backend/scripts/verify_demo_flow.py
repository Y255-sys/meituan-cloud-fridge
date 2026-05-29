from fastapi.testclient import TestClient

from app.main import app


def main() -> None:
    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"phone": "13800000000", "password": "12345678"},
        )
        login_response.raise_for_status()
        token = login_response.json()["data"]["token"]
        headers = {"Authorization": f"Bearer {token}"}

        inventory_response = client.get("/api/v1/inventory", headers=headers)
        inventory_response.raise_for_status()

        recommendation_response = client.get("/api/v1/recipes/recommendations", headers=headers)
        recommendation_response.raise_for_status()

        purchase_plan_response = client.post(
            "/api/v1/purchase-plans",
            headers=headers,
            json={"recipe_ids": ["rcp_beef_pepper"], "strategy": "lowest_cost"},
        )
        purchase_plan_response.raise_for_status()
        plan_id = purchase_plan_response.json()["data"]["plan_id"]

        product_match_response = client.post(
            "/api/v1/products/match",
            headers=headers,
            json={"plan_id": plan_id},
        )
        product_match_response.raise_for_status()

    print("Demo flow verified successfully.")


if __name__ == "__main__":
    main()
