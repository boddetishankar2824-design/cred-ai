<footer class="footer">
    <p>&copy; <?php echo date("Y"); ?> AI Financial Assistant. Built for efficiency.</p>
</footer>

<!-- Side Assistant Overlay & Panel -->
<div class="side-assistant-overlay" id="sa-overlay" onclick="toggleAssistant()"></div>

<div class="side-assistant-panel" id="sa-panel">
    <!-- WhatsApp-style Header -->
    <div class="side-assistant-header">
        <div class="side-assistant-header-info">
            <div class="side-assistant-avatar">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div>
                <div style="font-weight: 600; font-size: 1rem;">CredBuddha Expert</div>
                <div style="font-size: 0.75rem; color: #d1d9e6;">Online</div>
            </div>
        </div>
        <button class="side-assistant-close" onclick="toggleAssistant()"><i class="fa-solid fa-xmark"></i></button>
    </div>

    <!-- Chat Messages Area -->
    <div class="side-assistant-messages" id="sa-messages">
        <div class="sa-msg sa-msg-ai">
            Hello! I'm here to help you make smarter financial decisions. What can I assist you with today?
            <span class="sa-msg-time">10:00 AM</span>
        </div>
    </div>

    <!-- Chat Input -->
    <div class="sa-input-area">
        <input type="file" id="sa-file-upload" accept=".pdf,.txt" style="display: none;" onchange="handleFileUpload(event)">
        <button class="sa-upload-btn" onclick="document.getElementById('sa-file-upload').click()" title="Upload PDF">
            <i class="fa-solid fa-paperclip"></i>
        </button>
        <input type="text" id="sa-input" class="sa-input" placeholder="Type a message..." onkeypress="if(event.key === 'Enter') sendSAMessage()">
        <button class="sa-send-btn" onclick="sendSAMessage()">
            <i class="fa-solid fa-paper-plane"></i>
        </button>
    </div>
</div>

<script>
    function toggleAssistant(e) {
        if(e) e.preventDefault();
        const panel = document.getElementById('sa-panel');
        const overlay = document.getElementById('sa-overlay');
        
        panel.classList.toggle('active');
        overlay.classList.toggle('active');
    }

    async function handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        const messagesContainer = document.getElementById('sa-messages');
        const now = new Date();
        const timeStr = now.getHours() + ':' + String(now.getMinutes()).padStart(2, '0');

        // Show uploading indicator
        const loadingId = 'upload-' + Date.now();
        const loadingHtml = `
            <div id="${loadingId}" class="sa-msg sa-msg-user" style="opacity: 0.8;">
                <i class="fa-solid fa-spinner fa-spin"></i> Uploading ${file.name}...
                <span class="sa-msg-time">${timeStr}</span>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', loadingHtml);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        try {
            // Read file as Base64
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = async function () {
                const base64String = reader.result.split(',')[1];
                
                // Send to FastAPI/Mock Server
                const response = await fetch('http://localhost:8001/api/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ filename: file.name, content: base64String })
                });
                
                const data = await response.json();
                document.getElementById(loadingId).remove();
                
                if(response.ok) {
                    const successHtml = `
                        <div class="sa-msg sa-msg-user">
                            <i class="fa-solid fa-file-pdf"></i> ${file.name} uploaded successfully!
                            <span class="sa-msg-time">${timeStr}</span>
                        </div>
                    `;
                    messagesContainer.insertAdjacentHTML('beforeend', successHtml);
                } else {
                    throw new Error(data.detail || "Upload failed");
                }
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            };
        } catch (error) {
            document.getElementById(loadingId).remove();
            const errHtml = `
                <div class="sa-msg sa-msg-ai" style="color: red;">
                    Error uploading PDF: ${error.message}
                </div>
            `;
            messagesContainer.insertAdjacentHTML('beforeend', errHtml);
        }
    }

    async function sendSAMessage() {
        const input = document.getElementById('sa-input');
        const msgText = input.value.trim();
        if(!msgText) return;

        const messagesContainer = document.getElementById('sa-messages');
        const now = new Date();
        const timeStr = now.getHours() + ':' + String(now.getMinutes()).padStart(2, '0');

        // Add User Message
        const userHtml = `
            <div class="sa-msg sa-msg-user">
                ${msgText}
                <span class="sa-msg-time">${timeStr}</span>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', userHtml);
        input.value = '';
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Add loading indicator
        const loadingId = 'loading-' + Date.now();
        const loadingHtml = `
            <div id="${loadingId}" class="sa-msg sa-msg-ai">
                <i class="fa-solid fa-spinner fa-spin"></i> Thinking...
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', loadingHtml);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        try {
            // Call FastAPI Backend
            const response = await fetch('http://localhost:8001/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msgText, history: [] })
            });
            
            const data = await response.json();
            
            // Remove loading indicator
            document.getElementById(loadingId).remove();
            
            // Render AI Response
            let replyText = data.reply || "Error: No reply from server.";
            
            // Parse Markdown to HTML if marked.js is available
            if (typeof marked !== 'undefined') {
                replyText = marked.parse(replyText);
            }

            const docsHtml = data.source_documents && data.source_documents.length > 0 
                ? `<div style="margin-top: 8px; font-size: 0.75rem; color: var(--cb-blue);">Sources: ${data.source_documents.join(", ")}</div>` 
                : "";

            const aiHtml = `
                <div class="sa-msg sa-msg-ai">
                    ${replyText}
                    ${docsHtml}
                    <span class="sa-msg-time">${timeStr}</span>
                </div>
            `;
            messagesContainer.insertAdjacentHTML('beforeend', aiHtml);
            
        } catch (error) {
            document.getElementById(loadingId).remove();
            const errHtml = `
                <div class="sa-msg sa-msg-ai" style="color: red;">
                    Error connecting to FastAPI backend. Is it running on port 8001?
                    <span class="sa-msg-time">${timeStr}</span>
                </div>
            `;
            messagesContainer.insertAdjacentHTML('beforeend', errHtml);
        }
        
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
</script>

<!-- Add Markdown Parser for AI Responses -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<!-- Add styling for Markdown elements like tables and lists -->
<style>
.sa-msg-ai {
    line-height: 1.5;
}
.sa-msg-ai p {
    margin-bottom: 0.5rem;
}
.sa-msg-ai ul, .sa-msg-ai ol {
    margin-left: 1.5rem;
    margin-bottom: 0.5rem;
}
.sa-msg-ai table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.5rem 0;
    font-size: 0.85rem;
}
.sa-msg-ai th, .sa-msg-ai td {
    border: 1px solid #d1d9e6;
    padding: 6px;
    text-align: left;
}
.sa-msg-ai th {
    background-color: #f1f5f9;
}
</style>

</body>
</html>
