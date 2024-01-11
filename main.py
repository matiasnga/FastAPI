import uvicorn
from fastapi import FastAPI
from app.routers import certificates_router

app = FastAPI()

app.include_router(certificates_router.router)


@app.get("/health", include_in_schema=False)
def health():
    return {"Status": "UP"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
