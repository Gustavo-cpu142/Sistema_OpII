import pandas as pd
from collections import deque

# Función para leer procesos desde un archivo CSV
def leer_procesos(archivo):
    try:
        procesos = pd.read_csv(archivo)
        return [
            (fila['Nombre'], int(fila['TiempoLlegada']), int(fila['TiempoEjecucion']))
            for _, fila in procesos.iterrows()
        ]
    except Exception as e:
        print("Error al leer el archivo:", e)
        return []

# Algoritmo Round Robin
def round_robin(procesos, quantum):
    secuencia_ejecucion = []
    cola = deque(procesos)
    tiempo = 0

    while cola:
        proceso_actual = cola.popleft()
        nombre, llegada, rafaga = proceso_actual

        # Avanzar el tiempo si el proceso aún no ha llegado
        if llegada > tiempo:
            tiempo = llegada

        tiempo_ejecucion = min(quantum, rafaga)

        # Agregar proceso a la secuencia de ejecución
        secuencia_ejecucion.extend([nombre] * tiempo_ejecucion)

        # Actualizar tiempo y ráfaga restante
        tiempo += tiempo_ejecucion
        rafaga -= tiempo_ejecucion

        if rafaga > 0:
            cola.append((nombre, tiempo, rafaga))

    return secuencia_ejecucion

# Algoritmo Shortest Job First (SJF)
def shortest_job_first(procesos):
    secuencia_ejecucion = []
    procesos.sort(key=lambda x: (x[1], x[2]))  # Ordenar por tiempo de llegada y ráfaga

    tiempo = 0
    while procesos:
        listos = [p for p in procesos if p[1] <= tiempo]
        if not listos:
            tiempo += 1
            continue

        proximo = min(listos, key=lambda x: x[2])  # Proceso con menor ráfaga
        procesos.remove(proximo)

        nombre, llegada, rafaga = proximo
        secuencia_ejecucion.extend([nombre] * rafaga)
        tiempo += rafaga

    return secuencia_ejecucion

# Función para imprimir secuencia de ejecución
def imprimir_secuencia(secuencia):
    print(", ".join(secuencia))

if __name__ == "__main__":
    archivo_procesos = 'C:/Users/pato7/Desktop/RoundFirst/procesos.csv'
    procesos = leer_procesos(archivo_procesos)

    if procesos:
        try:
            quantum = int(input("Ingrese el valor de quantum para Round Robin: "))
            if quantum <= 0:
                raise ValueError("El quantum debe ser un número positivo.")
        except ValueError as e:
            print(e)
        else:
            # Round Robin
            secuencia_rr = round_robin(procesos.copy(), quantum)
            print("\nSecuencia de ejecución para Round Robin:")
            imprimir_secuencia(secuencia_rr)

            # Shortest Job First
            secuencia_sjf = shortest_job_first(procesos.copy())
            print("\nSecuencia de ejecución para Shortest Job First:")
            imprimir_secuencia(secuencia_sjf)
    else:
        print("No se encontraron procesos para ejecutar.")
