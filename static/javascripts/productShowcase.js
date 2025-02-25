// Remove the showToast and createToastContainer functions completely
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
        // Remove any existing click listeners first
        button.removeEventListener('click', handleWishlistClick);
        // Add new click listener
        button.addEventListener('click', handleWishlistClick);
    });
});

// Separate function for handling wishlist clicks
function handleWishlistClick(event) {
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
            
            const message = data.in_wishlist ? 'Added to wishlist' : 'Removed from wishlist';
            if (window.showToast) {
                window.showToast(message);
            }
        } else {
            if (data.message === 'Please login first') {
                window.location.href = '/auth';
            } else if (window.showToast) {
                window.showToast(data.message, 'error');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (window.showToast) {
            window.showToast('Error updating wishlist. Please try again.', 'error');
        }
    });
}

// Add to cart function
function addToCart(productId, event) {
    event.preventDefault();
    event.stopPropagation();
    
    fetch(`/api/cart/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        const category = data.success ? 'success' : 'error';
        if (window.showToast) {
            window.showToast(data.message || 'Added to cart successfully', category);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (window.showToast) {
            window.showToast('Error adding to cart. Please try again.', 'error');
        }
    });
}