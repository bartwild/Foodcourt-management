const duration = 1200; // duration in seconds
const timerText = document.getElementById('timer');

let interval;
let remaining = duration;

function calculateMinutesSeconds() {
    const minutes = Math.floor(remaining / 60);
    const seconds = remaining % 60;
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}

function updateTimer() {
    timerText.textContent = calculateMinutesSeconds();
}

function extendTimer() {
    remaining += 600;;
    document.getElementById('extendContainer').style.display = 'none';
}

function dismissContainer() {
    document.getElementById('extendContainer').style.display = 'none';
}

function freeTable() {
    var table = 2;
    var postData = {'table_number': parseInt(table), 'status': 'free'};
    console.log('Table 1 is now free');
    fetch('/update_tables', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(postData)
        })
        
}

document.getElementById('extendButton').addEventListener('click', extendTimer);
document.getElementById('dismissButton').addEventListener('click', dismissContainer);
document.getElementById('free-table').addEventListener('click', freeTable);

function startTimer() {
    interval = setInterval(() => {
        if (remaining <= 0) {
            clearInterval(interval);
            window.location.href = '/';
            freeTable();
            return;
        }
        if (remaining === 300) {
            document.getElementById('extendContainer').style.display = 'block';
        }

        remaining--;
        updateTimer();
    }, 1000);
}

window.onload = startTimer;