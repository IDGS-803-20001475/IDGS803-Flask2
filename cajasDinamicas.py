from flask import Flask, render_template
from flask import request
from collections import Counter
import forms
app = Flask(__name__)

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


if __name__== "__main__":
    app.run(debug = True)