from fastapi.testclient import TestClient
from app.main import app
# Ejemplo con ruta relativa

client = TestClient(app)


def test_generate_base_64_with_valid_body_response_base_64_file_200():
    # Datos de ejemplo para el cuerpo del POST
    item_data = {
        "taxpayerId": 20314775229,
        "period": 202401,
        "taxId": 216,
        "WithholdingGroupingId": 285
    }

    response = client.post("/v1/certificates", json=item_data)

    assert response.status_code == 200

    assert response.json() == {
        "filename": None,
        "base64": None
    }
