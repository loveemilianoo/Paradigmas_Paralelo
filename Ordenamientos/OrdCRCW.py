import random
import threading
import time

lock = threading.Lock()

def comparador(L, win, hiloI, hiloJ):
    idxI = hiloI - 1
    idxJ = hiloJ - 1

    valorI = L[idxI]
    valorJ = L[idxJ]

    if valorI > valorJ:
        perdedor = hiloI
    else:
        perdedor = hiloJ
    idxPerdedor = perdedor - 1

    with lock:
        win[idxPerdedor] += 1
        print(f"[Hilo P{hiloI:02d}-P{hiloJ:02d}] Fase 2 | L[{idxI:02d}]={valorI:02d} vs L[{idxJ:02d}]={valorJ:02d} -> Pierde P{perdedor:02d}")

def trabajador(L, win, L_ordenado, hiloI):
    idxOrigen = hiloI - 1

    valor = L[idxOrigen]
    rango = win[idxOrigen]

    with lock:
        L_ordenado[rango] = valor
        print(f"[Hilo P{hiloI:02d}] Fase 3 | Valor {valor:02d} tiene rango {rango:02d} -> Se mueve al índice {rango:02d}")

def Ordenamiento(L):
    n = len(L)
    win = [0] * n
    L_ordenado = [None] * n

    # --- Fase 2: Comparaciones ---
    hilos_comp = []
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            t = threading.Thread(target=comparador, args=(L, win, i, j))
            hilos_comp.append(t)
            t.start()
    
    for t in hilos_comp:
        t.join()

    # --- Fase 3: Movimiento ---
    hilos_trab = []
    for i in range(1, n + 1):
        t = threading.Thread(target=trabajador, args=(L, win, L_ordenado, i))
        hilos_trab.append(t)
        t.start()
            
    for t in hilos_trab:
        t.join()

    return L_ordenado

if __name__ == "__main__":
    n = 32
    L = random.sample(range(1, 101), n)
    
    print(f"Lista original ({n} elementos):\n{L}\n")
    
    print("--- Iniciando Ordenamiento CRCW con hilos ---")
    tiempoIn = time.perf_counter()
    
    L_ordenada = Ordenamiento(L)
    
    tiempo_final = time.perf_counter()
    print("\n--- Finalizado ---")
    print(f"Lista ordenada:\n{L_ordenada}")
    print(f"\nTiempo de ejecución: {(tiempo_final - tiempoIn):.6f} segundos")
