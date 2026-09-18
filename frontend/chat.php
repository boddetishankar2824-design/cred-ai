<?php include 'header.php'; ?>

<main class="main-content" style="max-width: 800px;">
    
    <div class="chat-container">
        <div class="chat-header">
            <i class="fa-solid fa-robot" style="font-size: 1.5rem;"></i>
            <div>
                <h3 style="color: var(--cb-white); margin: 0; font-size: 1.1rem;">Financial Assistant</h3>
                <span style="font-size: 0.8rem; color: #a1bde0;">Online</span>
            </div>
        </div>

        <div class="chat-messages" id="chat-messages">
            <div class="message message-ai">
                Hello! I am your AI Financial Assistant. How can I help you today? You can ask me about your expenses, uploaded invoices, or general financial advice.
            </div>
            
            <!-- Example user message for styling -->
            <div class="message message-user">
                Can you summarize my spending for last month?
            </div>

            <!-- Example AI message for styling -->
            <div class="message message-ai">
                Based on your uploaded documents, you spent a total of $1,250 last month. The largest category was "Dining out" at $400.
            </div>
        </div>

        <div class="chat-input-area">
            <input type="text" class="form-control" placeholder="Ask a financial question..." id="chat-input">
            <button class="btn btn-primary chat-btn" id="send-btn">
                <i class="fa-solid fa-paper-plane"></i>
            </button>
        </div>
    </div>

</main>

<script>
    // Placeholder script to show simple UI interaction
    document.getElementById('send-btn').addEventListener('click', function() {
        const input = document.getElementById('chat-input');
        const msg = input.value.trim();
        if(msg) {
            const chatMessages = document.getElementById('chat-messages');
            
            // Add user message
            const userDiv = document.createElement('div');
            userDiv.className = 'message message-user';
            userDiv.textContent = msg;
            chatMessages.appendChild(userDiv);
            
            input.value = '';
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // Simulate AI typing delay
            setTimeout(() => {
                const aiDiv = document.createElement('div');
                aiDiv.className = 'message message-ai';
                aiDiv.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Thinking...';
                chatMessages.appendChild(aiDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;

                // Simulate response after 1 second
                setTimeout(() => {
                    aiDiv.innerHTML = 'This is a placeholder response from the PHP frontend. Eventually, this will connect to your Python FastAPI backend!';
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }, 1500);

            }, 500);
        }
    });

    document.getElementById('chat-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('send-btn').click();
        }
    });
</script>

<?php include 'footer.php'; ?>
