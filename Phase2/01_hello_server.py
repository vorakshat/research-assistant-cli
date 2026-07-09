from fastapi import FastAPI

# 1. Initialize the central API web application object
app = FastAPI(title="AI Engineering Server")

# 2. Bind an HTTP GET method to the root ("/") web pathway
@app.get("/")
def read_root():
    """
    Exposes a public gateway. When an external client visits this path,
    we instantly transmit a structured JSON response back across the web.
    """
    return {"message": "Welcome to your Phase 2 Backend Engine!"}