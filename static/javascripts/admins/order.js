// Initialize Feather Icons
document.addEventListener('DOMContentLoaded', function() {
    feather.replace();
});

/**
 * Search functionality for orders table
 * Filters rows based on Order ID, Customer Name, or Email
 */
function searchOrders() {
    const searchInput = document.getElementById('orderSearch');
    const filter = searchInput.value.toLowerCase();
    const rows = document.getElementsByClassName('order-row');

    for (let row of rows) {
        const orderId = row.querySelector('td:first-child').textContent.toLowerCase();
        const name = row.querySelector('.user-name').textContent.toLowerCase();
        const email = row.querySelector('td:nth-child(3)').textContent.toLowerCase();
        
        const shouldShow = orderId.includes(filter) || 
                         name.includes(filter) || 
                         email.includes(filter);
        row.style.display = shouldShow ? '' : 'none';
    }
}

/**
 * Updates order status via API call
 * @param {string} orderId - The ID of the order to update
 * @param {string} newStatus - The new status to set
 */
function updateOrderStatus(orderId, newStatus) {
    fetch(`/admin/update-order-status/${orderId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the status badge in the table
            const row = document.querySelector(`tr[data-order-id="${orderId}"]`);
            const statusCell = row.querySelector('.status-cell');
            statusCell.innerHTML = `<span class="status-badge ${newStatus.toLowerCase()}">${newStatus}</span>`;
            
            // Update the stats
            updateOrderStats(newStatus);
        } else {
            alert('Error updating order status: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating order status. Please try again.');
    });
}

/**
 * Updates the order statistics displayed in the dashboard
 * @param {string} newStatus - The new status that was set
 */
function updateOrderStats(newStatus) {
    const totalOrdersElement = document.querySelector('.stat-card:nth-child(1) .number');
    const pendingOrdersElement = document.querySelector('.stat-card:nth-child(2) .number');
    const completedOrdersElement = document.querySelector('.stat-card:nth-child(3) .number');

    const pendingCount = parseInt(pendingOrdersElement.textContent);
    const completedCount = parseInt(completedOrdersElement.textContent);

    if (newStatus === 'Delivered') {
        pendingOrdersElement.textContent = pendingCount - 1;
        completedOrdersElement.textContent = completedCount + 1;
    } else if (newStatus === 'Cancelled') {
        pendingOrdersElement.textContent = pendingCount - 1;
    }
}

/**
 * Exports the orders table data to a CSV file
 * Excludes action buttons column from export
 */
function exportOrderData() {
    const table = document.querySelector('.orders-table');
    const rows = Array.from(table.querySelectorAll('tr'));
    
    const csvContent = rows.map(row => {
        const cells = Array.from(row.querySelectorAll('th, td'));
        return cells.map(cell => {
            // Skip the action buttons cell
            if (!cell.querySelector('.status-btn')) {
                let text = cell.textContent.trim().replace(/,/g, '');
                return `"${text}"`;
            }
            return '';
        }).join(',');
    }).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `orders_data_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}