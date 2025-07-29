document.addEventListener('DOMContentLoaded', () => {
    // Check if on login page and setup the login form submission handler
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            errorMessage.textContent = ''; // Clear any previous error messages

            const email = loginForm.email.value;
            const password = loginForm.password.value;
            
            try {
                const response = await loginUser(ip, email, password);
                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/; SameSite=Strict`; // Store token

                    // Redirect to the index page after login
                    window.location.href = 'index.html'; 
                } else {
                    errorMessage.textContent = 'Login failed: ' + response.statusText;
                }
            } catch (error) {
                errorMessage.textContent = 'An error occurred: ' + error.message;
            }
        });
    }

    if (logoutLink) {
        logoutLink.addEventListener('click', (event) => {
            event.preventDefault();
            logout();
        });
    }

    // Check authentication and setup page based on the presence of specific elements
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthentication();
        setupCountryFilter();
    }
});

const ip = '127.0.0.1:5000';

async function loginUser(ip, email, password) {
    const url_login = 'http://'.concat(ip, '/login');
    
    try {
        const response = await fetch(url_login, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        return response;
    } catch (error) {
        console.error('Error during login:', error);
        return { ok: false, statusText: 'Network error' };
    }
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (loginLink && logoutLink) {
        if (token) {
            loginLink.style.display = 'none'; // Hide the login link if token is present
            logoutLink.style.display = 'block'; // Show the logout link if token is present
        } else {
            loginLink.style.display = 'block'; // Show the login link if no token
            logoutLink.style.display = 'none'; // Hide the logout link if no token
        }
    }

    // Fetch places only if 'places-list' is present
    const placesList = document.getElementById('places-list');
    if (placesList) {
        fetchPlaces(ip, token);
    }
}

function getCookie(name) {
    const cookieArr = document.cookie.split(';');
    for (let i = 0; i < cookieArr.length; i++) {
        const cookiePair = cookieArr[i].split('=');
        if (name === cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}

function logout() {
    // Remove the token from cookies
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'; 

    // Redirect to the login page or home page
    window.location.href = 'index.html'; 

    // Update UI
    checkAuthentication();
}

const fetchPlaces = async (ip, token) => {
    try {
        const url_places = 'http://'.concat(ip, '/places');
        
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        const response = await fetch(url_places, { headers });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
            populateCountryFilter(places); // Populate country filter options
        } else {
            console.error('Failed to fetch places');
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

const displayPlaces = (places) => {
    const placesList = document.getElementById('places-list');
    if (placesList) {
        placesList.innerHTML = '';

        places.forEach(place => {
            const placeElement = document.createElement('div');
            placeElement.className = 'place-item';
            placeElement.innerHTML = `
                <h3>${place.description}</h3>
                <p>Price per night: $${place.price_per_night}</p>
                <p><strong>Location:</strong> ${place.city_name}, ${place.country_name}</p>
            `;

            // Create the details button
            const detailsButton = document.createElement('button');
            detailsButton.className = 'details-button';
            detailsButton.textContent = 'View Details';
            detailsButton.addEventListener('click', () => {
                console.log(`Clicked on details for ${place.name}`);
            });

            placeElement.appendChild(detailsButton);
            placesList.appendChild(placeElement);
        });
    }
};

const populateCountryFilter = (places) => {
    const countryFilter = document.getElementById('country-filter');
    if (countryFilter) {
        const countries = new Set();

        places.forEach(place => {
            const country = place.country_name;
            countries.add(country);
        });

        countryFilter.innerHTML = '<option value="">All</option>';
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            countryFilter.appendChild(option);
        });
    }
};

const setupCountryFilter = () => {
    const countryFilter = document.getElementById('country-filter');
    if (countryFilter) {
        countryFilter.addEventListener('change', (event) => {
            filterPlacesByCountry(event.target.value);
        });
    }
};

const filterPlacesByCountry = (country) => {
    const placesList = document.getElementById('places-list');
    if (placesList) {
        const places = Array.from(placesList.children);

        places.forEach(place => {
            const location = place.querySelector('p:nth-of-type(2)').innerText;
            if (country === '' || location.includes(country)) {
                place.style.display = 'inline-block';
            } else {
                place.style.display = 'none';
            }
        });
    }
};