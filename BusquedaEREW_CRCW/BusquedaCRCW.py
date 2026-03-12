import threading
import time
import random

def minCRCW (L, n):
    win = [0] * n
    hilos = []

    def inicializar(idx):
        win[idx] =0

    for i in range(n):
        t = threading.Thread(target=inicializar, args=(i,))
        hilos.append(t)
        t.start()
    for t in hilos:
        t.join()

    hilosComp = []
    def compararElementos (i,j):
        if L[i] > L[j]:
            win[i] = 1
        elif L[i] < L[j]:
            win[j] = 1

    for i in range(n):
        for j in range (i+1, n):
            t = threading.Thread(target= compararElementos, args=(i,j))
            hilosComp.append(t)
            t.start()
    for t in hilosComp:
        t.join()

    minimoIDX = -1
    for i in range(n):
        if win[i] == 0:
            minimoIDX = i
            break

    return L[minimoIDX] if minimoIDX != -1 else None

if __name__ == "__main__":
    n = 32
    arreglo = random.sample(range(1, 100), n)

    print("Minimo en modelo CRCW")
    print(f"\nLista L[0..{n-1}]: {arreglo}\n")

    tiempoInicial = time.perf_counter()
    resultado = minCRCW(arreglo, n)
    tiempoTotal = time.perf_counter() - tiempoInicial

    print(f"El minimo es: {resultado}")
    print(f"\nTiempo de ejecución: {tiempoTotal:.6f} segundos") 
