import io
import PyPDF2
import pdfkit
from jinja2 import Template

from app.dto.request.generate_base_64_request_dto import GenerateBase64Request
from app.repository import s3_repository
from app.services import utils_service
from app.dto.response.generate_base_64_response_dto import GenerateBase64Response


def generate_base_64_file(generateBase64Request: GenerateBase64Request, company_id: int):
    json_certificates = s3_repository.get_data_from_file(generateBase64Request, company_id)

    print(len(json_certificates))
    if len(json_certificates) == 0:
        return GenerateBase64Response()
    list_base64 = []

    output_file = f"tmp/{generateBase64Request.taxpayerId}_{generateBase64Request.taxId}_{generateBase64Request.period}.pdf"
    for certificado in json_certificates:
        with open("template/certificado_template.html", "r", encoding='utf-8') as certificado_template:
            template = Template(certificado_template.read())

        certificado['firma_src'] = '../app/template/Firma_' + certificado['CUITAgente'].replace("-", "") + '.png'
        html_template = template.render(**certificado)

        with open('../tmp/tmp.html', 'w', encoding='utf-8') as f:
            f.write(html_template)

        pdf_options = utils_service.get_pdf_options(output_file)
        filename = f'../tmp/tmp.pdf'
        pdfkit.from_file('../tmp/tmp.html', filename, options=pdf_options)

        pdf_bytes = _pdf_to_bytes(filename)
        list_base64.append(pdf_bytes)

    merged_pdf_bytes = _merge_pdfs(list_base64)
    # Nombre del archivo de salida
    base64_file = utils_service.convertir_a_base64(merged_pdf_bytes)
    response = GenerateBase64Response(filename=output_file.replace('tmp/', ''), base64=base64_file)
    return response


def _merge_pdfs(pdf_list):
    try:
        pdf_merger = PyPDF2.PdfMerger()

        for byteosio in pdf_list:
            # Asegúrate de que estás al principio del archivo BytesIO
            byteosio.seek(0)

            # Agrega la página al objeto PdfFileMerger
            pdf_merger.append(byteosio)

        # Creamos un nuevo objeto BytesIO para almacenar el PDF combinado
        result_bytesio = io.BytesIO()
        pdf_merger.write(result_bytesio)

        with open("../tmp/tmp.pdf", "wb") as output_file:
            output_file.write(result_bytesio.getvalue())
        return _pdf_to_bytes("../tmp/tmp.pdf")

    except Exception as e:
        print(f"Error al combinar PDFs: {str(e)}")
        return None


def _pdf_to_bytes(file_path):
    try:
        with open(file_path, 'rb') as file:
            binary_data = file.read()
            bytesio_object = io.BytesIO(binary_data)
        return bytesio_object
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")
        return None


def _copy_to_memory(file_path):
    with open(file_path, 'rb') as file:
        # Leer el contenido del archivo en BytesIO
        file_content = io.BytesIO(file.read())
    return file_content
