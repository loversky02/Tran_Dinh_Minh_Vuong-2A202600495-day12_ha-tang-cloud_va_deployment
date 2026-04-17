"""
🚀 Production-Ready AI Agent
Day 12 Lab - Final Project

Features:
  ✅ Environment-based configuration
  ✅ Structured JSON logging
  ✅ Health & readiness checks
  ✅ Graceful shutdown
  ✅ API key authentication
  ✅ Rate limiting (in-memory)
  ✅ Input validation
  ✅ Security headers
  ✅ CORS configuration

Deploy: Railway
URL: https://wonderful-delight-production-9390.up.railway.app
"""
import os
import time
import signal
import logging
import json
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from collections import defaultdict, deque

from fastapi import FastAPI, HTTPException, Request, Response, Security, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field
import uvicorn
from utils.mock_llm import ask

# ============================================================
# Configuration
# ============================================================
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
PORT = int(os.getenv("PORT", 8000))
API_KEY = os.getenv("AGENT_API_KEY", "demo-key-change-me")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))

# ============================================================
# Logging
# ============================================================
logging.basicConfig(
    level=logging.INFO if ENVIRONMENT == "production" else logging.DEBUG,
    format='{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

# ============================================================
# Global State
# ============================================================
START_TIME = time.time()
_is_ready = False
_in_flight_requests = 0

# Rate limiter (in-memory, simple sliding window)
_rate_limit_windows = defaultdict(deque)

# ============================================================
# Lifecycle Management
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    
    # Startup
    logger.info(json.dumps({
        "event": "startup",
        "environment": ENVIRONMENT,
        "port": PORT,
        "version": "2.0.0"
    }))
    time.sleep(0.1)  # Simulate initialization
    _is_ready = True
    logger.info("Agent ready to serve requests")
    
    yield
    
    # Shutdown
    _is_ready = False
    logger.info("Graceful shutdown initiated")
    
    # Wait for in-flight requests
    timeout = 30
    elapsed = 0
    while _in_flight_requests > 0 and elapsed < timeout:
        logger.info(f"Waiting for {_in_flight_requests} in-flight requests...")
        time.sleep(1)
        elapsed += 1
    
    logger.info("Shutdown complete")

# ============================================================
# FastAPI App
# ============================================================
app = FastAPI(
    title="Production AI Agent",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs" if ENVIRONMENT != "production" else None,
)

# ============================================================
# Middleware
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.middleware("http")
async def track_requests(request: Request, call_next):
    """Track in-flight requests for graceful shutdown"""
    global _in_flight_requests
    _in_flight_requests += 1
    try:
        response = await call_next(request)
        return response
    finally:
        _in_flight_requests -= 1

@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Add security headers"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# ============================================================
# Authentication
# ============================================================
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verify API key from header"""
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Include header: X-API-Key: <your-key>"
        )
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# ============================================================
# Rate Limiting
# ============================================================
def check_rate_limit(user_id: str = "default"):
    """Simple in-memory rate limiter"""
    now = time.time()
    window = _rate_limit_windows[user_id]
    
    # Remove old timestamps
    while window and window[0] < now - 60:
        window.popleft()
    
    if len(window) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT} requests per minute."
        )
    
    window.append(now)

# ============================================================
# Request Models
# ============================================================
class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)

# ============================================================
# Endpoints
# ============================================================
@app.get("/")
def root():
    """Public endpoint"""
    return {
        "app": "Production AI Agent",
        "version": "2.0.0",
        "environment": ENVIRONMENT,
        "docs": "/docs" if ENVIRONMENT != "production" else "disabled",
        "health": "/health",
        "ready": "/ready",
    }

@app.post("/ask")
async def ask_agent(
    body: AskRequest,
    request: Request,
    _key: str = Depends(verify_api_key),
):
    """
    Protected endpoint - requires API key
    Rate limited to prevent abuse
    """
    # Rate limiting
    check_rate_limit("default")
    
    # Log request
    logger.info(json.dumps({
        "event": "request",
        "question_length": len(body.question),
        "client_ip": request.client.host,
    }))
    
    # Call LLM
    answer = ask(body.question)
    
    # Log response
    logger.info(json.dumps({
        "event": "response",
        "answer_length": len(answer),
    }))
    
    return {
        "question": body.question,
        "answer": answer,
        "platform": "Railway",
        "version": "2.0.0",
    }

@app.get("/health")
def health():
    """
    Liveness probe - Platform checks if agent is alive
    Returns 200 if healthy, non-200 if degraded
    """
    uptime = round(time.time() - START_TIME, 1)
    
    return {
        "status": "ok",
        "uptime_seconds": uptime,
        "version": "2.0.0",
        "environment": ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@app.get("/ready")
def ready():
    """
    Readiness probe - Is agent ready to serve traffic?
    Returns 503 if not ready (startup/shutdown)
    """
    if not _is_ready:
        raise HTTPException(503, "Agent not ready")
    
    return {
        "ready": True,
        "in_flight_requests": _in_flight_requests,
    }

@app.get("/metrics")
def metrics():
    """Basic metrics endpoint"""
    return {
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "in_flight_requests": _in_flight_requests,
        "environment": ENVIRONMENT,
        "version": "2.0.0",
    }

# ============================================================
# Signal Handlers
# ============================================================
def handle_sigterm(signum, frame):
    """Handle SIGTERM for graceful shutdown"""
    logger.info(f"Received signal {signum} - initiating graceful shutdown")

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)

# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    logger.info(f"Starting Production AI Agent on port {PORT}")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"API Key configured: {'Yes' if API_KEY != 'demo-key-change-me' else 'No (using demo key)'}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        timeout_graceful_shutdown=30,
    )
