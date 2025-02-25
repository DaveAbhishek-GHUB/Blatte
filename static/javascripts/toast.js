// Only define showToast if it doesn't already exist
if (!window.showToast) {
    window.showToast = function(message, category = 'success') {
        const toastContainer = document.querySelector('.toast-container') || createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast ${category}`;
        toast.setAttribute('role', 'alert');
        
        const messageElement = document.createElement('p');
        messageElement.className = 'toast-message';
        messageElement.textContent = message;
        
        toast.appendChild(messageElement);
        toastContainer.appendChild(toast);
        
        // Remove toast after 3 seconds
        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.3s ease-in-out forwards';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }
}

// Only define createToastContainer if it doesn't already exist
if (!window.createToastContainer) {
    window.createToastContainer = function() {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    }
}

// Initialize toast functionality only once
if (!window.toastInitialized) {
    window.toastInitialized = true;
    
    document.addEventListener('DOMContentLoaded', function() {
        const toasts = document.querySelectorAll('.toast');
        
        toasts.forEach(toast => {
            setTimeout(() => {
                toast.style.animation = 'fadeOut 0.3s ease-in-out forwards';
                setTimeout(() => {
                    toast.remove();
                }, 300);
            }, 3000);
        });
    });
} 