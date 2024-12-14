import random

import pytest
from flask import Flask, jsonify
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()


class TestEndpoints:
    def test_register_success(self, client):
        response = client.post('auth/register', json={
            'username': 'testuser'+str(random.randint(1,100000)),
            'password': 'password123'
        })
        assert response.status_code == 201
        assert response.json.get('message') == 'User registered successfully'

    def test_register_failure_incomplete_data(self, client):
        response = client.post('auth/register', json={
            'username': 'testuser'
        })
        assert response.status_code == 400
        assert response.json.get('message') == 'Invalid data'

    def test_register_failure_user_exists(self, client):
        client.post('auth/register', json={
            'username': 'testuser',
            'password': 'password123'
        })
        response = client.post('auth/register', json={
            'username': 'testuser',
            'password': 'anotherpassword'
        })
        assert response.status_code == 400
        assert response.json.get('message') == 'User already exists'

    def test_login_success(self, client):
        client.post('auth/register', json={
            'username': 'testuser',
            'password': 'password123'
        })
        response = client.post('auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        assert response.status_code == 200
        assert 'access_token' in response.json

    def test_login_failure_wrong_credentials(self, client):
        client.post('auth/register', json={
            'username': 'testuser',
            'password': 'password123'
        })
        response = client.post('auth/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        assert response.status_code == 401
        assert response.json.get('message') == 'Invalid username or password'

    def test_login_failure_missing_data(self, client):
        response = client.post('auth/login', json={})
        assert response.status_code == 401
        assert response.json.get('message') == 'Invalid username or password'

    def test_refresh_success(self, client):
        client.post('auth/register', json={
            'username': 'testuser',
            'password': 'password123'
        })
        login_response = client.post('auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        refresh_token = login_response.json.get('refresh_token')
        response = client.post('auth/refresh', json={
            'refresh_token': refresh_token
        })
        assert response.status_code == 200
        assert 'access_token' in response.json

    def test_refresh_failure_invalid_token(self, client):
        response = client.post('auth/refresh', json={
            'refresh_token': 'invalidtoken'
        })
        assert response.status_code == 401
        assert response.json.get('message') == 'Invalid token'

    def test_refresh_failure_missing_token(self, client):
        response = client.post('auth/refresh', json={})
        assert response.status_code == 401
        assert response.json.get('message') == 'Invalid token'

    # def test_protected_success(self, client):
    #     client.post('auth/register', json={
    #         'username': 'admin',
    #         'password': 'password123'
    #     })
    #     login_response = client.post('auth/login', json={
    #         'username': 'admin',
    #         'password': 'password123'
    #     })
    #     token = login_response.json.get('token')
    #     response = client.get('auth/protected', headers={
    #         'Authorization': f'Bearer {token}'
    #     })
    #     assert response.status_code == 200
    #     assert response.json.get('message') == 'Access granted.'

    def test_protected_failure_invalid_token(self, client):
        response = client.get('auth/protected', headers={
            'Authorization': 'Bearer invalidtoken'
        })
        assert response.status_code == 401
        assert response.json.get('message') == 'Invalid token'

    def test_protected_failure_missing_token(self, client):
        response = client.get('auth/protected')
        assert response.status_code == 401
        assert response.json.get('message') == 'Token missing'

    # def test_modify_role_success(self, client):
    #     client.post('auth/register', json={
    #         'username': 'admin',
    #         'password': 'password123'
    #     })
    #     login_response = client.post('auth/login', json={
    #         'username': 'admin',
    #         'password': 'password123'
    #     })
    #     token = login_response.json.get('access_token')
    #     response = client.put('auth/modify-role', json={
    #         'username': 'testuser',
    #         'role': 'moderator'
    #     }, headers={
    #         'Authorization': f'Bearer {token}'
    #     })
    #     assert response.status_code == 200
    #     assert response.json.get('message') == 'Role updated successfully.'

    def test_modify_role_failure_incomplete_data(self, client):
        client.post('auth/register', json={
            'username': 'admin',
            'password': 'password123'
        })
        login_response = client.post('auth/login', json={
            'username': 'admin',
            'password': 'password123'
        })
        token = login_response.json.get('token')
        response = client.put('auth/modify-role', json={
            'username': 'testuser'
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 401
        assert response.json.get('message') == 'Invalid token'

    def test_modify_role_failure_invalid_token(self, client):
        response = client.put('auth/modify-role', json={
            'username': 'testuser',
            'role': 'moderator'
        }, headers={
            'Authorization': 'Bearer invalidtoken'
        })
        assert response.status_code == 401
        assert response.json.get('message') == 'Invalid token'
