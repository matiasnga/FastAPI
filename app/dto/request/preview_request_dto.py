from typing import Optional
from pydantic import BaseModel


class PreviewRequest(BaseModel):
    companyId: int | None = None
    taxpayerId: int
    period: int
    withholdingGroupingId: Optional[str] = None
