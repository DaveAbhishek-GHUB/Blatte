document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather icons
    feather.replace();

    // Get all payment methods and details
    const paymentMethods = document.querySelectorAll('.payment-method');
    const paymentDetails = document.querySelectorAll('.payment-details');

    // Initially hide all payment details except the first one
    paymentDetails.forEach((detail, index) => {
        if (index === 0) {
            detail.style.display = 'block';
            const method = paymentMethods[0];
            method.classList.add('selected');
            const methodCheck = method.querySelector('.method-check i');
            if (methodCheck) methodCheck.style.display = 'block';
        } else {
            detail.style.display = 'none';
        }
    });

    // Add click event listeners to payment methods
    paymentMethods.forEach(method => {
        method.addEventListener('click', function() {
            // Remove selected class and hide check icons from all methods
            paymentMethods.forEach(m => {
                m.classList.remove('selected');
                const checkIcon = m.querySelector('.method-check i');
                if (checkIcon) checkIcon.style.display = 'none';
            });

            // Add selected class and show check icon for clicked method
            this.classList.add('selected');
            const checkIcon = this.querySelector('.method-check i');
            if (checkIcon) checkIcon.style.display = 'block';

            // Hide all payment details
            paymentDetails.forEach(detail => {
                detail.style.display = 'none';
            });

            // Show the selected payment details
            const methodType = this.getAttribute('data-method');
            const selectedDetails = document.querySelector(`.${methodType}-details`);
            if (selectedDetails) {
                selectedDetails.style.display = 'block';
            }

            // Update hidden payment method input in all forms
            document.querySelectorAll('input[name="payment_method"]').forEach(input => {
                input.value = methodType;
            });
        });
    });

    // Add hidden payment method input to all forms if not exists
    document.querySelectorAll('.payment-form').forEach(form => {
        if (!form.querySelector('input[name="payment_method"]')) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'payment_method';
            input.value = 'card'; // Default value
            form.appendChild(input);
        }
    });

    // Form submission handling
    document.querySelectorAll('.payment-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const button = this.querySelector('.pay-button');
            const buttonContent = button.querySelector('.button-content');
            const buttonLoader = button.querySelector('.button-loader');
            
            // Show loading state
            if (buttonContent && buttonLoader) {
                buttonContent.style.display = 'none';
                buttonLoader.style.display = 'block';
                button.disabled = true;
            }

            // Submit the form
            this.submit();
        });
    });

    // Initialize phone inputs
    const phoneInputs = document.querySelectorAll('.phone-input');
    phoneInputs.forEach(input => {
        window.intlTelInput(input, {
            utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
            preferredCountries: ['in', 'us', 'gb'],
            separateDialCode: true
        });
    });

    // Add this after the existing validation functions
    let countryList = [];
    let stateList = [];
    let cityList = [];

    // Fetch countries from API
    fetch('https://restcountries.com/v3.1/all')
        .then(response => response.json())
        .then(data => {
            countryList = data.map(country => country.name.common);
        })
        .catch(error => {
            console.error('Error fetching countries:', error);
        });

    // Fetch states from API
    fetch('https://mocki.io/v1/a78fb490-bee1-4b4c-b1c7-cfb048491e55')
        .then(response => response.json())
        .then(data => {
            stateList = data.states;
        })
        .catch(error => {
            console.error('Error fetching states:', error);
        });

    // Fetch cities from API - using a more comprehensive cities API
    fetch('https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json')
        .then(response => response.json())
        .then(data => {
            cityList = data.map(city => city.name);
        })
        .catch(error => {
            console.error('Error fetching cities:', error);
            // Fallback to a basic list of major cities if the API fails
            cityList = ["New York", "London", "Paris", "Tokyo", "Sydney", "Mumbai", "Dubai", 
                       "Singapore", "Hong Kong", "Shanghai", "Seoul", "Moscow", "Berlin", 
                       "Madrid", "Rome", "Amsterdam", "Stockholm", "Vienna", "Prague", 
                       "Budapest", "Warsaw", "Athens", "Cairo", "Istanbul", "Tehran", 
                       "Baghdad", "Riyadh", "Jakarta", "Manila", "Bangkok", "Hanoi", 
                       "Beijing", "Toronto", "Mexico City", "Buenos Aires", "Rio de Janeiro",
                       "São Paulo", "Lima", "Bogotá", "Santiago", "Johannesburg", "Lagos",
                       "Nairobi", "Cape Town", "Casablanca", "Auckland", "Melbourne"];
        });

    function setupAutocomplete() {
        const autocompleteInputs = document.querySelectorAll('.autocomplete-input');
        
        autocompleteInputs.forEach(input => {
            const suggestionsContainer = input.nextElementSibling;
            
            input.addEventListener('input', function() {
                const inputValue = this.value.toLowerCase();
                let suggestions = [];
                
                if (this.dataset.type === 'country') {
                    suggestions = countryList.filter(country => 
                        country.toLowerCase().startsWith(inputValue)
                    );
                } else if (this.dataset.type === 'state') {
                    suggestions = stateList.filter(state =>
                        state.toLowerCase().startsWith(inputValue)
                    );
                } else if (this.dataset.type === 'city') {
                    suggestions = cityList.filter(city =>
                        city.toLowerCase().startsWith(inputValue)
                    );
                }
                
                displaySuggestions(suggestions, suggestionsContainer, input);
            });
            
            // Hide suggestions when clicking outside
            document.addEventListener('click', (e) => {
                if (!input.contains(e.target)) {
                    suggestionsContainer.innerHTML = '';
                }
            });
        });
    }

    function displaySuggestions(suggestions, container, input) {
        container.innerHTML = '';
        if (suggestions.length > 0) {
            suggestions.forEach(suggestion => {
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.textContent = suggestion;
                div.addEventListener('click', () => {
                    input.value = suggestion;
                    container.innerHTML = '';
                    // Trigger change event for dependent fields
                    input.dispatchEvent(new Event('change'));
                });
                container.appendChild(div);
            });
        }
    }

    // Update the validateInput function
    function validateInput(input) {
        const errorMsg = input.closest('.form-group').querySelector('.error-message');
        let isValid = true;
        let errorText = '';

        // Clear previous errors
        input.classList.remove('error');
        errorMsg.textContent = '';

        // Required field validation
        if (input.required && !input.value) {
            errorText = 'This field is required';
            isValid = false;
        }
        // Pattern validation
        else if (input.pattern && !new RegExp(input.pattern).test(input.value)) {
            switch (input.name) {
                case 'cvv':
                    errorText = 'Please enter a valid 3-digit CVV';
                    break;
                case 'accountNumber':
                    errorText = 'Please enter a valid numeric account number';
                    break;
                case 'ifscCode':
                    errorText = 'Please enter a valid 11-character IFSC code';
                    break;
                case 'bankName':
                case 'accountHolder':
                case 'fullName':
                case 'city':
                    errorText = 'Please enter valid alphabetic characters only';
                    break;
                case 'pincode':
                    errorText = 'Please enter a valid 6-digit pincode';
                    break;
                default:
                    errorText = 'Please enter a valid value';
            }
            isValid = false;
        }

        if (!isValid) {
            input.classList.add('error');
            errorMsg.textContent = errorText;
        }

        return isValid;
    }

    // Real-time validation
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', () => {
            if (!input.classList.contains('phone-input')) {
                validateInput(input);
            }
        });
    });

    // Input validation and formatting
    const cardNumberInput = document.querySelector('input[placeholder="Card Number"]');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{4})/g, '$1 ').trim();
            e.target.value = value.substring(0, 19);
        });
    }

    const expiryInput = document.querySelector('input[placeholder="MM / YY"]');
    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.substring(0, 2) + ' / ' + value.substring(2);
            }
            e.target.value = value.substring(0, 7);
        });
    }

    setupAutocomplete();
});