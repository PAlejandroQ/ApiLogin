import requests

BASE_URL = 'http://127.0.0.1:5000/auth'

def register_user(username, password, role='user'):
    response = requests.post(f'{BASE_URL}/register', json={
        'username': username,
        'password': password,
        'role': role
    })
    print(response.json())

def login_user(username, password):
    response = requests.post(f'{BASE_URL}/login', json={
        'username': username,
        'password': password
    })
    return response.json()

def access_protected_endpoint(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/protected', headers=headers)
    print(response.json())

# Ejemplo de uso
#register_user('admin', 'admin123', 'admin')
tokens = login_user('admin', 'admin123')
access_protected_endpoint(tokens['access_token'])