from pydantic import BaseModel


class GenerateBase64Response(BaseModel):
    filename: str | None = None
    base64: str | None = None
