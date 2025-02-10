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
    
    // Convert array inputs to JSON arrays
    const description = Array.from(formData.getAll('description[]'));
    const ingredients = Array.from(formData.getAll('ingredients[]')).filter(item => item);
    const brewingNotes = Array.from(formData.getAll('brewing_notes[]')).filter(item => item);
    const additionalImages = Array.from(formData.getAll('additional_images[]')).filter(item => item);
    
    // Remove the array inputs and add the JSON strings
    formData.delete('description[]');
    formData.delete('ingredients[]');
    formData.delete('brewing_notes[]');
    formData.delete('additional_images[]');
    
    formData.append('description', JSON.stringify(description));
    formData.append('ingredients', JSON.stringify(ingredients));
    formData.append('brewing_notes', JSON.stringify(brewingNotes));
    formData.append('additional_images', JSON.stringify(additionalImages));
    
    // Send the form data to your backend
    // Add your fetch or AJAX call here
    console.log(Object.fromEntries(formData));
});