from typing import List, Optional
from pydantic import BaseModel


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
