from wtforms import Form
from wtforms import StringField, IntegerField, EmailField,PasswordField
from wtforms import validators


class UserForm(Form):
    id=IntegerField("ID")
    nombre=StringField('Nombre')
    apaterno=StringField('Apaterno')
    amaterno=StringField('Amaterno')
    edad=IntegerField("Edad")
    correo=EmailField('Correo')

class MaestrosForm(Form):
    matricula=StringField('matricula', [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=3, max=10, message="Ingrese una matricula válida")
    ])
    nombre=StringField('Nombre', [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=3, max=10, message="Ingrese un nombre válido")
    ])
    apellidos=StringField('Apellidos', [
        validators.DataRequired(message="El campo es requerido")
    ])
    especialidad=StringField('Especialidad', [
        validators.DataRequired(message="Ingrese una especialidad válida")
    ])
    email=StringField('Email', [
        validators.Email(message="Ingrese un correo válido")
    ])