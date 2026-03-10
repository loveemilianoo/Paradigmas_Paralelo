import math
import threading
import time
import random

def minCRCW (L, win, n):
    for i in range (n):
        win[i] = 0

    lock = threading.Lock()
    
    def comparador(i):
        esMenor = True
        for j in range(n):
            if i != j and L[i] > L[j]:
                esMenor = False
                break
        if not esMenor:
            with lock:
                win[i] = 1

    hilos = []
    for i in range(n):
        t = threading.Thread(target= comparador, args=(i,))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    indexMin = None
    for i in range (n):
        if(win[i] == 0):
            indexMin = i
            break

    print("Indice Minimo: ",indexMin+1)
    print ("RESULTADO: ",L[indexMin])
    return L[indexMin]

if __name__ == "__main__":
    n = 32
    valores = random.sample(range(1, 100), n)
    win = [0] * n

    print("Mínimo en modelo CRCW")
    print(f"\nLista L[0..{n-1}]: {valores}\n")

    tiempoInicial = time.perf_counter()
    resultado = minCRCW(valores, win, n)
    tiempoTotal = time.perf_counter() - tiempoInicial

    print(f"\nTiempo de ejecución: {tiempoTotal:.6f} segundos") 
