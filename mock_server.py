import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio
import urllib.request
import urllib.error
import base64
import io
import PyPDF2

# Global state to act as our "In-Memory Vector Database"
uploaded_document_text = ""

# Simple .env parser to avoid needing python-dotenv pip package
def load_env():
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    env_vars[key.strip()] = val.strip()
    except FileNotFoundError:
        pass
    return env_vars

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

# Global cache for repeated questions
response_cache = {}

class MockAIService:
    def get_chat_response(self, user_message):
        # 1. Apply Guardrails before anything else
        guardrail_error = check_guardrails(user_message)
        if guardrail_error:
            return guardrail_error, []
            
        cache_key = user_message.strip().lower()
        if cache_key in response_cache:
            return response_cache[cache_key]
            
        # Reload env variables on every request so we don't have to restart the server
        # when the user updates the .env file!
        self.env = load_env()
        api_key = self.env.get("GROQ_API_KEY", "your_groq_api_key_here")
        
        # If the user has added a real API key, use Groq!
        if api_key and api_key != "your_groq_api_key_here":
            try:
                # Groq provides an extremely fast OpenAI-compatible endpoint
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                    "User-Agent": "CredBuddha-App/1.0"
                }
                
                global uploaded_document_text
                
                # Limit size to prevent Groq API Payload Too Large (413)
                max_chars = 15000
                doc_text = uploaded_document_text[:max_chars] if uploaded_document_text else ""
                
                if doc_text:
                    system_prompt = (
                        "You are the CredBuddha Financial AI Assistant. "
                        "You must ONLY answer questions related to financial matters, loans, company policies, and the provided document. "
                        "If the user asks an off-topic question (e.g., weather, temperature, sports, general knowledge), politely decline and state that you are a company financial assistant. "
                        "You must use ONLY the following retrieved document to answer the user's question. "
                        "Crucially, be highly resilient to typos, incorrect spelling, and bad grammar. Infer the user's intent. "
                        "CRITICAL: You must format your ENTIRE response using clean, semantic HTML tags (e.g., <p>, <ul>, <li>, <strong>, <h3>, <table class='styled-table'>, <tr>, <th>, <td>). "
                        "Do NOT use any Markdown formatting like **bold** or | tables. Your response must be pure HTML.\n\n"
                        "If the question is off-topic or the answer is not in the document, you MUST reply exactly with: 'I am a CredBuddha financial assistant. I can only assist you with company-related matters like loans, expenses, and policies.'\n\n"
                        f"--- UPLOADED DOCUMENT START ---\n{doc_text}\n--- UPLOADED DOCUMENT END ---\n"
                    )
                else:
                    system_prompt = (
                        "You are the CredBuddha Financial AI Assistant. "
                        "You must ONLY answer questions related to financial matters, loans, company policies, and the provided document. "
                        "If the user asks an off-topic question (e.g., weather, temperature, sports, general knowledge), politely decline and state that you are a company financial assistant. "
                        "You must use the following retrieved documents to answer the user's question:\n"
                        "- Bank Statement: Spent $450 on Food.\n"
                        "- Invoice #10294: Total tax applied is $45.20 at a 10% rate.\n"
                        "- Company Policy: Dinner expenses up to $50 are reimbursable.\n\n"
                        "Crucially, be highly resilient to typos, incorrect spelling, and bad grammar. Infer the user's intent. "
                        "CRITICAL: You must format your ENTIRE response using clean, semantic HTML tags (e.g., <p>, <ul>, <li>, <strong>, <h3>, <table class='styled-table'>, <tr>, <th>, <td>). "
                        "Do NOT use any Markdown formatting like **bold** or | tables. Your response must be pure HTML.\n\n"
                        "If the question is off-topic or the answer is still not in the documents, you MUST reply exactly with: 'I am a CredBuddha financial assistant. I can only assist you with company-related matters like loans, expenses, and policies.'"
                    )
                
                data = {
                    "model": "groq/compound-mini",  # Updated Groq model
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ]
                }
                
                req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
                response = urllib.request.urlopen(req, timeout=10)
                result = json.loads(response.read().decode('utf-8'))
                
                reply = result['choices'][0]['message']['content']
                docs = ["Groq Model Generated (Llama 3)", "RAG Context Document injected via prompt"]
                return reply, docs
                
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    error_msg = (
                        "Groq API Error 429: Rate limit exceeded! "
                        "Don't worry, I am automatically falling back to the local Mock RAG mode so you can keep testing the UI."
                    )
                elif e.code == 401:
                    error_msg = "Groq API Error 401: Your API key is invalid or incorrect. Falling back to local Mock RAG mode."
                else:
                    error_msg = f"Groq API Error {e.code}. Falling back to local Mock RAG mode."
                
                # Proceed to fallback below
                print(error_msg)
                
            except Exception as e:
                error_msg = f"Failed to connect to Groq API: {str(e)}. Falling back to local Mock RAG mode."
                print(error_msg)
                
        # --- MOCK FALLBACK ---
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
            
        if 'error_msg' in locals():
            reply = f"**{error_msg}**\n\n---\n\n{reply}"
            
        response_cache[cache_key] = (reply, docs)
        return reply, docs

ai_service = MockAIService()

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                user_message = data.get('message', '')
                
                reply, docs = ai_service.get_chat_response(user_message)
                
                response_data = {
                    "reply": reply,
                    "source_documents": docs
                }
                
                self._set_headers(200)
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"detail": str(e)}).encode('utf-8'))
        
        elif self.path == '/api/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename', '')
                base64_content = data.get('content', '')
                
                # Decode Base64
                file_bytes = base64.b64decode(base64_content)
                extracted_text = ""
                
                # Check if it's a Text file or PDF
                if filename.lower().endswith('.txt'):
                    extracted_text = file_bytes.decode('utf-8')
                else:
                    # Extract text using PyPDF2
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        if text:
                            extracted_text += text + "\n"
                
                # Save to global variable (In-Memory RAG)
                global uploaded_document_text
                uploaded_document_text = extracted_text.strip()
                
                print(f"Successfully processed uploaded PDF: {filename} ({len(uploaded_document_text)} characters extracted)")
                
                self._set_headers(200)
                self.wfile.write(json.dumps({"message": "File processed successfully"}).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"detail": str(e)}).encode('utf-8'))
                
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"detail": "Not Found"}).encode('utf-8'))

def run_server(port=8001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Starting mock backend server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
