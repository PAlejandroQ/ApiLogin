import jwt
from flask import request, jsonify
from functools import wraps
from app.models import User
from .audit_logging import  log_event, setup_log
import json

SECRET_KEY = 'your_secret_key'

setup_log()
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

def audit_log(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = request.json.get('username', None)

            retval =  func(*args, **kwargs)
            if retval:
                if retval[1] == 200 or retval[1] == 201:
                    log_event(
                        level="info",
                        message=f"OK - Action: {action}, User: {user}, Endpoint: {request.path}"
                    )
                else:
                    log_event(
                        level="error",
                        message=f"ERROR - Status: {retval[1]}, Action: {action}, User: {user}, Endpoint: {request.path}\n {json.loads(retval[0].get_data().decode('utf-8'))}"
                    )

            return retval
        return wrapper
    return decorator
