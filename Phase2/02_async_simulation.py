import asyncio
from fastapi import FastAPI

app = FastAPI(title="Async Simulation Engine")

@app.get("/simulate-ai")
async def simulate_ai_call():
    """
    Simulates the latency of a real Large Language Model generation.
    By using 'await asyncio.sleep', we tell the server it is free to 
    handle other incoming traffic while this network pause occurs.
    """
    # Simulate a 3-second token generation latency over the network
    await asyncio.sleep(3) 
    
    return {
        "status": "success",
        "data": "This response simulated a non-blocking 3-second AI generation payload."
    }