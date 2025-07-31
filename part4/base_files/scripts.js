// Configuration for API
const API_BASE_URL = 'http://localhost:5000/api/v1';
// Sample Data containing place details and if API is not available
const places = {
    1: {
        title: "Beautiful Beach House",
        price: "$150 per night",
        icon: "🏖️",
        host: "Sarah Johnson",
        guests: "6 guests",
        bedrooms: "3 bedrooms",
        bathrooms: "2 bathrooms",
        description: "Escape to this stunning beachfront house with panoramic ocean views. This spacious 3-bedroom, 2-bathroom home features modern amenities, a fully equipped kitchen, and direct beach access. Perfect for families or groups looking for a peaceful retreat by the sea. Wake up to the sound of waves and enjoy your morning coffee on the private deck overlooking the endless horizon.",
        amenities: ["🌊 Beach Access", "🍳 Full Kitchen", "📶 Free WiFi", "🅿️ Free Parking", "🏊‍♂️ Pool", "🔥 Fireplace", "📺 Smart TV", "🧺 Washer & Dryer"]
    },
    2: {
        title: "Cozy Mountain Cabin",
        price: "$100 per night",
        icon: "🏔️",
        host: "John Mountain",
        guests: "4 guests",
        bedrooms: "2 bedrooms",
        bathrooms: "1 bathroom",
        description: "A rustic mountain cabin surrounded by pine trees and hiking trails. Features a cozy fireplace, fully equipped kitchen, and stunning mountain views. Perfect for outdoor enthusiasts and those seeking a peaceful mountain retreat away from the city noise.",
        amenities: ["🔥 Fireplace", "🥾 Hiking Trails", "📶 Free WiFi", "🅿️ Free Parking", "🌲 Forest View", "🍳 Full Kitchen", "🛏️ Cozy Beds", "☕ Coffee Maker"]
    },
    3: {
        title: "Modern City Apartment",
        price: "$200 per night",
        icon: "🏙️",
        host: "Alex Urban",
        guests: "4 guests",
        bedrooms: "2 bedrooms",
        bathrooms: "2 bathrooms",
        description: "Stylish downtown apartment in the heart of the city. Walking distance to restaurants, shops, and attractions. Features modern amenities, high-speed internet, and city skyline views. Perfect for business travelers and urban explorers.",
        amenities: ["🏢 City View", "🚇 Metro Access", "📶 High-Speed WiFi", "🎯 Central Location", "🍽️ Restaurants Nearby", "🛍️ Shopping", "💼 Business Center", "🚗 Uber/Taxi Access"]
    },
}    
    const reviews = {
    1: [
        {
            user: "Michael Chen",
            rating: 5,
            comment: "Amazing location right on the beach! The house was spotless and had everything we needed for our family vacation. The kids loved having direct beach access, and the adults enjoyed the peaceful atmosphere. Sarah was a wonderful host who responded quickly to all our questions. Highly recommend!",
            date: "January 15, 2025"
        },
        {
            user: "Emma Rodriguez",
            rating: 5,
            comment: "Perfect getaway spot! The house is beautifully decorated and very comfortable. The kitchen was well-equipped for cooking meals, and the deck was our favorite spot for morning coffee and evening sunsets. Will definitely be back!",
            date: "January 10, 2025"
        },
        {
            user: "David Thompson",
            rating: 4,
            comment: "Great place for a weekend retreat. The location is unbeatable and the house has all the amenities you need. Only minor issue was the WiFi was a bit slow, but that actually helped us disconnect and enjoy our time together. Overall, excellent experience.",
            date: "January 5, 2025"
        }
    ],
    2: [
        {
            user: "Lisa Park",
            rating: 5,
            comment: "Perfect mountain retreat! The cabin was cozy and had everything we needed. The fireplace was amazing for the cold nights, and the hiking trails right outside were fantastic. John was very helpful with local recommendations.",
            date: "January 12, 2025"
        },
        {
            user: "Mike Wilson",
            rating: 4,
            comment: "Great cabin for a mountain getaway. Loved the rustic feel and the views were spectacular. The kitchen was well-equipped and the beds were comfortable. Would definitely come back!",
            date: "January 8, 2025"
        }
    ],
    3: [
        {
            user: "Sarah Kim",
            rating: 4,
            comment: "Excellent location in the city center. The apartment was modern and clean with great amenities. Easy access to restaurants and attractions. Perfect for our business trip. Alex was very responsive to our needs.",
            date: "January 18, 2025"
        },
        {
            user: "Tom Garcia",
            rating: 5,
            comment: "Loved staying here! The city views were incredible and the location couldn't be better. Walking distance to everything we wanted to see. The apartment was stylish and comfortable. Highly recommend for city visits!",
            date: "January 14, 2025"
        }
    ]
};
// Function to obtain a cookies by his name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}
// Authentication Management
class AuthManager {
    static isLoggedIn() {
        const tokenFromCookie = getCookie('token');
        if (tokenFromCookie) {
            return true;
        }
        return localStorage.getItem('isLoggedIn') === 'true';
    }

    static getAuthToken() {
        // Get token from cookie if available
        return getCookie('token');
        }

    static login(email, password) {
        // Simple validation (in real app, this would be server-side)
        if (email && password) {
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('userEmail', email);
            //Simulate token JWT of cookie
            document.cookie = `token=jwt_your_token_value_${Date.now()}'; path=/; max-age=86400`;
            this.updateAuthState();
            return true;
        }
        return false;
    }

    static logout() {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('userEmail');
        // Remove token from cookie
        document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT;';
        this.updateAuthState();
        window.location.href = 'index.html';
    }

    static updateAuthState() {
        if (this.isLoggedIn()) {
            document.body.classList.add('authenticated');
        } else {
            document.body.classList.remove('authenticated');
        }
    }

    static getUserEmail() {
        return localStorage.getItem('userEmail') || '';
    }

    static getUserName() {
        const email = this.getUserEmail();
        return email ? email.split('@')[0] : 'Guest';
    }
}

// Place Management with integration of API
class PlaceManager {
    static async fetchPlaceFromAPI(placeId) {  
        try {
            const headers = {
                'Content-Type': 'application/json',
            };
            
            // Add the token authorization if is available
            const authToken = AuthManager.getAuthToken();
            if (authTokentoken) {
                headers['Authorization'] = `Bearer ${authToken}`;
            }

            const response = await fetch(`https://api.example.com/places/${placeId}`, {
                method: 'GET',
                headers,
            });

            if (!response.ok) {
                throw new Error('Error HTTP/ ${response.status}');
            }

            const placeData = await response.json();
            return placeData;
        } catch (error) {
            console.error('Error fetching place from API:', error);
            return this.getPlace(placeId);
        }
    }

    static getPlace(Id) {
        return places[Id] || null;
    }

    static getAllPlaces() {
        return places;
    }

    static loadPlacesGrid(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '';
        
        Object.entries(places).forEach(([id, place]) => {
            const card = document.createElement('div');
            card.className = 'place-card';
            card.innerHTML = `
                <div class="place-image">${place.icon}</div>
                <div class="place-info">
                    <h3>${place.title}</h3>
                    <div class="place-price">${place.price}</div>
                    <a href="place.html?id=${id}" class="details-button">View Details</a>
                </div>
            `;
            container.appendChild(card);
        });
    }

    static loadPlaceDetails(placeId, containerId) {
        const place = this.getPlace(placeId);
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '';

        Object.entries(places).forEach(([id, place]) => {
            const card = document.createElement('div');
            card.className = 'place-card';
            card.innerHTML = `
                <div class="place-image">${place.icon}</div>
                <div class="place-info">
                    <h3>${place.title}</h3>
                    <div class="place-price">${place.price}</div>
                    <a href="place.html?id=${id}" class="details-button">View Details</a>
                </div>
            `;
            container.appendChild(card);
        });
    }

    // Fonction modifiée pour charger les détails du lieu avec API
    static async loadPlaceDetailsFromAPI(placeId, containerId) {
        const container = document.getElementById(containerId);
        
        if (!container) {
            console.error(`Container avec l'ID '${containerId}' non trouvé`);
            return;
        }

        // Afficher un loader pendant le chargement
        container.innerHTML = `
            <div class="loading-message">
                <h2>Chargement des détails du lieu...</h2>
            </div>
        `;

        try {
            // Récupérer les détails depuis l'API
            const place = await this.fetchPlaceFromAPI(placeId);
            
            if (!place) {
                throw new Error('Lieu non trouvé');
            }

            // Populer les détails du lieu
            this.populatePlaceDetails(place, container);

        } catch (error) {
            console.error('Erreur lors du chargement des détails:', error);
            container.innerHTML = `
                <div class="error-message">
                    <h2>Erreur</h2>
                    <p>Impossible de charger les détails du lieu. Veuillez réessayer plus tard.</p>
                </div>
            `;
        }
    }

    // Fonction pour populer les détails du lieu dans le conteneur
    static populatePlaceDetails(place, container) {
        container.innerHTML = `
            <div class="place-header">
                <div>
                    <h1 class="place-title">${place.title || place.name}</h1>
                    <div class="place-price">${place.price ? place.price : (place.price_per_night ? `$${place.price_per_night} per night` : 'Prix non disponible')}</div>
                </div>
            </div>

            <div class="place-image">${place.icon || '🏠'}</div>

            <div class="place-info">
                <div class="place-description">
                    <h3>About this place</h3>
                    <p>${place.description || 'Aucune description disponible'}</p>
                </div>

                <div class="place-meta">
                    <h3>Property Details</h3>
                    <div class="meta-item">
                        <span>Host:</span>
                        <span>${place.host || place.host_name || 'Non spécifié'}</span>
                    </div>
                    <div class="meta-item">
                        <span>Guests:</span>
                        <span>${place.guests || place.max_guests || 'Non spécifié'}</span>
                    </div>
                    <div class="meta-item">
                        <span>Bedrooms:</span>
                        <span>${place.bedrooms || place.number_of_rooms || 'Non spécifié'}</span>
                    </div>
                    <div class="meta-item">
                        <span>Bathrooms:</span>
                        <span>${place.bathrooms || place.number_of_bathrooms || 'Non spécifié'}</span>
                    </div>
                    <div class="meta-item">
                        <span>Check-in:</span>
                        <span>3:00 PM</span>
                    </div>
                    <div class="meta-item">
                        <span>Check-out:</span>
                        <span>11:00 AM</span>
                    </div>
                </div>
            </div>

            <div class="amenities-section">
                <h3>Amenities</h3>
                ${this.createAmenitiesHTML(place.amenities)}
            </div>
        `;
    }

    // Fonction pour créer l'HTML des équipements
    static createAmenitiesHTML(amenities) {
        if (!amenities || amenities.length === 0) {
            return '<p>Aucun équipement spécifié</p>';
        }

        const amenitiesList = amenities.map(amenity => `<li>${amenity}</li>`).join('');
        return `<ul class="amenities-list">${amenitiesList}</ul>`;
    }

    // Fonction de compatibilité pour les anciennes pages
    static loadPlaceDetails(placeId, containerId) {
        const place = this.getPlace(placeId);
        const container = document.getElementById(containerId);
        
        if (!place || !container) return;

        this.populatePlaceDetails(place, container);
    }
}
// Review Management
class ReviewManager {
    // Fonction pour récupérer les avis depuis l'API
    static async fetchReviewsFromAPI(placeId) {
        try {
            const headers = {
                'Content-Type': 'application/json'
            };

            const authToken = AuthManager.getAuthToken();
            if (authToken) {
                headers['Authorization'] = `Bearer ${authToken}`;
            }

            const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
                method: 'GET',
                headers: headers
            });

            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }

            const reviewsData = await response.json();
            return reviewsData;
        } catch (error) {
            console.error('Erreur lors de la récupération des avis depuis l\'API:', error);
            // Fallback vers les données locales
            return this.getReviews(placeId);
        }
    }

    // Fonction pour soumettre un avis via l'API
    static async submitReviewToAPI(placeId, rating, comment) {
        try {
            const authToken = AuthManager.getAuthToken();
            if (!authToken) {
                throw new Error('Authentification requise pour ajouter un avis');
            }

            const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify({
                    rating: parseInt(rating),
                    comment: comment
                })
            });

            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Erreur lors de la soumission de l\'avis:', error);
            throw error;
        }
    }

    static getReviews(placeId) {
        return reviews[placeId] || [];
    }

    static addReview(placeId, rating, comment) {
        if (!reviews[placeId]) {
            reviews[placeId] = [];
        }

        const newReview = {
            user: AuthManager.getUserName(),
            rating: parseInt(rating),
            comment: comment,
            date: new Date().toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            })
        };

        reviews[placeId].unshift(newReview);
        return newReview;
    }

    // Fonction modifiée pour charger les avis avec API
    static async loadReviewsFromAPI(placeId, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        try {
            const placeReviews = await this.fetchReviewsFromAPI(placeId);
            this.renderReviews(placeReviews, container);
        } catch (error) {
            console.error('Erreur lors du chargement des avis:', error);
            // Fallback vers les données locales
            const placeReviews = this.getReviews(placeId);
            this.renderReviews(placeReviews, container);
        }
    }

    // Fonction pour afficher les avis
    static renderReviews(placeReviews, container) {
        if (placeReviews.length === 0) {
            container.innerHTML = '<p>No reviews yet. Be the first to review this place!</p>';
            return;
        }

        container.innerHTML = placeReviews.map(review => `
            <div class="review-card">
                <div class="review-header">
                    <div class="review-user">${review.user || review.user_name}</div>
                    <div class="review-rating">${'⭐'.repeat(review.rating)}</div>
                </div>
                <div class="review-comment">${review.comment}</div>
                <div class="review-date">${review.date || new Date(review.created_at).toLocaleDateString()}</div>
            </div>
        `).join('');
    }

    static loadReviews(placeId, containerId) {
        const placeReviews = this.getReviews(placeId);
        const container = document.getElementById(containerId);
        
        if (!container) return;

        this.renderReviews(placeReviews, container);
    }
}

// Utility Functions
class Utils {
    static getUrlParameter(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    static showMessage(elementId, message, type = 'success', duration = 3000) {
        const element = document.getElementById(elementId);
        if (!element) return;

        element.textContent = message;
        element.className = `message ${type}`;
        element.style.display = 'block';

        setTimeout(() => {
            element.style.display = 'none';
        }, duration);
    }

    static hideMessage(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'none';
        }
    }

    static populatePlaceSelect(selectId) {
        const select = document.getElementById(selectId);
        if (!select) return;

        select.innerHTML = '<option value="">Choose a place</option>';
        
        Object.entries(places).forEach(([id, place]) => {
            const option = document.createElement('option');
            option.value = id;
            option.textContent = `${place.icon} ${place.title}`;
            select.appendChild(option);
        });
    }
}

// Form Handlers
class FormHandlers {
    static handleLogin(formId) {
        const form = document.getElementById(formId);
        if (!form) return;

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (AuthManager.login(email, password)) {
                Utils.showMessage('loginSuccess', 'Login successful! Redirecting...', 'success');
                Utils.hideMessage('loginError');
                
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 2000);
            } else {
                Utils.showMessage('loginError', 'Invalid email or password. Please try again.', 'error');
                Utils.hideMessage('loginSuccess');
            }
        });
    }

    // Fonction modifiée pour gérer l'ajout d'avis avec API
    static handleAddReview(formId, placeId = null) {
        const form = document.getElementById(formId);
        if (!form) return;

        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!AuthManager.isLoggedIn()) {
                alert('Please login to add a review.');
                return;
            }

            const selectedPlaceId = placeId || document.getElementById('reviewPlace')?.value;
            const ratingField = formId.includes('inline') ? 'inlineRating' : 'reviewRating';
            const commentField = formId.includes('inline') ? 'inlineComment' : 'reviewComment';
            const rating = document.getElementById(ratingField).value;
            const comment = document.getElementById(commentField).value;
            
            if (!selectedPlaceId || !rating || !comment) {
                alert('Please fill in all fields.');
                return;
            }

            try {
                // Essayer de soumettre via l'API d'abord
                await ReviewManager.submitReviewToAPI(selectedPlaceId, rating, comment);
                
                // Si succès, afficher le message et recharger les avis
                if (formId.includes('inline')) {
                    alert('Review added successfully!');
                    // Recharger les avis depuis l'API
                    await ReviewManager.loadReviewsFromAPI(selectedPlaceId, 'reviewsContainer');
                    // Masquer le formulaire
                    const inlineForm = document.getElementById('addReviewInline');
                    if (inlineForm) inlineForm.style.display = 'none';
                } else {
                    Utils.showMessage('reviewSuccess', 'Review added successfully!', 'success');
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 2000);
                }
                
                // Réinitialiser le formulaire
                form.reset();
                
            } catch (error) {
                console.error('Erreur API, fallback vers les données locales:', error);
                
                // Fallback vers l'ancienne méthode
                ReviewManager.addReview(selectedPlaceId, rating, comment);
                
                if (formId.includes('inline')) {
                    alert('Review added successfully!');
                    ReviewManager.loadReviews(selectedPlaceId, 'reviewsContainer');
                    const inlineForm = document.getElementById('addReviewInline');
                    if (inlineForm) inlineForm.style.display = 'none';
                } else {
                    Utils.showMessage('reviewSuccess', 'Review added successfully!', 'success');
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 2000);
                }
                
                form.reset();
            }
        });
    }

    static handleLogout() {
        const logoutBtns = document.querySelectorAll('.logout-button');
        logoutBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                AuthManager.logout();
            });
        });
    }
}

// Page-specific initialization functions
const PageInit = {
    // Initialize Index Page
    index: function() {
        AuthManager.updateAuthState();
        PlaceManager.loadPlacesGrid('placesGrid');
        FormHandlers.handleLogout();
    },

    // Initialize Login Page
    login: function() {
        AuthManager.updateAuthState();
        
        // Redirect if already logged in
        if (AuthManager.isLoggedIn()) {
            window.location.href = 'index.html';
            return;
        }
        
        FormHandlers.handleLogin('loginForm');
    },

    // Initialize Place Details Page (MODIFIÉ POUR LA TÂCHE 3)
    place: function() {
        AuthManager.updateAuthState();
        FormHandlers.handleLogout();
        
        const placeId = Utils.getUrlParameter('id') || '1';
        
        // Charger les détails du lieu depuis l'API
        PlaceManager.loadPlaceDetailsFromAPI(placeId, 'placeDetailsContent');
        
        // Charger les avis depuis l'API
        ReviewManager.loadReviewsFromAPI(placeId, 'reviewsContainer');
        
        // Gérer le formulaire d'avis inline
        FormHandlers.handleAddReview('inlineReviewForm', placeId);
        
        // Gérer le bouton "Add Review"
        const addReviewBtn = document.querySelector('.add-review-btn');
        if (addReviewBtn) {
            addReviewBtn.addEventListener('click', function(e) {
                e.preventDefault();
                if (!AuthManager.isLoggedIn()) {
                    alert('Please login to add a review.');
                    window.location.href = 'login.html';
                    return;
                }
                const inlineForm = document.getElementById('addReviewInline');
                if (inlineForm) {
                    inlineForm.style.display = inlineForm.style.display === 'none' ? 'block' : 'none';
                }
            });
        }
    },

    // Initialize Add Review Page
    addReview: function() {
        AuthManager.updateAuthState();
        FormHandlers.handleLogout();
        
        // Check authentication
        if (!AuthManager.isLoggedIn()) {
            document.getElementById('authRequired').style.display = 'block';
            document.getElementById('reviewContent').style.display = 'none';
            return;
        }
        
        // Populate place selection
        Utils.populatePlaceSelect('reviewPlace');
        
        // Handle review form
        FormHandlers.handleAddReview('addReviewForm');
    }
};

// Navigation Helper
class Navigation {
    static setActiveNavLink() {
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        const navLinks = document.querySelectorAll('.nav-links a');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPage) {
                link.classList.add('active');
            }
        });
    }
}

// Global initialization when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Set active navigation link
    Navigation.setActiveNavLink();
    
    // Get current page name
    const currentPage = window.location.pathname.split('/').pop().replace('.html', '') || 'index';
    
    // Initialize based on current page
    if (PageInit[currentPage]) {
        PageInit[currentPage]();
    }
    
    // Add hover effects to place cards
    document.querySelectorAll('.place-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-5px)';
        });
    });
});

// Global functions (for onclick handlers in HTML)
window.logout = function() {
    AuthManager.logout();
};

window.showSignupMessage = function() {
    alert('Sign up functionality would redirect to a registration page.');
};

window.showForgotPassword = function() {
    alert('Password reset functionality would send a reset email.');
};

// Export for use in other scripts if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AuthManager,
        PlaceManager,
        ReviewManager,
        Utils,
        FormHandlers,
        PageInit
    };
}