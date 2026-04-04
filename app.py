from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate

# Importar Blueprints
from maestros import maestros_bp
from alumnos import alumnos_bp
from cursos import cursos_bp
from inscripciones import inscripciones_bp

# Importar modelos y base de datos
from models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Inicializar extensiones
db.init_app(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

# Registrar Blueprints ANTES de las rutas principales
app.register_blueprint(maestros_bp, url_prefix="/maestros")
app.register_blueprint(alumnos_bp, url_prefix="/alumnos")
app.register_blueprint(cursos_bp, url_prefix="/cursos")
app.register_blueprint(inscripciones_bp, url_prefix="/inscripciones")

# --- RUTA PRINCIPAL (DASHBOARD) ---
@app.route("/")
def dashboard(): 
    # Usamos un nombre de función único 'dashboard' para evitar el RecursionError
    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Importante: debug=True para ver si algo más falla en la terminal
    app.run(debug=True, port=5000)