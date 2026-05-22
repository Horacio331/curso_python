from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import re
from pdf_processor import get_pdfs, main_dictionary, pdf_dictionary, buscar_palabras_ratio

app = Flask(__name__)

# Base de datos en memoria simplificada para las URLs de Configuración/Scrapper
URLS_DATA = {
    "https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/": {
        "status": "No escrapeada",
        "files": []
    }
}

def calcular_estadisticas():
    """Calcula dinámicamente los datos para la página Home."""
    total_docs = len(pdf_dictionary)
    
    # Contar palabras totales de los contenidos indexados
    total_palabras = sum(len(doc.content.split()) for doc in pdf_dictionary.values())
    
    # Extraer documentos por año basándose en el nombre del archivo o contenido (ej: 2026, 2025)
    docs_por_anio = {}
    for filename in pdf_dictionary.keys():
        # Intentamos buscar un año de 4 dígitos (2020-2029) en el nombre del archivo
        match = re.search(r'(202\d)', filename)
        anio = match.group(1) if match else "Desconocido"
        docs_por_anio[anio] = docs_por_anio.get(anio, 0) + 1
        
    return total_docs, total_palabras, docs_por_anio

@app.route('/')
def home():
    total_docs, total_palabras, docs_por_anio = calcular_estadisticas()
    return render_template('home.html', total_docs=total_docs, total_palabras=total_palabras, docs_por_anio=docs_por_anio)

@app.route('/scrapper')
def scrapper():
    return render_template('scrapper.html', urls=URLS_DATA)

@app.route('/run_scrapper', methods=['POST'])
def run_scrapper():
    url = request.form.get('url')
    if url in URLS_DATA:
        print(f"[*] Iniciando scraping web para: {url}")
        # Llamamos a tu función de procesamiento
        nuevos_pdfs = get_pdfs(url)
        
        # Actualizamos el estatus y la lista de archivos asociados a esa URL
        URLS_DATA[url]["status"] = "Escrapeada"
        URLS_DATA[url]["files"] = list(nuevos_pdfs.keys())
        
        # Re-indexar los chunks en el diccionario global de búsqueda
        reindexar_chunks()
        
    return redirect(url_for('scrapper'))

@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    if request.method == 'POST':
        nueva_url = request.form.get('url_nueva')
        if nueva_url and nueva_url not in URLS_DATA:
            URLS_DATA[nueva_url] = {"status": "No escrapeada", "files": []}
        return redirect(url_for('configuration'))
    return render_template('configuration.html', urls=URLS_DATA)

@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    anio_seleccionado = request.args.get('anio', 'Todos') # Recibe el año elegido
    
    umbral_fijo = 0.25
    resultados = []
    
    # 1. Detectar qué años existen en los PDFs indexados actualmente
    anios_disponibles = set()
    for filename in pdf_dictionary.keys():
        match = re.search(r'(202\d)', filename)
        if match:
            anios_disponibles.add(match.group(1))
    anios_ordenados = sorted(list(anios_disponibles), reverse=True)

    if query:
        coincidencias = buscar_palabras_ratio(main_dictionary, query, umbral=umbral_fijo)
        
        for chunk, archivos, ratio in coincidencias:
            for archivo in archivos:
                # Extaer el año de este archivo en específico para poder filtrarlo
                match_file = re.search(r'(202\d)', archivo)
                anio_archivo = match_file.group(1) if match_file else "Desconocido"
                
                # FILTRO: Si el usuario eligió un año específico, ignoramos los demás
                if anio_seleccionado != "Todos" and anio_archivo != anio_seleccionado:
                    continue
                    
                url_original = pdf_dictionary[archivo].url if archivo in pdf_dictionary else "#"
                resultados.append({
                    "url": url_original,
                    "archivo": archivo,
                    "bloque": chunk,
                    "porcentaje": round(ratio * 100, 1)  
                })
                
    return render_template('search.html', 
                           query=query, 
                           resultados=resultados, 
                           anios=anios_ordenados, 
                           anio_seleccionado=anio_seleccionado)

def reindexar_chunks():
    """Actualiza el main_dictionary global con los bloques de 20 palabras."""
    main_dictionary.clear()
    chunk_length = 20
    for filename, pdf_doct in pdf_dictionary.items():
        words = (pdf_doct.content or "").split()
        for i in range(0, len(words), chunk_length):
            chunk_text = " ".join(words[i:i+chunk_length])
            if chunk_text not in main_dictionary:
                main_dictionary[chunk_text] = [filename]
            elif filename not in main_dictionary[chunk_text]:
                main_dictionary[chunk_text].append(filename)

if __name__ == '__main__':
    app.run(debug=True)