from flask import Flask, render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from flask import make_response
from flask import flash
import forms
app = Flask(__name__)
app.config['SECRET_KEY']="Esta es la clave encriptada"
csrf=CSRFProtect()

@app.route("/cookies", methods=['GET','POST'])
def cookies():
    reg_user=forms.LoginForm(request.form)
    datos=''
    if request.method=='POST' and reg_user.validate():
        user=reg_user.username.data
        passw=reg_user.password.data
        datos=user+'@'+passw
        success_message='Bienvenido {}'.format(user)
        flash(success_message)

    response=make_response(render_template('cookies.html',form=reg_user))
    if len(datos)>0:
        response.set_cookie('datos_user',datos)
    return response






@app.route("/formulario")
def formulario():
    return render_template('formulario.html')

@app.route("/palabras", methods=['GET','POST'])
def palabras():
    trad_form=forms.traductor(request.form)
    if request.method=='POST' and trad_form.validate():
        palabra= str(trad_form.palabra.data)
        word= str(trad_form.word.data)
        f=open('diccionario.txt','a')
        f.write('\n'+palabra.upper()+' = '+word.upper())
        f.close()
    return render_template('Act1_Diccionario.html',form=trad_form)



if __name__== "__main__":
    csrf.init_app(app)
    app.run(debug = True)