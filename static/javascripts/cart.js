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

        // Initialize Feather Icons after DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            feather.replace();
        });