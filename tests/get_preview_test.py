from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_preview_with_valid_params_return_preview_200():
    response = client.get("/v1/certificates?taxpayerId=20314775229&period=202401&withholdingGroupingId=285")

    assert response.status_code == 200
    assert response.json() == {
        "companyId": 30716829436,
        "taxpayerId": 20314775229,
        "withholdingGroupingId": 285,
        "period": 202401,
        "totalWithholdingAmount": 0.0,
        "certificates": [
            {
                "taxId": 216,
                "netAmount": 1222.0,
                "withholdingAmount": 12.2,
                "rate": 0.1
            },
            {
                "taxId": 217,
                "netAmount": 222.0,
                "withholdingAmount": 2.2,
                "rate": 0.02
            }
        ]
    }


def test_get_preview_without_period_return_error_422():
    response = client.get("/v1/certificates?taxpayerId=20314775229&withholdingGroupingId=285")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "query",
                    "period"
                ],
                "msg": "Field required",
                "input": None,
                "url": "https://errors.pydantic.dev/2.5/v/missing"
            }
        ]
    }


def test_get_preview_without_taxpayer_id_return_error_422():
    response = client.get("/v1/certificates?period=202401&withholdingGroupingId=285")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "query",
                    "taxpayerId"
                ],
                "msg": "Field required",
                "input": None,
                "url": "https://errors.pydantic.dev/2.5/v/missing"
            }
        ]
    }
