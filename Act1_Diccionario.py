from flask import Flask, render_template, redirect
from flask import request
from flask_wtf.csrf import CSRFProtect
from flask import make_response
from flask import flash
import forms
from forms import SearchForm
app = Flask(__name__)
app.config['SECRET_KEY']="Esta es la clave encriptada"
csrf=CSRFProtect()

@app.route("/formulario")
def formulario():
    return render_template('formulario.html')

@app.route('/')
def index():
    return render_template('Act1_Diccionario.html')

@app.route("/palabras", methods=['GET','POST'])
def palabras():
    trad_form=SearchForm(request.form)
    if request.method=='POST':
        palabra= str(trad_form.palabra.data)
        word= str(trad_form.word.data)
        with open('diccionario.txt','a') as f:
            f.write(f'{palabra.upper()}:{word.upper()}\n')
        flash('Palabra agregada al diccionario', 'success')
        trad_form.palabra.data =""
        trad_form.word.data=""
    return render_template('Act1_Diccionario.html',form=trad_form)

@app.route('/buscarPalabra', methods=['GET', 'POST'])
def traduccion():
    speak_form = SearchForm(request.form)

    translation = ""
    diccionario = {}
    encontrado = False

    if request.method=="POST":
        translation = speak_form.search.data

        with open("diccionario.txt", "r") as f:
            for linea in f:
                clave, valor = linea.strip().split(":")
                diccionario[clave.upper()] = valor.upper()
                
           

        if request.form.get("idioma") == "ingles":
            for clave, valor in diccionario.items():
                if valor == translation.upper():
                    print(clave)
                    encontrado = True
                    return render_template("Act1_Diccionario.html", form=speak_form, translation=clave)
                speak_form.search.data=""
            if not encontrado:
                    return render_template("Act1_Diccionario.html", form=speak_form, translation="No hay")
            speak_form.search.data=""
                
            return
        if request.form.get("idioma") == "espanol":
            for clave, valor in diccionario.items():
                if clave == translation.upper():
                    print(valor)
                    encontrado = True
                    return render_template("Act1_Diccionario.html", form=speak_form, translation=valor)
                speak_form.search.data=""
            if not encontrado:
                return render_template("Act1_Diccionario.html", form=speak_form, translation="No hay")
            speak_form.search.data=""

if __name__== "__main__":
    csrf.init_app(app)
    app.run(debug = True)