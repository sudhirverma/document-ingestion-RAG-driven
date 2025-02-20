from fastapi import FastAPI
from app.api import ingestion, qna, selection
from app.db import init_db

app = FastAPI()

# Include routers
app.include_router(ingestion.router, prefix="/api/ingestion", tags=["Ingestion"])
app.include_router(qna.router, prefix="/api/qna", tags=["Q&A"])
app.include_router(selection.router, prefix="/api/selection", tags=["Selection"])

# Initialize database
@app.on_event("startup")
async def startup():
    await init_db()
