import concurrent.futures
import time
import random

def minCRCW(L, n):
    win = [0] * n
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        def inicializar(idx):
            win[idx] = 0
        
        list(executor.map(inicializar, range(n)))

        def compararElementos(indices):
            i, j = indices
            if L[i] > L[j]:
                win[i] = 1
            elif L[i] < L[j]:
                win[j] = 1

        pares_indices = [(i, j) for i in range(n) for j in range(i + 1, n)]
        list(executor.map(compararElementos, pares_indices))

        def buscarMinimo(i):
            if win[i] == 0:
                return L[i]
            return None

        resultados_min = list(executor.map(buscarMinimo, range(n)))
        
        for val in resultados_min:
            if val is not None:
                return val

    return None

if __name__ == "__main__":
    n = 32
    arreglo = random.sample(range(1, 100), n)

    print("Búsqueda de Mínimo en modelo CRCW con ThreadPoolExecutor")
    print(f"\nLista L[0..{n-1}]: {arreglo}\n")

    tiempoInicial = time.perf_counter()
    resultado = minCRCW(arreglo, n)
    tiempoTotal = time.perf_counter() - tiempoInicial

    print(f"El mínimo es: {resultado}")
    print(f"\nTiempo de ejecución: {tiempoTotal:.6f} segundos")
    