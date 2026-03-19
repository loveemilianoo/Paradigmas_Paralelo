import threading
import time
import random
import math

def MatMultCRCW(A, B):
    n = len(A)
    C = [[[0.0] * (n+1) for _ in range(n+1)] for _ in range(n+1)]

    def paso1(i,j,k):
        C [i][j][k] = A[i-1][k-1] * B[j-1][k-1]

    hilos = []
    for i in range(1, n+1):
        for j in range(1, n+1):
            for k in range(1, n+1):
                t = threading.Thread(target=paso1, args=(i,j,k))
                hilos.append(t)
                t.start()
    for t in hilos:
        t.join()

    pasosLog = int(math.log2(n))

    for L in range (1, pasosLog +1):
        lock = threading.Lock()
        hilos = []

        def paso2 (i,j,k, L=L):
            dosK = 2*k
            potenciaL = 2 ** L
            potenciaLmenos1 = 2 ** (L-1)
            if (dosK % potenciaL) == 0:
                C[i][j][dosK] = C[i][j][dosK] + C[i][j][dosK - potenciaLmenos1]

        nMitad = n // 2
        for i in range (1, n+1):
            for j in range (1, n+1):
                for k in range (1, nMitad +1):
                    t = threading.Thread(target=paso2, args= (i,j,k))
                    hilos.append(t)
                    t.start()
        for t in hilos:
            t.join()

    resultado = [[ C[i][j][n] for j in range(1 ,n+1)] for i in range(1, n+1)]
    return resultado

def imprimir_matriz(nombre, M):
    print(f"\n{nombre}:")
    for fila in M:
        print("  " + "  ".join(f"{v:8.2f}" for v in fila))

if __name__ == "__main__":
    n = 4
    A = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
 
    imprimir_matriz("Matriz A", A)
    imprimir_matriz("Matriz B", B)
 
    print("\n--- Ejecutando MatMultCREW con hilos ---")
    t0 = time.time()
    MatMultCRCW(A, B)
    t1 = time.time()
    imprimir_matriz("Resultado de las matrices" ,MatMultCRCW(A,B))

    print(f"  Tiempo CREW: {t1 - t0:.4f}s")