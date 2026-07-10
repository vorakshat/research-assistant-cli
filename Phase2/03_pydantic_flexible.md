## Accessing Extra Fields Not Defined in Your Pydantic Model

By default, if a client sends extra fields in their JSON payload that are **not** explicitly declared in your Pydantic model (`ResearchRequest`), FastAPI and Pydantic will simply **ignore them**.

They will not trigger a validation error, but they will be stripped out during parsing. This means if you try to call `payload.someNewField`, Python will throw an `AttributeError` because that field was never initialized on your object.

If you want to catch or access fields that you haven't explicitly defined or validated, you have **three clean architectural approaches** depending on what you are trying to achieve:

---

### Option 1: Access the Raw JSON Directly (Quickest)

If you want standard Pydantic parsing for your core fields but still want to occasionally peek at unvalidated data, you can inject FastAPI's `Request` object directly into your function. This allows you to read the raw incoming JSON payload alongside your validated model:

```python
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class ResearchRequest(BaseModel):
    prompt: str
    temperature: float = 0.7

@app.post("/research")
async def conduct_research(payload: ResearchRequest, request: Request):
    # 1. Grab the raw, unvalidated JSON dictionary package
    raw_json = await request.json()
    
    # 2. Extract fields that bypassed Pydantic validation safely
    some_new_field = raw_json.get("someNewField", "default_value")
    
    return {
        "validated_prompt": payload.prompt,
        "unvalidated_extra_field": some_new_field
    }

```

---

### Option 2: Change Pydantic's Settings to "Allow" Extra Fields

You can configure your Pydantic model's inner configurations to store any extra fields sent by the client inside a special internal dictionary named `__pydantic_extra__`.

To do this, update your model settings to use `extra="allow"`:

```python
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

app = FastAPI()

class ResearchRequest(BaseModel):
    # Tell Pydantic to collect unlisted fields instead of ignoring them
    model_config = ConfigDict(extra="allow")
    
    prompt: str
    temperature: float = 0.7

@app.post("/research")
async def conduct_research(payload: ResearchRequest):
    # Access regular fields with standard dot notation
    user_prompt = payload.prompt 
    
    # Access unvalidated fields directly from the extra storage vault
    # This prevents your app from crashing if the field is missing!
    extra_field = getattr(payload, "someNewField", "default_value")
    
    return {
        "prompt": user_prompt,
        "extra_data_collected": extra_field,
        "all_extra_fields": payload.__pydantic_extra__ # Shows everything extra
    }

```

---

### Option 3: Accept a Flexible Wildcard Dictionary

If you are building an endpoint where you don't want to enforce *any* rigid structure or validation on certain fields (for instance, if you are letting a user pass an arbitrary dictionary of custom metadata for your RAG pipeline), you can type-hint a field directly as a standard Python `dict`:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ResearchRequest(BaseModel):
    prompt: str
    # This field accepts any valid JSON object without enforcing type checks!
    custom_metadata: dict = {} 

@app.post("/research")
async def conduct_research(payload: ResearchRequest):
    # Read it naturally like a normal Python dictionary
    new_field = payload.custom_metadata.get("someNewField", "fallback")
    
    return {
        "prompt": payload.prompt,
        "extracted_metadata_value": new_field
    }

```

---

## Which one should you choose for Project 2?

For your upcoming **Docs Q&A Backend**, **Option 3** is highly favored when managing advanced RAG pipelines. When users upload documents, they often want to tag them with highly unpredictable data (e.g., `{"department": "HR", "year": 2026, "importance": "high"}`). Wrapping those inside a dedicated `metadata: dict` field keeps your endpoint secure while giving your vector database maximum flexibility.

Does this clarify how Pydantic seals your server gateways while allowing room for dynamic payloads? If you're ready, we can formally introduce how **PostgreSQL** handles structured data storage!