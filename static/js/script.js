document.addEventListener('DOMContentLoaded', async function () {

	// Show popup

	const popup = document.querySelector('#loading-popup');
	popup.classList.remove('hidden');

	// Requests stats to python API

	const response = await fetch('/get_player_data/', {
		method: 'GET',
		headers: { 'Content-Type': 'application/json' }
	});

	if (!response.ok) {
		throw new Error('Network response was not ok');
	}

	const stats = await response.json();

	// Update GUI and draw charts

	updateNumbers(stats);

	drawTimeChart(stats['timeChart']);
	drawTypeChart(stats['typeChart']);
	updatePositionChart(stats['positionChart']);


	// Hide popup

	popup.classList.add('hidden');

});