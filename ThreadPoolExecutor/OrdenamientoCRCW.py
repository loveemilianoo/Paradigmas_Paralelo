import random
import concurrent.futures
import threading
import time

lock = threading.Lock()

def comparador (L, hiloI, hiloJ):
    idxI = hiloI - 1
    idxJ = hiloJ - 1

    valorI = L [idxI]
    valorJ = L [idxJ]

    if valorI > valorJ:
        perdedor = hiloI
    else:
        perdedor = hiloJ
    idxPerdedor = perdedor - 1

    with lock:
        print(f"[Hilo P{hiloI:02d}-P{hiloJ:02d}] Fase 2 | L[{idxI:02d}]={valorI:02d} vs L[{idxJ:02d}]={valorJ:02d} -> Pierde P{perdedor:02d}")
    return idxPerdedor

def trabajador (L, win, hiloI):
    idxOrigen = hiloI - 1

    valor = L [idxOrigen]
    rango = win [idxOrigen]

    with lock:
        print(f"[Hilo P{hiloI:02d}] Fase 3 | Valor {valor:02d} tiene rango {rango:02d} -> Se mueve al índice {rango:02d}")
    return rango, valor

def Ordenamiento (L):
    n = len(L)
    win = [0] * n
    L_ordenado = [None] * n

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuros = []
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                futuro = executor.submit(comparador, L, i, j)
                futuros.append(futuro)
        
        for futuro in concurrent.futures.as_completed(futuros):
            idx_perdedor = futuro.result()
            win[idx_perdedor] += 1

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuros = []
        for i in range(1, n + 1):
            futuro = executor.submit(trabajador, L, win, i)
            futuros.append(futuro)
            
        for futuro in concurrent.futures.as_completed(futuros):
            rango_final, valor = futuro.result()
            L_ordenado[rango_final] = valor

    return L_ordenado

if __name__ == "__main__":
    n = 32
    L = random.sample(range(1, 101), n)
    
    print(f"Lista original ({n} elementos):\n{L}\n")
    
    print("--- Iniciando Ordenamiento CRCW ---")
    tiempoIn = time.perf_counter()
    L_ordenada = Ordenamiento(L)
    
    print("\n--- Finalizado ---")
    print(f"Lista ordenada:\n{L_ordenada}")
    print(f"\nTiempo de ejecución: {(tiempoIn - time.perf_counter()):.6f} segundos")