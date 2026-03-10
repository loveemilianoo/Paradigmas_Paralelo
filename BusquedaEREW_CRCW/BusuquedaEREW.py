import threading
import time
import math
import random

#Constante
INF = float('inf')

def broadcast (A, X, n):
    tiempoInicial = time.perf_counter()
    A[1]= X
    k = int(math.log2(n))

    for i in range(1,k+1):
        inicio = 2 ** (i-1) +1
        fin = 2 ** i
        paso = 2 ** (i -1)

        def tarea (j,p):
            A[j] = A[j-p]

        hilos = []
        
        for j in range (inicio,fin+1):
            if j<= n:
                t = threading.Thread(target=tarea, args=(j,paso))
                hilos.append(t)
        
        for t in hilos:
            t.start()
        for t in hilos:
            t.join()
    fin = time.perf_counter()
    tiempoTotal = fin - tiempoInicial
    print(f"Tiempo del metodo Broadcast: {(tiempoTotal): .6f} segundos")

def minimo (L, n):
    tiempoInicial = time.perf_counter()
    rondas = int(math.log2(n))

    for j in range (1, rondas+1):
        cantidadPares = n // (2**j)

        hilos = []
        resultados = {}
        lock = threading.Lock()

        def tareaMinimo (i):
            izq = 2* i-1
            der = 2* i
            valor = L[der] if L[izq] > L[der] else L[izq]
            with lock:
                resultados[i] = valor

        for i in range (1, cantidadPares+1):
            t = threading.Thread(target=tareaMinimo, args=(i,))
            hilos.append(t)

        for t in hilos:
            t.start()
        for t in hilos:
            t.join()        
        
        for i, valor in resultados.items():
            L[i] = valor
    fin = time.perf_counter()
    tiempoTotal = fin - tiempoInicial
    print(f"Tiempo del metodo minimo: {(tiempoTotal): .6f} segundos")
    return L[1]
    

def busquedaEREW (L, X, n):
    tiempoInicial = time.perf_counter()
    Temp = [0] * (n+1)
    broadcast(Temp,X,n)

    hilos = []
    lock = threading.Lock()

    def tareaComparacion(i):
        if L[i] == Temp[i]:
            with lock:
                Temp[i] = i
        else:
            with lock:
                Temp[i] = INF

    for i in range (1, n+1):
        t = threading.Thread(target=tareaComparacion, args=(i,))
        hilos.append(t)
    
    for t in hilos:
        t.start()
    for t in hilos:
        t.join() 

    fin = time.perf_counter()
    tiempoTotal = fin - tiempoInicial
    print(f"Tiempo del metodo BusquedaEREW: {(tiempoTotal): .6f} segundos")
    return (minimo(Temp,n))

if __name__ == "__main__":
    n = 32             
    valores = random.sample(range(1, 100), n)
    lista = [0] + valores    

    print("BÚSQUEDA EREW EN MODELO DE PARALELISMO")
    print(f"  {lista[1:]}")

    X = int(input("\n¿Qué número querés buscar? "))
    
    resultado = busquedaEREW(lista, X, n)

    if resultado == INF:
        print(f"\nEl elemento {X} NO fue encontrado en la lista.")
    else:
        print(f"\nEl elemento {X} fue encontrado en la posición {int(resultado)}.")
