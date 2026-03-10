const ctx = document.getElementById('velocityChart').getContext('2d');
const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(99, 102, 241, 0.5)');
gradient.addColorStop(1, 'rgba(99, 102, 241, 0)');

new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['10:00', '10:15', '10:30', '10:45', '11:00'],
        datasets: [{
            label: 'Market Velocity',
            data: [12, 19, 15, 25, 22],
            borderColor: '#6366f1',
            fill: true,
            backgroundColor: gradient,
            tension: 0.4 // Makes the line smooth/attractive
        }]
    },
    options: {
        plugins: { legend: { display: false } },
        scales: { y: { display: false }, x: { grid: { display: false } } }
    }
});