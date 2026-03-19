import concurrent.futures
import time
import math
import random

INF = float('inf')

def broadcast(A, X, n, executor):
    tiempoInicial = time.perf_counter()
    A[1] = X
    k = int(math.log2(n))

    for i in range(1, k + 1):
        inicio = 2 ** (i - 1) + 1
        fin = 2 ** i
        paso = 2 ** (i - 1)

        def tarea_broadcast(j, p):
            return j, A[j - p]

        futuros = [executor.submit(tarea_broadcast, j, paso) for j in range(inicio, fin + 1) if j <= n]
        
        for f in concurrent.futures.as_completed(futuros):
            idx, val = f.result()
            A[idx] = val

    tiempoTotal = time.perf_counter() - tiempoInicial
    print(f"Tiempo del método Broadcast: {tiempoTotal:.6f} segundos")

def minimo(L, n, executor):
    tiempoInicial = time.perf_counter()
    rondas = int(math.log2(n))

    for j in range(1, rondas + 1):
        cantidadPares = n // (2 ** j)
        
        def tareaMinimo(i):
            izq = 2 * i - 1
            der = 2 * i
            return i, (L[der] if L[izq] > L[der] else L[izq])

        futuros = [executor.submit(tareaMinimo, i) for i in range(1, cantidadPares + 1)]
        
        for f in concurrent.futures.as_completed(futuros):
            idx, valor = f.result()
            L[idx] = valor

    tiempoTotal = time.perf_counter() - tiempoInicial
    print(f"Tiempo del método mínimo: {tiempoTotal:.6f} segundos")
    return L[1]

def busquedaEREW(L, X, n):
    tiempoInicial = time.perf_counter()
    Temp = [0] * (n + 1)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        broadcast(Temp, X, n, executor)

        def tareaComparacion(i):
            if L[i] == Temp[i]:
                return i, i
            else:
                return i, INF

        futuros = [executor.submit(tareaComparacion, i) for i in range(1, n + 1)]
        
        for f in concurrent.futures.as_completed(futuros):
            idx, val = f.result()
            Temp[idx] = val

        resultado = minimo(Temp, n, executor)

    tiempoTotal = time.perf_counter() - tiempoInicial
    print(f"Tiempo del método BusquedaEREW: {tiempoTotal:.6f} segundos")
    return resultado

if __name__ == "__main__":
    n = 32             
    valores = random.sample(range(1, 100), n)
    lista = [0] + valores    

    print("BÚSQUEDA EREW EN MODELO DE PARALELISMO (ThreadPoolExecutor)")
    print(f"  {lista[1:]}")

    try:
        X = int(input("\n¿Qué número querés buscar? "))
    except ValueError:
        print("Entrada no válida. Usando un número aleatorio de la lista.")
        X = random.choice(valores)
        print(f"Buscando: {X}")
    
    resultado = busquedaEREW(lista, X, n)

    if resultado == INF:
        print(f"\nEl elemento {X} NO fue encontrado en la lista.")
    else:
        print(f"\nEl elemento {X} fue encontrado en la posición {int(resultado)} (índice 1-based).")
