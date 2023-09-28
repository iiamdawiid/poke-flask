from app import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), index=True)
    last_name = db.Column(db.String(50), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)