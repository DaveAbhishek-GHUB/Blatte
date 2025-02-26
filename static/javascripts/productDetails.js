document.addEventListener('DOMContentLoaded', function() {
    // Dropdown functionality
    const dropdownBtn = document.querySelector('.dropdown-btn');
    dropdownBtn.addEventListener('click', function() {
        this.classList.toggle('active');
    });

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
});

// Add new function for cart handling
function addToCart(productId) {
    const quantity = document.getElementById('product-quantity').value;
    
    fetch(`/api/cart/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quantity: parseInt(quantity) })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/cart';
        } else {
            // Handle error case
            alert(data.message || 'Error adding to cart');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding to cart');
    });
}