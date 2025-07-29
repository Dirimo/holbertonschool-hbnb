// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get form data
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            
            // Basic validation
            if (!email || !password) {
                displayError('Please enter both email and password.');
                return;
            }
            
            // Show loading state
            setLoadingState(true);
            
            try {
                await loginUser(email, password);
            } catch (error) {
                console.error('Login error:', error);
                displayError('An unexpected error occurred. Please try again.');
            } finally {
                setLoadingState(false);
            }
        });
    }
});

/**
 * Sends login request to the API
 * @param {string} email - User's email
 * @param {string} password - User's password
 */
async function loginUser(email, password) {
    try {
        const response = await fetch('https://your-api-url/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // Store JWT token in cookie
            storeTokenInCookie(data.access_token);
            
            // Clear any existing error messages
            clearError();
            
            // Redirect to main page
            window.location.href = 'index.html';
            
        } else {
            // Handle different error status codes
            let errorMessage = 'Login failed. Please try again.';
            
            if (response.status === 401) {
                errorMessage = 'Invalid email or password.';
            } else if (response.status === 429) {
                errorMessage = 'Too many login attempts. Please try again later.';
            } else if (response.status >= 500) {
                errorMessage = 'Server error. Please try again later.';
            }
            
            // Try to get more specific error from response
            try {
                const errorData = await response.json();
                if (errorData.message) {
                    errorMessage = errorData.message;
                }
            } catch (parseError) {
                // Use default error message if JSON parsing fails
            }
            
            displayError(errorMessage);
        }
        
    } catch (error) {
        // Network or other fetch errors
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            displayError('Network error. Please check your connection and try again.');
        } else {
            displayError('An unexpected error occurred. Please try again.');
        }
        throw error; // Re-throw to be caught by the calling function
    }
}

/**
 * Stores JWT token in a secure cookie
 * @param {string} token - JWT token to store
 */
function storeTokenInCookie(token) {
    // Set cookie with security options
    const cookieOptions = [
        `token=${token}`,
        'path=/',
        'SameSite=Strict'
        // Add 'Secure' flag if using HTTPS
        // 'Secure'
    ];
    
    // Optional: Set expiration (example: 7 days)
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + 7);
    cookieOptions.push(`expires=${expirationDate.toUTCString()}`);
    
    document.cookie = cookieOptions.join('; ');
}

/**
 * Displays error message to the user
 * @param {string} message - Error message to display
 */
function displayError(message) {
    // Remove any existing error messages
    clearError();
    
    // Create error element
    const errorDiv = document.createElement('div');
    errorDiv.id = 'login-error';
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        color: #dc3545;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
        font-size: 14px;
    `;
    
    // Insert error message at the top of the form
    const loginForm = document.getElementById('login-form');
    loginForm.insertBefore(errorDiv, loginForm.firstChild);
    
    // Auto-remove error after 5 seconds
    setTimeout(clearError, 5000);
}

/**
 * Clears any existing error messages
 */
function clearError() {
    const existingError = document.getElementById('login-error');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Sets loading state for the form
 * @param {boolean} isLoading - Whether the form is in loading state
 */
function setLoadingState(isLoading) {
    const submitButton = document.querySelector('#login-form button[type="submit"]');
    const formInputs = document.querySelectorAll('#login-form input');
    
    if (submitButton) {
        if (isLoading) {
            submitButton.disabled = true;
            submitButton.textContent = 'Logging in...';
        } else {
            submitButton.disabled = false;
            submitButton.textContent = 'Login';
        }
    }
    
    // Disable/enable form inputs
    formInputs.forEach(input => {
        input.disabled = isLoading;
    });
}

/**
 * Utility function to get token from cookie (for other parts of your app)
 * @returns {string|null} JWT token or null if not found
 */
function getTokenFromCookie() {
    const name = 'token=';
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');
    
    for (let cookie of cookieArray) {
        cookie = cookie.trim();
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length);
        }
    }
    return null;
}

/**
 * Utility function to remove token cookie (for logout functionality)
 */
function removeTokenCookie() {
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT; SameSite=Strict';
}