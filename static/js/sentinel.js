const video = document.createElement('video');
const canvas = document.createElement('canvas');

// Start Sentinel Eye
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; video.play(); })
    .catch(e => console.error("Bio-Sentinel Error: Camera access required."));

async function runSentinelProtocol() {
    canvas.width = 160;
    canvas.height = 120;
    canvas.getContext('2d').drawImage(video, 0, 0, 160, 120);
    
    const frame = canvas.toDataURL('image/jpeg');

    try {
        const response = await fetch('/sentinel/analyze/', {
            method: 'POST',
            body: JSON.stringify({ image: frame }),
            headers: { 'Content-Type': 'application/json' }
        });

        const result = await response.json();
        handleSentinelResponse(result.status);
    } catch (err) {
        console.log("Sentinel Connection Latency...");
    }
}

function handleSentinelResponse(status) {
    const viewport = document.getElementById('main-viewport');
    const overlay = document.getElementById('stress-overlay');
    const ring = document.getElementById('sentinel-ring');
    const label = document.getElementById('sentinel-label');

    if (status === "LOCKDOWN") {
        // APPLY BLUR AND RED ALERT
        viewport.classList.add('system-lockdown');
        overlay.style.opacity = "1";
        overlay.style.animation = "pulse-stress 1.5s infinite alternate";
        
        ring.style.background = "#ff3131";
        ring.style.boxShadow = "0 0 20px #ff3131";
        label.innerText = "STRESS_ALERT";
        label.style.color = "#ff3131";
    } else {
        // RESTORE STABILITY
        viewport.classList.remove('system-lockdown');
        overlay.style.opacity = "0";
        overlay.style.animation = "none";
        
        ring.style.background = "#10b981";
        ring.style.boxShadow = "0 0 15px #10b981";
        label.innerText = "STABLE";
        label.style.color = "white";
    }
}

// Sync frequency: every 2000ms
setInterval(runSentinelProtocol, 2000);