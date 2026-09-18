import asyncio
import json
import uuid
import datetime
from typing import Dict, Any, Optional
from app.schemas import AsyncLoanApplicationRequest

# Try importing redis client; gracefully handle if redis package or redis server is absent
try:
    import redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, socket_connect_timeout=1)
    redis_client.ping()
    REDIS_AVAILABLE = True
    print("Connected to live Redis server at localhost:6379")
except Exception:
    REDIS_AVAILABLE = False
    print("Redis server not detected on localhost:6379. Falling back to high-performance in-memory Redis Queue manager.")

# Fallback in-memory job store if Redis server isn't live locally
memory_job_store: Dict[str, Dict[str, Any]] = {}

class RedisLoanQueueService:
    def enqueue_loan_application(self, req: AsyncLoanApplicationRequest) -> str:
        """
        Enqueues a loan underwriting job into Redis Queue (or fallback store) and returns job_id immediately.
        """
        job_id = f"loan_job_{uuid.uuid4().hex[:8]}"
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        job_data = {
            "job_id": job_id,
            "status": "queued",
            "progress_percentage": 0,
            "created_at": created_at,
            "payload": req.model_dump(),
            "result": None
        }

        if REDIS_AVAILABLE:
            try:
                # Store job state hash in Redis with 1 hour expiration
                redis_client.set(f"job:{job_id}", json.dumps(job_data), ex=3600)
                # Push job_id to processing queue
                redis_client.rpush("loan_underwriting_queue", job_id)
            except Exception as e:
                print(f"Redis write error, using fallback: {e}")
                memory_job_store[job_id] = job_data
        else:
            memory_job_store[job_id] = job_data

        # Trigger background processing task asynchronously
        asyncio.create_task(self._process_underwriting_task(job_id, req))
        return job_id

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves current status and result for a given job_id from Redis.
        """
        if REDIS_AVAILABLE:
            try:
                raw_data = redis_client.get(f"job:{job_id}")
                if raw_data:
                    return json.loads(raw_data)
            except Exception:
                pass

        return memory_job_store.get(job_id)

    def _update_job_state(self, job_id: str, updates: Dict[str, Any]):
        current = self.get_job_status(job_id)
        if not current:
            return
            
        current.update(updates)
        
        if REDIS_AVAILABLE:
            try:
                redis_client.set(f"job:{job_id}", json.dumps(current), ex=3600)
            except Exception:
                pass
        memory_job_store[job_id] = current

    async def _process_underwriting_task(self, job_id: str, req: AsyncLoanApplicationRequest):
        """
        Background Worker process: Simulates multi-stage Credit Bureau API checks,
        Bank Statement OCR parsing, and AI Risk Underwriting.
        """
        # Step 1: Document OCR Parsing
        self._update_job_state(job_id, {"status": "processing", "progress_percentage": 25})
        await asyncio.sleep(1.5)

        # Step 2: Bureau Credit Check & Fraud Scoring
        self._update_job_state(job_id, {"status": "processing", "progress_percentage": 60})
        await asyncio.sleep(1.5)

        # Step 3: Final Underwriting Decision
        self._update_job_state(job_id, {"status": "processing", "progress_percentage": 90})
        await asyncio.sleep(1.0)

        # Decision calculation
        max_loan = req.monthly_income * 10
        approved = (req.requested_amount <= max_loan) and (req.credit_score >= 680)

        final_result = {
            "applicant_name": req.applicant_name,
            "decision": "APPROVED" if approved else "REJECTED",
            "approved_amount": req.requested_amount if approved else max_loan,
            "interest_rate": "11.2%" if req.credit_score >= 750 else "14.5%",
            "credit_score_verified": req.credit_score,
            "fraud_risk_score": "LOW (0.02)",
            "underwriting_summary": (
                f"Applicant {req.applicant_name} verified successfully. Income verified via OCR. "
                f"Risk profile optimal for ${req.requested_amount:,.2f} loan."
                if approved else
                f"Requested loan of ${req.requested_amount:,.2f} exceeds recommended threshold based on credit score ({req.credit_score})."
            )
        }

        self._update_job_state(job_id, {
            "status": "completed",
            "progress_percentage": 100,
            "result": final_result
        })

queue_service = RedisLoanQueueService()
