document.addEventListener('DOMContentLoaded', () => {
    const pickupBtn = document.getElementById('pickup-btn');

    pickupBtn.addEventListener('click', () => {
        setTimeout(() => {
            window.location.href = '/timer'; // Redirect to the timer page after 10 seconds
        }, 10000); // 10 seconds delay
    });
});
