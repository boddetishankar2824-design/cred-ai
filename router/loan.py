from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel

router = APIRouter(prefix="/api/loan", tags=["Loan"])

class ChatRequest(BaseModel):
    message: str

class LoanApplication(BaseModel):
    applicant_name: str
    income: float
    loan_amount: float

@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    return {
        "reply": f"AI Assistant response to: '{request.message}'. Based on your financial records, your credit profile looks strong!"
    }

@router.post("/upload")
async def upload_document(
    doc_name: str = Form(...),
    doc_type: str = Form(...),
    file: UploadFile = File(...)
):
    return {
        "status": "success",
        "filename": file.filename,
        "doc_name": doc_name,
        "doc_type": doc_type,
        "message": "Document uploaded and parsed successfully."
    }

@router.post("/apply")
async def apply_loan(application: LoanApplication):
    approved = application.income * 5 >= application.loan_amount
    return {
        "status": "approved" if approved else "under_review",
        "applicant": application.applicant_name,
        "max_eligible_amount": application.income * 5
    }
