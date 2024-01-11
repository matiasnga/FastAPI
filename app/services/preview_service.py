from app.services.utils_service import convert_to_float, convert_rate_to_float

from app.repository import s3_repository
from app.dto.response.preview_response_dto import PreviewResponse
from app.dto.request.preview_request_dto import PreviewRequest


def get_preview_response(preview_request: PreviewRequest):
    json_certificates = s3_repository.read_file_from_s3(preview_request.companyId, preview_request.period)
    response_preview = PreviewResponse(**preview_request.model_dump(), certificates=[])
    dictionary_response = response_preview.model_dump()
    taxpayer_id = str(preview_request.taxpayerId)
    taxpayer_id = f"{taxpayer_id[:2]}-{taxpayer_id[2:10]}-{taxpayer_id[-1]}"
    certificates_filtered = []
    for certificate in json_certificates:
        if certificate['CUITContribuyente'] == taxpayer_id \
                and certificate['IdAgrupacionRetenciones'] == preview_request.withholdingGroupingId:
            certificates_filtered.append(certificate)
            dictionary_response['certificates'].append({'taxId': certificate['Impuesto'],
                                                        'netAmount': convert_to_float(
                                                            certificate['Retenciones'][0]['BaseRetencion']),
                                                        'withholdingAmount': convert_to_float(
                                                            certificate['Retenciones'][0]['Retencion']),
                                                        'rate': convert_rate_to_float(
                                                            certificate['Retenciones'][0]['Alicuota'])
                                                        })

    totals_by_tax_id = {}
    total_withholding_amount = 0

    for certificate in dictionary_response["certificates"]:
        tax_id = certificate["taxId"]
        net_amount = certificate["netAmount"]
        withholding_amount = certificate["withholdingAmount"]
        rate = certificate["rate"]
        total_withholding_amount += withholding_amount

        # Si el taxId ya existe en el diccionario, acumular los montos
        if tax_id in totals_by_tax_id:
            totals_by_tax_id[tax_id]["netAmount"] += net_amount
            totals_by_tax_id[tax_id]["withholdingAmount"] += withholding_amount
            current_count = totals_by_tax_id[tax_id]["count"]
            new_count = current_count + 1
            totals_by_tax_id[tax_id]["rate"] = (current_count * totals_by_tax_id[tax_id]["rate"] + rate) / new_count
            totals_by_tax_id[tax_id]["count"] = new_count
        # Si el taxId no existe, agregar un nuevo objeto al diccionario
        else:
            totals_by_tax_id[tax_id] = {
                "taxId": tax_id,
                "netAmount": net_amount,
                "withholdingAmount": withholding_amount,
                "rate": rate,
                "count": 1  # Inicializar el contador en 1
            }

    # Actualizar la lista de certificados con los totales por taxId
    dictionary_response["certificates"] = list(totals_by_tax_id.values())
    dictionary_response["totalWithholdingAmount"] = total_withholding_amount

    for certificate in dictionary_response.get("certificates", []):
        certificate['withholdingAmount'] = round(certificate['withholdingAmount'], 2)
        certificate.pop("count", None)
    dictionary_response['totalWithholdingAmount'] = round(dictionary_response['totalWithholdingAmount'], 2)
    return PreviewResponse(**dictionary_response)
