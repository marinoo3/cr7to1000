function countUp(element, target) {
    const startTime = performance.now();
    const duration = 1300; // milliseconds

    function update(timestamp) {
        // Calculate normalized progress [0..1]
        const elapsed = timestamp - startTime;
        let progress = Math.min(elapsed / duration, 1);

        // Ease-out
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



function updateNumbers(stats) {

    // Set goals to 0 and run count up
    const goalElement = document.querySelector('#goals');
    goalElement.textContent = 0;
    countUp(goalElement, stats['player']['goals']);
    // Set progress bar label
    const percentElement = document.querySelector('.progress-label');
    percentElement.textContent = stats['player']['progress'] + '%';
    // Set progress
    const progressBar = document.querySelector('.progress-slider');
    progressBar.style.width = stats['player']['progress'] + '%';

    // Set prediction date
    const predictedDate = document.querySelector('#prediction');
    predictedDate.textContent = stats['player']['prediction'];

    // Set saison
    const playedGames = document.querySelector('#played-games');
    playedGames.textContent = stats['player']['seasons'];

    // Set average goals
    const averageGoals = document.querySelector('#average-goals');
    averageGoals.textContent = stats['player']['goals_per_saison'];

}