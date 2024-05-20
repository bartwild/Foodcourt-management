document.addEventListener('DOMContentLoaded', () => {
    const notification = document.getElementById('notification');
    const closeBtn = document.getElementById('close-btn');
    const orderBtn = document.getElementById('order-btn');

    closeBtn.addEventListener('click', () => {
        notification.classList.remove('show');
    });

    orderBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent the default action (navigation)
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
            window.location.href = orderBtn.href; // Navigate to the link after 5 seconds
        }, 5000); // Hide notification after 5 seconds and then navigate
    });
});
