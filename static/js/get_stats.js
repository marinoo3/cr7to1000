function countUp(element, target) {
    const startTime = performance.now();
    const duration = 1300; // milliseconds
    
    function update(timestamp) {
      // Calculate normalized progress [0..1]
      const elapsed = timestamp - startTime;
      let progress = Math.min(elapsed / duration, 1);
      
      // Quadratic ease-out
      progress = 1 - (1 - progress) * (1 - progress);
      
      // Update the element's text
      element.textContent = Math.floor(target * progress);
      
      // Keep animating until we reach the end
      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        element.textContent = target; // Ensure final value is exact
      }
    }
  
    requestAnimationFrame(update);
  }

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
    goalElement.textContent = 0;

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

    countUp(goalElement, result['stats']['goals']);
});