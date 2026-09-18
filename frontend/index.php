<?php include 'header.php'; ?>

<main class="hero-section">
    <div class="hero-pill">
        Empowering Smarter Borrowing
    </div>
    
    <h1 class="hero-title">Your Smart Borrowing Partner<br>- CredBuddha</h1>
    <p class="hero-subtitle">A trusted partner for smarter financial decisions, offering clarity, support, and tools to move ahead. Begin your journey toward confident financial progress today.</p>

    <!-- Decorative Elements -->
    <i class="fa-solid fa-signature deco-doodle"></i>
    <i class="fa-solid fa-sparkles deco-star"></i>
    
    <div class="hero-graphics">
        <div class="bg-gradient-circle"></div>
        
        <div class="deco-sunburst">
            <i class="fa-solid fa-arrow-pointer deco-cursor"></i>
        </div>

        <div class="floating-card-left">
            <h4 style="color: #cbd5e1;"><i class="fa-solid fa-sack-dollar" style="color: #fbbf24;"></i> Find Your Ideal Loan Match</h4>
            <h3>20+ Verified Lending Partners</h3>
            
            <div class="check-item">
                <i class="fa-solid fa-circle-check"></i> Free Credit Score Access
            </div>
            <div class="check-item">
                <i class="fa-solid fa-circle-check"></i> No Application Fee
            </div>
            <div class="check-item">
                <i class="fa-solid fa-circle-check"></i> Smart Rate Comparison
            </div>
        </div>

        <!-- Phone Mockup Container -->
        <div class="phone-mockup">
            <!-- Simulating UI inside phone -->
            <div style="padding: 1rem; color: white;">
                <p style="font-size: 0.8rem; margin-bottom: 2rem;">Hi, User!</p>
                
                <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 8px; color: black; margin-bottom: 1rem;">
                    <h5 style="color: var(--cb-blue);">Your Pre-Approved Offers</h5>
                    <p style="font-size: 0.6rem; color: #666;">Empowering financial decisions</p>
                </div>
                
                <p style="font-size: 0.7rem;">Our Products</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                    <div style="background: white; border-radius: 6px; padding: 10px; text-align: center; color: black;">
                        <i class="fa-solid fa-money-bills" style="color: #fbbf24;"></i>
                        <div style="font-size: 0.6rem; margin-top: 5px;">Personal Loan</div>
                    </div>
                    <div style="background: white; border-radius: 6px; padding: 10px; text-align: center; color: black;">
                        <i class="fa-solid fa-building" style="color: #6366f1;"></i>
                        <div style="font-size: 0.6rem; margin-top: 5px;">Business Loan</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</main>

<!-- Redis Queue Feature Demo Widget -->
<section style="max-width: 900px; margin: 2rem auto; padding: 2rem; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
    <h2 style="color: #1e293b; margin-bottom: 0.5rem;"><i class="fa-solid fa-bolt" style="color: #f59e0b;"></i> Redis Queue Asynchronous Loan Underwriting</h2>
    <p style="color: #64748b; margin-bottom: 1.5rem;">Experience high-speed background processing with Redis. Submit an application and watch the AI worker process your credit scoring asynchronously.</p>

    <form id="redis-loan-form" onsubmit="event.preventDefault(); submitRedisLoan();" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
        <div>
            <label style="font-weight: 600; font-size: 0.85rem; color: #475569;">Applicant Name</label>
            <input type="text" id="applicant-name" value="Shankar" required style="width: 100%; padding: 0.6rem; border: 1px solid #cbd5e1; border-radius: 6px;">
        </div>
        <div>
            <label style="font-weight: 600; font-size: 0.85rem; color: #475569;">Monthly Income ($)</label>
            <input type="number" id="monthly-income" value="5000" required style="width: 100%; padding: 0.6rem; border: 1px solid #cbd5e1; border-radius: 6px;">
        </div>
        <div>
            <label style="font-weight: 600; font-size: 0.85rem; color: #475569;">Requested Loan ($)</label>
            <input type="number" id="requested-amount" value="15000" required style="width: 100%; padding: 0.6rem; border: 1px solid #cbd5e1; border-radius: 6px;">
        </div>
        <div>
            <label style="font-weight: 600; font-size: 0.85rem; color: #475569;">Credit Score</label>
            <input type="number" id="credit-score" value="750" required style="width: 100%; padding: 0.6rem; border: 1px solid #cbd5e1; border-radius: 6px;">
        </div>
        <div style="grid-column: 1 / -1;">
            <button type="submit" id="submit-redis-btn" style="background: #2563eb; color: white; padding: 0.8rem 1.5rem; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; width: 100%;">
                <i class="fa-solid fa-paper-plane"></i> Submit Application to Redis Queue (Async)
            </button>
        </div>
    </form>

    <!-- Progress & Result Box -->
    <div id="queue-status-box" style="display: none; padding: 1.5rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-weight: 600; color: #1e293b;" id="job-id-text">Job ID: -</span>
            <span style="font-size: 0.85rem; font-weight: 700; color: #2563eb; padding: 4px 8px; background: #dbeafe; border-radius: 4px;" id="status-badge">QUEUED</span>
        </div>

        <div style="width: 100%; background: #e2e8f0; height: 10px; border-radius: 5px; overflow: hidden; margin-bottom: 1rem;">
            <div id="progress-bar" style="width: 0%; height: 100%; background: #2563eb; transition: width 0.4s ease;"></div>
        </div>

        <div id="result-details" style="font-size: 0.9rem; color: #334155;"></div>
    </div>
</section>

<script>
async function submitRedisLoan() {
    const btn = document.getElementById('submit-redis-btn');
    const box = document.getElementById('queue-status-box');
    const jobIdText = document.getElementById('job-id-text');
    const statusBadge = document.getElementById('status-badge');
    const progressBar = document.getElementById('progress-bar');
    const resultDetails = document.getElementById('result-details');

    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Pushing to Redis Queue...';

    const payload = {
        applicant_name: document.getElementById('applicant-name').value,
        monthly_income: parseFloat(document.getElementById('monthly-income').value),
        requested_amount: parseFloat(document.getElementById('requested-amount').value),
        credit_score: parseInt(document.getElementById('credit-score').value)
    };

    try {
        const response = await fetch('/api/loan/apply-async', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        box.style.display = 'block';
        jobIdText.innerText = `Job ID: ${data.job_id}`;
        statusBadge.innerText = 'QUEUED';
        progressBar.style.width = '10%';
        resultDetails.innerHTML = '<em>Application queued in Redis. Initializing background underwriting worker...</em>';

        const pollInterval = setInterval(async () => {
            const statusRes = await fetch(`/api/loan/job-status/${data.job_id}`);
            const statusData = await statusRes.json();

            statusBadge.innerText = statusData.status.toUpperCase();
            progressBar.style.width = `${statusData.progress_percentage}%`;

            if (statusData.status === 'processing') {
                resultDetails.innerHTML = `<strong>Processing (${statusData.progress_percentage}%):</strong> Verifying Income, OCR Statement & Credit Bureau Check...`;
            } else if (statusData.status === 'completed') {
                clearInterval(pollInterval);
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Submit Application to Redis Queue (Async)';
                
                const res = statusData.result;
                const isApproved = res.decision === 'APPROVED';

                resultDetails.innerHTML = `
                    <div style="margin-top: 0.5rem; padding: 1rem; background: ${isApproved ? '#dcfce7' : '#fee2e2'}; border-radius: 6px; border-left: 4px solid ${isApproved ? '#22c55e' : '#ef4444'};">
                        <h4 style="margin: 0 0 0.5rem 0; color: ${isApproved ? '#15803d' : '#b91c1c'};">Decision: ${res.decision}</h4>
                        <p style="margin: 0 0 0.5rem 0;"><strong>Underwriting Summary:</strong> ${res.underwriting_summary}</p>
                        <p style="margin: 0;"><strong>Verified Rate:</strong> ${res.interest_rate} | <strong>Approved Amount:</strong> $${res.approved_amount.toLocaleString()}</p>
                    </div>
                `;
            }
        }, 1000);

    } catch (err) {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Submit Application to Redis Queue (Async)';
        alert('Error connecting to backend: ' + err.message);
    }
}
</script>

<a href="#" class="floating-agent-btn" onclick="toggleAssistant(event)">
    <div class="agent-avatar"><i class="fa-solid fa-robot"></i></div>
</a>

<?php include 'footer.php'; ?>
