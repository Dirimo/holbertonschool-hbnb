from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Cannot review your own place or duplicate review')
    @jwt_required()
    def post(self):
        """Register a new review"""
        try:
            #Get the current user from JWT
            current_user_id = get_jwt_identity()

            #set user_id to current user
            review_data = api.payload
            review_data['user_id'] = current_user_id
            #Check if place exists and user is not the owner
            place = facade.get_place(review_data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404
            if place.owner_id == current_user_id:
                return {'error': 'Cannot review your own place'}, 403
            #check for duplicates reviews
            existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
            for existing_review in existing_reviews:
                if existing_review.user_id == current_user_id:
                    return {'error': 'You have already reviewed this place'}, 403
            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized - not the review author')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        # Get current user form JWT
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        #check if current user is the review author
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized - you can only modify your own reviews'}, 403
        try:
            updated_review = facade.update_review(review_id, api.payload)
            return updated_review.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unautorized - not the review author')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized - you can only delete your own reviews'}, 403
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in reviews], 200
