""" PDF functions for searching and processing PDF files from a webpage. """
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

# Ignorar advertencias de obsolescencia de EasyOCR para una salida limpia
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Configuración de ruta para el motor de Poppler (indispensable en Windows)
POPPLER_PATH = r"C:\Users\Usuario\poppler_windows\poppler-26.02.0\Library\bin"

# Inicialización del lector OCR y MarkItDown (afuera para reutilizarlos de forma eficiente)
print("[*] Inicializando motores de OCR y Conversión...")
reader = easyocr.Reader(['es'], gpu=False)
converter = MarkItDown()

class pdf_document:
    """ Class to represent a PDF document with its URL, pdf path and markdown path filename."""
    def __init__(self, url, pdf_path, markdown_path):
        self.url = url
        self.pdf_path = pdf_path
        self.markdown_path = markdown_path
        self.content = ""  # Se almacena el contenido del PDF convertido
        
        # Ejecutamos la conversión automáticamente al crear el objeto
        self.convert_pdf_to_markdown()
        
    def convert_pdf_to_markdown(self):
        """ Converts a PDF file to Markdown format using MarkItDown + Manual OCR backup."""
        try:
            # Intentamos conversión normal de texto usando la instancia global
            result = converter.convert(self.pdf_path)
            markdown_content = result.markdown or result.text_content or ""
            
            # Lógica de respaldo si el PDF es una imagen (OCR)
            if len(markdown_content.strip()) < 50:
                print(f"   [!] Detectada posible imagen o PDF vacío. Iniciando OCR para: {os.path.basename(self.pdf_path)}")
                try:
                    # Convertimos PDF a imágenes usando Poppler
                    images = convert_from_path(self.pdf_path, poppler_path=POPPLER_PATH)
                    ocr_text = ""
                    for i, image in enumerate(images):
                        img_np = np.array(image)
                        # Extraemos el texto página por página
                        results = reader.readtext(img_np, detail=0)
                        ocr_text += f"\n\n### Página {i+1}\n" + " ".join(results)
                    markdown_content = ocr_text
                except Exception as e_ocr:
                    print(f"   [Error OCR]: {e_ocr}")
                    markdown_content = f"Error: No se pudo procesar OCR. Revisar Poppler. {e_ocr}"

            # Guardamos en el atributo de clase
            self.content = markdown_content
            
            # Escribimos el archivo de respaldo físico .md
            with open(self.markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
                
        except Exception as e:
            print(f"Error converting PDF to Markdown ({self.pdf_path}): {e}")


def get_webpage(url):
    """ Fetches the content of a webpage given its URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None 
    

def extract_pdf_links(html, base_url):
    """ Parses the HTML content and extracts all PDF links."""
    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            full_url = urljoin(base_url, href)
            pdf_links.append(full_url)
    return pdf_links


def download_pdf(url, filename):
    """ Downloads a PDF file from a given URL and saves it with a specified filename."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the PDF: {e}")


def get_pdfs(url="https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/"):
    """ Orchestrates downloading and instantiating PDF objects. """
    download_path = "downloaded_pdfs"
    markdown_path = "markdown_files"
    
    if not os.path.exists(download_path):
        os.makedirs(download_path, exist_ok=True)
    if not os.path.exists(markdown_path):
        os.makedirs(markdown_path, exist_ok=True)
        
    html = get_webpage(url)
    if not html:
        print(f"Failed to fetch the webpage: {url}")
        return {}

    pdf_links = extract_pdf_links(html, url)
    pdf_dict = {}  # Almacenará pares -> { nombre_archivo: objeto_pdf_document }
    
    for link in pdf_links:
        filename = link.split('/')[-1]
        downloaded_file = os.path.join(download_path, filename) 
        markdown_file = os.path.join(markdown_path, f"{os.path.splitext(filename)[0]}.md")
        
        # 1. Asegurar descarga del archivo
        if not os.path.exists(downloaded_file):
            print(f"Descargando: {filename}...")
            download_pdf(link, downloaded_file)
        else:
            print(f"El archivo ya existe localmente: {filename}")
            
        # 2. Instanciar el objeto (ejecuta el OCR/Conversión internamente)
        print(f"Procesando contenido de: {filename}...")
        pdf_doct = pdf_document(link, downloaded_file, markdown_file)
        
        # Guardamos el objeto completo indexado por su nombre de archivo
        pdf_dict[filename] = pdf_doct
        
    return pdf_dict


def buscar_palabras_ratio(chunks_dict: dict, frase_a_buscar: str, umbral: float = 0.50) -> list:
    """
    Busca una frase/palabra aproximada dentro de las llaves (chunks) de nuestro diccionario principal.
    Devuelve una lista de tuplas con (chunk_detectado, lista_de_archivos, ratio_similitud).
    """
    resultados = []
    frase_a_buscar = frase_a_buscar.lower().strip()
    
    for chunk, archivos in chunks_dict.items():
        chunk_lower = chunk.lower()
        
        # Si la palabra exacta está dentro del bloque, le damos prioridad máxima (ratio 1.0)
        if frase_a_buscar in chunk_lower:
            resultados.append((chunk, archivos, 1.0))
        else:
            # Si no, calculamos la similitud de Levenshtein aproximada
            ratio = Levenshtein.ratio(chunk_lower, frase_a_buscar)
            if ratio >= umbral:
                resultados.append((chunk, archivos, round(ratio, 2)))
                
    # Ordenar resultados por los de mayor similitud (ratio)
    resultados.sort(key=lambda x: x[2], reverse=True)
    return resultados


def main():
    """ Main function to orchestrate the PDF downloading and conversion process."""
    # Descargar y procesar todos los archivos estructurándolos en objetos
    pdf_dictionary = get_pdfs()
    
    if not pdf_dictionary:
        print("No se encontraron PDFs o no se pudo acceder al sitio.")
        return

    print(f"\n Documentos cargados con éxito: {list(pdf_dictionary.keys())}\n")
    
    # Construcción del diccionario invertido (Chunk de palabras -> lista de PDFs que lo contienen)
    main_dictionary = {}
    chunk_length = 20  # Bloques de 20 palabras
    
    for filename, pdf_doct in pdf_dictionary.items():
        content = pdf_doct.content or ""
        # Dividimos por espacios para obtener una lista de palabras limpias
        words = content.split()
        
        # Agrupamos las palabras de 20 en 20
        for i in range(0, len(words), chunk_length):
            chunk_words = words[i:i+chunk_length]
            chunk_text = " ".join(chunk_words)
            
            if chunk_text not in main_dictionary:
                main_dictionary[chunk_text] = [filename]
            else:
                # Evitar duplicar el mismo archivo en el mismo chunk
                if filename not in main_dictionary[chunk_text]:
                    main_dictionary[chunk_text].append(filename)
                    
    # --- Interfaz de búsqueda interactiva ---
    print("="*50)
    print(" SISTEMA DE BÚSQUEDA PROXIMAL DE TEXTO ")
    print("="*50)
    
    while True:
        busqueda = input("\nIntroduce la palabra o frase a buscar (o escribe 'salir'): ")
        if busqueda.lower() == 'salir':
            break
            
        if not busqueda.strip():
            continue
            
        # Ejecutamos la búsqueda con Levenshtein usando un umbral razonable (ej. 0.45)
        coincidencias = buscar_palabras_ratio(main_dictionary, busqueda, umbral=0.45)
        
        if coincidencias:
            print(f"\n Se encontraron {len(coincidencias)} posibles coincidencias:\n")
            for chunk, archivos, ratio in coincidencias[:5]:  # Mostrar los mejores 5
                print(f"-> [Coincidencia Ratio: {ratio}]")
                print(f"   Bloque de texto: \"... {chunk} ...\"")
                print(f"   Encontrado en: {', '.join(archivos)}")
                print("-" * 40)
        else:
            print(" No se encontraron términos similares en los documentos.")

if __name__ == "__main__":
    main()