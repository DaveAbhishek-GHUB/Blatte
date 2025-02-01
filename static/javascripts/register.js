function validateForm() {
    const password = document.querySelector('input[name="password"]').value;
    const confirmPassword = document.querySelector('input[name="confirm-password"]').value;
    
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return false;
    }
    
    return true;
}