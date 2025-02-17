document.addEventListener('DOMContentLoaded', function() {
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    
    // First check initial wishlist state for all products
    wishlistButtons.forEach(button => {
        const productId = button.dataset.productId;
        
        fetch(`/api/wishlist/${productId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.in_wishlist) {
                const svg = button.querySelector('svg');
                svg.style.fill = '#000';
            }
        })
        .catch(error => console.error('Error checking wishlist state:', error));
    });

    // Add click event listeners to all wishlist buttons
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            
            const productId = this.dataset.productId;
            
            fetch(`/api/wishlist/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const svg = this.querySelector('svg');
                    const newFillColor = data.in_wishlist ? '#000' : 'none';
                    svg.style.fill = newFillColor;
                    
                    // Show a temporary success message
                    const message = data.in_wishlist ? 'Added to wishlist' : 'Removed from wishlist';
                    const toast = document.createElement('div');
                    toast.className = 'toast-message';
                    toast.textContent = message;
                    document.body.appendChild(toast);
                    setTimeout(() => toast.remove(), 2000);
                } else {
                    if (data.message === 'Please login first') {
                        window.location.href = '/auth';
                    } else {
                        alert(data.message);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating wishlist. Please try again.');
            });
        });
    });
});