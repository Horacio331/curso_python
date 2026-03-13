"""Realizar un programa en Python que lea los archivos anexos (clases.csv y zoo.csv) y permita listar animales por dos condiciones:
Por su clasificación o clase
Por alguna de sus características
El programa deberá contar con un menú que permita seleccionar el listado por clase o listar por alguna característica. Si tiene tiempo, debe escribir un módulo que permita 
agregar un nuevo animal o varios animales al listado. Al salir, se deberán grabar los cambios realizados, para que al volver a entrar al programa, no sea necesario volver a agregarlos.

Es recomendable que se divida el programa en dos archivos: Un archivo de funciones auxiliares donde se encuentren las funciones que hacen todo el procesamiento y 
otro donde se encuentre la ejecución de la lógica principal, llamando a las funciones. Hay dos archivos csv: clases.csv y zoo.csv, es necesario escribir una sola función que cargue el contenido de un archivo en un diccionario. 
Así la función podrá ser usada para cargar un archivo a la vez en el diccionario de clases y en el diccionario de animales. """


"""Función para agregar un nuevo animal al diccionario del zoológico. Recibe el diccionario del zoológico y un objeto de la clase Animal."""
import os
import csv
class Animal:
    def __init__(self, nombre, clase, habitat, dieta, caracteristicas=None):
        self.nombre = nombre
        self.clase = clase
        self.habitat = habitat
        self.dieta = dieta
        self.caracteristicas = caracteristicas if caracteristicas else []

    def __str__(self):
        return f"{self.nombre} ({self.clase}) - Hábitat: {self.habitat}, Dieta: {self.dieta}"

    def __repr__(self):
        return f"Animal({self.nombre}, {self.clase}, {self.habitat}, {self.dieta}, {self.caracteristicas})"
def cargar_csv_en_diccionario(nombre_archivo, clave):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    diccionario = {}
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            valores = linea.strip().split(",")
            diccionario[valores[0]] = valores[1:]
    return diccionario


def guardar_csv(nombre_archivo, diccionario, campos):
    with open(nombre_archivo, "w", newline='', encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for fila in diccionario.values():
            escritor.writerow(fila)


def listar_por_clase(zoo, clases, clase):
    print(f"\nAnimales de la clase {clase}:")
    for animal, datos in zoo.items():
        if datos["clase"] == clase:
            print(f"- {animal} ({clases[clase]['descripcion']})")


def listar_por_caracteristica(zoo, caracteristica, valor):
    print(f"\nAnimales con {caracteristica} = {valor}:")
    for animal, datos in zoo.items():
        if datos.get(caracteristica) == valor:
            print(f"- {animal}")


def agregar_animal(zoo, nuevo_animal: Animal):
    zoo[nuevo_animal.nombre] = {
        "nombre": nuevo_animal.nombre,
        "clase": nuevo_animal.clase,
        "habitat": nuevo_animal.habitat,
        "dieta": nuevo_animal.dieta,
        "caracteristicas": ",".join(nuevo_animal.caracteristicas)
    }