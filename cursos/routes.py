from . import cursos_bp
from flask import render_template, request, redirect, url_for
from models import db, Curso, Maestros
from . import forms

@cursos_bp.route("", methods=['GET'])
def lista():
    cursos = Curso.query.all()
    return render_template("cursos/lista.html", cursos=cursos)

@cursos_bp.route("/insertar", methods=['GET', 'POST'])
def insertar():
    create_form = forms.CursosForm(request.form)
    maestros = Maestros.query.all()
    
    if request.method == 'POST':
        # Guardado básico
        curso = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=request.form.get('maestro_id') # Viene del select html
        )
        db.session.add(curso)
        db.session.commit()
        return redirect(url_for('cursos.lista'))
        
    return render_template("cursos/insertar.html", form=create_form, maestros=maestros)

@cursos_bp.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    if request.method == 'GET':
        id = request.args.get('id')
        curso = Curso.query.get(id)
        if curso:
            db.session.delete(curso)
            db.session.commit()
    return redirect(url_for('cursos.lista'))
