from fastapi import APIRouter

from app.dto.request.generate_base_64_request_dto import GenerateBase64Request
from app.dto.response.preview_response_dto import PreviewResponse
from app.dto.request.preview_request_dto import PreviewRequest
from app.dto.response.generate_base_64_response_dto import GenerateBase64Response
from app.services import preview_service, generate_base_64_service

router = APIRouter()


@router.get("/v1/certificates", response_model=PreviewResponse)
def get_preview(taxpayerId: int, period: int, withholdingGroupingId: str | None = None):
    request_data = PreviewRequest(companyId=30716829436, taxpayerId=taxpayerId, period=period,
                                  withholdingGroupingId=withholdingGroupingId)
    response = preview_service.get_preview_response(request_data)
    return response


@router.post("/v1/certificates", response_model=GenerateBase64Response)
def generate_base64(generateBase64Request: GenerateBase64Request):
    company_id = 30716829436
    response = generate_base_64_service.generate_base_64_file(generateBase64Request, company_id)
    return response
