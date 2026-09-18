<?php include 'header.php'; ?>

<main class="main-content">
    <h1 style="margin-bottom: 0.5rem;">Welcome to Your Financial Assistant</h1>
    <p style="color: var(--cb-text-muted); margin-bottom: 2rem;">Get intelligent insights into your finances using AI.</p>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
        
        <div class="card">
            <h2 class="card-title"><i class="fa-solid fa-robot"></i> AI Chatbot</h2>
            <p style="margin-bottom: 1.5rem; color: var(--cb-text-muted);">Ask questions about your finances, analyze spending patterns, and get personalized advice from our advanced AI.</p>
            <a href="chat.php" class="btn btn-primary">Start Chatting</a>
        </div>

        <div class="card">
            <h2 class="card-title"><i class="fa-solid fa-file-invoice"></i> Document Vault</h2>
            <p style="margin-bottom: 1.5rem; color: var(--cb-text-muted);">Upload invoices, bank statements, and receipts. Our AI will automatically extract and understand the data.</p>
            <a href="upload.php" class="btn btn-outline">Upload Documents</a>
        </div>

        <div class="card">
            <h2 class="card-title"><i class="fa-solid fa-chart-pie"></i> Quick Stats</h2>
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--cb-border);">
                <span>Documents Processed</span>
                <span style="font-weight: 700; color: var(--cb-blue);">0</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding-bottom: 0.5rem;">
                <span>AI Queries This Month</span>
                <span style="font-weight: 700; color: var(--cb-blue);">0</span>
            </div>
        </div>

    </div>
</main>

<?php include 'footer.php'; ?>
