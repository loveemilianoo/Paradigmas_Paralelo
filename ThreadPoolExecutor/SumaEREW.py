import concurrent.futures
import math
import time
import random

def suma (arreglo):
    print("Suma Paralela EREW con ThreadPoolExecutor")
    datos = arreglo.copy()
    n = len(datos)
    pasos = math.ceil(math.log2(n))

    inicio = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for paso in range(pasos):
            stride = 2**paso
            buffer = datos.copy()
            futuros = []
            
            def tarea (idx, s, buf):
                return idx, buf[idx] + buf [idx+s]
            
            for i in range (0,n,stride*2):
                if i + stride < n:
                    futuros.append(executor.submit(tarea, i, stride, buffer))

            for f in concurrent.futures.as_completed(futuros):
                idx, val = f.result()
                datos[idx] = val

            print(f"Paso {paso + 1} | {len(futuros)} tarea(s) activa(s): {datos}")

    fin = time.perf_counter()

    print(f"Resultado: {datos[0]}")
    print(f"Tiempo: {(fin-inicio):.6f} segundos")
    return datos[0]

if __name__ == "__main__":
    n = 32
    arreglo = [random.randint(1, 100) for _ in range(n)]
    print(f"Arreglo ({len(arreglo)} elementos): {arreglo}")

    r1 = suma(arreglo)

    print(f"Paralela: {r1}")