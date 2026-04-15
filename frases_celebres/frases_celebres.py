""" frases_celebres.py : Archivo con las funciones básicas para manipular las frases celebres de películas """
import csv
import json 
import Levenshtein
    
class Frase:
    def __init__(self, frase, pelicula):
        self.frase = frase
        self.pelicula = pelicula

    def __str__(self):
        """ Devuelve la frase en formato string """
        return f"{self.frase} - {self.pelicula}"
    
    def to_dict(self):
        """ Devuelve la frase en formato diccionario """
        return {"frase": self.frase, "pelicula": self.pelicula}

    def to_json(self):
        """ Devuelve la frase en formato json """
        return json.dumps(self.to_dict())

def carga_archivo_csv(nombre_archivo):
    """ Carga las frases desde un archivo csv """
    frases = []
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            next(lector)
            for linea in lector:
                if len(linea) == 2:
                    frases.append(Frase(linea[0], linea[1]))
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no se encontro")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
    return frases   

def crea_diccionario_titulos(lista_frases:list) -> dict:
    """ Crea un diccionario con los titulos de las peliculas como claves y las frases como valores """
    stopwords_español = ["el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "al", "a", "y", "o", "pero", "si", "no", "es", "son", "en", "por", "para", "con", "sin", "sobre", "entre", "hacia", "desde", "hasta", "que", "quien", "cuyo", "cuya", "cuyos", "cuyas", "cual", "cuales", "cuanto", "cuanta", "cuantos", "cuantas", "como", "cuando", "donde", "mientras", "aunque", "siempre", "nunca", "aqui", "alli", "alla"]
    diccionario_titulos = {}
    for frase in lista_frases:
        #Frase completa
        if frase.pelicula in diccionario_titulos:
            diccionario_titulos[frase.pelicula].append(frase)
        else:
            diccionario_titulos[frase.pelicula] = [frase]
        #Palabras
        palabras = frase.frase.split()
        for palabra in palabras:
            if palabra in diccionario_titulos:
                diccionario_titulos[palabra].append(frase)
            else:
                diccionario_titulos[palabra] = [frase]
        # removemos stopwords
        palabras_sin_stopwords = [palabra for palabra in palabras if palabra not in stopwords_español]  
        # dos palabras
        for i in range(len(palabras_sin_stopwords) - 1):
            dos_palabras = palabras_sin_stopwords[i] + " " + palabras_sin_stopwords[i+1]
            if dos_palabras in diccionario_titulos:
                diccionario_titulos[dos_palabras].append(frase)
            else:
                diccionario_titulos[dos_palabras] = [frase]
        # tres palabras
        for i in range(len(palabras_sin_stopwords) - 2):
            tres_palabras = palabras_sin_stopwords[i] + " " + palabras_sin_stopwords[i+1] + " " + palabras_sin_stopwords[i+2]
            if tres_palabras in diccionario_titulos:
                diccionario_titulos[tres_palabras].append(frase)
            else:
                diccionario_titulos[tres_palabras] = [frase]
    return diccionario_titulos
    


def buscar_palabras(frases:list, frase_a_buscar:str)->list:
    """ Busca una frase en una lista de frases """
    frases_encontradas = []
    frase_a_buscar = frase_a_buscar.lower()
    for frase in frases:
        frase_lower = frase.frase.lower()
        ratio = Levenshtein.ratio(frase_lower, frase_a_buscar)
        if ratio >=0.50:
            frase.ratio = ratio
            frases_encontradas.append(frase)
    return frases_encontradas

if __name__ == "__main__":
    frases = carga_archivo_csv("frases_consolidadas.csv")
    #for frase in frases[0:5]:
    #    print(frase)
    diccionario_titulos = crea_diccionario_titulos(frases)
    lista_frase_amor = diccionario_titulos["distancia tiempo"]
    for frase in lista_frase_amor:
        print(frase)
    print("############ Levensthein ############")
    lista_frase_amor = buscar_palabras(frases, "Las palabras nos pueden hacer infinitamente ")
    for frase in lista_frase_amor:
        print(frase, frase.ratio)
    