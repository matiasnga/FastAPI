import logging

from fastapi import APIRouter
from app.models.preview_model import PreviewRequest, PreviewResponse
from app.models.generate_base_64_model import GenerateBase64Request, GenerateBase64Response
from app.services import preview_service

router = APIRouter()


@router.get("/v1/certificates", response_model=PreviewResponse)
def get_preview(taxpayerId: int, period: int, withholdingGroupingId: str | None = None):
    request_data = PreviewRequest(companyId=30716829436, taxpayerId=taxpayerId, period=period,
                                  withholdingGroupingId=withholdingGroupingId)
    response_preview = preview_service.get_preview_response(request_data)
    logging.info(response_preview)
    return response_preview




@router.post("/v1/certificates", response_model=GenerateBase64Response)
def generate_base64(generateBase64Request: GenerateBase64Request):
    response = GenerateBase64Response()
    return response
