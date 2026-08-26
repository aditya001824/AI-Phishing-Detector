document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('phishing-form');
    const submitBtn = document.getElementById('analyze-btn');
    const resultContainer = document.getElementById('result-container');
    const resultCard = document.getElementById('result-card');
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const resultDesc = document.getElementById('result-desc');

    const icons = {
        safe: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`,
        phishing: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`,
        error: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const messageInput = document.getElementById('email-content').value;
        if (!messageInput.trim()) return;

        // Reset UI state
        submitBtn.classList.add('loading');
        resultContainer.classList.add('hidden');
        resultCard.className = 'result-card'; // override previous states

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: messageInput })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Server error occurred');
            }

            // Display Results
            resultContainer.classList.remove('hidden');

            if (data.result === 'phishing') {
                resultCard.classList.add('state-phishing');
                resultIcon.innerHTML = icons.phishing;
                resultTitle.textContent = "Threat Detected";
                resultDesc.textContent = "This message exhibits characteristics typical of phishing attempts. Do not click on any links, and avoid providing personal information.";
            } else {
                resultCard.classList.add('state-safe');
                resultIcon.innerHTML = icons.safe;
                resultTitle.textContent = "Message Appears Safe";
                resultDesc.textContent = "Our AI analysis did not detect any known phishing patterns in this text. However, always exercise caution with unknown senders.";
            }

        } catch (error) {
            resultContainer.classList.remove('hidden');
            resultCard.classList.add('state-phishing'); // use red for error
            resultIcon.innerHTML = icons.error;
            resultTitle.textContent = "Error";
            resultDesc.textContent = error.message;
        } finally {
            submitBtn.classList.remove('loading');
            
            // Scroll to results smoothly
            setTimeout(() => {
                resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 50);
        }
    });
});
