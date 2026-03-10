import threading
import math
import time
import random

def suma (arreglo):
    print("Suma Paralela CREW")
    datos = arreglo.copy()
    n = len(datos)
    pasos = math.ceil(math.log2(n))

    inicio = time.perf_counter()

    for paso in range(pasos):
        stride = 2 ** paso
        hilos = []

        indices_activos = [i for i in range(0,n-stride) 
                           if i % (stride*2) == 0]
        num_hilos = len(indices_activos)

        if num_hilos == 0:
            continue

        barrier = threading.Barrier(num_hilos)

        def tarea (idx, s, dest):
            val = dest[idx] + dest[idx + s]
            barrier.wait()
            dest[idx] = val
        
        for i in indices_activos:
            hilo = threading.Thread(target=tarea, args=(i, stride,datos))
            hilos.append(hilo)

        for h in hilos:
            h.start()
        for h in hilos:
            h.join()
        
        print(f"Paso {paso+1} | {num_hilos:2} hilo(s) activo(s) | indices: {indices_activos}")
        print(f"    Estado: {datos}")
    
    fin = time.perf_counter()

    print(f"Resultado: {datos[0]}")
    print(f"Tiempo: {(fin-inicio):.6f} segundos")
    return datos[0]

if __name__ == "__main__":
    arreglo = []
    for i in range(32):
        numeroRandom = random.randint(1,1000)
        arreglo.append(numeroRandom)
    print(f"Arreglo ({len(arreglo)} elementos): {arreglo}")
    print(f"Suma esperada: {sum(arreglo)}")

    r1 = suma(arreglo)

    print(f"Paralela: {r1}")
    