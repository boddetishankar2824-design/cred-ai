import asyncio
import os
from typing import List, Tuple

# NOTE FOR LATER: When you have an OpenAI API Key, you will uncomment these:
# from langchain_openai import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

class AIService:
    def __init__(self):
        # We will use a mock LLM for now so you can test the API without paying for credits.
        self.is_mock = True

# Global cache for repeated questions
response_cache = {}

def check_guardrails(message: str) -> str:
    """
    Checks the user message against safety and policy guardrails.
    Returns an error message if violated, else None.
    """
    msg_lower = message.lower()
    
    # 1. Profanity / Inappropriate Content
    profanity_list = ["fuck", "shit", "ass", "bitch", "crap", "idiot", "stupid"]
    if any(word in msg_lower for word in profanity_list):
        return "Your message contains inappropriate language. Please maintain a professional tone."
        
    # 2. Prompt Injection / System override attempts
    injection_list = ["ignore previous", "system prompt", "forget your instructions", "you are now", "bypass"]
    if any(phrase in msg_lower for phrase in injection_list):
        return "I cannot comply with requests that attempt to override my core instructions."
        
    # 3. Explicit off-topic topics (catch-all before hitting the model)
    off_topic_list = ["weather", "temperature", "sport", "movie", "news", "joke", "politics"]
    if any(word in msg_lower for word in off_topic_list):
        return "I am a CredBuddha financial assistant. I cannot answer off-topic questions. Please ask me about loans, expenses, or company policies!"
        
    return None

    async def get_chat_response(self, user_message: str, history: List[dict] = None) -> Tuple[str, List[str]]:
        """
        Simulates sending the user's message to an LLM using RAG.
        Returns a tuple of (AI_Reply, List_of_Source_Documents).
        """
        # Apply Guardrails first
        guardrail_error = check_guardrails(user_message)
        if guardrail_error:
            await asyncio.sleep(0.5)
            return guardrail_error, []
            
        cache_key = user_message.strip().lower()
        if cache_key in response_cache:
            return response_cache[cache_key]
            
        # Simulate network delay to make it feel like a real API call
        await asyncio.sleep(1.5)

        # Basic keyword routing for the mock (to show RAG in action)
        user_message_lower = user_message.lower()

        if any(word in user_message_lower for word in ["spend", "spent", "food", "din", "eat", "cost"]):
            reply = "<h3>🍔 Food & Dining Expenses</h3><p>Based on your uploaded Bank Statement, you spent <strong>$450</strong> on Food and Dining this month.</p>"
            docs = ["Bank Statement - October 2023 (Page 2)"]
        
        elif any(word in user_message_lower for word in ["tax", "invoice", "bill", "chrg", "charg", "pay"]):
            reply = "<h3>🧾 Invoice & Tax Details</h3><p>I found the invoice. The total tax applied is <strong>$45.20</strong> at a <strong>10%</strong> rate.</p>"
            docs = ["Invoice #10294 (Page 1)"]
            
        elif any(word in user_message_lower for word in ["policy", "expense", "reimburs", "rule", "trav"]):
            reply = "<h3>💼 Company Expense Policy</h3><p>According to the company policy, dinner expenses up to <strong>$50</strong> are fully reimbursable if you are traveling.</p>"
            docs = ["Company Expense Policy V2.pdf (Section 3.1)"]
            
        elif any(word in user_message_lower for word in ["loan", "10000", "step", "apply", "want", "wnat", "get", "money"]):
            reply = "<h3>🚀 Loan Application Process</h3><p>To apply for a loan, please follow these 3 steps:</p><ul><li><strong>Step 1:</strong> Fill out your details</li><li><strong>Step 2:</strong> Upload your documents</li><li><strong>Step 3:</strong> Get instant approval!</li></ul>"
            docs = ["CredBuddha Loan Application Process"]
            
        elif any(word in user_message_lower for word in ["weather", "temperature", "sport", "movie", "news", "joke"]):
            reply = "I am a CredBuddha financial assistant. I cannot answer off-topic questions like this. Please ask me about loans, expenses, or company policies!"
            docs = []
            
        else:
            reply = (
                "<p>I'm sorry, I couldn't quite understand that or find it in your documents. Could you please rephrase or check the spelling?</p>"
                "<p><em>For example, you can ask about your food expenses, tax invoices, or company policies.</em></p>"
                f"<p style='font-size:0.8em; color:gray;'>(Mock Mode - You said: '{user_message}')</p>"
            )
            docs = []

        response_cache[cache_key] = (reply, docs)
        return reply, docs

# Singleton instance to be used across the app
ai_service = AIService()
