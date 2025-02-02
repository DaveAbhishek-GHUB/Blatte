document.addEventListener('DOMContentLoaded', function() {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const innerNavbar = document.querySelector('.innerNavbar');

    hamburgerMenu.addEventListener('click', function() {
        innerNavbar.classList.toggle('active');
    });
});
