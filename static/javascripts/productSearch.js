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
                    <img src="${product.main_product_image}" alt="${product.product_name}">
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