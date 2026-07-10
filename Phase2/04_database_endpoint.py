import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from google import genai
from google.genai import types 

# Import our infrastructure tools and blueprints from our separate files
from database import AsyncSessionLocal
from models import Document, Chunk

# 1. Force find the parent folder's .env file explicitly
root_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=root_dir / ".env")

app = FastAPI()

# 2. Clean initialization: Let the SDK look for GEMINI_API_KEY naturally in environment memory
ai_client = genai.Client()

# The Database Session Dependency Engine
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db  
    finally:
        await db.close()  

# Pydantic Input Schema for Route Protection
class DocumentCreate(BaseModel):
    filename: str = Field(min_length=1, max_length=255, example="attention.pdf")

# POST Route: Write a new Document record to Postgres
@app.post("/documents")
async def create_document(payload: DocumentCreate, db: AsyncSession = Depends(get_db)):
    new_doc = Document(filename=payload.filename)
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    
    return {
        "status": "Success",
        "message": "Document record permanently saved to local PostgreSQL.",
        "data": {
            "id": new_doc.id,
            "filename": new_doc.filename,
            "uploaded_at": new_doc.uploaded_at
        }
    }

# GET Route: Fetch all Document records from Postgres
@app.get("/documents")
async def list_documents(db: AsyncSession = Depends(get_db)):
    query = select(Document)
    result = await db.execute(query)
    documents_list = result.scalars().all()
    
    return {"documents": [
        {"id": doc.id, "filename": doc.filename, "uploaded_at": doc.uploaded_at}
        for doc in documents_list
    ]}

# Pydantic Input Schema for Inbound Text Payloads
class ChunkIngestPayload(BaseModel):
    raw_text: str = Field(min_length=1, description="The block of document text to process.")

# POST Route: Relational chunk ingestion with vector geometry arrays
@app.post("/documents/{document_id}/chunks")
async def ingest_document_chunks(document_id: int, payload: ChunkIngestPayload, db: AsyncSession = Depends(get_db)):
    doc_query = await db.execute(select(Document).where(Document.id == document_id))
    parent_document = doc_query.scalar_one_or_none()
    
    if not parent_document:
        raise HTTPException(status_code=404, detail="Parent Document record not found.")

    # Slicing text by sentences
    sentences = [s.strip() for s in payload.raw_text.split(".") if s.strip()]
    
    saved_chunks = []
    
    for sentence in sentences:
        try:
            # 🚀 FIXED LINE: Removed 'await' because this method is synchronous!
            response = ai_client.models.embed_content(
                model="text-embedding-004",  # Google's premier embedding model
                contents=sentence
            )
            # Extract the raw float array out of the response structure
            real_embedding = response.embeddings[0].values
            
            # Instantiate our child database model using the live vector payload
            new_chunk = Chunk(
                document_id=document_id,
                content=sentence,
                embedding=real_embedding
            )
            db.add(new_chunk)
            saved_chunks.append(new_chunk)
            
        except Exception as ai_error:
            raise HTTPException(status_code=502, detail=f"Gemini Embedding API failure: {str(ai_error)}")
        
    # Commit the transaction block to persist all child rows atomically
    await db.commit()
    
    return {
        "status": "Success",
        "parent_document": parent_document.filename,
        "chunks_processed": len(saved_chunks),
        "message": f"Successfully mapped and stored {len(saved_chunks)} vector chunks relationally."
    }