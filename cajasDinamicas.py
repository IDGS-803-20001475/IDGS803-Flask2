from flask import Flask, render_template
from flask import request
import forms
app = Flask(__name__)

@app.route("/cajasD")
def cajasD():
    if request.method == 'POST':
        num_inputs = int(request.form['num_inputs'])
        return render_template('cajasDinamicas.html', num_inputs=num_inputs)



if __name__== "__main__":
    app.run(debug = True)