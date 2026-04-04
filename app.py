from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate

# Importar Blueprints
from maestros import maestros_bp
from alumnos import alumnos_bp
from cursos import cursos_bp
from inscripciones import inscripciones_bp

from models import db, Alumnos, Maestros, Curso, Inscripcion

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Registrar Blueprints
app.register_blueprint(maestros_bp, url_prefix="/maestros")
app.register_blueprint(alumnos_bp, url_prefix="/alumnos")
app.register_blueprint(cursos_bp, url_prefix="/cursos")
app.register_blueprint(inscripciones_bp, url_prefix="/inscripciones")

db.init_app(app)
csrf=CSRFProtect()
migrate=Migrate(app, db)


@app.route("/",methods=["GET","POST"])
@app.route("/index")
def index():
    # El index ahora es solo el dashboard visual
    return render_template("index.html")


if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()