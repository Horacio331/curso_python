""" PDF functions for searching and processing PDF files from a webpage. """
import requests
from bs4 import BeautifulSoup
import os

def get_webpage(url):
    """ Fetches the content of a webpage given its url. """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def extract_pdf_links(html):
    """ Parses the html content and extracts all PDF links."""
    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.lower().endswith('.pdf'):
            pdf_links.append(href)
    return pdf_links

def download_pdf(url, filename):
    """ Downloads a PDF file from the given url and saves it with the specified filename. """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
    except requests.request.exceptions.RequestException as e:
        print(f"Error downloading the PDF: {e}")

if __name__ == "__main__":
    url = "https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/"
    html = get_webpage(url)
    if not html:
        print(f"Failed to retrieve the webpage: {url}")
        exit(1)
    pdf_links = extract_pdf_links(html)
    for link in pdf_links:
        print(link)
        filename = link.split('/')[-1]  # Extract the filename from the URL
        download_pdf(link, f"pdf_{filename}")
        print(f"Downloaded: {filename}")