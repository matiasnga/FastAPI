from typing import Optional
from pydantic import BaseModel


class GenerateBase64Request(BaseModel):
    taxpayerId: int
    taxId: int
    period: int
    withholdingGroupingId: Optional[str] = None
