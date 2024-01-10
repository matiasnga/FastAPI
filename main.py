from fastapi import FastAPI
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


app = FastAPI()


@app.get("/v1/certificates", response_model=PreviewResponse)
def get_preview(taxpayerId: int, period: int, withholdingGroupingId: int | None = None):
    request_data = PreviewRequest(taxpayerId=taxpayerId, period=period, withholdingGroupingId=withholdingGroupingId)
    certificate = CertificateResponse(taxId=216, netAmount=1222.0, withholdingAmount=12.2, rate=0.1)
    response_preview = PreviewResponse(**request_data.dict(), certificates=[certificate])

    return response_preview


@app.get("/health")
def health_check():
    return {"Status": "UP"}
