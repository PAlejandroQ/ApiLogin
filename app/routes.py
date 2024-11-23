from flask import Blueprint, request, jsonify
from .services import (
    register_user,
    login_user,
    generate_access_token,
    refresh_access_token,
)
from .decorators import jwt_required, role_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    response = register_user(data)
    return jsonify(response), response.get('status', 400)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    response = login_user(data)
    return jsonify(response), response.get('status', 400)

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    response = refresh_access_token(refresh_token)
    return jsonify(response), response.get('status', 400)

@auth_bp.route('/protected', methods=['GET'])
@jwt_required
@role_required('admin')
def protected():
    return jsonify({'message': 'Access granted to admin'}), 200

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
