import io
import PyPDF2
import pdfkit
from jinja2 import Template
from app.services import utils_service
from app.models.generate_base_64_model import GenerateBase64Request, GenerateBase64Response


def generate_base_64_file(generateBase64Request: GenerateBase64Request, company_id: int):
    json_certificates = [
        {"Titulo1": "Certificado de Retención de Ingresos Brutos Santa Fe", "RazonSocial": "PLAY DIGITAL SA",
         "Direccion": "LIBERTADOR DEL AV. 7208 Piso:3 Dpto:3.1  T:PPAL", "CodigoPostal": "1429",
         "Localidad": "CIUDAD AUTONOMA BUENOS AIRES", "Provincia": "CIUDAD AUTONOMA BUENOS AIRES",
         "Fecha": "15-12-2023", "CUITAgente": "30-71682943-6", "NroIIBB": 30716829436,
         "RazonSocialContribuyente": "VALERI AUGUSTO JOSE", "DireccionContribuyente": "",
         "CodigoPostalContribuyente": "", "LocalidadContribuyente": "", "ProvinciaContribuyente": "",
         "CUITContribuyente": "20-12222694-9", "NroCertificado": "232300000019", "Impuesto": 921,
         "Condicion": "Contribuyente local", "EnPalabras": "En palabras: Pesos argentinos, un mil cuarenta con 0/100.",
         "Referencia": "Período de Retenciones: DICIEMBRE 2023 - 1era quincena", "IdAgrupacionRetenciones": "285",
         "NombreApoderado": "Martín Quiroga", "Retenciones": [
            {"TaxRegimeId": "516", "TaxRegime": "Servicios de gestión de pagos y cobros",
             "BaseRetencion": "$ 52.000,00", "Alicuota": "2,00 %", "Retencion": "$ 1.040,00"},
            {"TaxRegimeId": "TOTAL", "TaxRegime": "", "BaseRetencion": "$ 52.000,00", "Alicuota": "",
             "Retencion": "$ 1.040,00"}]},
        {"Titulo1": "Certificado de Retención de Ingresos Brutos Santa Fe", "RazonSocial": "PLAY DIGITAL SA",
         "Direccion": "LIBERTADOR DEL AV. 7208 Piso:3 Dpto:3.1  T:PPAL", "CodigoPostal": "1429",
         "Localidad": "CIUDAD AUTONOMA BUENOS AIRES", "Provincia": "CIUDAD AUTONOMA BUENOS AIRES",
         "Fecha": "15-12-2023", "CUITAgente": "30-71682943-6", "NroIIBB": 30716829436,
         "RazonSocialContribuyente": "SARUTI JORGE OMAR", "DireccionContribuyente": "", "CodigoPostalContribuyente": "",
         "LocalidadContribuyente": "", "ProvinciaContribuyente": "", "CUITContribuyente": "20-12519026-0",
         "NroCertificado": "232300000022", "Impuesto": 921, "Condicion": "Convenio multilateral",
         "EnPalabras": "En palabras: Pesos argentinos, ochocientos noventa y seis con 10/100.",
         "Referencia": "Período de Retenciones: DICIEMBRE 2023 - 1era quincena", "IdAgrupacionRetenciones": "285",
         "NombreApoderado": "Martín Quiroga", "Retenciones": [
            {"TaxRegimeId": "516", "TaxRegime": "Servicios de gestión de pagos y cobros",
             "BaseRetencion": "$ 59.740,00", "Alicuota": "1,50 %", "Retencion": "$ 896,10"},
            {"TaxRegimeId": "TOTAL", "TaxRegime": "", "BaseRetencion": "$ 59.740,00", "Alicuota": "",
             "Retencion": "$ 896,10"}]}]
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

        with open('tmp/tmp.html', 'w', encoding='utf-8') as f:
            f.write(html_template)

        pdf_options = utils_service.get_pdf_options(output_file)
        filename = f'tmp/tmp.pdf'
        pdfkit.from_file('tmp/tmp.html', filename, options=pdf_options)

        pdf_bytes = pdf_to_bytes(filename)
        list_base64.append(pdf_bytes)

    input_directory = "tmp/"

    merged_pdf_bytes = merge_pdfs(list_base64)
    # Nombre del archivo de salida
    base64_file = utils_service.convertir_a_base64(merged_pdf_bytes)
    response = GenerateBase64Response(filename=output_file.replace('tmp/', ''), base64=base64_file)
    return response


def merge_pdfs(pdf_list):
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

        with open("tmp/tmp.pdf", "wb") as output_file:
            output_file.write(result_bytesio.getvalue())
        return pdf_to_bytes("tmp/tmp.pdf")

    except Exception as e:
        print(f"Error al combinar PDFs: {str(e)}")
        return None


def pdf_to_bytes(file_path):
    try:
        with open(file_path, 'rb') as file:
            binary_data = file.read()
            bytesio_object = io.BytesIO(binary_data)
        return bytesio_object
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")
        return None


def copy_to_memory(file_path):
    with open(file_path, 'rb') as file:
        # Leer el contenido del archivo en BytesIO
        file_content = io.BytesIO(file.read())
    return file_content
