// Move showToast and createToastContainer functions to global scope
function showToast(message, category = 'success') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast ${category}`;
    toast.setAttribute('role', 'alert');
    
    const messageElement = document.createElement('p');
    messageElement.className = 'toast-message';
    messageElement.textContent = message;
    
    toast.appendChild(messageElement);
    toastContainer.appendChild(toast);
    
    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease-in-out forwards';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

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
                    
                    const message = data.in_wishlist ? 'Added to wishlist' : 'Removed from wishlist';
                    showToast(message);
                } else {
                    if (data.message === 'Please login first') {
                        window.location.href = '/auth';
                    } else {
                        showToast(data.message, 'error');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error updating wishlist. Please try again.', 'error');
            });
        });
    });
});

// Add to cart function
function addToCart(productId, event) {
    event.preventDefault();
    event.stopPropagation(); // Add this to prevent event bubbling
    
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
        showToast(data.message || 'Added to cart successfully', category);
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error adding to cart. Please try again.', 'error');
    });
}