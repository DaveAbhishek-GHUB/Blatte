// Initialize Feather Icons
feather.replace();

/**
 * Search functionality for users table
 * Filters rows based on name or email matching the search input
 */
function searchUsers() {
    const searchInput = document.getElementById('userSearch');
    const filter = searchInput.value.toLowerCase();
    const rows = document.getElementsByClassName('user-row');

    for (let row of rows) {
        const name = row.querySelector('.user-name').textContent.toLowerCase();
        const email = row.querySelector('td:nth-child(3)').textContent.toLowerCase();
        const shouldShow = name.includes(filter) || email.includes(filter);
        row.style.display = shouldShow ? '' : 'none';
    }
}

/**
 * Delete user functionality
 * @param {string} userId - The ID of the user to delete
 * @param {HTMLElement} button - The button element that triggered the deletion
 */
function deleteUser(userId, button) {
    if (confirm('Are you sure you want to delete this user?')) {
        fetch(`/admin/delete-user/${userId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the row from the table
                button.closest('tr').remove();
                // Update the total users count
                const totalUsersElement = document.querySelector('.stat-card:first-child .number');
                const currentCount = parseInt(totalUsersElement.textContent);
                totalUsersElement.textContent = currentCount - 1;
            } else {
                alert('Error deleting user: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting user. Please try again.');
        });
    }
}

/**
 * Export user data to CSV
 * Generates a CSV file containing user information and triggers download
 */
function exportUserData() {
    // Get table data
    const table = document.querySelector('.users-table');
    const rows = Array.from(table.querySelectorAll('tr'));
    
    // Prepare CSV content
    const csvContent = rows.map(row => {
        const cells = Array.from(row.querySelectorAll('th, td'));
        return cells.map(cell => {
            // Get text content and remove any commas to avoid CSV issues
            let text = cell.textContent.trim().replace(/,/g, '');
            // Skip the action buttons cell
            if (!cell.querySelector('.action-buttons')) {
                return `"${text}"`;
            }
            return '';
        }).join(',');
    }).join('\n');

    // Create blob and download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    // Set download attributes
    link.setAttribute('href', url);
    link.setAttribute('download', `users_data_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    
    // Trigger download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}