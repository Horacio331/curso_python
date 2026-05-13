""" PDF functions for searching and processing PDF files from a webpage. """
import warnings
# SE AGREGÓ: Ignorar advertencias de obsolescencia de EasyOCR para una salida limpia
warnings.filterwarnings("ignore", category=DeprecationWarning)

from markitdown import MarkItDown
import requests
from bs4 import BeautifulSoup
import os 
# SE AGREGÓ: Importaciones para el manejo de URLs, imágenes y OCR
from urllib.parse import urljoin 
from pdf2image import convert_from_path
import numpy as np
import easyocr

# SE AGREGÓ: Configuración de ruta para el motor de Poppler (indispensable en Windows)
POPPLER_PATH = r"C:\Users\Usuario\poppler_windows\poppler-26.02.0\Library\bin"

# SE AGREGÓ: Inicialización del lector OCR (se hace afuera para que no sea lento)
reader = easyocr.Reader(['es'], gpu=False)

def get_webpage(url):
    """ Fetches the content of a webpage given its URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the request was successful
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
            # SE CAMBIÓ: Ahora usa urljoin para asegurar que los links sean descargables
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

def get_pdfs(url = "https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/"):
    """ Main function to orchestrate the PDF downloading process."""
    download_path = "downloaded_pdfs"
    if not os.path.exists(download_path):
        os.makedirs(download_path, exist_ok=True)
        
    html = get_webpage(url)
    if not html:
        print(f"Failed to fetch the webpage: {url}")
        exit(1)

    # SE CAMBIÓ: Se pasa la 'url' para completar las direcciones de los archivos
    pdf_links = extract_pdf_links(html, url)
    for link in pdf_links:
        filename = link.split('/')[-1]
        downloaded_file = os.path.join(download_path, filename) 
        
        # SE AGREGÓ: Verificación para no descargar archivos que ya existen
        if not os.path.exists(downloaded_file):
            download_pdf(link, downloaded_file)
            print(f"Downloaded: {downloaded_file}")
        else:
            print(f"Already exists: {filename}")

def convert_pdf_to_markdown(pdf_path, markdown_path, converter):
    """ Converts a PDF file to Markdown format using MarkItDown + Manual OCR backup."""
    try:
        # Intentamos conversión normal de texto
        result = converter.convert(pdf_path)
        markdown_content = result.markdown or result.text_content or ""
        
        # SE AGREGÓ: Lógica de respaldo si el PDF es una imagen (OCR)
        if len(markdown_content.strip()) < 50:
            print(f"   [!] Detectada posible imagen. Iniciando OCR para: {os.path.basename(pdf_path)}")
            try:
                # Convertimos PDF a imágenes usando Poppler
                images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
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

        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    except Exception as e:
        print(f"Error converting PDF to Markdown: {e}")

def main():
    """ Main function to orchestrate the PDF downloading and conversion process."""
    # Descomenta la siguiente línea si quieres descargar los PDFs primero
    get_pdfs()
    
    if not os.path.exists("markdown_files"):
        os.makedirs("markdown_files", exist_ok=True)
    
    # SE AGREGÓ: El convertidor se crea aquí para reutilizarlo y ganar velocidad
    converter = MarkItDown()
    
    for filename in os.listdir("downloaded_pdfs"):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join("downloaded_pdfs", filename)
            markdown_path = os.path.join("markdown_files", f"{os.path.splitext(filename)[0]}.md")
            
            # SE CAMBIÓ: Se agregó el parámetro 'converter' a la función
            convert_pdf_to_markdown(pdf_path, markdown_path, converter)
            print(f"Converted {pdf_path} to {markdown_path}")

if __name__ == "__main__":
    main()