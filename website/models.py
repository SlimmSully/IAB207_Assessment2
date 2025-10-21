from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(32), default='attendee', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Event(db.Model):
    pass

class Comment(db.Model):
    pass

class Order(db.Model):
    pass
