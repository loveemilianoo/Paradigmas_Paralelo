import threading
import math
import time
import random

def suma (arreglo):
    print("Suma Secuencial CREW")
    datos = arreglo.copy()
    n = len(datos)
    pasos = math.ceil(math.log2(n))

    inicio = time.perf_counter()

    for paso in range(pasos):
        stride = 2 ** paso
        for i in range(0,n-stride):
            if i % (stride*2) == 0:
                datos[i] = datos[i] + datos[i+stride]
        print(f"Paso {paso+1}: {datos}")

    fin = time.perf_counter()

    print(f"Resultado: {datos[0]}")
    print(f"Tiempo: {(fin-inicio):.6f} segundos")
    return datos[0]

if __name__ == "__main__":
    arreglo = []
    for i in range(32):
        numeroRandom = random.randint(1,1000)
        arreglo.append(numeroRandom)
    print(f"Arreglo ({len(arreglo)} elementos): {arreglo}")
    print(f"Suma esperada: {sum(arreglo)}")

    r1 = suma(arreglo)

    print(f"Secuencial: {r1}")