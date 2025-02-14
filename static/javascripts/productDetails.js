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