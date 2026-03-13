"""Este programa es un sistema de gestión para un zoológico. 
Permite cargar datos de animales y clases desde archivos CSV, 
listar animales por clase o por características específicas, y 
agregar nuevos animales al sistema. Al finalizar, guarda los cambios 
realizados en el archivo CSV correspondiente. La función menu() es el
 punto de entrada del programa, que muestra un menú interactivo para el usuario."""

from Funciones import (
    cargar_csv_en_diccionario,
    guardar_csv,
    listar_por_clase,
    listar_por_caracteristica,
    agregar_animal,
    Animal
)

def menu():
    clases = cargar_csv_en_diccionario("clases.csv", "nombre")
    zoo = cargar_csv_en_diccionario("zoo.csv", "nombre")

    while True:
        print("\nMenú:")
        print("1. Listar animales por clase")
        print("2. Listar animales por característica")
        print("3. Agregar nuevo animal")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        