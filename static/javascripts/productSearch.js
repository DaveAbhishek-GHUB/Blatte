document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('productSearch');
    const searchButton = document.getElementById('searchButton');
    
    function performSearch() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        const productCards = document.querySelectorAll('.productWrapper');
        
        productCards.forEach(card => {
            const productName = card.querySelector('.product-title').textContent.toLowerCase();
            const productDescription = card.querySelector('.description')?.textContent.toLowerCase() || '';
            const productCategory = card.querySelector('.category')?.textContent.toLowerCase() || '';
            
            const matches = productName.includes(searchTerm) || 
                          productDescription.includes(searchTerm) || 
                          productCategory.includes(searchTerm);
            
            card.style.display = matches ? '' : 'none';
        });
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