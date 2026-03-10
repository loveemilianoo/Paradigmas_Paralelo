import threading
import math
import random
import time

resultadosGen = {}

def average(arreglo):
    resultado = 0
    tamaño = len(arreglo)
    for i in range (tamaño):
        resultado += arreglo[i]
    resultado = resultado / tamaño
    resultadosGen["Promedio"] = resultado

def minimum (arreglo):
    tamaño = len(arreglo)
    min = arreglo[0]
    for i in range (tamaño):
        if (arreglo[i] < min):
            min = arreglo [i]
    resultadosGen["Minimo"] = min

def binary_or(arreglo):
    resultado = 0
    for num in arreglo:
        resultado |= num
    resultadosGen["OR Binario"] = resultado

def geoMean(arreglo):
    tamaño = len(arreglo)
    radicando = 1
    for i in range (tamaño):
        radicando *= arreglo[i]
    resultado = math.pow(radicando, 1/tamaño)
    resultadosGen["Media Geometrica"] = resultado

def crearHilos(arreglo):
    threads = [
        threading.Thread(target=average, args= (arreglo,)),
        threading.Thread(target=minimum, args= (arreglo,)),
        threading.Thread(target=binary_or, args= (arreglo,)),
        threading.Thread(target=geoMean, args= (arreglo,)),
    ]

    for i in threads:
        i.start()
    for i in threads:
        i.join()

    print("\n--- Resultados ---")
    print(f"Promedio:          {resultadosGen['Promedio']}")
    print(f"Minimo:            {resultadosGen['Minimo']}")
    print(f"OR Binario:        {resultadosGen['OR Binario']}")
    print(f"Media Geometrica:  {resultadosGen['Media Geometrica']:.4f}")


if __name__ == "__main__":
    arreglo = []
    for i in range(32):
        numeroRandom = random.randint(1,1000)
        arreglo.append(numeroRandom)
    print(f"Arreglo generado {arreglo}")
    
    inicio = time.perf_counter()
    crearHilos(arreglo)
    fin = time.perf_counter()

    print(f"\nTiempo de ejecucion: {fin - inicio:.6f} segundos")