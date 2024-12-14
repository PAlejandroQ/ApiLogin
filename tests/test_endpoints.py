import requests

BASE_URL = 'http://127.0.0.1:5000/auth'

def register_user(username, password, role):
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

def modify_user_role(token, username, new_role):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.put(f'{BASE_URL}/modify-role', json={
        'username': username,
        'role': new_role
    }, headers=headers)
    print(response.json())

# Ejemplo de uso
# Caso 1:
print("\n[TEST CASE 1] Modificar el rol de 'user2' a 'admin'")
register_user('admin', 'admin123', 'admin')
tokens = login_user('admin', 'admin123')
access_token = tokens['access_token']
register_user('user2', 'password123', 'user')
modify_user_role(access_token, 'user1', 'admin')

# Caso 2:
print("\n[TEST CASE 2] Intentar modificar el rol de 'user2' a 'invalid_role'")
modify_user_role(access_token, 'user2', 'invalid_role')

# Caso 3:
print("\n[TEST CASE 3] Intentar modificar el rol de un usuario inexistente 'nonexistent_user'")
modify_user_role(access_token, 'nonexistent_user', 'admin')

# Caso 4:
print("\n[TEST CASE 4] Intentar modificar el rol de 'user2' al rol que ya tiene 'admin'")
modify_user_role(access_token, 'user2', 'admin')

# Caso 5: Intentar modificar sin un token válido
print("\n[TEST CASE 5] Intentar modificar el rol de 'user2' sin un token válido")
modify_user_role(None, 'user2', 'user')