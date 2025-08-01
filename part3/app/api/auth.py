from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token,  jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade
from app.models.user import User

auth_ns = Namespace('auth', description='Authentication operations')

# Templates for the documentation
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

token_model = auth_ns.model('Token', {
    'access_token': fields.String(description='JWT access token'),
    'user_id': fields.String(description='User ID')
})

facade = HBnBFacade()

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(token_model)
    def post(self):
        """User authentication"""
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return {'error': 'Email and password are required'}, 400
            
            # Recover user
            user = facade.get_user_by_email(email)
            if not user or not user.check_password(password):
                return {'error': 'Invalid credentials'}, 401
            
            # Generate token
            access_token = user.generate_token()
            
            return {
                'access_token': access_token,
                'user_id': user.id
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

@auth_ns.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """User logout"""
        # Note: With JWT, server-side logout is optional
        # Token expires automatically
        return {'message': 'Successfully logged out'}, 200

@auth_ns.route('/me')
class Me(Resource):
    @jwt_required()
    def get(self):
        """Informations about the user connection"""
        try:
            user_id = get_jwt_identity()
            user = facade.get_user(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            return user.to_dict(), 200
            
        except Exception as e:
            return {'error': str(e)}, 500

