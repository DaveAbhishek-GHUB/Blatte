        /**
         * Removes a product from the cart
         * @param {string} productId - The ID of the product to remove
         */
        function removeFromCart(productId) {
            fetch(`/api/cart/${productId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        }

        /**
         * Adds a product to the wishlist and removes it from cart
         * @param {string} productId - The ID of the product to move
         */
        function addToWishlist(productId) {
            fetch(`/api/wishlist/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    removeFromCart(productId);
                }
            });
        }

        /**
         * Redirects user to the checkout page
         */
        function proceedToCheckout() {
            window.location.href = '/checkout';
        }

        /**
         * Updates the quantity of a product in the cart and recalculates the price
         * @param {string} productId - The ID of the product to update
         * @param {string} quantity - The new quantity
         */
        function updateQuantity(productId, quantity) {
            const cartItem = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
            const priceElement = cartItem.querySelector('.price-section p');
            const basePrice = parseFloat(priceElement.getAttribute('data-base-price') || priceElement.textContent.replace('₹', ''));
            
            // Store the base price if not already stored
            if (!priceElement.hasAttribute('data-base-price')) {
                priceElement.setAttribute('data-base-price', basePrice);
            }
            
            // Calculate new price
            const newPrice = basePrice * parseInt(quantity);
            
            // Update the displayed price
            priceElement.textContent = `₹${newPrice.toFixed(2)}`;
            
            // Update the quantity in the backend
            fetch(`/api/cart/${productId}/quantity`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity: parseInt(quantity) })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    if (window.showToast) {
                        window.showToast('Quantity updated successfully', 'success');
                    }
                } else {
                    // Show error message and reset quantity
                    if (window.showToast) {
                        window.showToast('Failed to update quantity', 'error');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (window.showToast) {
                    window.showToast('Error updating quantity', 'error');
                }
            });
        }

        // Initialize Feather Icons after DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            feather.replace();
        });