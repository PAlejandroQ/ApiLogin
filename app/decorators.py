import jwt
from flask import request, jsonify
from functools import wraps
from app.models import User

SECRET_KEY = 'your_secret_key'

def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            return jsonify({'message': 'Token missing'}), 401

        try:
            payload = jwt.decode(token.split()[1], SECRET_KEY, algorithms=['HS256'])
            request.user = User.query.get(payload['id'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return func(*args, **kwargs)
    return wrapper

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = getattr(request, 'user', None)
            if not user or user.role != required_role:
                return jsonify({'message': 'Access denied'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
