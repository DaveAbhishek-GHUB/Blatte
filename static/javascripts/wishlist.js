function addToCart(productId) {
    fetch(`/api/cart/${productId}`, {
        method: 'POST',
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove product from wishlist
            removeFromWishlist(productId);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding to cart');
    });
}

function removeFromWishlist(productId) {
    fetch(`/api/wishlist/${productId}`, {
        method: 'POST',
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove product from DOM
            const item = document.querySelector(`.wishlist-item[data-product-id="${productId}"]`);
            item.remove();
            
            // Check if wishlist is empty
            const items = document.querySelectorAll('.wishlist-item');
            if (items.length === 0) {
                location.reload(); // Reload to show empty state
            }
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating wishlist');
    });
}


