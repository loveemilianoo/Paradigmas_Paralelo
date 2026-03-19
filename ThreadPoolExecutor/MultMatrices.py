import concurrent.futures
import time
import random
import math

def MatMultCRCW_Pool(A, B):
    n = len(A)
    C = [[[0.0] * (n + 1) for _ in range(n + 1)] for _ in range(n + 1)]

    def tarea_paso1(i, j, k):
        return i, j, k, A[i-1][k-1] * B[k-1][j-1]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuros1 = []
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                for k in range(1, n + 1):
                    futuros1.append(executor.submit(tarea_paso1, i, j, k))
        
        for f in concurrent.futures.as_completed(futuros1):
            i, j, k, val = f.result()
            C[i][j][k] = val

        pasosLog = int(math.log2(n))
        for L_paso in range(1, pasosLog + 1):
            futuros2 = []
            potenciaL = 2 ** L_paso
            potenciaLmenos1 = 2 ** (L_paso - 1)
            
            def tarea_paso2(i, j, dosK, pL, pL_1):
                return i, j, dosK, C[i][j][dosK] + C[i][j][dosK - pL_1]

            nMitad = n // 2
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    for k in range(1, nMitad + 1):
                        dosK = 2 * k
                        if (dosK % potenciaL) == 0:
                            futuros2.append(executor.submit(tarea_paso2, i, j, dosK, potenciaL, potenciaLmenos1))
            
            for f in concurrent.futures.as_completed(futuros2):
                i, j, dosK, val_sumado = f.result()
                C[i][j][dosK] = val_sumado

    resultado = [[C[i][j][n] for j in range(1, n + 1)] for i in range(1, n + 1)]
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
 
    print(f"\n--- Ejecutando MatMultCRCW con ThreadPoolExecutor (n={n}) ---")
    t0 = time.perf_counter()
    resultado_pool = MatMultCRCW_Pool(A, B)
    t1 = time.perf_counter()
    
    imprimir_matriz("Resultado (C = A x B)", resultado_pool)
    print(f"\nTiempo de ejecución: {t1 - t0:.6f} segundos")
