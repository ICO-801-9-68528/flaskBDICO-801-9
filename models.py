from flask_sqlalchemy import SQLAlchemy #ORM
import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apaterno = db.Column(db.String(50), nullable=False)
    amaterno = db.Column(db.String(150), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    correo = db.Column(db.String(200), nullable=False)

class Maestros(db.Model):
    __tablename__ = 'maestros'
    matricula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
  