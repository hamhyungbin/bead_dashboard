from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config
from .models import db  # Import db instance

migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app) # Enable CORS for all routes

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app