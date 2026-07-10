from fastapi import FastAPI

# 1. Initialize the Server Application Instance
app = FastAPI()

# 2. Define an Entry Gateway (Route)
@app.get("/")
async def read_root():
    # 3. Ship back a structured JSON payload
    return {"message": "Hello World! Your AI Backend is officially live."}