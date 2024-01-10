from fastapi import FastAPI
from .routers import certificates

app = FastAPI()

app.include_router(certificates.router)


@app.get("/health")
def health_check():
    return {"Status": "UP"}
