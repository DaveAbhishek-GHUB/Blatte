/**
 * Filter products based on search input
 */
function searchProducts() {
    const searchInput = document.getElementById('productSearch');
    const filter = searchInput.value.toLowerCase();
    const rows = document.getElementsByClassName('product-row');

    for (let row of rows) {
        const name = row.querySelector('.product-name').textContent.toLowerCase();
        const category = row.querySelector('td:nth-child(3)').textContent.toLowerCase();
        const shouldShow = name.includes(filter) || category.includes(filter);
        row.style.display = shouldShow ? '' : 'none';
    }
}

/**
 * Delete a product with confirmation
 * @param {string} productId - The ID of the product to delete
 * @param {HTMLElement} button - The button that triggered the deletion
 */
function deleteProduct(productId, button) {
    if (confirm('Are you sure you want to delete this product?')) {
        fetch(`/admin/delete-product/${productId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the row from the table
                button.closest('tr').remove();
                // Update the total products count
                const totalProductsElement = document.querySelector('.stat-card:first-child .number');
                const currentCount = parseInt(totalProductsElement.textContent);
                totalProductsElement.textContent = currentCount - 1;
            } else {
                alert('Error deleting product: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting product. Please try again.');
        });
    }
}

/**
 * Export product data to CSV file
 */
function exportProductData() {
    const table = document.querySelector('.products-table');
    const rows = Array.from(table.querySelectorAll('tr'));
    
    const csvContent = rows.map(row => {
        const cells = Array.from(row.querySelectorAll('th, td'));
        return cells.map(cell => {
            if (cell.querySelector('img')) {
                return '"' + cell.querySelector('img').src + '"';
            }
            let text = cell.textContent.trim().replace(/,/g, '');
            if (!cell.querySelector('.action-buttons')) {
                return `"${text}"`;
            }
            return '';
        }).join(',');
    }).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `products_data_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Initialize Feather Icons
feather.replace();