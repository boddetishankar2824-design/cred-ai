from fastapi import APIRouter, HTTPException, status
import datetime
from app.schemas import AsyncLoanApplicationRequest, AsyncLoanJobResponse, LoanJobStatusResponse
from app.services.queue_service import queue_service

router = APIRouter()

@router.post(
    "/loan/apply-async", 
    response_model=AsyncLoanJobResponse, 
    status_code=status.HTTP_202_ACCEPTED
)
async def submit_async_loan_application(request: AsyncLoanApplicationRequest):
    """
    Submits a loan application to the Redis Queue for background underwriting & credit scoring.
    Returns HTTP 202 Accepted immediately with a unique job_id for polling.
    """
    if request.monthly_income <= 0:
        raise HTTPException(status_code=400, detail="Monthly income must be greater than zero.")
        
    if request.requested_amount <= 0:
        raise HTTPException(status_code=400, detail="Requested loan amount must be greater than zero.")

    job_id = queue_service.enqueue_loan_application(request)
    
    return AsyncLoanJobResponse(
        job_id=job_id,
        status="queued",
        created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        estimated_wait_seconds=4,
        message="Application queued successfully into Redis for background underwriting."
    )

@router.get("/loan/job-status/{job_id}", response_model=LoanJobStatusResponse)
async def get_loan_job_status(job_id: str):
    """
    Polls Redis to get the current progress percentage and result of a queued loan job.
    """
    job = queue_service.get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Loan job '{job_id}' not found in Redis queue.")
        
    return LoanJobStatusResponse(
        job_id=job["job_id"],
        status=job["status"],
        progress_percentage=job["progress_percentage"],
        result=job.get("result")
    )
