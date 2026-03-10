async function updateAIInsight() {
    // We can pass the latest EAR from the sentinel.js global state
    const currentStatus = document.getElementById('sentinel-label').innerText;
    let earParam = (currentStatus === "STABLE") ? 0.25 : 0.15;

    try {
        const response = await fetch(`/core/ai-insight/?ear=${earParam}`);
        const data = await response.json();
        
        const aiCardText = document.querySelector('.glass-card p');
        aiCardText.style.opacity = '0'; // Fade out effect
        
        setTimeout(() => {
            aiCardText.innerText = data.insight;
            aiCardText.style.opacity = '1'; // Fade in
        }, 500);
    } catch (err) {
        console.log("AI Agent offline...");
    }
}

// Update AI insights every 5 seconds (to avoid overwhelming the user)
setInterval(updateAIInsight, 5000);