function showContent(contentId) {
    // Hide all content sections
    document.getElementById('dashboard-content').style.display = 'none';
    document.getElementById('insertProducts-content').style.display = 'none';
    document.getElementById('usersInformation-content').style.display = 'none';
    document.getElementById('order-content').style.display = 'none';
    
    // Show the selected content section
    document.getElementById(contentId + '-content').style.display = 'block';
    
    // Update active state in navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    event.currentTarget.classList.add('active');
}