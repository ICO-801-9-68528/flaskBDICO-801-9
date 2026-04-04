from wtforms import Form
from wtforms import StringField, IntegerField, TextAreaField
from wtforms import validators

class CursosForm(Form):
    id = IntegerField('ID')
    nombre = StringField('Nombre del Curso', [
        validators.DataRequired(message="El nombre es obligatorio")
    ])
    descripcion = TextAreaField('Descripción')
    maestro_id = IntegerField('ID del Maestro Titular', [
        validators.DataRequired(message="Debe asignar un maestro")
    ])
