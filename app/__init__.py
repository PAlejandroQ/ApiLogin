from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        from .routes import register_routes
        from .models import User

        db.create_all()  # Crear tablas en la primera ejecución
        register_routes(app)

    return app
