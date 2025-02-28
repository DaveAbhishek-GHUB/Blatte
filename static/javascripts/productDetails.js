document.addEventListener('DOMContentLoaded', function() {
    // Dropdown functionality
    const dropdownBtn = document.querySelector('.dropdown-btn');
    if (dropdownBtn) {
        dropdownBtn.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    }

    // Image gallery functionality
    const thumbnails = document.querySelectorAll('.thumbnail-list img');
    const mainImage = document.querySelector('.main-image img');

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            mainImage.src = this.src;
            
            // Remove active class from all thumbnails
            thumbnails.forEach(thumb => thumb.classList.remove('active'));
            // Add active class to clicked thumbnail
            this.classList.add('active');
        });
    });

    // Add to cart functionality
    const addToCartBtn = document.querySelector('.add-to-cart-btn');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const quantity = document.getElementById('product-quantity').value;
            
            fetch(`/api/cart/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity: quantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (window.showToast) {
                        window.showToast('Added to cart');
                    }
                } else {
                    if (window.showToast) {
                        window.showToast(data.message, 'error');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (window.showToast) {
                    window.showToast('Error adding to cart', 'error');
                }
            });
        });
    }

    // Wishlist functionality
    const wishlistBtn = document.querySelector('.wishlist-btn');
    if (wishlistBtn) {
        const productId = wishlistBtn.dataset.productId;

        // Check initial wishlist state
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
                wishlistBtn.classList.add('in-wishlist');
                wishlistBtn.innerHTML = `
                    <i data-feather="heart"></i>
                    Remove from Wishlist
                `;
                feather.replace();
            }
        })
        .catch(error => console.error('Error checking wishlist state:', error));

        // Add click event listener
        wishlistBtn.addEventListener('click', function(event) {
            event.preventDefault();
            
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
                    this.classList.toggle('in-wishlist');
                    if (data.in_wishlist) {
                        this.innerHTML = `
                            <i data-feather="heart"></i>
                            Remove from Wishlist
                        `;
                        if (window.showToast) {
                            window.showToast('Added to wishlist');
                        }
                    } else {
                        this.innerHTML = `
                            <i data-feather="heart"></i>
                            Add to Wishlist
                        `;
                        if (window.showToast) {
                            window.showToast('Removed from wishlist');
                        }
                    }
                    feather.replace();
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
        });
    }
});