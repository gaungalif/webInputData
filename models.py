# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pemilih(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    no_ktp = db.Column(db.String(16), nullable=False)
    kecamatan = db.Column(db.String(50), nullable=False)
    kelurahan = db.Column(db.String(50), nullable=False)
    koordinator = db.Column(db.String(255), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    role = db.Column(db.String(10), nullable=False)

