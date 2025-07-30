from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade
from app.utils.decorators import admin_required

# Principal for the reviews namespace
api = Namespace('reviews', description='Review operations')

# Principal for the places reviews namespace
places_reviews_ns = Namespace('places_reviews', description='Place reviews operations')

# Model for review data
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

facade = HBnBFacade()

# routes for the main reviews namespace
@api.route('/')
class ReviewList(Resource):
    @admin_required
    def get(self):
        """Get all reviews (admin only)"""
        try:
            reviews = facade.get_all_reviews()
            return [review.to_dict() for review in reviews], 200
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/<review_id>')
class ReviewDetail(Resource):
    @jwt_required()
    def get(self, review_id):
        """Get a specific review"""
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            return review.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        try:
            current_user_id = get_jwt_identity()
            review = facade.get_review(review_id)
            
            if not review:
                return {'error': 'Review not found'}, 404
            
            # Only the review author can update it
            if review.user_id != current_user_id:
                return {'error': 'Access denied'}, 403
            
            data = request.get_json()
            updated_review = facade.update_review(review_id, data)
            return updated_review.to_dict(), 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        try:
            current_user_id = get_jwt_identity()
            review = facade.get_review(review_id)
            
            if not review:
                return {'error': 'Review not found'}, 404
            
            # Only the review author can delete it
            if review.user_id != current_user_id:
                return {'error': 'Access denied'}, 403
            
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

# Routes pour le namespace 'places_reviews'
@places_reviews_ns.route('/')
class PlaceReviewsList(Resource):
    @places_reviews_ns.expect(review_model)
    @jwt_required()
    def post(self):
        """Create a new review for a place"""
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            data['user_id'] = current_user_id
            
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500