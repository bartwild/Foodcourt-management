document.addEventListener('DOMContentLoaded', () => {
    const notification = document.getElementById('notification');
    const closeBtn = document.getElementById('close-btn');
    const orderBtn = document.getElementById('order-btn');
    const clearBtn = document.getElementById('clear-button');

    closeBtn.addEventListener('click', () => {
        notification.classList.remove('show');
    });

    orderBtn.addEventListener('click', (event) => {
        const cartItems = document.querySelectorAll('.list-group-item');
        if (cartItems.length === 0) {
            event.preventDefault();
            notification.classList.add('show');
            setTimeout(() => {
                notification.classList.remove('show');
            }, 5000);
        } else {
            clearBtn.click();
        }
    });

    function occupieTable() {
        const table = window.location.pathname.split('/')[1];

        var postData = { 'table_number': parseInt(table), 'status': 'occupied' };
        console.log('Table 1 is now occupied');
        fetch('/update_tables', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(postData)
        });
    }

    document.getElementById('order-btn').addEventListener('click', occupieTable);
});
