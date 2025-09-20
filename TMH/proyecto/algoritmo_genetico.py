# Algoritmo Genético para Optimización de Rutas Turísticas
import random
from typing import List, Tuple
from utils import lugares_turisticos, distancia_haversine, redondear_a_franja_15

tiempo_dia = 12 * 60  # 12 horas 

"""
Limitaciones

Tiempo Disponible Fijo:
Aunque el tamaño de las rutas es dinámico, el tiempo disponible es constante (12 horas). Esto limita la adaptabilidad del algoritmo a diferentes escenarios.

Falta de Diversidad Controlada:
No se garantiza que las rutas iniciales cubran diferentes regiones geográficas o incluyan lugares con puntuaciones altas.

Dependencia de Parámetros:
El límite de 90 minutos por lugar es arbitrario y podría no ser adecuado para todos los casos.
"""

def crear_ruta(tiempo_dia: int = tiempo_dia, num_lugares: int = len(lugares_turisticos)) -> List[int]:
    max_lugares_dinamico = max(3, min(num_lugares, tiempo_dia // 90))  # Asegurar que el mínimo sea 2
    num_lugares = random.randint(2, max_lugares_dinamico)
    return random.sample(range(len(lugares_turisticos)), num_lugares)

def crear_poblacion_inicial(tamaño_poblacion: int, tiempo_disponible: int) -> List[List[int]]:
    poblacion = []

    while len(poblacion) < tamaño_poblacion:
        ruta = crear_ruta(tiempo_disponible)
        if ruta not in poblacion:
            poblacion.append(ruta)

    return poblacion

def evaluar_ruta(ruta: List[int], tiempo_max: int = tiempo_dia, w_puntos: float = 1.0, w_distancia: float = 1.0) -> dict:
    if len(ruta) == 0:
        return {"puntos": 0, "distancia": 0, "tiempo": 0, "fitness": 0, "valida": False}

    puntos_total = 0
    distancia_total = 0
    tiempo_total = 0

    # Calcular puntos y tiempo de visita
    for i in ruta:
        lugar = lugares_turisticos[i]
        puntos_total += lugar["puntos"]
        tiempo_total += lugar["tiempo_visita"]

    # Calcular distancia total y tiempo de traslado
    for i in range(len(ruta) - 1):
        lugar_actual = lugares_turisticos[ruta[i]]
        lugar_siguiente = lugares_turisticos[ruta[i + 1]]
        distancia = distancia_haversine(lugar_actual, lugar_siguiente)
        distancia_total += distancia

        # Convertir distancia a tiempo de traslado (en minutos)
        tiempo_traslado = distancia * 20  # 20 minutos por kilómetro
        tiempo_traslado_redondeado = redondear_a_franja_15(tiempo_traslado)
        tiempo_total += tiempo_traslado_redondeado

    # Verificar si la ruta es válida (dentro del tiempo máximo)
    exceso_tiempo = max(0, tiempo_total - tiempo_max)
    penalizacion = exceso_tiempo * 0.7  # Penalización proporcional al exceso de tiempo

    # Verificar restricciones de horarios
    hora_actual = 10 * 60  # Día comienza a las 10:00 (en minutos)
    penalizacion_horarios = 0

    for i in ruta:
        lugar = lugares_turisticos[i]
        apertura = int(lugar["apertura"].split(":")[0]) * 60 + int(lugar["apertura"].split(":")[1])
        cierre = int(lugar["cierre"].split(":")[0]) * 60 + int(lugar["cierre"].split(":")[1])

        if hora_actual < apertura or hora_actual + lugar["tiempo_visita"] > cierre:
            penalizacion_horarios += 1000  # Penalización alta por violar horarios

        hora_actual += lugar["tiempo_visita"]

    # Calcular fitness: maximizar puntos, minimizar distancia y aplicar penalización
    fitness = (w_puntos * puntos_total) - (w_distancia * distancia_total) - penalizacion - penalizacion_horarios

    return {
        "puntos": puntos_total,
        "distancia": round(distancia_total, 2),
        "tiempo": round(tiempo_total, 2),
        "fitness": max(0, round(fitness, 2)),  # Asegurar que el fitness no sea negativo
        "valida": tiempo_total <= tiempo_max
    }

def seleccion_ranking(poblacion: List[List[int]], fitness_scores: List[float], tamaño_seleccion: int = 200) -> List[List[int]]:
    """
    Selección por ranking con elitismo: selecciona un porcentaje fijo de los mejores individuos
    y el resto basándose en el ranking de fitness.
    """
    # Ordenar población por fitness (mayor a menor)
    ranking = sorted(zip(poblacion, fitness_scores), key=lambda x: x[1], reverse=True)

    # Determinar el número de individuos para elitismo (10% de tamaño_seleccion)
    num_elitismo = max(1, tamaño_seleccion // 10)  # Al menos 1 individuo
    elite = [individuo[0] for individuo in ranking[:num_elitismo]]

    # Crear una lista acumulativa de probabilidades para el resto
    total = sum(range(1, len(ranking) + 1))  # Suma de 1 + 2 + ... + n
    probabilidades = [(i + 1) / total for i in range(len(ranking))]

    # Seleccionar el resto de los individuos basados en las probabilidades
    seleccionados = random.choices(ranking, weights=probabilidades, k=tamaño_seleccion - num_elitismo)
    seleccionados = [individuo[0] for individuo in seleccionados]

    # Combinar elite con los seleccionados
    return elite + seleccionados

def cruce_dinamico_uniforme(padre1: List[int], padre2: List[int]) -> Tuple[List[int], List[int]]:
    """
    Cruce dinámico basado en la longitud de los padres y uniforme.
    Cada gen del hijo se selecciona aleatoriamente de uno de los dos padres.
    """
    # Determinar la longitud dinámica de los hijos basada en la longitud promedio de los padres
    longitud_hijo = random.randint(2, (len(padre1) + len(padre2)) // 2)

    # Crear hijos seleccionando genes de forma uniforme
    hijo1 = random.sample(padre1 + padre2, longitud_hijo)
    hijo2 = random.sample(padre1 + padre2, longitud_hijo)

    # Asegurar que no haya duplicados en los hijos
    hijo1 = list(dict.fromkeys(hijo1))
    hijo2 = list(dict.fromkeys(hijo2))

    return hijo1, hijo2

def mutacion(ruta: List[int], prob_mutacion: float = 0.1) -> List[int]:
    """
    Mutación simple: puede cambiar un lugar, agregar uno o quitar uno
    """
    ruta_mutada = ruta.copy()
    
    if random.random() < prob_mutacion:
        tipo_mutacion = random.choice(['cambiar', 'agregar', 'quitar'])
        
        if tipo_mutacion == 'cambiar' and len(ruta_mutada) > 0:
            # Cambiar un lugar por otro
            idx = random.randint(0, len(ruta_mutada) - 1)
            nuevo_lugar = random.randint(0, len(lugares_turisticos) - 1)
            if nuevo_lugar not in ruta_mutada:
                ruta_mutada[idx] = nuevo_lugar
        
        elif tipo_mutacion == 'agregar' and len(ruta_mutada) < len(lugares_turisticos):
            # Agregar un nuevo lugar
            lugares_disponibles = [i for i in range(len(lugares_turisticos)) if i not in ruta_mutada]
            if lugares_disponibles:
                ruta_mutada.append(random.choice(lugares_disponibles))
        
        elif tipo_mutacion == 'quitar' and len(ruta_mutada) > 2:
            # Quitar un lugar
            idx = random.randint(0, len(ruta_mutada) - 1)
            ruta_mutada.pop(idx)
    
    return ruta_mutada

def algoritmo_genetico_simple(generaciones: int = 100, tamaño_poblacion: int = 1000, 
                             prob_cruce: float = 0.8, prob_mutacion: float = 0.3, tiempo_disponible: int = tiempo_dia) -> dict:
    """
    Ejecuta el algoritmo genético simple
    """
    print(f"\n🧬 ALGORITMO GENÉTICO")
    print(f"Generaciones: {generaciones}, Población: {tamaño_poblacion}")
    print(f"Prob. cruce: {prob_cruce}, Prob. mutación: {prob_mutacion}")
    print("="*50)
    
    # 1. Crear población inicial
    poblacion = crear_poblacion_inicial(tamaño_poblacion, tiempo_disponible)
    mejor_fitness_historico = -999999
    mejor_ruta_historica = []
    historial_fitness = []
    
    for generacion in range(generaciones):
        # 2. Evaluar población
        fitness_scores = []
        for ruta in poblacion:
            evaluacion = evaluar_ruta(ruta)
            fitness_scores.append(evaluacion["fitness"])
        
        # 3. Encontrar el mejor de esta generación
        mejor_idx = fitness_scores.index(max(fitness_scores))
        mejor_ruta_gen = poblacion[mejor_idx]
        mejor_fitness_gen = fitness_scores[mejor_idx]
        
        # 4. Actualizar el mejor histórico
        if mejor_fitness_gen > mejor_fitness_historico:
            mejor_fitness_historico = mejor_fitness_gen
            mejor_ruta_historica = mejor_ruta_gen.copy()
        
        # 5. Guardar para histórico
        historial_fitness.append(mejor_fitness_gen)
        
        # 6. Mostrar progreso cada 5 generaciones
        if generacion % 5 == 0 or generacion == generaciones - 1:
            print(f"Gen {generacion:2d}: Mejor fitness = {mejor_fitness_gen:7.2f}, "
                  f"Promedio = {sum(fitness_scores)/len(fitness_scores):7.2f}")
        
        # 7. Crear nueva población
        nueva_poblacion = []
        
        # Mantener el mejor (elitismo)
        nueva_poblacion.append(mejor_ruta_gen.copy())
        
        # Generar el resto
        while len(nueva_poblacion) < tamaño_poblacion:
            # Selección
            padre1 = seleccion_ranking(poblacion, fitness_scores, 2)[0]  # Seleccionar un individuo
            padre2 = seleccion_ranking(poblacion, fitness_scores, 2)[0]  # Seleccionar otro individuo
            
            # Cruce
            if random.random() < prob_cruce:
                hijo1, hijo2 = cruce_dinamico_uniforme(padre1, padre2)
            else:
                hijo1, hijo2 = padre1.copy(), padre2.copy()
            
            # Mutación
            hijo1 = mutacion(hijo1, prob_mutacion)
            hijo2 = mutacion(hijo2, prob_mutacion)
            
            # Agregar a nueva población
            nueva_poblacion.extend([hijo1, hijo2])
        
        # Ajustar tamaño si se pasó
        poblacion = nueva_poblacion[:tamaño_poblacion]
    
    # Resultado final
    evaluacion_final = evaluar_ruta(mejor_ruta_historica)
    return {
        "mejor_ruta": mejor_ruta_historica,
        "evaluacion": evaluacion_final,
        "historial_fitness": historial_fitness,
        "algoritmo": "Genético"
    }

def imprimir_ruta(ruta: List[int], evaluacion: dict):
    """Imprime los detalles de una ruta"""
    print("\n" + "="*50)
    print("RUTA:")
    for i, lugar_idx in enumerate(ruta):
        lugar = lugares_turisticos[lugar_idx]
        print(f"{i+1}. {lugar['nombre']} (Puntos: {lugar['puntos']}, Tiempo: {lugar['tiempo_visita']}min)")
    
    print(f"\nRESULTADOS:")
    print(f"Puntos totales: {evaluacion['puntos']}")
    print(f"Distancia total: {evaluacion['distancia']}")
    print(f"Tiempo total: {evaluacion['tiempo']} minutos")
    print(f"Válida: {'Sí' if evaluacion['valida'] else 'No'}")
    print(f"Fitness: {evaluacion['fitness']}")
    
# Ejemplo de uso
if __name__ == "__main__":
    print("OPTIMIZACIÓN CON ALGORITMO GENÉTICO")
    print("="*60)
    
    # Ejecutar algoritmo genético
    resultado = algoritmo_genetico_simple()
    
    print(f"\n🏆 MEJOR SOLUCIÓN ENCONTRADA:")
    imprimir_ruta(resultado["mejor_ruta"], resultado["evaluacion"])
    
    print(f"\n📊 EVOLUCIÓN DEL FITNESS:")
    for i, fitness in enumerate(resultado["historial_fitness"]):
        if i % 4 == 0:  # Mostrar cada 4 generaciones
            print(f"Generación {i:2d}: {fitness:7.2f}")