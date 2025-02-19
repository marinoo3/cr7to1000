const baseFontSize = window.innerHeight * 0.015; //vh units

function drawTimeChart(timeChart) {

  const ctx = document.getElementById('time-chart');

  var gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 250);
  gradient.addColorStop(0, 'rgba(133, 61, 67, .4)');   
  gradient.addColorStop(1, 'rgba(133, 61, 67, 0)');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: timeChart['labels'],
      datasets: [{
        data: timeChart['data'],
        borderWidth: baseFontSize/8,
        borderColor: '#E8545F',
        // backgroundColor: '#53D43',
        fill: true,
        backgroundColor: gradient,
        tension: 0.4
      }]
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'ÉVOLUTION DU NOMBRE DE BUT',
          font: {
            size: baseFontSize,
            family: 'Montserrat'
          },
          color: 'white',
          padding: {
            bottom: 40
          }
        },
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            font: {
              size: baseFontSize
            }
          }
        },
        x: {
          ticks: {
            font: {
              size: baseFontSize
            }
          }
        }
      }
    }
  });
}

function drawGoalsTypeChart(goalsTypeChart) {

  const ctx = document.getElementById('goals-type-chart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: goalsTypeChart['labels'],
      datasets: [{
        data: goalsTypeChart['data'],
        borderWidth: baseFontSize/8,
        borderColor: '#E8545F',
        backgroundColor: '#853D43'
      }]
    },
    options: {
      indexAxis: 'y',
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'TYPE DE BUT',
          font: {
            size: baseFontSize,
            family: 'Montserrat'
          },
          color: 'white',
          padding: {
            bottom: 40
          }
        },
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            font: {
              size: baseFontSize
            }
          }
        },
        x: {
          ticks: {
            font: {
              size: baseFontSize
            }
          }
        }
      }
    }
  });
}

function updatePositionChart(positionChart) {

  const custom_ctx = document.getElementById('position-custom-chart');

  for(position in positionChart) {

    const percent = positionChart[position]['percent'];
    const position_element = custom_ctx.querySelector('#' + position);
    const size = (.5+ percent) * 6 + 'vh';

    position_element.style.height = size;
    position_element.style.width = size;

    position_element.dataset.count = positionChart[position]['count']
  }

  custom_ctx.querySelectorAll('.position-points > li').forEach(item => {
    item.addEventListener('mouseenter', function() {
      // Store the original text in a data attribute so it can be restored on mouseleave
      item.dataset.originalText = item.textContent;
      // Set textContent to the value of data-count attribute
      item.textContent = item.dataset.count;
    });
  
    item.addEventListener('mouseleave', function() {
      // Restore the original text
      item.textContent = item.dataset.originalText;
    });
  });

}

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


document.addEventListener('DOMContentLoaded', async function() {

  const popup = document.querySelector('#loading-popup');
  popup.classList.add('loading');

  const response = await fetch('/get_player_data/', {
    method: 'GET',
    headers: {'Content-Type': 'application/json'}
  });

  if(!response.ok) {
    throw new Error('Network response was not ok');
  }

  const stats = await response.json();
  const goalElement = document.querySelector('#goals');
  goalElement.textContent = 0;

  const percentElement = document.querySelector('.progress-label');
  percentElement.textContent = stats['player']['progress'] + '%';

  const progressBar = document.querySelector('.progress-slider');
  progressBar.style.width = stats['player']['progress'] + '%';

  const predictedDate = document.querySelector('#prediction');
  predictedDate.textContent = stats['player']['prediction'];

  const playedGames = document.querySelector('#played-games');
  playedGames.textContent = stats['player']['seasons'];

  const averageGoals = document.querySelector('#average-goals');
  averageGoals.textContent = stats['player']['goals_per_saison'];

  countUp(goalElement, stats['player']['goals']);

  drawTimeChart(stats['timeChart']);
  drawGoalsTypeChart(stats['goalsTypeChart']);
  updatePositionChart(stats['positionChart']);

  popup.classList.remove('loading');

});