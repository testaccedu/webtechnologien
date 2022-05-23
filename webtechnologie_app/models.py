from webtechnologie_app import db
from flask_login import UserMixin

class Mitarbeiter(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100), unique=True)
    vorname = db.Column(db.String(100))
    passwort = db.Column(db.String(100))
    previligiert = db.Column(db.Integer())


class Hallen(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    bezeichnung = db.Column(db.String(100), unique=True)
