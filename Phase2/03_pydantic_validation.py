from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# 1. Initialize our central web application orchestrator
app = FastAPI(title="Pydantic Ingestion Engine")

# 2. Construct the strict schema blueprint for incoming client payloads
class RAGQuerySchema(BaseModel):
    # Field(...) means this key is strictly REQUIRED by the backend
    question: str = Field(
        ..., 
        min_length=3, 
        max_length=500,
        description="The primary question or prompt intended for the RAG engine" # Not a check, just a description
    )
    # ge = Greater than or equal to, le = Less than or equal to
    max_answers: int = Field(
        default=1, 
        ge=1, 
        le=5, 
        description="The maximum number of context chunks requested from storage"
    )
    # Tell Pydantic to strictly reject any unlisted keys
    model_config = {
        "extra": "forbid"
    }
    # if you "allow"
    # will collect the extra two strings and two numbers, preserve them, 
    # and place them inside a hidden dictionary attribute named payload.model_extra

# 3. Create a secure POST route that consumes your data schema blueprint
@app.post("/ask")
async def process_rag_query(payload: RAGQuerySchema):
    """
    Receives incoming request traffic. FastAPI automatically runs 
    the raw JSON body through RAGQuerySchema before passing it here.
    """
    # At this line, the payload is verified as completely safe and sanitised!
    processed_prompt = payload.question.strip()
    
    return {
        "status": "validated_and_approved",
        "received_question": processed_prompt,
        "allocated_chunks": payload.max_answers
    }