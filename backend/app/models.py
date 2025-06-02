from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid # For widget IDs

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Widget(db.Model):
    __tablename__ = 'widgets'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # Use UUID for client-side generation
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    widget_type = db.Column(db.String(50), nullable=False) # 'notes', 'weather'
    config = db.Column(db.JSON, nullable=True) # For notes content, weather city etc.
    layout = db.Column(db.JSON, nullable=False) # For x, y, w, h from react-grid-layout

    user = db.relationship('User', backref=db.backref('widgets', lazy=True))