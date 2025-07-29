from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

def token_required(f):
    """Decorator to verify authentication"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to verify administrator rights"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin access required'}, 403
        return f(*args, **kwargs)
    return decorated_function

def owner_required(f):
    """Decorator to verify user ownership"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        # This function wil be used in specific endpoints
        return f(current_user_id, *args, **kwargs)
    return decorated_function