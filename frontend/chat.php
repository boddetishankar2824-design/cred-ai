<?php include 'header.php'; ?>

<main style="padding: 2rem;">
    
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; color: var(--cb-navy);">Financial Support & AI Concierge</h1>
        <p style="color: var(--cb-text-muted);">Personalized AI assistance for your financial decisions — without compromising accuracy.</p>
    </div>

    <div class="flowchart-container">
        
        <div class="flowchart-grid">
            
            <!-- Left Column (User) -->
            <div class="flow-column" style="align-items: flex-end;">
                <span style="font-size: 0.7rem; font-weight: 600; color: #a1a1aa; text-transform: uppercase;">YOU</span>
                <div class="flow-node node-user">
                    I need a personal loan with the lowest interest rate.
                </div>
            </div>

            <!-- Horizontal Line 1 -->
            <div class="flow-line"></div>

            <!-- Middle Column (AI Agent / System) -->
            <div class="flow-column flow-column-center">
                <div class="flow-node node-ai">
                    <span class="node-label center"><i class="fa-solid fa-robot"></i> AI AGENT</span>
                    <strong>Based on your profile, here are top matches:</strong>
                    <div style="display: flex; align-items: center; gap: 15px; margin-top: 15px; background: #f8fafc; padding: 10px; border-radius: 8px;">
                        <i class="fa-solid fa-building-columns" style="font-size: 1.5rem; color: var(--cb-blue);"></i>
                        <div>
                            <div style="font-weight: 600;">HDFC Bank</div>
                            <div style="font-size: 0.8rem; color: var(--cb-text-muted);">10.5% p.a. • Pre-approved</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px; margin-top: 10px; background: #f8fafc; padding: 10px; border-radius: 8px;">
                        <i class="fa-solid fa-building-columns" style="font-size: 1.5rem; color: var(--cb-success);"></i>
                        <div>
                            <div style="font-weight: 600;">SBI</div>
                            <div style="font-size: 0.8rem; color: var(--cb-text-muted);">10.2% p.a. • Processing fee applies</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Horizontal Line 2 -->
            <div class="flow-line"></div>

            <!-- Right Column (Follow up / Resolution) -->
            <div class="flow-column">
                <span style="font-size: 0.7rem; font-weight: 600; color: #a1a1aa; text-transform: uppercase;">RESOLUTION</span>
                <div class="flow-node node-user" style="background: #e2e8f0; color: var(--cb-text-main);">
                    Applying for HDFC Pre-approved...
                </div>
                
                <div class="flow-node node-ai">
                    <span class="node-label center"><i class="fa-solid fa-check-circle" style="color: var(--cb-success);"></i> SYSTEM</span>
                    Application initiated successfully.
                </div>
            </div>

        </div>

        <!-- Chat Input floating at bottom -->
        <div class="chat-input-wrapper">
            <input type="text" placeholder="Type your financial question here...">
            <button><i class="fa-solid fa-paper-plane"></i></button>
        </div>

    </div>

</main>

<a href="#" class="floating-agent-btn" onclick="toggleAssistant(event)">
    <div class="agent-avatar"><i class="fa-solid fa-robot"></i></div>
</a>

<?php include 'footer.php'; ?>
