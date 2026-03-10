async function refreshGreeks() {
    // Only refresh if the system is NOT in lockdown
    const viewport = document.getElementById('main-viewport');
    if (viewport.classList.contains('system-lockdown')) return;

    try {
        const response = await fetch('/markets/live-greeks/');
        const data = await response.json();
        
        const tableBody = document.getElementById('options-data');
        tableBody.innerHTML = ''; // Clear old rows

        data.greeks.forEach(row => {
            const htmlRow = `
                <tr>
                    <td>${row.strike}</td>
                    <td style="color: #39ff14;">${row.ltp}</td>
                    <td>${row.delta}</td>
                    <td>${row.gamma}</td>
                    <td style="color: #ff3131;">${row.theta}</td>
                </tr>
            `;
            tableBody.innerHTML += htmlRow;
        });
    } catch (err) {
        console.error("Market Data Link Severed:", err);
    }
}

// Update the grid every 1 second
setInterval(refreshGreeks, 1000);