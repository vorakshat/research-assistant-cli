from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

# Import the Base master registry notebook we built in database.py
from database import Base

# 1. The Parent Mirror: Maps to the "documents" Table
class Document(Base):
    __tablename__ = "documents"

    # Explicitly map the core schema columns
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Express the Relationship: One Document can have a list of many Chunks
    chunks: Mapped[List["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")


# 2. The Child Mirror: Maps to the "chunks" Table
class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    # The Foreign Key: Locks this column to documents.id
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # The AI Powerhouse: Maps the 1536-dimensional pgvector float array!
    embedding: Mapped[list] = mapped_column(Vector(1536), nullable=True)

    # Express the Relationship: Links this chunk instance back to its unique parent Document object
    document: Mapped["Document"] = relationship(back_populates="chunks")