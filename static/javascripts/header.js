document.addEventListener('DOMContentLoaded', function() {
    // Hamburger menu functionality
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const innerNavbar = document.querySelector('.innerNavbar');

    hamburgerMenu?.addEventListener('click', function() {
        innerNavbar.classList.toggle('active');
    });

    // Search functionality
    const searchIcon = document.querySelector('.search-icon');
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.querySelector('.search-results');
    let searchTimeout = null;

    // Toggle search input
    searchIcon?.addEventListener('click', function(e) {
        e.preventDefault();
        searchInput.classList.toggle('active');
        if (searchInput.classList.contains('active')) {
            searchInput.focus();
        } else {
            searchInput.value = '';
            searchResults.style.display = 'none';
        }
    });

    // Close search when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            searchInput.classList.remove('active');
            searchInput.value = '';
            searchResults.style.display = 'none';
        }
    });

    // Handle search input
    searchInput?.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const searchTerm = this.value.trim();

        if (searchTerm.length === 0) {
            searchResults.style.display = 'none';
            return;
        }

        // Debounce search requests
        searchTimeout = setTimeout(() => {
            fetch(`/api/search-products?term=${encodeURIComponent(searchTerm)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.products.length > 0) {
                        searchResults.innerHTML = data.products.map(product => `
                            <a href="/productDetails/${product.id}" class="search-result-item">
                                <img src="${product.main_product_image}" alt="${product.product_name}">
                                <div class="search-result-info">
                                    <div class="search-result-name">${product.product_name}</div>
                                    <div class="search-result-price">$${product.price}</div>
                                </div>
                            </a>
                        `).join('');
                        searchResults.style.display = 'block';
                    } else {
                        searchResults.innerHTML = '<div class="search-result-item">No products found</div>';
                        searchResults.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Search error:', error);
                    searchResults.innerHTML = '<div class="search-result-item">Error searching products</div>';
                    searchResults.style.display = 'block';
                });
        }, 300); // Delay of 300ms
    });
});
