import base64


def convertir_a_base64(pdf_in_memory):
    try:
        data = pdf_in_memory.read()
        base64_data = base64.b64encode(data).decode('utf-8')
        return base64_data
    except Exception as e:
        print(f"Error al convertir a base64: {e}")


def get_pdf_options(output_file):
    return {
        'page-size': 'A4',
        'margin-top': '20mm',
        'margin-right': '0mm',
        'margin-bottom': '10mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'enable-local-file-access': '',
        'title': output_file,
        'no-outline': None,
        'footer-left': 'Página [page]/[topage]',
        'footer-font-size': 9,
        'zoom': 1.2,
    }


def convert_to_float(value_str):
    cleaned_str = value_str.replace('.', '').replace(',', '.').replace('$ ', '')
    return float(cleaned_str)


def convert_rate_to_float(value_str):
    return float(value_str.replace('%', '').replace(',', '.')) / 100
