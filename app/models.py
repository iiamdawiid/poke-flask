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

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.date_created = datetime.utcnow()

class CatchPokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String(50))
    base_hp = db.Column(db.Integer)
    base_defense = db.Column(db.Integer)
    base_attack = db.Column(db.Integer)
    image = db.Column(db.String(200))
    ability = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, pokemon_name, base_hp, base_defense, base_attack, image, ability, user_id):
        self.pokemon_name = pokemon_name
        self.base_hp = base_hp
        self.base_defense = base_defense 
        self.base_attack = base_attack
        self.image = image
        self.ability = ability
        self.user_id = user_id