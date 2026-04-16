from flask import Flask, render_template, request
from frases_celebres import Frase, carga_archivo_csv, crea_diccionario_titulos, buscar_palabras, buscar_palabras_ratio

app = Flask(__name__)

frases = carga_archivo_csv("frases_consolidadas.csv")
diccionario_titulos = crea_diccionario_titulos(frases)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pelicula')
def pelicula():
    return render_template("peliculas.html")

@app.route('/frase')
def frase():
    if request.method == 'POST':
        frase = request.form['frase']
        umbral = request.form['umbral']
        frases_encontradas = buscar_palabras_ratio(frases, frase, umbral)
        return render_template("frases.html", frases=frases_encontradas)
    else:
        return render_template("frases.html", frases=frases)

if __name__ == "__main__":
    app.run(debug=True)