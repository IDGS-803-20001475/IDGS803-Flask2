from flask import Flask, render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from flask import make_response
from flask import flash
from flask import Flask, render_template, redirect
from flask import request
from flask_wtf.csrf import CSRFProtect
from flask import make_response
from flask import flash
from forms import SearchForm
from collections import Counter
import forms
app = Flask(__name__)
app.config['SECRET_KEY']="Esta es la clave encriptada"
csrf=CSRFProtect()

@app.errorhandler(404)
def no_encontrada(e):
    return render_template('404.html'),404
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

@app.route("/saludo")
def saludo():
    valor_cookie=request.cookies.get('datos_user')
    nombres=valor_cookie.split('@')
    return render_template('saludo.html',nom=nombres[0])

@app.route("/formulario")
def formulario():
    return render_template('formulario.html')

#CajasDinamicas
@app.route("/cajasD", methods=['GET', 'POST'])
def cajasDinamicas():
    if request.method == 'POST':
        cant = request.form.get('txtCant')
        return render_template('cajasDinamicas.html', cantidad = int(cant))
    else:
        return render_template('cajasDinamicas.html', cantidad = 0)

@app.route("/resultados", methods=['POST'])
def resCajasDinamicas():
    cantNums = request.form.get('txtCantNums')
    listaNums = []

    for i in range(1, int(cantNums)+1):
        value = request.form.get('caja'+str(i))
        listaNums.append(int(value))

    numMax = max(listaNums)
    numMin = min(listaNums)
    promedio = sum(listaNums)/int(cantNums)

    contador = Counter(listaNums)
    
    return render_template('resCajas.html', numMax = str(numMax), numMin = str(numMin), 
                           promedio = str(promedio), contador = contador, lenCont = len(contador))

#Alumnos
@app.route("/alumnos", methods=['GET','POST'])
def alumnos():
    alum_form=forms.UserForm(request.form)
    if request.method=='POST' and alum_form.validate():
        print(alum_form.matricula.data)
        print(alum_form.nombre.data)
    return render_template('Alumnos.html',form=alum_form)

#Diccionario-Traductor
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

#Calculadora de Resistencias

@app.route('/calculate', methods=['GET', 'POST'])
def resistencia():
    
    if request.method=='POST':
        colores = ['black','chocolate','red','orange','yellow','green','blue','purple','gray','white']
        tolerancia = ['goldenrod', 'silver']

        primerBanda = int(request.form.get('primerBanda'))
        segundaBanda = int(request.form.get('segundaBanda'))
        tercerBanda = int(request.form.get('tercerBanda'))
        cuartaBanda = int(request.form.get('cuartaBanda'))

        porcentajeTolerancia=int(10)
        if cuartaBanda == 0:
            porcentajeTolerancia=int(5)

        total = str(primerBanda) + "" + str(segundaBanda) + str( '0' * tercerBanda) 

        minimo = int(total) * (1 - (int(porcentajeTolerancia) / 100))
        maximo = int(total) * (1 + (int(porcentajeTolerancia) / 100))

        return render_template('Act2_Resistencias.html', total=total + "Ω Ohms "+ "Tolerancia: +/- " + str(porcentajeTolerancia) + "%",
                               minimo=minimo,maximo=maximo,
                               primero=str(primerBanda), segundo=str(segundaBanda),
                               tercero=str(tercerBanda),cuarto=str(cuartaBanda),
                               primerColor=colores[primerBanda],segundoColor=colores[segundaBanda],
                               tercerColor=colores[tercerBanda], cuartoColor=tolerancia[cuartaBanda]
                               )
    else:
        
        return render_template('Act2_Resistencias.html', total=0 ,minimo=0,maximo=0)
    
if __name__== "__main__":
    csrf.init_app(app)
    app.run(debug = True)