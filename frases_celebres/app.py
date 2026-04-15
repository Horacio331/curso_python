from flask import Flask, render_template, request
from frases_celebres import Frase, carga_archivo_csv, crea_diccionario_titulos, buscar_palabras

app = Flask(__name__)

frases = carga_archivo_csv("frases_consolidadas.csv")
diccionario_titulos = crea_diccionario_titulos(frases)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pelicula')
def pelicula():
    return render_template("pelicula.html")

@app.route('/frase')
def frase():
    return render_template("frase.html")

if __name__ == "__main__":
    app.run(debug=True) 