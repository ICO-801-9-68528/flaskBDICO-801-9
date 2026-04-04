from . import inscripciones_bp
from flask import render_template, request, redirect, url_for
from models import db, Inscripcion, Alumnos, Curso

@inscripciones_bp.route("", methods=['GET'])
def lista():
    # Join con alumnos y cursos para obtener los detalles visuales
    records = db.session.query(Inscripcion, Alumnos, Curso)\
        .join(Alumnos, Alumnos.id == Inscripcion.alumno_id)\
        .join(Curso, Curso.id == Inscripcion.curso_id).all()
    
    return render_template("inscripciones/lista.html", records=records)

@inscripciones_bp.route("/insertar", methods=['GET', 'POST'])
def insertar():
    alumnos = Alumnos.query.all()
    cursos = Curso.query.all()
    
    if request.method == 'POST':
        alumno_id = request.form.get('alumno_id')
        curso_id = request.form.get('curso_id')
        
        try:
            insc = Inscripcion(
                alumno_id=alumno_id,
                curso_id=curso_id
            )
            db.session.add(insc)
            db.session.commit()
        except:
            # En caso de error (e.g., registro duplicado)
            db.session.rollback()
            
        return redirect(url_for('inscripciones.lista'))
        
    return render_template("inscripciones/insertar.html", alumnos=alumnos, cursos=cursos)

@inscripciones_bp.route("/eliminar", methods=['GET'])
def eliminar():
    id = request.args.get('id')
    insc = Inscripcion.query.get(id)
    if insc:
        db.session.delete(insc)
        db.session.commit()
    return redirect(url_for('inscripciones.lista'))
