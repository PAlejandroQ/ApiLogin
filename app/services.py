import jwt
import datetime
from .models import User
from . import db

SECRET_KEY = 'your_secret_key'

def register_user(data):
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    if not username or not password:
        return {'message': 'Invalid data', 'status': 400}

    if User.query.filter_by(username=username).first():
        return {'message': 'User already exists', 'status': 400}

    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return {'message': 'User registered successfully', 'status': 201}

def login_user(data):
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {'message': 'Invalid username or password', 'status': 401}

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    return {'access_token': access_token, 'refresh_token': refresh_token, 'status': 200}

def generate_access_token(user):
    payload = {
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def generate_refresh_token(user):
    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def refresh_access_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])
        user = User.query.get(payload['id'])
        if not user:
            return {'message': 'Invalid refresh token', 'status': 401}
        access_token = generate_access_token(user)
        return {'access_token': access_token, 'status': 200}
    except jwt.ExpiredSignatureError:
        return {'message': 'Refresh token expired', 'status': 401}
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token', 'status': 401}
