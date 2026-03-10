import threading
import math
import time
import random

def suma (arreglo):
    print("Suma Paralela EREW")
    datos = arreglo.copy()
    n = len(datos)
    pasos = math.ceil(math.log2(n))

    inicio = time.perf_counter()

    for paso in range(pasos):
        stride = 2**paso
        buffer = datos.copy()
        hilos= []
        barrier = threading.Barrier(
            sum(
                1 for i in range(0,n,stride*2)
                if i + stride < n) 
                or 1)
        
        def tarea (idx, s, buf, dest):
            val = buf[idx] + buf [idx+s]
            barrier.wait()
            dest[idx] = val
        
        for i in range (0,n,stride*2):
            if i +stride < n:
                hilo= threading.Thread(target=tarea, args=(i, stride, buffer, datos))
                hilos.append(hilo)

        for h in hilos:
            h.start()
            
        for h in hilos:
            h.join()

        print(f"Paso {paso + 1} | {len(hilos)} hilo(s) activo(s): {datos}")

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