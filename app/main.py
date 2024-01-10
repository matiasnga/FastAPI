from fastapi import FastAPI
from .routers import certificates_router
app = FastAPI()

app.include_router(certificates_router.router)


@app.get("/health", include_in_schema=False)
def health():
    return {"Status": "UP"}
