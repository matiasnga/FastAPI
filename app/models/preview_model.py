from typing import List, Optional
from pydantic import BaseModel


class PreviewRequest(BaseModel):
    companyId: int | None = None
    taxpayerId: int
    period: int
    withholdingGroupingId: Optional[str] = None


class CertificateResponse(BaseModel):
    taxId: int
    netAmount: float
    withholdingAmount: float
    rate: float


class PreviewResponse(BaseModel):
    companyId: int
    taxpayerId: int
    withholdingGroupingId: str | None = None
    period: int
    totalWithholdingAmount: float | None = 0
    certificates: List[CertificateResponse]
