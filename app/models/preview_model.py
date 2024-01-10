from typing import List, Optional
from pydantic import BaseModel


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
