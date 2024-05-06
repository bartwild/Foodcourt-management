document.addEventListener("DOMContentLoaded", function() {
    var timerDisplay = document.getElementById('timer');
    var secondsLeft = 60; // Change this to set the initial countdown time

    function countdown() {
        var minutes = Math.floor(secondsLeft / 60);
        var seconds = secondsLeft % 60;
        timerDisplay.textContent = minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
        if (secondsLeft <= 0) {
            clearInterval(timerInterval);
            timerDisplay.textContent = "Time's up!";
            window.location.href = '/timer/complete';
            // You can add additional logic here for what to do when the timer reaches 0
        } else {
            secondsLeft--;
        }
    }

    countdown(); // Call once to initialize the display
    var timerInterval = setInterval(countdown, 1000); // Update every second
});
