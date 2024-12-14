<h2 align="center">
<p>IMPLEMENTACIÓN DE UN SISTEMA DE AUTORIZACIÓN USANDO AOP</p>
</h2>

<h2 align="center">
<img src="https://img.shields.io/badge/python-3670A0?&style=for-the-badge&logo=python&logoColor=ffdd54"/>
<img src="https://img.shields.io/badge/Flask-%23E23237.svg?style=for-the-badge&logo=flask&logoColor=black" />
<img src="https://img.shields.io/badge/SQLite-%23003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white" />
</h2>

Este proyecto desarrolla un sistema de autorización basado en roles utilizando **Programación Orientada a Aspectos (AOP)** en Flask. La API incluye:

- **Control de acceso por roles**: Verifica si un usuario tiene permisos para acceder a ciertos recursos basándose en su rol.
- **Autenticación con JWT**: Asegura que los usuarios estén autenticados antes de acceder a endpoints protegidos.
- **Auditoría de acciones**: Registra las actividades clave realizadas en el sistema.

El uso de AOP centraliza la lógica transversal como la validación de roles, la autenticación y la auditoría, evitando la duplicación de código y mejorando la escalabilidad del sistema.

## Integrantes del Proyecto

1. **Tello Leon Jose**
2. **Quispe Olaechea Pablo**
3. **Colque Unoc Gabriela**
5. **Cadillo Tarazona Jharvy**
6. **Rodriguez Ricra Emhir**
7. **Quispe Villena Renzo**

## Problema que Resuelve

En sistemas donde múltiples funciones requieren validaciones como verificar tokens JWT o roles de usuario, es común duplicar lógica en varios puntos. Esto dificulta el mantenimiento y la escalabilidad. 

Con este proyecto se centraliza esa lógica en decoradores basados en AOP, lo que:

- **Aumenta la seguridad**, asegurando que las validaciones se ejecuten siempre que sea necesario.
- **Reduce el acoplamiento**, separando las preocupaciones transversales del código principal.
- **Facilita el mantenimiento**, al permitir cambios en una sola ubicación para impactar todo el sistema.

## Estructura del Proyecto
```
.
├── app
│   └── audit_logging.py
│   └── decorators.py
│   └── __init__.py
│   └── models.py
│   └── routes.py
│   └── services.py
│   └── utils.py
├── app.py
├── instance
│   └── app.db
├── logs
│   └── audit_2024-11-23.log
├── tests
│   └── mobile_app_simulator.py
│   └── test_endpoints.py
```

## Instrucciones para Ejecutar el Proyecto
### **1. Clonar el Repositorio**
Clona el repositorio desde GitHub usando el siguiente comando:

```bash
git clone https://github.com/PAlejandroQ/ApiLogin.git
cd ApiLogin
```
### **2. Instalar las Dependencias**
Instala las dependencias requeridas con:

```bash
pip install -r requirements.txt
```
### **3. Iniciar la Aplicación**
Ejecuta la aplicación con el siguiente comando:

```bash
python app.py
```
### **4. Ejecutar las Pruebas**
Después de iniciar Flask, puedes ejecutar los dos scripts de prueba incluidos en el proyecto:

#### **4.1. Prueba de los Endpoints**
Ejecuta el archivo `test_endpoints.py` para verificar los endpoints principales de la API:

```bash
python tests/test_endpoints.py
```
#### **4.2. Simulación de Usuario Móvil**
Ejecuta el archivo `mobile_app_simulator.py` para simular solicitudes desde un cliente móvil::

```bash
python tests/mobile_app_simulator.py
```
