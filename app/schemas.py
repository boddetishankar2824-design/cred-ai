from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    reply: str
    source_documents: Optional[List[str]] = []

# --- New Feature Schemas ---
class LoanEligibilityRequest(BaseModel):
    monthly_income: float
    requested_amount: float
    tenure_months: int = 24
    credit_score: Optional[int] = 750

class LoanEligibilityResponse(BaseModel):
    is_eligible: bool
    max_loan_amount: float
    estimated_emi: float
    interest_rate: float
    recommendation: str
