import os
import boto3
import json
from dotenv import load_dotenv
import logging

load_dotenv()



def read_file(cuit_agente, periodo):
    try:
        carpeta = 'Certificates/' + cuit_agente + '/' + periodo + '/'
        nombre_archivo = carpeta + cuit_agente + '_' + periodo + '.txt'
        bucket_name = os.getenv('BUCKET')
        s3_client = boto3.client('s3',
                                 aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
                                 aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=nombre_archivo)
        response = json.loads(s3_object['Body'].read().decode('utf-8'))
        logging.info(len(response))

    except Exception as e:
        logging.info(f"Error ->: {e}")
        response = []
    return response
