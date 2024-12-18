from flask import Blueprint, request, jsonify
from .services import (
    register_user,
    login_user,
    generate_access_token,
    refresh_access_token,
    update_user_role,
)
from .decorators import jwt_required, role_required, audit_log

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@audit_log('REGISTER')
def register():
    data = request.json
    response = register_user(data)
    return jsonify(response), response.get('status', 400)

@auth_bp.route('/login', methods=['POST'])
@audit_log('LOGIN')
def login():
    data = request.json
    response = login_user(data)
    return jsonify(response), response.get('status', 400)

@auth_bp.route('/refresh', methods=['POST'])
@audit_log('REFRESH')
def refresh():
    refresh_token = request.json.get('refresh_token')
    response = refresh_access_token(refresh_token)
    return jsonify(response), response.get('status', 400)

@auth_bp.route('/protected', methods=['GET'])
@jwt_required
@role_required('admin')
#@audit_log('PROTECTED')
def protected():
    return jsonify({'message': 'Access granted to admin'}), 200

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')

@auth_bp.route('/modify-role', methods = ['PUT'])
@jwt_required
@role_required('admin')
@audit_log('MODIFY')
def modify_role():
    data = request.json
    response = update_user_role(data)
    return jsonify(response), response.get('status', 400)