// sentinel.js - OmniQuant Active Biometric HUD v5.0
console.log("[SENTINEL] Booting Visual Biometric Engine...");

// 1. Create a VISIBLE camera feed on the HUD (Prevents browser throttling)
const video = document.createElement('video');
video.setAttribute('autoplay', 'true');
video.setAttribute('playsinline', 'true');
video.style.position = 'fixed';
video.style.bottom = '20px';
video.style.right = '20px';
video.style.width = '160px';
video.style.border = '2px solid var(--theme-color)';
video.style.borderRadius = '8px';
video.style.boxShadow = '0 0 15px var(--theme-dim)';
video.style.opacity = '0.8';
video.style.zIndex = '9999';
video.style.transform = 'scaleX(-1)'; // Mirror effect
document.body.appendChild(video);

// Hidden canvas for math calculations
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true });
canvas.width = 64;  
canvas.height = 48;

let previousFrame = [];
let fatigueMeter = 0; // 0 to 100
let isSystemLocked = false;

// 2. Start the Webcam
navigator.mediaDevices.getUserMedia({ video: { width: 320, height: 240 }, audio: false })
    .then(stream => {
        video.srcObject = stream;
        console.log("[SENTINEL] Camera Feed Acquired.");
        
        video.onplaying = () => {
            updateUI("BIOMETRICS ONLINE // TRACKING", "#00ff88");
            setInterval(trackPresence, 200); // Run exactly 5 times a second
        };
    })
    .catch(err => {
        console.error("[SENTINEL] Camera access denied:", err);
        updateUI("CAMERA DENIED // CHECK BROWSER PERMISSIONS", "#ffaa00");
    });

// 3. The Core Tracking Algorithm
function trackPresence() {
    if (video.paused || video.ended) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frameData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    
    let movementScore = 0;

    if (previousFrame.length > 0) {
        for (let i = 0; i < frameData.length; i += 4) {
            const diff = Math.abs(frameData[i] - previousFrame[i]);
            if (diff > 15) movementScore++; // Lowered threshold to catch micro-movements
        }
    }

    previousFrame = new Uint8ClampedArray(frameData);

    // 4. Calculate Fatigue
    if (movementScore > 20) {
        // Movement detected (awake) -> Reduce fatigue quickly
        fatigueMeter -= 15;
        if (fatigueMeter < 0) fatigueMeter = 0;
        
        if (isSystemLocked && fatigueMeter === 0) {
            restoreSystem();
        }
    } else {
        // No movement (eyes closed/asleep) -> Increase fatigue
        fatigueMeter += 10;
        if (fatigueMeter > 100) fatigueMeter = 100;
        
        if (fatigueMeter >= 100 && !isSystemLocked) {
            triggerSystemLockdown();
        }
    }

    // Live UI Update of Fatigue
    const statusUI = document.querySelector('.ai-core span.highlight');
    if (statusUI && !isSystemLocked) {
        statusUI.innerText = `BIOMETRICS ACTIVE // FATIGUE: ${fatigueMeter}%`;
        statusUI.style.color = fatigueMeter > 50 ? "#ffaa00" : "#00ff88";
    }
}

// --- UI EFFECTS ---
function updateUI(message, color) {
    const statusUI = document.querySelector('.ai-core span.highlight');
    if (statusUI) {
        statusUI.innerText = message;
        statusUI.style.color = color;
    }
}

function triggerSystemLockdown() {
    isSystemLocked = true;
    video.style.borderColor = '#ff003c';
    
    document.documentElement.style.setProperty('--theme-color', '#ff003c');
    document.documentElement.style.setProperty('--theme-glow', 'rgba(255, 0, 60, 0.6)');
    
    updateUI("FATIGUE CRITICAL // SYSTEM LOCKED", "#ff003c");

    const aiPanel = document.getElementById('ai-insight');
    if(aiPanel) {
        aiPanel.innerHTML = '<span style="color:#ff003c; font-weight:bold; font-size:1.1rem;">SYSTEM_LOCKDOWN: Operator fatigue detected (100%). Intelligence feed suspended to preserve capital. Move to restore.</span>';
    }
}

function restoreSystem() {
    isSystemLocked = false;
    video.style.borderColor = '#00f3ff';
    
    document.documentElement.style.setProperty('--theme-color', '#00f3ff');
    document.documentElement.style.setProperty('--theme-glow', 'rgba(0, 243, 255, 0.4)');
    
    updateUI("BIOMETRICS ONLINE // TRACKING", "#00ff88");

    // Attempt to re-trigger AI analysis based on current UI state
    try {
        const currentSymbol = document.getElementById('asset-label').innerText;
        if(typeof updateAIIntelligence === "function") {
            updateAIIntelligence(currentSymbol, currentSegment);
        }
    } catch(e) {}
}