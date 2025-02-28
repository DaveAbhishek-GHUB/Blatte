// Category scroll functionality
document.addEventListener('DOMContentLoaded', function() {
    const categorySection = document.querySelector('.categorySection');
    const leftArrow = document.querySelector('.scroll-left');
    const rightArrow = document.querySelector('.scroll-right');
    const scrollAmount = 300; // Adjust scroll amount as needed

    if (categorySection && leftArrow && rightArrow) {
        leftArrow.addEventListener('click', () => {
            categorySection.scrollBy({
                left: -scrollAmount,
                behavior: 'smooth'
            });
        });

        rightArrow.addEventListener('click', () => {
            categorySection.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
        });

        // Show/hide arrows based on scroll position
        const toggleArrows = () => {
            leftArrow.style.display = categorySection.scrollLeft <= 0 ? 'none' : 'flex';
            rightArrow.style.display = 
                categorySection.scrollLeft + categorySection.clientWidth >= categorySection.scrollWidth 
                ? 'none' : 'flex';
        };

        categorySection.addEventListener('scroll', toggleArrows);
        window.addEventListener('resize', toggleArrows);
        toggleArrows(); // Initial check
    }
});