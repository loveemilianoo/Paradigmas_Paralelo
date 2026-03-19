import concurrent.futures
import math
import time
import random

def suma_crew(arreglo):
    print("Suma Paralela CREW con ThreadPoolExecutor")
    datos = arreglo.copy()
    n = len(datos)
    pasos = math.ceil(math.log2(n))

    inicio = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for paso in range(pasos):
            stride = 2 ** paso
            futuros = []

            indices_activos = [i for i in range(0, n - stride) 
                               if i % (stride * 2) == 0]
            
            if not indices_activos:
                continue

            def tarea(idx, s, current_data):
                return idx, current_data[idx] + current_data[idx + s]

            buffer_lectura = datos.copy()

            for i in indices_activos:
                futuros.append(executor.submit(tarea, i, stride, buffer_lectura))

            for f in concurrent.futures.as_completed(futuros):
                idx, resultado = f.result()
                datos[idx] = resultado
            
            print(f"Paso {paso + 1} | {len(indices_activos):2} tarea(s) activa(s) | indices: {indices_activos}")
            print(f"    Estado: {datos}")

    fin = time.perf_counter()

    print(f"Resultado: {datos[0]}")
    print(f"Tiempo: {(fin - inicio):.6f} segundos")
    return datos[0]

if __name__ == "__main__":
    n = 32
    arreglo = [random.randint(1, 100) for _ in range(n)]
    
    print(f"Arreglo ({n} elementos): {arreglo}")
    resultado = suma_crew(arreglo)
