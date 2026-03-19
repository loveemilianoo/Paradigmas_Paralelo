import threading
import time
import random

lock = threading.Lock()

def intervalo(L, odd, even, idx):
    L[2*idx] = odd[idx]
    L[2*idx + 1] = even[idx]

def comparador(L, i, nivel):
    idxIzq = 2*i - 1
    idxDer = 2*i

    if L[idxIzq] > L[idxDer]:
        L[idxIzq], L[idxDer] = L[idxDer], L[idxIzq]
        with lock: 
            print(f"[Hilo P{2*i:02d}-P{2*i+1:02d}] Fase 2 | L[{idxIzq:02d}]={L[idxIzq]:02d} vs L[{idxDer:02d}]={L[idxDer]:02d} -> Intercambia")

def oddEvenMerge(L, nivel=1):
    n = len(L)

    if n == 2:
        if L[0] > L[1]:
            L[0], L[1] = L[1], L[0]
            with lock: 
                print(f"[Hilo P02-P03] Fase 2 | L[00]={L[0]:02d} vs L[01]={L[1]:02d} -> Intercambia")
        return
    
    odd = L[0::2]
    even = L[1::2]

    t1 = threading.Thread(target=oddEvenMerge, args=(odd, nivel+1))
    t2 = threading.Thread(target=oddEvenMerge, args=(even, nivel+1))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    hilos_int = []
    for i in range(n // 2):
        t = threading.Thread(target=intervalo, args=(L, odd, even, i))
        hilos_int.append(t)
        t.start()
    for t in hilos_int:
        t.join()
        
    hilos_comp = []
    for i in range(1, n // 2):
        t = threading.Thread(target=comparador, args=(L, i, nivel))
        hilos_comp.append(t)
        t.start()
    for t in hilos_comp:
        t.join()

def oddEvenSort(L, nivel=1):
    n = len(L)
    if n <= 1:
        return
    
    mitad = n // 2
    izq = L[:mitad]
    der = L[mitad:]

    with lock:
        print(f"Sort N{nivel} Dividiendo arreglo de tamaño {n}")

    t1 = threading.Thread(target=oddEvenSort, args=(izq, nivel+1))
    t2 = threading.Thread(target=oddEvenSort, args=(der, nivel+1))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    for i in range(mitad):
        L[i] = izq[i]
        L[i+mitad] = der[i]
    
    with lock:
        print(f"Sort N{nivel} Fusionando arreglo de tamaño {n}")

    oddEvenMerge(L, nivel)

if __name__ == "__main__":
    n = 32
    arreglo = [random.randint(1, 100) for _ in range(n)]
    
    print(f"Arreglo original ({n} elementos):\n{arreglo}\n")
    
    print("--- Iniciando Ordenamiento Batcher Odd-Even Merge Sort (EREW) con hilos ---")
    t_inicio = time.perf_counter()
    oddEvenSort(arreglo)
    t_fin = time.perf_counter()
    
    print("\n--- Ordenamiento Finalizado ---")
    print(f"Arreglo ordenado:\n{arreglo}")
    print(f"\nTiempo total de ejecución: {t_fin - t_inicio:.6f} segundos")