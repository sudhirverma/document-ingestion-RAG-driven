from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from app.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    embedding = Column(String, nullable=False, comment="Generated embeddings for the document")
