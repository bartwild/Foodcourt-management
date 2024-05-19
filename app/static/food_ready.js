document.addEventListener('DOMContentLoaded', () => {
    const notification = document.getElementById('notification');
    const closeBtn = document.getElementById('close-btn');
    const pickupBtn = document.getElementById('pickup-btn');

    closeBtn.addEventListener('click', () => {
        notification.classList.remove('show');
    });

    pickupBtn.addEventListener('click', () => {
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
            // You can add any additional action here after the notification hides
        }, 5000); // Hide notification after 5 seconds
    });
});
