import os
from unittest import mock
from unittest.mock import patch
import boto3
from fastapi.testclient import TestClient
from moto import mock_s3
from app.main import app

client = TestClient(app)


@mock_s3
def test_get_preview_with_valid_params_return_preview_200():
    # Configura el bucket y la clave en S3
    bucket_name = 'test-bucket'
    key = 'test-key'
    mock_s3().start()
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket_name)

    with open(os.path.abspath('tests/data_test/30716829436_202312.txt'), 'r', encoding='utf-8') as file:
        data_content = file.read()

    s3.put_object(Bucket=bucket_name, Key=key, Body=data_content)

    with patch('boto3.client') as mock_client:
        mock_s3_client = mock_client.return_value
        mock_s3_client.get_object.return_value = {
            'Body': mock.MagicMock()  # Mockear el objeto de streaming
        }
        mock_s3_client.get_object.return_value['Body'].read.return_value = data_content.encode('utf-8')

        response = client.get('/v1/certificates?taxpayerId=20122226949&period=202312&withholdingGroupingId=285')

        assert response.status_code == 200
        assert response.json() == {
            "companyId": 30716829436,
            "taxpayerId": 20122226949,
            "withholdingGroupingId": "285",
            "period": 202312,
            "totalWithholdingAmount": 1040.0,
            "certificates": [
                {
                    "taxId": 921,
                    "netAmount": 52000.0,
                    "withholdingAmount": 1040.0,
                    "rate": 0.02
                }
            ]
        }

    mock_s3().stop()

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
