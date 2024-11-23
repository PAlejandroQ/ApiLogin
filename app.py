from flask import Flask
from app.routes import register_routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900  #  15 minutos
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400  # 1 día

db = SQLAlchemy(app)
migrate = Migrate(app, db)

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
