import threading
import math
import time

def suma (arreglo):
    print("Suma Secuencial EREW")
    datos = arreglo.copy()
    n = len(datos)
    pasos = math.ceil(math.log2(n))

    inicio = time.perf_counter()

    for paso in range(pasos):
        stride = 2 ** paso
        for i in range (0,n,stride *2):
            if i + stride < n:
                datos[i] = datos[i] + datos [i+stride]
        print (f"Paso {paso+1}: {datos}")

    fin = time.perf_counter()

    print(f"Resultado: {datos[0]}")
    print(f"Tiempo: {(fin-inicio): .6f} segundos")
    return datos[0]

if __name__ == "__main__":
    arreglo = [3, 1, 4, 1, 5, 9, 2, 6, 7, 3, 8, 4, 2, 7, 1, 9, 6, 5, 3, 8, 4, 2, 7, 1, 9, 6, 5, 3, 8, 4, 2, 7]
    print(f"Arreglo ({len(arreglo)} elementos): {arreglo}")
    print(f"Suma esperada: {sum(arreglo)}")

    r1 = suma(arreglo)

