""" programa para hacer operaciones aritmeticas basicas """

import os
"""limpiar terminal cada vez que se ejecute el programa"""

os.system("cls" if os.name == "nt" else "clear")

"""
def sumar(a, b):
    suma = a + b
    return suma

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b == 0:
        return "Error: División por cero"
    return a / b

print(f"sumar 5 + 3 = {sumar.suma(5,3)}")
"""
frutas = ["Manzana", "Pera", "Piña"]
# len(frutas) es 3, por lo tanto range(3) nos da 0, 1 y 2
for i in range(len(frutas)):
    print(f"En el cajón {i} hay una {frutas[i]}")
"""
def tabla_de_multiplicar(n):
    for i in range(1, 11):
        print(f"{n} x {i} = {n * i}")

print("Tabla de multiplicar del 5:")
tabla_de_multiplicar(6)
"""