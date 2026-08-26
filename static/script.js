document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('phishing-form');
    const submitBtn = document.getElementById('analyze-btn');
    const clearBtn = document.getElementById('clear-btn');
    const textarea = document.getElementById('email-content');
    const charCounter = document.getElementById('char-counter');
    
    const resultContainer = document.getElementById('result-container');
    const resultCard = document.getElementById('result-card');
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const resultDesc = document.getElementById('result-desc');
    const badgeContainer = document.getElementById('badge-container');
    const confidenceVal = document.getElementById('confidence-val');
    const meterBarFill = document.getElementById('meter-bar-fill');
    const riskFlagsSection = document.getElementById('risk-flags-section');
    const riskFlagsList = document.getElementById('risk-flags-list');

    // Samples
    const samples = {
        phishing1: "URGENT SECURITY ALERT: Your account access has been suspended due to unauthorized login attempts. Click here immediately to verify your identity: http://192.168.1.1/login.php or your account will be permanently deleted.",
        phishing2: "CONGRATULATIONS! You have been selected as the WINNER of our exclusive 1,000,000 lottery prize. Claim your reward immediately by sending your bank details to prize@reward-claim.xyz",
        safe: "Hi team, please find attached the slides and project agenda for tomorrow's 10:00 AM sprint sync meeting. Let me know if you have any questions or feedback."
    };

    // Sample buttons event listeners
    document.getElementById('sample-phishing-1')?.addEventListener('click', () => {
        textarea.value = samples.phishing1;
        updateCharCount();
    });

    document.getElementById('sample-phishing-2')?.addEventListener('click', () => {
        textarea.value = samples.phishing2;
        updateCharCount();
    });

    document.getElementById('sample-safe')?.addEventListener('click', () => {
        textarea.value = samples.safe;
        updateCharCount();
    });

    // Character counter
    function updateCharCount() {
        const count = textarea.value.length;
        charCounter.textContent = `${count} character${count === 1 ? '' : 's'}`;
    }
    textarea.addEventListener('input', updateCharCount);

    // Clear button
    clearBtn.addEventListener('click', () => {
        textarea.value = '';
        updateCharCount();
        resultContainer.classList.add('hidden');
    });

    const icons = {
        safe: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`,
        phishing: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`,
        error: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const messageInput = textarea.value.trim();
        if (!messageInput) return;

        // Reset UI state
        submitBtn.classList.add('loading');
        resultContainer.classList.add('hidden');
        resultCard.className = 'result-card';
        badgeContainer.innerHTML = '';
        riskFlagsList.innerHTML = '';
        riskFlagsSection.classList.add('hidden');

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: messageInput })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Server error occurred during analysis');
            }

            // Display Results
            resultContainer.classList.remove('hidden');

            const confidencePercent = Math.round((data.confidence || 0.95) * 100);
            confidenceVal.textContent = `${confidencePercent}%`;
            meterBarFill.style.width = `${confidencePercent}%`;

            if (data.is_phishing || data.result === 'phishing') {
                resultCard.classList.add('state-phishing');
                resultIcon.innerHTML = icons.phishing;
                resultTitle.textContent = "Malicious Phishing Detected";
                resultDesc.textContent = "High probability of phishing attack. The message exhibits known deceptive patterns or suspicious links.";
                
                badgeContainer.innerHTML = `<span class="badge badge-high">Threat Level: ${data.risk_level || 'HIGH'}</span>`;
            } else {
                resultCard.classList.add('state-safe');
                resultIcon.innerHTML = icons.safe;
                resultTitle.textContent = "Message Verified Safe";
                resultDesc.textContent = "No phishing indicators detected. The text appears to be legitimate correspondence.";
                
                badgeContainer.innerHTML = `<span class="badge badge-low">Risk Level: ${data.risk_level || 'LOW'}</span>`;
            }

            // Render risk flags if present
            if (data.flags && data.flags.length > 0) {
                riskFlagsSection.classList.remove('hidden');
                data.flags.forEach(flag => {
                    const li = document.createElement('li');
                    li.textContent = flag;
                    riskFlagsList.appendChild(li);
                });
            }

        } catch (error) {
            resultContainer.classList.remove('hidden');
            resultCard.classList.add('state-phishing');
            resultIcon.innerHTML = icons.error;
            resultTitle.textContent = "Analysis Failed";
            resultDesc.textContent = error.message;
            confidenceVal.textContent = "N/A";
            meterBarFill.style.width = "0%";
        } finally {
            submitBtn.classList.remove('loading');
            setTimeout(() => {
                resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 50);
        }
    });
});
