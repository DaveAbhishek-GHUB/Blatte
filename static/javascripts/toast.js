document.addEventListener('DOMContentLoaded', function() {
    const toasts = document.querySelectorAll('.toast');
    
    toasts.forEach(toast => {
        // Auto-remove toast after 3 seconds
        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.3s ease-in-out forwards';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    });
}); 