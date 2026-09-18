<?php include 'header.php'; ?>

<main class="main-content" style="max-width: 800px;">
    
    <div class="card">
        <h2 class="card-title">Upload Financial Document</h2>
        <p style="color: var(--cb-text-muted); margin-bottom: 2rem;">Upload your invoices, receipts, or bank statements here. Our AI will extract the data and add it to your Vector Database for querying.</p>

        <form id="upload-form" onsubmit="event.preventDefault(); simulateUpload();">
            <div class="form-group">
                <label class="form-label">Document Name</label>
                <input type="text" class="form-control" placeholder="e.g. September Invoice" required>
            </div>

            <div class="form-group">
                <label class="form-label">Document Type</label>
                <select class="form-control" required>
                    <option value="" disabled selected>Select Type</option>
                    <option value="invoice">Invoice</option>
                    <option value="receipt">Receipt</option>
                    <option value="bank_statement">Bank Statement</option>
                    <option value="other">Other</option>
                </select>
            </div>

            <div class="upload-area" id="upload-box" onclick="document.getElementById('file-input').click();">
                <i class="fa-solid fa-cloud-arrow-up upload-icon"></i>
                <h3 style="margin-bottom: 0.5rem;">Click to upload or drag and drop</h3>
                <p style="color: var(--cb-text-muted);">PDF, JPG, PNG (Max 10MB)</p>
                <input type="file" id="file-input" style="display: none;" accept=".pdf,.jpg,.jpeg,.png" required>
            </div>
            
            <div id="file-name-display" style="margin-top: 1rem; font-weight: 500; color: var(--cb-navy); text-align: center;"></div>

            <div style="margin-top: 2rem; text-align: center;">
                <button type="submit" class="btn btn-primary" style="width: 100%; font-size: 1.1rem;" id="submit-btn">
                    <i class="fa-solid fa-upload"></i> Process Document
                </button>
            </div>
        </form>

        <div id="success-msg" style="display: none; margin-top: 1.5rem; padding: 1rem; background-color: #d1e7dd; color: var(--cb-success); border-radius: 8px; text-align: center; border: 1px solid #badbcc;">
            <i class="fa-solid fa-circle-check"></i> Document uploaded and processed successfully!
        </div>
    </div>

</main>

<script>
    document.getElementById('file-input').addEventListener('change', function(e) {
        if(e.target.files.length > 0) {
            document.getElementById('file-name-display').innerHTML = '<i class="fa-solid fa-file"></i> ' + e.target.files[0].name;
            document.getElementById('upload-box').style.borderColor = 'var(--cb-success)';
        }
    });

    function simulateUpload() {
        const btn = document.getElementById('submit-btn');
        btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing with AI...';
        btn.disabled = true;

        setTimeout(() => {
            document.getElementById('upload-form').reset();
            document.getElementById('file-name-display').innerHTML = '';
            document.getElementById('upload-box').style.borderColor = 'var(--cb-blue)';
            
            btn.innerHTML = '<i class="fa-solid fa-upload"></i> Process Document';
            btn.disabled = false;
            
            const successMsg = document.getElementById('success-msg');
            successMsg.style.display = 'block';
            
            setTimeout(() => {
                successMsg.style.display = 'none';
            }, 5000);

        }, 2000);
    }
</script>

<?php include 'footer.php'; ?>
