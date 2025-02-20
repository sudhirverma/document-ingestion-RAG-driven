from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.document import Document
from app.db import get_db

router = APIRouter()

@router.get("/")
async def select_documents(
    ids: list[int] = Query(..., description="List of document IDs"),
    db_context = Depends(get_db),
):
    async with db_context as db:
        result = await db.execute(select(Document).filter(Document.id.in_(ids)))
        documents = result.scalars().all()
        return documents
