from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade
from datetime import timedelta

# Namespace for authentication operations
api = Namespace('auth', description='Authentication operations')

# Model for user login
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

# Modele pour l'enregistrement
register_model = api.model('Register', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

facade = HBnBFacade()

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """User login"""
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return {'error': 'Email and password are required'}, 400
            
            # Vérify user credentials via the facade
            user = facade.authenticate_user(email, password)
            
            if not user:
                return {'error': 'Invalid credentials'}, 401
            
            # Create JWT token for the user
            additional_claims = {
                'is_admin': user.is_admin if hasattr(user, 'is_admin') else False
            }
            
            access_token = create_access_token(
                identity=user.id,
                additional_claims=additional_claims,
                expires_delta=timedelta(hours=1)
            )
            
            return {
                'access_token': access_token,
                'user': user.to_dict()
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        """User registration"""
        try:
            data = request.get_json()
            
            # Create a new user via the facade
            user = facade.create_user(data)
            
            # Create JWT token for the new user
            additional_claims = {
                'is_admin': user.is_admin if hasattr(user, 'is_admin') else False
            }
            
            access_token = create_access_token(
                identity=user.id,
                additional_claims=additional_claims,
                expires_delta=timedelta(hours=1)
            )
            
            return {
                'access_token': access_token,
                'user': user.to_dict()
            }, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/protected')
class Protected(Resource):
    @jwt_required()
    def get(self):
        """Protected route for testing JWT"""
        try:
            current_user_id = get_jwt_identity()
            user = facade.get_user(current_user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            return {
                'message': 'Access granted',
                'user_id': current_user_id,
                'user': user.to_dict()
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500