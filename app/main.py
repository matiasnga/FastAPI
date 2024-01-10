from fastapi import FastAPI
from .routers import certificates

app = FastAPI()

app.include_router(certificates.router)


@app.get("/health", include_in_schema=False)
def health():
    return {"Status": "UP"}
