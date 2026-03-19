import concurrent.futures
import threading
import time
import random

lock = threading.Lock()

def intervalo (L, odd, even, idx):
    L[2*idx] = odd[idx]
    L[2*idx + 1] = even[idx]

def comparador (L, i, nivel):
    idxIzq = 2*i - 1
    idxDer = 2*i

    if L[idxIzq] > L[idxDer]:
        L[idxIzq] , L[idxDer] = L[idxDer] , L[idxIzq]
        with lock: 
            print(f"[Hilo P{2*i:02d}-P{2*i+1:02d}] Fase 2 | L[{idxIzq:02d}]={L[idxIzq]:02d} vs L[{idxDer:02d}]={L[idxDer]:02d} -> Intercambia")

def oddEvenMerge (L, nivel=1):
    n = len(L)

    if n == 2:
        if L[0] > L[1]:
            L[0] , L[1] = L[1] , L[0]
            with lock: 
                print(f"[Hilo P{2*1:02d}-P{2*1+1:02d}] Fase 2 | L[{0:02d}]={L[0]:02d} vs L[{1:02d}]={L[1]:02d} -> Intercambia")
        return
    
    odd = L[0::2]
    even = L[1::2]

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(oddEvenMerge, odd, nivel+1)
        f2 = executor.submit(oddEvenMerge, even, nivel+1)
        concurrent.futures.wait([f1, f2])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        intervaloFuturos = [executor.submit(intervalo, L, odd, even, i) for i in range(n//2)]
        concurrent.futures.wait(intervaloFuturos)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futurosCE = [executor.submit(comparador, L, i, nivel) for i in range(1, n//2)]
        concurrent.futures.wait(futurosCE)

def oddEvenSort (L, nivel=1):
    n = len(L)
    if n <= 1:
        return
    
    mitad = n // 2
    izq = L [:mitad]
    der = L [mitad:]

    with lock:
        print(f"Sort N{nivel} Dividiendo arreglo de tamaño {n}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(oddEvenSort, izq, nivel+1)
        f2 = executor.submit(oddEvenSort, der, nivel+1)
        concurrent.futures.wait([f1, f2])

    for i in range (mitad):
        L[i] = izq[i]
        L[i+mitad] = der[i]
    
    with lock:
        print(f"Sort N{nivel} Fusionando arreglo de tamaño {n}")

    oddEvenMerge(L, nivel)

if __name__ == "__main__":
    n = 32
    arreglo = [random.randint(1, 100) for _ in range(n)]
    
    print(f"Arreglo original ({n} elementos):\n{arreglo}\n")
    
    print("--- Iniciando Ordenamiento Batcher Odd-Even Merge Sort (EREW) ---")
    t_inicio = time.perf_counter()
    oddEvenSort(arreglo)
    t_fin = time.perf_counter()
    
    print("\n--- Ordenamiento Finalizado ---")
    print(f"Arreglo ordenado:\n{arreglo}")
    print(f"\nTiempo total de ejecución: {t_fin - t_inicio:.6f} segundos")
