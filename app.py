from flask import Flask, render_template,request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate 
from config import DevelopmentConfig
import forms

from models import db, Alumnos, Maestros

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)


@app.route("/")
@app.route("/index")
def index():
     create_alumno=forms.UserForm(request.form)
     #select * alumnos alumnos 
     alumno=Alumnos.query.all()
     maestro=Maestros.query.all()
     return render_template("index.html",form=create_alumno, alumno=alumno, maestro=maestro)

@app.route("/",methods=["GET","POST"])
def usuario():
    mat=0
    nom=''
    apa=''
    ama=''
    edad=0
    email=''
    usuarios_clas=forms.UserForm(request.form)
    if request.method=='POST':
        mat=usuarios_clas.matricula.data
        nom=usuarios_clas.nombre.data
        apa=usuarios_clas.apaterno.data
        ama=usuarios_clas.amaterno.data
        edad=usuarios_clas.edad.data
        email=usuarios_clas.correo.data
    
    return render_template('usuarios.html',form=usuarios_clas,mat=mat,
                           nom=nom,apa=apa,ama=ama,edad=edad,email=email)

@app.route("/maestros", methods=["GET","POST"])
def maestros():
    create_maestro=forms.MaestroForm(request.form)
    alumno=Alumnos.query.all()
    maestro=Maestros.query.all()
    
    if request.method=='POST' and create_maestro.validate():
        try:
            nuevo_maestro = Maestros(
                matricula=create_maestro.matricula.data, 
                nombre=create_maestro.nombre.data, 
                apellidos=create_maestro.apellidos.data, 
                especialidad=create_maestro.especialidad.data, 
                email=create_maestro.email.data
            )
            db.session.add(nuevo_maestro)
            db.session.commit()
            flash('Maestro agregado exitosamente')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar maestro: {str(e)}')
    
    return render_template("index.html", form=create_maestro, maestro=maestro, alumno=alumno)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Agregar maestros de ejemplo si la tabla está vacía
        if Maestros.query.count() == 0:
            maestros_ejemplo = [
                Maestros(matricula=1001, nombre='Carlos', apellidos='García López', especialidad='Matemáticas', email='carlos.garcia@school.com'),
                Maestros(matricula=1002, nombre='María', apellidos='Rodríguez Pérez', especialidad='Física', email='maria.rodriguez@school.com'),
                Maestros(matricula=1003, nombre='Juan', apellidos='Martínez Silva', especialidad='Química', email='juan.martinez@school.com'),
            ]
            for mae in maestros_ejemplo:
                db.session.add(mae)
            db.session.commit()
    
    app.run()