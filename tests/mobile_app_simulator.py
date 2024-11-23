import requests
import time
import threading

BASE_URL = 'http://127.0.0.1:5000/auth'

# Usuario simulado
USERNAME = 'mobile_user'
PASSWORD = 'password123'

# Variables para almacenar tokens
access_token = None
refresh_token = None

def register_user():
    """Registra un usuario en caso de que no exista."""
    response = requests.post(f'{BASE_URL}/register', json={
        'username': USERNAME,
        'password': PASSWORD,
        'role': 'user'
    })
    if response.status_code == 201:
        print("[INFO] Usuario registrado exitosamente.")
    elif response.status_code == 400:
        print("[INFO] Usuario ya existe.")
    else:
        print(f"[ERROR] Error al registrar usuario: {response.json()}")

def login_user():
    """Inicia sesión y obtiene tokens de acceso y refresh."""
    global access_token, refresh_token
    response = requests.post(f'{BASE_URL}/login', json={
        'username': USERNAME,
        'password': PASSWORD
    })
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        print("[INFO] Inicio de sesión exitoso. Tokens obtenidos.")
    else:
        print(f"[ERROR] Error al iniciar sesión: {response.json()}")

def access_protected_endpoint():
    """Simula solicitudes a un endpoint protegido usando el access_token."""
    global access_token
    while True:
        if not access_token:
            print("[WARN] No hay access_token disponible. Esperando renovación...")
            time.sleep(10)
            continue

        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(f'{BASE_URL}/protected', headers=headers)
        if response.status_code == 200:
            print("[INFO] Acceso al endpoint protegido: ", response.json())
        elif response.status_code == 401:
            print("[WARN] Access token expirado o inválido.")
        else:
            print("[ERROR] Error al acceder al endpoint protegido: ", response.json())

        time.sleep(10)  # Simula accesos periódicos al endpoint

def renew_access_token():
    """Renueva el access_token usando el refresh_token."""
    global access_token, refresh_token
    while True:
        if not refresh_token:
            print("[WARN] No hay refresh_token disponible. Esperando login...")
            time.sleep(30)
            continue

        response = requests.post(f'{BASE_URL}/refresh', json={
            'refresh_token': refresh_token
        })
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens.get('access_token')
            print("[INFO] Access token renovado exitosamente.")
        else:
            print(f"[ERROR] Error al renovar access token: {response.json()}")

        time.sleep(30)  # Renueva el access_token cada 30 segundos

def modify_user_role(new_role):
    """Modifica el rol del usuario."""
    global access_token
    if not access_token:
        print("[WARN] No hay access_token disponible. No se puede modificar el rol.")
        return

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.put(f'{BASE_URL}/modify-role', json={
        'username': USERNAME,
        'role': new_role
    }, headers=headers)

    if response.status_code == 200:
        print("[INFO] Rol modificado exitosamente: ", response.json())
    else:
        print(f"[ERROR] Error al modificar el rol: {response.json()}")

def main():
    """Punto de entrada principal."""
    # Registrar usuario
    register_user()

    # Iniciar sesión
    login_user()

    # Modificar el rol del usuario
    modify_user_role('admin')

    # Ejecutar tareas periódicas en hilos separados
    threading.Thread(target=access_protected_endpoint, daemon=True).start()
    threading.Thread(target=renew_access_token, daemon=True).start()

    # Mantener el script corriendo
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
