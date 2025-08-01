from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

# Namespace for protected operations
api = Namespace('protected', description='Protected operations')

facade = HBnBFacade()

@api.route('/admin-only')
class AdminOnly(Resource):
    @jwt_required()
    def get(self):
        """Admin only endpoint"""
        try:
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            if not is_admin:
                return {'error': 'Admin access required'}, 403
            
            return {
                'message': 'Admin access granted',
                'user_id': current_user_id
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/user-info')
class UserInfo(Resource):
    @jwt_required()
    def get(self):
        """Get current user info"""
        try:
            current_user_id = get_jwt_identity()
            user = facade.get_user(current_user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            return {
                'user': user.to_dict()
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/test')
class TestProtected(Resource):
    @jwt_required()
    def get(self):
        """Test protected endpoint"""
        try:
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            
            return {
                'message': 'Protected route accessed successfully',
                'user_id': current_user_id,
                'claims': claims
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500