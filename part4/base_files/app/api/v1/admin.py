from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade
from app.utils.decorators import admin_required

admin_ns = Namespace('admin', description='Admin operations')

facade = HBnBFacade()

@admin_ns.route('/users')
class AdminUserList(Resource):
    @admin_required
    def get(self):
        """Lists all users with admin details"""
        try:
            users = facade.get_all_users()
            return [user.to_dict() for user in users], 200
        except Exception as e:
            return {'error': str(e)}, 500

@admin_ns.route('/users/<user_id>')
class AdminUserDetail(Resource):
    @admin_required
    def delete(self, user_id):
        """Deletes a user(Admin only)"""
        try:
            result = facade.delete_user(user_id)
            if result:
                return {'message': 'User deleted successfully'}, 200
            else:
                return {'error': 'User not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500

@admin_ns.route('/places')
class AdminPlaceList(Resource):
    @admin_required
    def get(self):
        """Lists all locations with admin details"""
        try:
            places = facade.get_all_places()
            return [place.to_dict() for place in places], 200
        except Exception as e:
            return {'error': str(e)}, 500

@admin_ns.route('/places/<place_id>')
class AdminPlaceDetail(Resource):
    @admin_required
    def delete(self, place_id):
        """Deletes a location(Admin only)"""
        try:
            result = facade.delete_place(place_id)
            if result:
                return {'message': 'Place deleted successfully'}, 200
            else:
                return {'error': 'Place not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500