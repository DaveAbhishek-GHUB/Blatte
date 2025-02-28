document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('productSearch');
    const searchButton = document.getElementById('searchButton');
    const productsContainer = document.querySelector('.productsWrapper');
    const paginationContainer = document.querySelector('.pagination');
    
    async function performSearch() {
        const searchTerm = searchInput.value.trim();
        if (searchTerm === '') {
            // If search is empty, reload the page to show original pagination
            window.location.reload();
            return;
        }
        
        try {
            const response = await fetch(`/api/search-products?term=${encodeURIComponent(searchTerm)}`);
            const data = await response.json();
            
            if (data.success) {
                // Clear existing products
                productsContainer.innerHTML = '';
                
                // Hide pagination during search results
                if (paginationContainer) {
                    paginationContainer.style.display = 'none';
                }
                
                // Display search results
                data.products.forEach(product => {
                    const productCard = createProductCard(product);
                    productsContainer.appendChild(productCard);
                });
                
                if (data.products.length === 0) {
                    productsContainer.innerHTML = `
                        <div class="no-results">
                            <h2>No products found</h2>
                            <p>Try different search terms</p>
                        </div>
                    `;
                }
            }
        } catch (error) {
            console.error('Search error:', error);
        }
    }
    
    function createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'productWrapper';
        
        card.innerHTML = `
            <a href="/productDetails/${product.id}">
                <div class="productImage">
                    <div class="tags">
                        ${product.discount_percentage ? `<span class="tag">-${product.discount_percentage}%</span>` : ''}
                        ${product.availability_status && product.availability_status !== 'In Stock' ? `<span class="tag">${product.availability_status}</span>` : ''}
                    </div>
                    <img src="${product.main_product_image}" alt="${product.product_name}">
                    <button class="wishlist-btn" data-product-id="${product.id}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                        </svg>
                    </button>
                </div>
                <div class="productInfo">
                    <div class="category">${product.product_category}</div>
                    <h3 class="product-title">${product.product_name}</h3>
                    <p class="description">${Array.isArray(product.description) ? product.description[0] || '' : ''}</p>
                    <div class="price-cart">
                        <span class="price">€${product.price}</span>
                        <button class="cart-btn" aria-label="Add to cart">
                            <img src="/static/images/svgs/cart.svg" alt="Cart icon">
                        </button>
                    </div>
                </div>
            </a>
        `;
        
        // Initialize wishlist functionality for this card
        const wishlistBtn = card.querySelector('.wishlist-btn');
        if (wishlistBtn) {
            // Check initial wishlist state
            const productId = wishlistBtn.dataset.productId;
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
                    const svg = wishlistBtn.querySelector('svg');
                    svg.style.fill = '#000';
                }
            })
            .catch(error => console.error('Error checking wishlist state:', error));

            // Add click event listener
            wishlistBtn.addEventListener('click', function(event) {
                event.preventDefault();
                event.stopPropagation();
                
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
            });
        }
        
        return card;
    }
    
    // Search on button click
    searchButton.addEventListener('click', performSearch);
    
    // Search on Enter key press
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // Optional: Live search as user types (with debounce)
    let debounceTimer;
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(performSearch, 300);
    });
});