from fastapi import FastAPI, Request, Response
from prometheus_client import generate_latest, Histogram, Counter, CONTENT_TYPE_LATEST
import json
import time
import os
import asyncio

app = FastAPI()

# Prometheus Metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "HTTP Request Latency", ["method", "endpoint"])

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    endpoint = request.url.path
    method = request.method
    
    response = await call_next(request)
    
    # Don't track latency for /metrics endpoint itself to keep it clean
    if endpoint != "/metrics":
        latency = time.time() - start_time
        REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)
        
    return response

@app.get("/metrics")
async def metrics():
    # Expose prometheus metrics
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.post("/api/simulate")
async def simulate(request: Request):
    """ The endpoint the load generator calls """
    delay = 0
    # Read config to get artificial delay dynamically without restart
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                delay = config.get("delay_ms", 0)
        except Exception:
            pass
            
    if delay > 0:
        await asyncio.sleep(delay / 1000.0)
        
    return {"status": "success", "delay_applied_ms": delay}
