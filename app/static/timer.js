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


function startTimer() {
    interval = setInterval(() => {
        if (remaining <= 0) {
            clearInterval(interval);
            window.location.href = '/timer/complete';
            return;
        }
        if (remaining === 300) {
            document.getElementById('extendContainer').style.display = 'block';
        }

        remaining--;
        updateTimer();
    }, 1000);
}

function extendTimer() {
    remaining += 600;;
    document.getElementById('extendContainer').style.display = 'none';
}

function dismissContainer() {
    document.getElementById('extendContainer').style.display = 'none';
}

document.getElementById('extendButton').addEventListener('click', extendTimer);
document.getElementById('dismissButton').addEventListener('click', dismissContainer);

window.onload = startTimer;
