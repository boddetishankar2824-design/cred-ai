from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    This is the endpoint the PHP frontend will call.
    It takes the user's message, sends it to the AI service (which handles RAG),
    and returns the AI's response along with the documents it used.
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    try:
        # Call our AI Service layer (which handles LangChain & LLM logic)
        reply, docs = await ai_service.get_chat_response(
            user_message=request.message,
            history=request.history
        )
        
        return ChatResponse(reply=reply, source_documents=docs)
    
    except Exception as e:
        # Catch any errors (like OpenAI API being down) and return a clean 500 error
        raise HTTPException(status_code=500, detail=str(e))
