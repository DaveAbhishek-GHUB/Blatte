function addInput(containerId, type) {
    const container = document.getElementById(containerId);
    const inputGroup = document.createElement('div');
    inputGroup.className = 'input-group';
    
    let input;
    if (type === 'description') {
        input = document.createElement('textarea');
        input.className = 'description-input';
        input.name = 'description[]';
        input.required = true;
    } else {
        input = document.createElement('input');
        input.type = type === 'additional_images' ? 'url' : 'text';
        input.className = type === 'ingredients' ? 'ingredient-input' : 
                         type === 'brewing_notes' ? 'brewing-note-input' : 
                         'additional-image-input';
        input.name = `${type}[]`;
    }

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'remove-btn';
    removeBtn.innerHTML = '×';
    removeBtn.onclick = function() { removeInput(this); };

    inputGroup.appendChild(input);
    inputGroup.appendChild(removeBtn);
    container.appendChild(inputGroup);

    // Show all remove buttons in this container
    updateRemoveButtons(container);
}

function removeInput(button) {
    const container = button.parentElement.parentElement;
    button.parentElement.remove();
    // Update remove buttons visibility after removing an input
    updateRemoveButtons(container);
}

function updateRemoveButtons(container) {
    const removeButtons = container.querySelectorAll('.remove-btn');
    removeButtons.forEach(btn => {
        btn.style.display = removeButtons.length === 1 ? 'none' : 'flex';
    });
}

// Initialize remove buttons visibility on page load
document.addEventListener('DOMContentLoaded', function() {
    const containers = [
        'description-container', 
        'ingredients-container', 
        'brewing-notes-container',
        'additional-images-container'
    ];
    containers.forEach(containerId => {
        const container = document.getElementById(containerId);
        updateRemoveButtons(container);
    });
});

// Handle form submission
document.getElementById('productForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    // Convert array inputs to JSON arrays and filter out empty values
    const description = Array.from(formData.getAll('description[]')).filter(item => item.trim());
    const ingredients = Array.from(formData.getAll('ingredients[]')).filter(item => item.trim());
    const brewingNotes = Array.from(formData.getAll('brewing_notes[]')).filter(item => item.trim());
    const additionalImages = Array.from(formData.getAll('additional_images[]')).filter(item => item.trim());
    
    // Remove the array inputs and add the JSON strings
    formData.delete('description[]');
    formData.delete('ingredients[]');
    formData.delete('brewing_notes[]');
    formData.delete('additional_images[]');
    
    formData.append('description', JSON.stringify(description));
    formData.append('ingredients', JSON.stringify(ingredients));
    formData.append('brewing_notes', JSON.stringify(brewingNotes));
    formData.append('additional_images', JSON.stringify(additionalImages));

    // Add discount percentage if it exists
    const discountPercentage = formData.get('discount_percentage');
    if (discountPercentage) {
        formData.append('discount_percentage', discountPercentage);
    }

    // Add dimensions if it exists
    const dimensions = formData.get('dimensions');
    if (dimensions) {
        formData.append('dimensions', dimensions);
    }
    
    // Submit the form
    fetch('/admins/add-product', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        window.location.href = '/admins/dashboard';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding product. Please try again.');
    });
});