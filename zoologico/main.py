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
    clases = clases = cargar_csv_en_diccionario("clases.csv", "clase")
    zoo = cargar_csv_en_diccionario("zoo.csv", "nombre")

    while True:
        print("\n--- MENÚ ---")
        print("1. Listar animales por clase")
        print("2. Listar animales por característica")
        print("3. Agregar nuevo animal")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clase = input("Ingrese la clase: ")
            listar_por_clase(zoo, clases, clase)

        elif opcion == "2":
            caracteristica = input("Ingrese la característica: ")
            valor = input("Ingrese el valor: ")
            listar_por_caracteristica(zoo, caracteristica, valor)

        elif opcion == "3":
            nombre = input("Nombre del animal: ")
            clase = input("Clase: ")
            habitat = input("Hábitat: ")
            dieta = input("Dieta: ")
            caracteristicas = input("Características (separadas por coma): ").split(",")

            nuevo_animal = Animal(nombre, clase, habitat, dieta, caracteristicas)
            agregar_animal(zoo, nuevo_animal)
            print(f"{nuevo_animal} agregado correctamente.")

        elif opcion == "4":
            campos = ["nombre", "clase", "habitat", "dieta", "caracteristicas"]
            guardar_csv("zoo.csv", zoo, campos)
            print("Cambios guardados. ¡Hasta luego!")
            break

        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()
