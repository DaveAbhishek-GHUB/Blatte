document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }

    // Add bank list array at the top with default values since API is not working
    let bankList = [
        "State Bank of India",
        "HDFC Bank",
        "ICICI Bank",
        "Punjab National Bank",
        "Bank of Baroda",
        "Canara Bank",
        "Axis Bank",
        "Union Bank of India",
        "Bank of India",
        "Indian Bank"
    ];
    let selectedBank = ''; // Track the selected bank

    // Validation patterns
    const validationPatterns = {
        cardNumber: /^(\d{4}\s){3}\d{4}$/, // 16 digits in groups of 4
        cvv: /^\d{3}$/, // 3 digits
        expiryDate: /^(0[1-9]|1[0-2])\s\/\s([0-9]{2})$/, // MM / YY format
        ifscCode: /^[A-Z]{4}0[A-Z0-9]{6}$/, // 4 chars, 0, 6 alphanumeric
        accountNumber: /^\d{9,18}$/, // 9-18 digits
        pincode: /^\d{6}$/, // 6 digits
        phone: /^\+?[\d\s-]{8,}$/, // At least 8 digits, can have +, spaces, -
        fullName: /^[A-Za-z\s]{2,50}$/, // 2-50 characters, letters and spaces
        houseNo: /^[A-Za-z0-9\s\-\/\\,.]{1,50}$/, // Alphanumeric with some special chars
        street: /^[A-Za-z0-9\s\-\/\\,.]{5,100}$/, // Alphanumeric with some special chars
        city: /^[A-Za-z\s]{2,50}$/, // Letters and spaces
        state: /^[A-Za-z\s]{2,50}$/, // Letters and spaces
        country: /^[A-Za-z\s]{2,50}$/ // Letters and spaces
    };

    // Validation messages
    const validationMessages = {
        cardNumber: 'Please enter a valid 16-digit card number',
        cvv: 'Please enter a valid 3-digit CVV',
        expiryDate: 'Please enter a valid expiry date (MM / YY)',
        ifscCode: 'Please enter a valid 11-character IFSC code',
        accountNumber: 'Please enter a valid account number (9-18 digits)',
        bankName: 'Please select a valid bank from the suggestions',
        pincode: 'Please enter a valid 6-digit pincode',
        phone: 'Please enter a valid phone number',
        fullName: 'Please enter a valid name (2-50 characters)',
        accountHolder: 'Please enter a valid account holder name (2-50 characters)',
        houseNo: 'Please enter a valid house/flat number',
        street: 'Please enter a valid street address (minimum 5 characters)',
        city: 'Please enter a valid city name',
        state: 'Please enter a valid state name',
        country: 'Please enter a valid country name'
    };

    // Function to validate expiry date
    function isValidExpiryDate(value) {
        if (!validationPatterns.expiryDate.test(value)) return false;
        
        const [month, year] = value.split(' / ');
        const expiry = new Date(2000 + parseInt(year), parseInt(month) - 1);
        const today = new Date();
        
        return expiry > today;
    }

    // Update the validateInput function with comprehensive validation
    function validateInput(input) {
        const formGroup = input.closest('.form-group');
        if (!formGroup) return true; // Skip validation if form group not found
        
        let errorMsg = formGroup.querySelector('.error-message');
        if (!errorMsg) {
            // Create error message element if it doesn't exist
            errorMsg = document.createElement('div');
            errorMsg.className = 'error-message';
            formGroup.appendChild(errorMsg);
        }
        
        let isValid = true;
        let errorText = '';

        // Clear previous errors
        input.classList.remove('error');
        errorMsg.textContent = '';

        // Required field validation
        if (input.required && !input.value) {
            errorText = 'This field is required';
            isValid = false;
        } else {
            switch (input.name) {
                case 'cardNumber':
                    if (!validationPatterns.cardNumber.test(input.value)) {
                        errorText = validationMessages.cardNumber;
                        isValid = false;
                    }
                    break;

                case 'cvv':
                    if (!validationPatterns.cvv.test(input.value)) {
                        errorText = validationMessages.cvv;
                        isValid = false;
                    }
                    break;

                case 'expiryDate':
                    if (!isValidExpiryDate(input.value)) {
                        errorText = validationMessages.expiryDate;
                        isValid = false;
                    }
                    break;

                case 'ifscCode':
                    if (!validationPatterns.ifscCode.test(input.value.toUpperCase())) {
                        errorText = validationMessages.ifscCode;
                        isValid = false;
                    }
                    break;

                case 'accountNumber':
                    if (!validationPatterns.accountNumber.test(input.value)) {
                        errorText = validationMessages.accountNumber;
                        isValid = false;
                    }
                    break;

                case 'bankName':
                    if (input.value !== selectedBank || !bankList.includes(input.value)) {
                        errorText = validationMessages.bankName;
                        isValid = false;
                    }
                    break;

                case 'pincode':
                    if (!validationPatterns.pincode.test(input.value)) {
                        errorText = validationMessages.pincode;
                        isValid = false;
                    }
                    break;

                case 'phone':
                case 'altPhone':
                    if (input.value && !validationPatterns.phone.test(input.value)) {
                        errorText = validationMessages.phone;
                        isValid = false;
                    }
                    break;

                case 'fullName':
                case 'accountHolder':
                    if (!validationPatterns.fullName.test(input.value)) {
                        errorText = validationMessages[input.name];
                        isValid = false;
                    }
                    break;

                case 'houseNo':
                    if (!validationPatterns.houseNo.test(input.value)) {
                        errorText = validationMessages.houseNo;
                        isValid = false;
                    }
                    break;

                case 'street':
                    if (!validationPatterns.street.test(input.value)) {
                        errorText = validationMessages.street;
                        isValid = false;
                    }
                    break;

                case 'city':
                    if (!validationPatterns.city.test(input.value)) {
                        errorText = validationMessages.city;
                        isValid = false;
                    }
                    break;

                case 'state':
                    if (!validationPatterns.state.test(input.value)) {
                        errorText = validationMessages.state;
                        isValid = false;
                    }
                    break;

                case 'country':
                    if (!validationPatterns.country.test(input.value)) {
                        errorText = validationMessages.country;
                        isValid = false;
                    }
                    break;
            }
        }

        if (!isValid) {
            input.classList.add('error');
            errorMsg.textContent = errorText;
        }

        return isValid;
    }

    // Add input formatters for specific fields
    function setupInputFormatters() {
        // Card number formatter
        const cardNumberInput = document.querySelector('input[name="cardNumber"]');
        if (cardNumberInput) {
            cardNumberInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                value = value.replace(/(\d{4})/g, '$1 ').trim();
                e.target.value = value.substring(0, 19);
                validateInput(this);
            });
        }

        // Expiry date formatter
        const expiryInput = document.querySelector('input[name="expiryDate"]');
        if (expiryInput) {
            expiryInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length >= 2) {
                    value = value.substring(0, 2) + ' / ' + value.substring(2);
                }
                e.target.value = value.substring(0, 7);
                validateInput(this);
            });
        }

        // IFSC code formatter
        const ifscInput = document.querySelector('input[name="ifscCode"]');
        if (ifscInput) {
            ifscInput.addEventListener('input', function(e) {
                let value = e.target.value.toUpperCase();
                e.target.value = value.substring(0, 11);
                validateInput(this);
            });
        }

        // Account number formatter
        const accountInput = document.querySelector('input[name="accountNumber"]');
        if (accountInput) {
            accountInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                e.target.value = value.substring(0, 18);
                validateInput(this);
            });
        }

        // Pincode formatter
        const pincodeInput = document.querySelector('input[name="pincode"]');
        if (pincodeInput) {
            pincodeInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                e.target.value = value.substring(0, 6);
                validateInput(this);
            });
        }
    }

    // Setup form submission validation
    document.querySelectorAll('.payment-form').forEach(form => {
        if (!form) return; // Skip if form not found
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            let isFormValid = true;
            const inputs = this.querySelectorAll('input[required]');
            
            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isFormValid = false;
                }
            });

            if (isFormValid) {
                const button = this.querySelector('.pay-button');
                if (!button) return; // Skip if button not found
                
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
            }
        });
    });

    // Initialize all formatters and validators
    setupInputFormatters();

    // Real-time validation for all inputs
    document.querySelectorAll('input').forEach(input => {
        if (!input.classList.contains('phone-input')) {
            input.addEventListener('blur', () => {
                validateInput(input);
            });
        }
    });

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
                
                displaySuggestions(suggestions, suggestionsContainer, this);
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

    setupAutocomplete();

    // Update all pay button amounts with the total from the server
    const totalAmountElement = document.querySelector('.price-row.total span:last-child');
    if (totalAmountElement) {
        const totalAmount = totalAmountElement.textContent;
        document.querySelectorAll('.button-amount').forEach(amount => {
            if (amount) {
                amount.textContent = totalAmount;
            }
        });
    }

    loadSavedData();

    // Add bank name specific handling
    const bankNameInput = document.querySelector('input[name="bankName"]');
    if (bankNameInput) {
        const suggestionsContainer = document.createElement('div');
        suggestionsContainer.className = 'suggestions-container';
        bankNameInput.parentNode.insertBefore(suggestionsContainer, bankNameInput.nextSibling);

        // Prevent direct typing/pasting in the input
        bankNameInput.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' || e.key === 'Delete') {
                selectedBank = '';
            }
        });

        bankNameInput.addEventListener('input', function() {
            const inputValue = this.value.toLowerCase();
            const suggestions = bankList.filter(bank => 
                bank.toLowerCase().includes(inputValue)
            ).slice(0, 10); // Limit to 10 suggestions

            displayBankSuggestions(suggestions, suggestionsContainer, this);
            
            // If the input value doesn't match the selected bank, mark as invalid
            if (this.value !== selectedBank) {
                this.classList.add('error');
                const errorMsg = this.closest('.form-group').querySelector('.error-message');
                errorMsg.textContent = 'Please select a bank from the suggestions';
            }
        });

        // Prevent pasting invalid values
        bankNameInput.addEventListener('paste', function(e) {
            e.preventDefault();
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!bankNameInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
                suggestionsContainer.innerHTML = '';
                // Validate the input when clicking outside
                if (bankNameInput.value !== selectedBank) {
                    bankNameInput.value = selectedBank; // Reset to last valid selection
                }
            }
        });
    }

    function displayBankSuggestions(suggestions, container, input) {
        container.innerHTML = '';
        if (suggestions.length > 0 && input.value.length > 0) {
            suggestions.forEach(suggestion => {
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.textContent = suggestion;
                div.addEventListener('click', () => {
                    input.value = suggestion;
                    selectedBank = suggestion; // Update selected bank
                    container.innerHTML = '';
                    input.classList.remove('error');
                    const errorMsg = input.closest('.form-group').querySelector('.error-message');
                    errorMsg.textContent = '';
                });
                container.appendChild(div);
            });
        }
    }
});

function loadSavedData() {
    fetch('/api/user/saved-data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data && typeof data === 'object') {
                populateSavedAddresses(data.addresses || []);
                populateSavedPaymentMethods(data.payment_methods || []);
            }
        })
        .catch(error => {
            console.warn('Error loading saved data:', error);
            // Initialize with empty data instead of failing
            populateSavedAddresses([]);
            populateSavedPaymentMethods([]);
        });
}

function populateSavedAddresses(addresses) {
    const container = document.querySelector('.saved-addresses-list');
    if (!container) return; // Add null check
    
    if (!addresses || !Array.isArray(addresses)) {
        addresses = []; // Provide empty array if addresses is invalid
    }
    
    container.innerHTML = addresses.map(address => `
        <div class="saved-item" data-address-id="${address.id}">
            <div class="saved-item-header">
                <span class="saved-item-title">${address.house_number}, ${address.street}</span>
                <i data-feather="check-circle" class="check-icon"></i>
            </div>
            <div class="saved-item-details">
                ${address.city}, ${address.state} ${address.pincode}<br>
                ${address.country}
            </div>
        </div>
    `).join('');
    
    // Initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Add click handlers
    container.querySelectorAll('.saved-item').forEach(item => {
        item.addEventListener('click', () => selectSavedAddress(item));
    });
}

function populateSavedPaymentMethods(methods) {
    const container = document.querySelector('.saved-payment-methods-list');
    if (!container) return; // Add null check
    
    if (!methods || !Array.isArray(methods)) {
        methods = []; // Provide empty array if methods is invalid
    }
    
    container.innerHTML = methods.map(method => `
        <div class="saved-item" data-method-id="${method.id || ''}">
            <div class="saved-item-header">
                <span class="saved-item-title">${method.type === 'card' ? 'Card' : 'Bank Account'}</span>
                <i data-feather="check-circle" class="check-icon"></i>
            </div>
            <div class="saved-item-details">
                ${method.type === 'card' 
                    ? `${method.card_number || ''}<br>Expires: ${method.expiry || ''}`
                    : `${method.bank_name || ''}<br>Account: ${method.account_number || ''}<br>IFSC: ${method.ifsc || ''}`}
            </div>
        </div>
    `).join('');
    
    // Initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Add click handlers
    container.querySelectorAll('.saved-item').forEach(item => {
        item.addEventListener('click', () => selectSavedPaymentMethod(item));
    });
}

function selectSavedAddress(item) {
    // Remove selection from other addresses
    item.closest('.saved-addresses-list')
        .querySelectorAll('.saved-item')
        .forEach(i => i.classList.remove('selected'));
    
    // Select this address
    item.classList.add('selected');
    
    // You can add logic here to populate the address form with the selected address
}

function selectSavedPaymentMethod(item) {
    // Remove selection from other payment methods
    item.closest('.saved-payment-methods-list')
        .querySelectorAll('.saved-item')
        .forEach(i => i.classList.remove('selected'));
    
    // Select this payment method
    item.classList.add('selected');
    
    // You can add logic here to handle the selected payment method
}