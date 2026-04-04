from wtforms import Form
from wtforms import StringField, IntegerField, EmailField, PasswordField
from wtforms import validators

class AlumnosForm(Form):
    id=IntegerField("ID")
    nombre=StringField('Nombre')
    apaterno=StringField('Apaterno')
    amaterno=StringField('Amaterno')
    edad=IntegerField("Edad")
    correo=EmailField('Correo')
