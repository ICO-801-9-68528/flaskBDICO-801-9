from flask import Flask, render_template,request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms

from models import db, Alumnos, Maestros

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
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
    maestro=Maestros.query.all()
    
    if request.method=='POST':
        mat=create_maestro.matricula.data
        nom=create_maestro.nombre.data
        apa=create_maestro.apellidos.data
        esp=create_maestro.especialidad.data
        email=create_maestro.email.data
    
    return render_template("maestros.html", form=create_maestro, maestro=maestro)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()