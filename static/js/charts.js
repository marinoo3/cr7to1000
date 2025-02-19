const ctx = document.getElementById('time-graph');

new Chart(ctx, {
    type: 'line',
    data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
        data: [20, 200, 367, 580, 790, 920],
        borderWidth: 1,
        tension: 0.4
    }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Évolution du nombre de but'
            },
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});