
from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, RadioField
from wtforms.fields import EmailField
from wtforms import validators

def mi_validacion(form,field):
    if len(field.data)==0:
        raise validators.ValidationError('El campo no tiene datos')
    
class UserForm(Form):
    matricula=StringField('Matricula',[
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=4,max=15, message="No cumple la longitud para el campo")
    ])
    nombre=StringField('Nombre',[
        validators.DataRequired(message="El campo es requerido")
    ])
    apaterno=StringField('Apaterno',[mi_validacion])
    email=EmailField('Correo')


class LoginForm(Form):
    username=StringField('usuario',[
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=4,max=15, message="No cumple la longitud para el campo")
    ])
    password=StringField('password',[
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=4,max=15, message="No cumple la longitud para el campo")
    ])

class traductor(Form):
    palabra=StringField('español',[
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=2,max=15, message="No cumple la longitud para el campo")
    ])
    word=StringField('ingles',[
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=2,max=15, message="No cumple la longitud para el campo")
    ])