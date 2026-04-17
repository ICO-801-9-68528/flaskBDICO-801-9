# Blueprint es para manejarlo como módulos
from . import maestros_bp
from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from models import db
from models import Maestros

from . import forms
from sqlalchemy.exc import IntegrityError


# Creamos la rutas con maestro en vez de app
@maestros_bp.route("", methods=["POST", "GET"])
def maestros():
	create_form = forms.MaestrosForm(request.form)
	maestro = Maestros.query.all()
	return render_template("maestros/maestros.html", form=create_form, maestro=maestro)


@maestros_bp.route("/insertar", methods=["GET", "POST"])
def insertar():
	maestro_Class = forms.MaestrosForm(request.form)
	if request.method == "POST":
		mae = Maestros(
			matricula=maestro_Class.matricula.data,
			nombre=maestro_Class.nombre.data,
			apellidos=maestro_Class.apellidos.data,
			especialidad=maestro_Class.especialidad.data,
			email=maestro_Class.email.data,
		)
		try:
			db.session.add(mae)
			db.session.commit()
			flash("¡Maestro registrado con éxito!", "success")
			return redirect(url_for("maestros.maestros"))
		except IntegrityError:
			db.session.rollback()
			flash(
				f"Error: La matrícula {maestro_Class.matricula.data} ya está ocupada por otro maestro.",
				"danger",
			)
			return redirect(url_for("maestros.insertar"))
	return render_template("maestros/insertar_maestro.html", form=maestro_Class)


@maestros_bp.route("/detalles", methods=["GET", "POST"])
def detalles():
	maestro_Class = forms.MaestrosForm(request.form)
	if request.method == "GET":
		matricula = request.args.get("mat")
		mae = (
			db.session.query(Maestros)
			.filter(Maestros.matricula == matricula)
			.first()
		)
		nombre = mae.nombre
		apellidos = mae.apellidos
		especialidad = mae.especialidad
		email = mae.email
	return render_template(
		"maestros/detalles_maestro.html",
		matricula=matricula,
		nombre=nombre,
		apellidos=apellidos,
		email=email,
		especialidad=especialidad,
	)


@maestros_bp.route("/modificar_maestro", methods=["GET", "POST"])
def modificar():
	maestro_Class = forms.MaestrosForm(request.form)
	if request.method == "GET":
		matricula = request.args.get("mat")
		mae = (
			db.session.query(Maestros)
			.filter(Maestros.matricula == matricula)
			.first()
		)
		maestro_Class.matricula.data = request.args.get("mat")
		maestro_Class.nombre.data = mae.nombre
		maestro_Class.apellidos.data = mae.apellidos
		maestro_Class.especialidad.data = mae.especialidad
		maestro_Class.email.data = mae.email
	if request.method == "POST":
		matricula = maestro_Class.matricula.data
		mae = (
			db.session.query(Maestros)
			.filter(Maestros.matricula == matricula)
			.first()
		)
		mae.matricula = matricula
		mae.nombre = str.rstrip(maestro_Class.nombre.data)
		mae.apellidos = maestro_Class.apellidos.data
		mae.especialidad = maestro_Class.especialidad.data
		mae.email = maestro_Class.email.data
		db.session.add(mae)
		db.session.commit()
		return redirect(url_for("maestros.maestros"))
	return render_template("maestros/modificar_maestro.html", form=maestro_Class)


@maestros_bp.route("/eliminar_maestro", methods=["GET", "POST"])
def eliminar():
	maestro_class = forms.MaestrosForm(request.form)
	from models import Curso

	if request.method == "GET":
		matricula = request.args.get("mat")
		mae = (
			db.session.query(Maestros)
			.filter(Maestros.matricula == matricula)
			.first()
		)
		maestro_class.matricula.data = request.args.get("mat")
		maestro_class.nombre.data = mae.nombre
		maestro_class.apellidos.data = mae.apellidos
		maestro_class.especialidad.data = mae.especialidad
		maestro_class.email.data = mae.email

		# Obtener la lista de maestros para reasignar cursos
		maestros_disponibles = Maestros.query.filter(Maestros.matricula != matricula).all()
		# Contar cursos asociados
		cursos_count = Curso.query.filter_by(maestro_id=matricula).count()
		return render_template(
			"maestros/eliminar_maestro.html",
			form=maestro_class,
			maestros_disponibles=maestros_disponibles,
			cursos_count=cursos_count,
		)

	if request.method == "POST":
		# Asegurar tipo entero para la clave primaria
		try:
			matricula = int(maestro_class.matricula.data)
		except (TypeError, ValueError):
			flash("Matrícula inválida.", "danger")
			return redirect(url_for("maestros.maestros"))
		mae = Maestros.query.get(matricula)

		# Reasignar o eliminar los cursos según la elección del usuario
		cursos_asociados = Curso.query.filter_by(maestro_id=matricula).all()
		delete_courses = request.form.get("delete_courses")
		nuevo_maestro_id = request.form.get("nuevo_maestro_id")

		if cursos_asociados:
			if delete_courses:
				# eliminar cursos asociados
				for curso in cursos_asociados:
					db.session.delete(curso)
			else:
				# requerir nuevo maestro para reasignar si hay cursos
				if not nuevo_maestro_id:
					flash(
						"Debe seleccionar un maestro para reasignar los cursos antes de eliminar.",
						"warning",
					)
					return redirect(url_for("maestros.eliminar") + f"?mat={matricula}")
				# reasignar al maestro seleccionado
				for curso in cursos_asociados:
					try:
						curso.maestro_id = int(nuevo_maestro_id)
					except (TypeError, ValueError):
						curso.maestro_id = None

			# Persistir cambios de cursos antes de eliminar al maestro
			try:
				db.session.commit()
			except Exception as e:
				db.session.rollback()
				current_app.logger.exception("Error al persistir cambios en cursos antes de eliminar maestro: %s", e)
				flash("No se pudo actualizar los cursos. Operación cancelada.", "danger")
				return redirect(url_for("maestros.eliminar") + f"?mat={matricula}")
		# si no hay cursos asociados, no es necesario seleccionar nuevo maestro ni checkbox

		# Log info for debugging
		current_app.logger.info("Reasignando %d cursos de maestro %s a %s", len(cursos_asociados), matricula, nuevo_maestro_id)

		try:
			current_app.logger.info("Borrando maestro matricula=%s; cursos=%s; nuevo_maestro=%s", matricula, len(cursos_asociados), nuevo_maestro_id)
			# refrescar sesión por si hubo commits previos
			db.session.expire_all()
			mae = Maestros.query.get(matricula)
			if mae:
				db.session.delete(mae)
				db.session.commit()
			else:
				current_app.logger.warning("Maestro matricula=%s no existe al intentar borrar.", matricula)
		except Exception as e:
			db.session.rollback()
			current_app.logger.exception("Error al eliminar/actualizar cursos: %s", e)
			flash("Ocurrió un error al eliminar el maestro. Revisa el registro.", "danger")
			return redirect(url_for("maestros.maestros"))

		# Verificar que se eliminó
		remaining = Maestros.query.get(matricula)
		if remaining:
			current_app.logger.warning("El maestro matricula=%s sigue presente tras commit.", matricula)
			flash('El maestro no se pudo eliminar completamente; revisa la base de datos.', 'warning')
		else:
			current_app.logger.info("Maestro matricula=%s eliminado correctamente.", matricula)
		flash("¡Maestro eliminado con éxito y los cursos han sido reasignados!", "success")
		return redirect(url_for("maestros.maestros"))

	return render_template("maestros/eliminar_maestro.html", form=maestro_class)


@maestros_bp.route("/asignar_curso", methods=["GET", "POST"])
def asignar_curso():
	from models import Curso

	if request.method == "POST":
		curso_id = request.form.get("curso_id")
		maestro_id = request.form.get("maestro_id")

		curso = Curso.query.get(curso_id)
		if curso:
			curso.maestro_id = maestro_id
			db.session.commit()
			flash("¡Maestro asignado al curso con éxito!", "success")
		else:
			flash("Curso no encontrado.", "danger")

		return redirect(url_for("maestros.maestros"))

	cursos = Curso.query.all()
	maestros = Maestros.query.all()
	return render_template("maestros/asignar_curso.html", cursos=cursos, maestros=maestros)