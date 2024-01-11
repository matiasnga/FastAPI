import io
import os
import PyPDF2
import pdfkit
from fastapi import HTTPException
from jinja2 import Template
from app.dto.request.generate_base_64_request_dto import GenerateBase64Request
from app.repository import s3_repository
from app.services import utils_service
from app.dto.response.generate_base_64_response_dto import GenerateBase64Response
from app.services.utils_service import convert_file_to_bytes

current_directory = os.path.dirname(os.path.abspath(__file__))

temp_path = os.path.join(current_directory, '../../tmp')
template_path = os.path.join(current_directory, '../template')
template_file = os.path.join(current_directory, '../template/certificado_template.html')
temp_pdf_file = os.path.join(current_directory, '../../tmp/tmp.pdf')
temp_html_file = os.path.join(current_directory, '../../tmp/tmp.html')


def generate_base_64_file(generateBase64Request: GenerateBase64Request, company_id: int):
    output_file = f"{generateBase64Request.taxpayerId}_{generateBase64Request.taxId}_{generateBase64Request.period}.pdf"

    json_certificates = s3_repository.get_data_from_file(generateBase64Request, company_id)
    certificates_bytes_list = []

    if len(json_certificates) == 0:
        raise HTTPException(status_code=404, detail="El certificado no existe")

    for certificado in json_certificates:
        with open(os.path.abspath(template_file), "r",
                  encoding='utf-8') as certificado_template:
            template = Template(certificado_template.read())

        certificado['firma_src'] = os.path.abspath(f'{template_path}/Firma_' + certificado['CUITAgente'].replace("-", "") + '.png')
        html_template = template.render(**certificado)

        with open(os.path.abspath(temp_html_file), 'w', encoding='utf-8') as f:
            f.write(html_template)

        pdf_options = utils_service.get_pdf_options()
        pdfkit.from_file(temp_html_file, temp_pdf_file, options=pdf_options)

        pdf_bytes = convert_file_to_bytes(temp_pdf_file)
        certificates_bytes_list.append(pdf_bytes)

    merged_pdf_bytes = _merge_pdfs(certificates_bytes_list)

    base64_file = utils_service.convert_bytes_to_base64(merged_pdf_bytes)
    response = GenerateBase64Response(filename=output_file, base64=base64_file)
    return response


def _merge_pdfs(pdf_list):
    try:
        pdf_merger = PyPDF2.PdfMerger()

        for byteosio in pdf_list:
            byteosio.seek(0)
            pdf_merger.append(byteosio)

        result_bytesio = io.BytesIO()
        pdf_merger.write(result_bytesio)

        with open(temp_pdf_file, "wb") as output_file:
            output_file.write(result_bytesio.getvalue())
        return convert_file_to_bytes(temp_pdf_file)

    except Exception as e:
        print(f"Error al combinar PDFs: {str(e)}")
        return None

