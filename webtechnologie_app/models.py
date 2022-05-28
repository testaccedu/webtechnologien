from webtechnologie_app import db
from flask_login import UserMixin
from datetime import datetime

class Mitarbeiter(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    vorname = db.Column(db.String(255))
    passwort = db.Column(db.String(255))
    previligiert = db.Column(db.Integer())
    erstellt = db.Column(db.DateTime, default=datetime.utcnow)
    status_updates = db.relationship("Inventar_status", backref='mitarbeier', lazy=True)

class Inventar_typ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(255))
    feld_1_bez = db.Column(db.String(255))
    feld_2_bez = db.Column(db.String(255))
    feld_3_bez = db.Column(db.String(255))
    feld_4_bez = db.Column(db.String(255))
    inventar = db.relationship("Inventar", backref='inventar_typ', lazy=True)

class Inventar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventar_typ_id = db.Column(db.Integer, db.ForeignKey('inventar_typ.id'))
    feld_1 = db.Column(db.String(255))
    feld_2 = db.Column(db.String(255))
    feld_3 = db.Column(db.String(255))
    feld_4 = db.Column(db.String(255))
    status = db.relationship("Inventar_status", backref='Inventar', order_by="desc(Inventar_status.erstellt)", lazy='dynamic')


class Hallen(db.Model):
    __tablename__ = 'hallen'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    bezeichnung = db.Column(db.String(100), unique=True)

class Inventar_status(db.Model):
    __tablename__ = 'inventar_status'
    id = db.Column(db.Integer, primary_key=True)
    inventar_id = db.Column(db.Integer, db.ForeignKey('inventar.id'))
    standort_halle_id = db.Column(db.Integer, db.ForeignKey('hallen.id'))
    standort_feld = db.Column(db.String(255))
    standort_bemerkung = db.Column(db.String(255))
    mitarbeiter_id = db.Column(db.Integer, db.ForeignKey('mitarbeiter.id'))
    erstellt = db.Column(db.DateTime, default=datetime.now)
    mitarbeiter = db.relationship("Mitarbeiter", backref='Inventar_status', lazy=True)
