from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# 1. Define the Immutable Data Blueprint (Pydantic Model)
class ResearchRequest(BaseModel):
    # The prompt must be a string, and cannot be completely empty
    prompt: str = Field(min_length=1, description="The user research query string.")
    # The temperature must be a float bounded between 0.0 and 2.0
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

# 2. Bind the Schema to a POST Endpoint
@app.post("/research")
async def conduct_research(payload: ResearchRequest):
    # FastAPI automatically guarantees 'payload' perfectly matches the schema!
    return {
        "status": "Validated",
        "received_prompt": payload.prompt,
        "applied_temperature": payload.temperature
    }