from . import alumnos_bp
from flask import render_template, request, redirect, url_for, flash
from models import db, Alumnos
from . import forms
from sqlalchemy.exc import IntegrityError

@alumnos_bp.route("", methods=['GET'])
def lista():
    alumno = Alumnos.query.all()
    return render_template("alumnos/lista.html", alumno=alumno)

@alumnos_bp.route("/Alumnos",methods=['GET','POST'])
def alumnos():
    create_form=forms.AlumnosForm(request.form)
    if request.method=='POST':
        alum=Alumnos(nombre=create_form.nombre.data,
                     apaterno=create_form.apaterno.data,
                     amaterno=create_form.amaterno.data,
                     edad=create_form.edad.data,
                     correo=create_form.correo.data)
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumnos.lista'))
    return render_template("alumnos/Alumnos.html",form=create_form)

@alumnos_bp.route("/modificar",methods=['GET','POST'])
def modificar():
    create_form=forms.AlumnosForm(request.form)
    if request.method=='GET':
         id=request.args.get('id')
         alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
         create_form.id.data=request.args.get('id')
         create_form.nombre.data=alum1.nombre
         create_form.apaterno.data=alum1.apaterno
         create_form.amaterno.data=alum1.amaterno
         create_form.edad.data=alum1.edad
         create_form.correo.data=alum1.correo
    
    if request.method=='POST':
        id=request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum1.id=id
        alum1.nombre=create_form.nombre.data
        alum1.apaterno=create_form.apaterno.data
        alum1.amaterno=create_form.amaterno.data
        alum1.edad=create_form.edad.data
        alum1.correo=create_form.correo.data
        db.session.add(alum1)
        db.session.commit()
        return redirect(url_for('alumnos.lista'))
    return render_template("alumnos/modificar.html",form=create_form)

@alumnos_bp.route('/eliminar',methods=['GET','POST'])
def eliminar():
    create_form=forms.AlumnosForm(request.form)
    if request.method=='GET':
         id=request.args.get('id')
         alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
         create_form.id.data=request.args.get('id')
         create_form.nombre.data=alum1.nombre
         create_form.apaterno.data=alum1.apaterno
         create_form.amaterno.data=alum1.amaterno
         create_form.edad.data=alum1.edad    
         create_form.correo.data=alum1.correo
    if request.method=='POST':
         id=request.form.get('id')
         alum = Alumnos.query.get_or_404(id)
         db.session.delete(alum) 
         db.session.commit()
         return redirect(url_for('alumnos.lista'))
    return render_template('alumnos/eliminar.html',form=create_form)

@alumnos_bp.route("/detalles",methods=['GET','POST'])
def detalles():
    create_form=forms.AlumnosForm(request.form)
    if request.method=='GET':
         id=request.args.get('id')
         alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
         id=request.args.get('id')
         nombre=alum1.nombre
         apaterno=alum1.apaterno
         amaterno=alum1.amaterno
         edad=alum1.edad     
         correo=alum1.correo
         
    return render_template('alumnos/detalles.html',id=id,nombre=nombre,apaterno=apaterno,
                           amaterno=amaterno,edad=edad,correo=correo)

@alumnos_bp.route("/usuarios",methods=["GET","POST"])
def usuario():
    mat=0
    nom=''
    apa=''
    ama=''
    edad=0
    email=''
    usuarios_clas=forms.AlumnosForm(request.form)
    if request.method=='POST':
        mat=usuarios_clas.id.data
        nom=usuarios_clas.nombre.data
        apa=usuarios_clas.apaterno.data
        ama=usuarios_clas.amaterno.data
        edad=usuarios_clas.edad.data
        email=usuarios_clas.correo.data
    
    return render_template('alumnos/usuarios.html',form=usuarios_clas,mat=mat,
                           nom=nom,apa=apa,ama=ama,edad=edad,email=email)

@alumnos_bp.route("/insertar", methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        nueva_matricula = request.form.get('matricula')
        
        nuevo_maestro = Alumnos(
            matricula=nueva_matricula,
            nombre=request.form.get('nombre'),
            apellidos=request.form.get('apellidos'),
            especialidad=request.form.get('especialidad'),
            email=request.form.get('email')
        )
        
        try:
            db.session.add(nuevo_maestro)
            db.session.commit()
            flash('¡Maestro registrado con éxito!', 'success')
            return redirect(url_for('alumnos.lista'))
        except IntegrityError:
            db.session.rollback() # Importante para limpiar la sesión fallida
            flash(f'Error: La matrícula {nueva_matricula} ya está ocupada por otro maestro.', 'danger')
            return redirect(url_for('alumnos.insertar')) # Regresa al formulario

    return render_template('alumnos/insertar.html')
