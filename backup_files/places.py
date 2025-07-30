from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade
from app.utils.decorators import admin_required

# Namespace for the places API
api = Namespace('places', description='Place operations')

# Model for place data
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='Owner ID')
})

facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    def get(self):
        """Get all places"""
        try:
            places = facade.get_all_places()
            return [place.to_dict() for place in places], 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @api.expect(place_model)
    @jwt_required()
    def post(self):
        """Create a new place"""
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            data['owner_id'] = current_user_id
            
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/<place_id>')
class PlaceDetail(Resource):
    def get(self, place_id):
        """Get a specific place"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            return place.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    def put(self, place_id):
        """Update a place"""
        try:
            current_user_id = get_jwt_identity()
            place = facade.get_place(place_id)
            
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Only the owner can update the place
            if place.owner_id != current_user_id:
                return {'error': 'Access denied'}, 403
            
            data = request.get_json()
            updated_place = facade.update_place(place_id, data)
            return updated_place.to_dict(), 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        try:
            current_user_id = get_jwt_identity()
            place = facade.get_place(place_id)
            
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Only the owner can delete the place
            if place.owner_id != current_user_id:
                return {'error': 'Access denied'}, 403
            
            facade.delete_place(place_id)
            return {'message': 'Place deleted successfully'}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500