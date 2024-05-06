const duration = 1200; // duration in seconds
const circle = document.querySelector('.circle');
const maskFull = document.querySelector('.mask.full');
const maskHalf = document.querySelector('.mask.half');
const fill = document.querySelectorAll('.fill');
const insideCircle = document.querySelector('.inside-circle');

let interval;
let remaining = duration;

function calculateMinutesSeconds() {
    const minutes = Math.floor(remaining / 60);
    const seconds = remaining % 60;
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}


function updateCircle() {
    const rotation = (360 * remaining) / duration;
    if (rotation <= 180) {
        maskFull.style.display = 'none';
        maskHalf.style.transform = `rotate(${rotation}deg)`;
    } else {
        maskFull.style.display = 'block';
        maskHalf.style.transform = 'rotate(180deg)';
        fill.forEach(f => f.style.transform = `rotate(${rotation}deg)`);
    }
    insideCircle.textContent = calculateMinutesSeconds();
}


function startTimer() {
    interval = setInterval(() => {
        if (remaining <= 0) {
            clearInterval(interval);
            window.location.href = '/timer/complete';
            return;
        }
        remaining--;
        updateCircle();
    }, 1000);
}

window.onload = startTimer;
