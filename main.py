from fastapi import FastAPI
from routes.resume_routes import router as resume_router
from utils.logger import logger

app = FastAPI(title="Distributed Job Intelligence (Layers 1+2)", version="0.1")

app.include_router(resume_router, prefix="/api/v1", tags=["analysis"])

@app.get("/")
async def root():
    return {"message": "Distributed Job Intelligence API — running"}

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete")
