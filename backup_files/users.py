from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade
from app.utils.decorators import admin_required

# Namespace for user operations
api = Namespace('users', description='Users related operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

facade = HBnBFacade()

@api.route('/')
class UserList(Resource):
    @admin_required
    def get(self):
        """The list of all users (only admin)"""
        try:
            users = facade.get_all_users()
            return [user.to_dict() for user in users], 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @api.expect(user_model)
    def post(self):
        """Creates a new user"""
        try:
            data = request.get_json()
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/<user_id>')
class UserDetail(Resource):
    @jwt_required()
    def get(self, user_id):
        """Retrieves a specific user"""
        try:
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Only the user himself or an admin can see the details
            if current_user_id != user_id and not is_admin:
                return {'error': 'Access denied'}, 403
            
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            
            return user.to_dict(), 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    def put(self, user_id):
        """Updates a user"""
        try:
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Only the user himself or admin can modify a user
            if current_user_id != user_id and not is_admin:
                return {'error': 'Access denied'}, 403
            
            data = request.get_json()
            user = facade.update_user(user_id, data)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            return user.to_dict(), 200
            
        except Exception as e:
            return {'error': str(e)}, 500