// Only define showToast if it doesn't already exist
if (!window.showToast) {
    // Keep track of shown messages
    window.shownMessages = new Set();

    window.showToast = function (message, category = 'success') {
        // Check if this message has already been shown
        if (window.shownMessages.has(message)) {
            return; // Skip if already shown
        }

        // Add message to shown messages set
        window.shownMessages.add(message);

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
                // Remove from tracking after toast is gone
                window.shownMessages.delete(message);
            }, 300);
        }, 3000);
    }
}

// Rest of your existing code remains the same
if (!window.createToastContainer) {
    window.createToastContainer = function () {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    }
}

// Initialize toast functionality only once
if (!window.toastInitialized) {
    window.toastInitialized = true;

    document.addEventListener('DOMContentLoaded', function () {
        const toasts = document.querySelectorAll('.toast');
        const shownMessages = new Set();

        toasts.forEach(toast => {
            const message = toast.querySelector('.toast-message').textContent;

            // Check for duplicates
            if (shownMessages.has(message)) {
                toast.remove(); // Remove duplicate toast
                return;
            }

            shownMessages.add(message);

            setTimeout(() => {
                toast.style.animation = 'fadeOut 0.3s ease-in-out forwards';
                setTimeout(() => {
                    toast.remove();
                }, 300);
            }, 3000);
        });
    });
}