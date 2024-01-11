import os
import boto3
import json
from dotenv import load_dotenv
import logging
from app.models.generate_base_64_model import GenerateBase64Request

load_dotenv()


def read_file_from_s3(company_id: int, period: int):
    try:
        file_location = f"Certificates/{str(company_id)}/{str(period)}/{str(company_id)}_{str(period)}.txt"
        bucket_name = os.getenv('BUCKET')
        s3_client = boto3.client('s3',
                                 aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=file_location)
        response = json.loads(s3_object['Body'].read().decode('utf-8'))

        logging.info(f'Cantidad de certificados encontrados: {len(response)} en {bucket_name} {file_location}')

    except Exception as e:
        logging.info(f"Error ->: {e}")
        response = []
    return response


def get_data_from_file(generateBase64Request: GenerateBase64Request, company_id: int):
    json_certificates = read_file_from_s3(company_id, generateBase64Request.period)
    taxpayer_id = str(generateBase64Request.taxpayerId)
    taxpayer_id = f"{taxpayer_id[:2]}-{taxpayer_id[2:10]}-{taxpayer_id[-1]}"
    resultado_filtrado = []
    for certificate in json_certificates:
        if certificate['CUITContribuyente'] == taxpayer_id \
                and certificate['Impuesto'] == generateBase64Request.taxId \
                and certificate['IdAgrupacionRetenciones'] == generateBase64Request.withholdingGroupingId:
            resultado_filtrado.append(certificate)
    return resultado_filtrado
