document.querySelector('form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    // Get all form inputs
    const inputs = this.querySelectorAll('input, textarea, select');
    let isValid = true;
    
    // Clear previous error messages
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    
    // Check each input
    inputs.forEach(input => {
        // Remove previous error styling
        input.classList.remove('error');
        
        // Skip optional empty fields
        if (!input.required && !input.value) {
            return;
        }
        
        // Check validity
        if (!input.checkValidity()) {
            isValid = false;
            input.classList.add('error');
            
            // Create and show error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = input.title || 'Please fill this field correctly';
            input.parentNode.insertBefore(errorDiv, input.nextSibling);
        }
    });
    
    if (isValid) {
        try {
            const formData = new FormData(this);
            const response = await fetch('/Contact', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                // Show success toast notification
                showToast('Message sent successfully', 'success');
                // Reset form after successful submission
                this.reset();
            } else {
                // Show error toast notification
                showToast('Error submitting form', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            // Show error toast notification
            showToast('Error submitting form', 'error');
        }
    }
});

// Toast notification function
function showToast(message, type) {
    const toast = document.querySelector('.toast');
    const toastMessage = document.querySelector('.toast-message');
    
    if (toast && toastMessage) {
        toastMessage.textContent = message;
        toast.className = `toast ${type}`; // Reset class and add type
        toast.style.display = 'block';
        
        // Auto hide after 3 seconds
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3000);
    }
} 