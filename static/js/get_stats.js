document.addEventListener('DOMContentLoaded', async function() {

    const response = await fetch('/get_player_data/', {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    });

    if(!response.ok) {
        throw new Error('Network response was not ok');
    }

    const result = await response.json();
    const goalElement = document.querySelector('#goals');
    goalElement.textContent = result['stats']['goals'];

    const percentElement = document.querySelector('.progress-label');
    percentElement.textContent = result['stats']['progress'] + '%';

    const progressBar = document.querySelector('.progress-slider');
    progressBar.style.width = result['stats']['progress'] + '%';

    const predictedDate = document.querySelector('#prediction');
    predictedDate.textContent = result['stats']['prediction'];

    const playedGames = document.querySelector('#played-games');
    playedGames.textContent = result['stats']['plays'];

    const averageGoals = document.querySelector('#average-goals');
    averageGoals.textContent = result['stats']['average_goals'];
});