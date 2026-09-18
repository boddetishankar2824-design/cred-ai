from fastapi import APIRouter, HTTPException
from app.schemas import LoanEligibilityRequest, LoanEligibilityResponse
from app.services.loan_service import loan_service

router = APIRouter()

@router.post("/loan/eligibility", response_model=LoanEligibilityResponse)
async def check_loan_eligibility(request: LoanEligibilityRequest):
    """
    Check loan eligibility and get estimated EMI & interest rate.
    """
    if request.monthly_income <= 0:
        raise HTTPException(status_code=400, detail="Monthly income must be greater than zero.")
        
    if request.requested_amount <= 0:
        raise HTTPException(status_code=400, detail="Requested loan amount must be greater than zero.")
        
    try:
        response = loan_service.calculate_eligibility(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
