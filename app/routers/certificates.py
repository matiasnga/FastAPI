from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional


class PreviewRequest(BaseModel):
    taxpayerId: int
    period: int
    withholdingGroupingId: Optional[int] = None


class CertificateResponse(BaseModel):
    taxId: int
    netAmount: float
    withholdingAmount: float
    rate: float


class PreviewResponse(BaseModel):
    companyId: int | None = 30716829436
    taxpayerId: int
    withholdingGroupingId: int | None = None
    period: int
    totalWithholdingAmount: float | None = 0
    certificates: List[CertificateResponse]


class GenerateBase64Request(BaseModel):
    taxpayerId: int
    taxId: int
    period: int
    withholdingGroupingId: Optional[int] = None


class GenerateBase64Response(BaseModel):
    filename: str | None = None
    base64: str | None = None


router = APIRouter()


@router.get("/v1/certificates", response_model=PreviewResponse)
def get_preview(taxpayerId: int, period: int, withholdingGroupingId: int | None = None):
    request_data = PreviewRequest(taxpayerId=taxpayerId, period=period, withholdingGroupingId=withholdingGroupingId)
    certificate_1 = CertificateResponse(taxId=216, netAmount=1222.0, withholdingAmount=12.2, rate=0.1)
    certificate_2 = CertificateResponse(taxId=217, netAmount=222.0, withholdingAmount=2.2, rate=0.02)
    response_preview = PreviewResponse(**request_data.model_dump(), certificates=[certificate_1, certificate_2])
    return response_preview


@router.post("/v1/certificates", response_model=GenerateBase64Response)
def generate_base64(generateBase64Request: GenerateBase64Request):
    response = GenerateBase64Response()
    return response
