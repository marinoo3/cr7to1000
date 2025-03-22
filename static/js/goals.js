function updateGoals(goals, goalsContainer) {

    for(monthYear of goals) {

        const monthYearString = monthYear['monthYear'];
		const monthYearElement = document.createElement('h2');
		monthYearElement.textContent = monthYearString;
		goalsContainer.appendChild(monthYearElement);

        for(const goal of monthYear['goals']) {
            
            const template = document.getElementById('goal-template');
            const clone = template.content.cloneNode(true);

            clone.querySelector('.date').textContent = goal['date'];
            clone.querySelector('.competition').textContent = goal['competition'];
            clone.querySelector('.position').textContent = goal['position'];
            clone.querySelector('.minute').textContent = goal['minute'];
            clone.querySelector('.type-of-goal').textContent = goal['typeOfGoal'];

            goalsContainer.appendChild(clone);
        }
    }
}


function onScroll() {

	// Calculate the bottom position
	const scrollTop = window.scrollY;
	const scrollHeight = document.documentElement.scrollHeight;
	const clientHeight = window.innerHeight;
  
	if (scrollTop + clientHeight >= scrollHeight) {
	  // User has scrolled to the bottom
	  console.log("You've reached the bottom!");
	}
  }


document.addEventListener('DOMContentLoaded', async function () {

	const goalsContainer = document.querySelector('.goals-container ul');

	// Show popup

	const popup = document.querySelector('#loading-popup');
	popup.classList.remove('hidden');

	// Requests stats to python API

	const response = await fetch('/get_goals_data/', {
		method: 'GET',
		headers: { 'Content-Type': 'application/json' },
	});

	if (!response.ok) {
		throw new Error('Network response was not ok');
	}

	const result = await response.json();

	// Add goals of the last 6 months
	updateGoals(result['goals'], goalsContainer);
	// Loads more when the user reach the bottom of the page
	document.addEventListener('scroll', onScroll);


	// Hide popup

	popup.classList.add('hidden');

});