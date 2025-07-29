from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


from app.services.repositories.user_repository import UserRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.amenity_repository import AmenityRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # --- User operations ---
    def create_user(self, user_data):
        """Creates a new User instance, hashes password, and adds it to the repository."""
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieves a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieves a user by email using the specific UserRepository method."""
        
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Retrieves all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Updates a user by ID."""
        user = self.user_repo.get(user_id)
        if user:
            self.user_repo.update(user_id, user_data)
            return self.user_repo.get(user_id)
        return None

    def delete_user(self, user_id):
        """Deletes a user by ID."""
        return self.user_repo.delete(user_id)

    # --- Amenity operations (CRUD simple, SANS RELATIONS) ---
    def create_amenity(self, amenity_data):
        """Creates a new Amenity instance and adds it to the repository."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieves all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an amenity by ID."""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            self.amenity_repo.update(amenity_id, amenity_data)
            return self.amenity_repo.get(amenity_id)
        return None

    def delete_amenity(self, amenity_id):
        """Deletes an amenity by ID."""
        return self.amenity_repo.delete(amenity_id)

    # --- Place operations (CRUD simple, SANS RELATIONS) ---
    def create_place(self, place_data):
        """Creates a new Place instance and adds it to the repository."""
        
        place_pure_data = {
            'title': place_data['title'],
            'description': place_data.get('description'),
            'price': place_data['price'],
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude']
        }
        place = Place(**place_pure_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieves a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieves all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Updates a place by ID."""
        place = self.place_repo.get(place_id)
        if place:
        
            self.place_repo.update(place_id, place_data)
            return self.place_repo.get(place_id)
        return None

    def delete_place(self, place_id):
        """Deletes a place by ID."""
        return self.place_repo.delete(place_id)

    # --- Review operations (CRUD simple, SANS RELATIONS) ---
    def create_review(self, review_data):
        """Creates a new Review instance and adds it to the repository."""
        
        review_pure_data = {
            'text': review_data['text'],
            'rating': review_data['rating']
        }
        review = Review(**review_pure_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieves a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieves all reviews."""
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """Updates a review by ID."""
        review = self.review_repo.get(review_id)
        if review:
        
            self.review_repo.update(review_id, review_data)
            return self.review_repo.get(review_id)
        return None

    def delete_review(self, review_id):
        """Deletes a review by ID."""
        return self.review_repo.delete(review_id)
