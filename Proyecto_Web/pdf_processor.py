import os 
import warnings
from urllib.parse import urljoin 
import requests
from bs4 import BeautifulSoup
from markitdown import MarkItDown
import Levenshtein
import numpy as np
import easyocr
from pdf2image import convert_from_path

warnings.filterwarnings("ignore", category=DeprecationWarning)
POPPLER_PATH = r"C:\Users\Usuario\poppler_windows\poppler-26.02.0\Library\bin"

# Estructuras de almacenamiento global en memoria
pdf_dictionary = {}  # { filename: objeto_pdf_document }
main_dictionary = {} # { chunk_text: [filenames] }

print("[*] Inicializando motores OCR y MarkItDown...")
reader = easyocr.Reader(['es'], gpu=False)
converter = MarkItDown()

class pdf_document:
    def __init__(self, url, pdf_path, markdown_path):
        self.url = url
        self.pdf_path = pdf_path
        self.markdown_path = markdown_path
        self.content = ""
        self.convert_pdf_to_markdown()
        
    def convert_pdf_to_markdown(self):
        try:
            result = converter.convert(self.pdf_path)
            markdown_content = result.markdown or result.text_content or ""
            
            if len(markdown_content.strip()) < 50:
                print(f"   [!] Iniciando OCR para: {os.path.basename(self.pdf_path)}")
                images = convert_from_path(self.pdf_path, poppler_path=POPPLER_PATH)
                ocr_text = ""
                for i, image in enumerate(images):
                    img_np = np.array(image)
                    results = reader.readtext(img_np, detail=0)
                    ocr_text += f"\n\n### Página {i+1}\n" + " ".join(results)
                markdown_content = ocr_text

            self.content = markdown_content
            with open(self.markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
        except Exception as e:
            print(f"Error en conversión: {e}")

def get_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except: return None 

def extract_pdf_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    return [urljoin(base_url, link['href']) for link in soup.find_all('a', href=True) if link['href'].endswith('.pdf')]

def download_pdf(url, filename):
    try:
        res = requests.get(url, timeout=10)
        with open(filename, 'wb') as f: f.write(res.content)
    except Exception as e: print(f"Error descarga: {e}")

def get_pdfs(url):
    download_path = "downloaded_pdfs"
    markdown_path = "markdown_files"
    os.makedirs(download_path, exist_ok=True)
    os.makedirs(markdown_path, exist_ok=True)
        
    html = get_webpage(url)
    if not html: return {}

    pdf_links = extract_pdf_links(html, url)
    nuevos_docs = {}
    
    for link in pdf_links:
        filename = link.split('/')[-1]
        downloaded_file = os.path.join(download_path, filename) 
        markdown_file = os.path.join(markdown_path, f"{os.path.splitext(filename)[0]}.md")
        
        if not os.path.exists(downloaded_file):
            download_pdf(link, downloaded_file)
            
        if filename not in pdf_dictionary:
            pdf_doct = pdf_document(link, downloaded_file, markdown_file)
            pdf_dictionary[filename] = pdf_doct
            nuevos_docs[filename] = pdf_doct
            
    return nuevos_docs

def buscar_palabras_ratio(chunks_dict, frase_a_buscar, umbral=0.20):
    """
    Busca una frase de forma proximal comparando contra las palabras individuales 
    y sub-frases dentro de cada bloque, devolviendo el porcentaje real más alto.
    """
    resultados = []
    frase_a_buscar = frase_a_buscar.lower().strip()
    palabras_busqueda = frase_a_buscar.split()
    n_palabras = len(palabras_busqueda)
    
    if not frase_a_buscar:
        return resultados

    for chunk, archivos in chunks_dict.items():
        chunk_lower = chunk.lower()
        palabras_chunk = chunk_lower.split()
        
        # Encontramos el mejor ratio comparando sub-fragmentos del bloque
        mejor_ratio = 0.0
        
        if n_palabras == 1:
            for palabra in palabras_chunk:
                # Si la palabra contiene exactamente la subcadena (ej. "univer" en "universidad")
                if frase_a_buscar in palabra:
                    # Escalamos el ratio basándonos en qué tan parecidas son las longitudes
                    ratio = len(frase_a_buscar) / len(palabra)
                else:
                    ratio = Levenshtein.ratio(palabra, frase_a_buscar)
                if ratio > mejor_ratio:
                    mejor_ratio = ratio
        else:
            # Si es una frase larga, barremos el bloque en sub-frases del mismo tamaño
            for i in range(len(palabras_chunk) - n_palabras + 1):
                sub_frase = " ".join(palabras_chunk[i:i+n_palabras])
                ratio = Levenshtein.ratio(sub_frase, frase_a_buscar)
                if ratio > mejor_ratio:
                    mejor_ratio = ratio

        if mejor_ratio >= umbral:
            # Redondeamos a 3 dígitos decimales para el porcentaje exacto
            resultados.append((chunk, archivos, round(mejor_ratio, 3)))
            
    # ORDENAR: Ponemos primero los que tengan el ratio MÁS ALTO (1.0 a 0.0)
    resultados.sort(key=lambda x: x[2], reverse=True)
    return resultados