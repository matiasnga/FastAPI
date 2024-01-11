from pydantic import BaseModel
from typing import Optional


class GenerateBase64Request(BaseModel):
    taxpayerId: int
    taxId: int
    period: int
    withholdingGroupingId: Optional[str] = None


class GenerateBase64Response(BaseModel):
    filename: str | None = None
    base64: str | None = None
