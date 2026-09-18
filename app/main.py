from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from router.loan import router as loan_router
from app.api import chat, loan_calculator, async_loan

app = FastAPI(
    title="CRED AI Financial Assistant API",
    description="Backend API for CRED AI loan assistant & financial document processing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(loan_router)
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(loan_calculator.router, prefix="/api", tags=["Loan Calculator"])
app.include_router(async_loan.router, prefix="/api", tags=["Redis Async Underwriting"])

# Mount static frontend directory if it exists
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CRED AI API"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Financial Assistant API! Go to /docs for Swagger."}
