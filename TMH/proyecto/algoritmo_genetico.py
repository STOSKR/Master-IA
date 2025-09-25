# Algoritmo Genético para Optimización de Rutas Turísticas
import random
from typing import List, Tuple
from utils import lugares_turisticos, distancia_haversine, redondear_a_franja_15

tiempo_dia = 12 * 60  # 12 horas 

def crear_ruta(tiempo_dia: int = tiempo_dia, num_lugares: int = len(lugares_turisticos)) -> List[int]:
    max_lugares_dinamico = max(3, min(num_lugares, tiempo_dia // 90))
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
        tiempo_traslado = distancia * 25 + random.randint(-5, 5)  # 25 minutos por kilómetro
        # tiempo_traslado_redondeado = redondear_a_franja_15(tiempo_traslado)
        tiempo_total += tiempo_traslado

    # Verificar si la ruta es válida (dentro del tiempo máximo)
    exceso_tiempo = max(0, tiempo_total - tiempo_max)
    penalizacion = exceso_tiempo * 3
    # Verificar restricciones de horarios
    hora_actual = 10 * 60 
    penalizacion_horarios = 0

    for i in ruta:
        lugar = lugares_turisticos[i]
        apertura = int(lugar["apertura"].split(":")[0]) * 60 + int(lugar["apertura"].split(":")[1])
        cierre = int(lugar["cierre"].split(":")[0]) * 60 + int(lugar["cierre"].split(":")[1])

        if hora_actual < apertura or hora_actual + lugar["tiempo_visita"] > cierre:
            penalizacion_horarios += 1000  # Penalización alta por violar horarios

        hora_actual += lugar["tiempo_visita"]

    # Calcular fitness: maximizar puntos, minimizar distancia y aplicar penalización
    fitness = (w_puntos * puntos_total) - (w_distancia * distancia_total * 100) - penalizacion - penalizacion_horarios

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


def cruce_ordenado(padre1: List[int], padre2: List[int]) -> Tuple[List[int], List[int]]:
    size = min(len(padre1), len(padre2))
    hijo1, hijo2 = [-1]*size, [-1]*size

    start, end = sorted([random.randrange(size) for _ in range(2)])

    hijo1[start:end] = padre1[start:end]
    hijo2[start:end] = padre2[start:end]

    p2_genes = [gen for gen in padre2 if gen not in hijo1]
    p1_genes = [gen for gen in padre1 if gen not in hijo2]

    idx = end
    for gen in p2_genes:
        if -1 not in hijo1[idx:]:
            idx = 0
        if hijo1[idx] == -1:
            hijo1[idx] = gen
            idx += 1

    idx = end
    for gen in p1_genes:
        if -1 not in hijo2[idx:]:
            idx = 0
        if hijo2[idx] == -1:
            hijo2[idx] = gen
            idx += 1

    return hijo1, hijo2

def mutacion(ruta: List[int], prob_mutacion: float = 0.1) -> List[int]:
    ruta_mutada = ruta.copy()
    
    if random.random() < prob_mutacion:
        tipo_mutacion = random.choices(['intercambio', 'inversion', 'agregar', 'quitar'], weights=[0.4, 0.3, 0.15, 0.15], k=1)[0]
        
        if tipo_mutacion == 'intercambio' and len(ruta_mutada) >= 2:
            idx1, idx2 = random.sample(range(len(ruta_mutada)), 2)
            ruta_mutada[idx1], ruta_mutada[idx2] = ruta_mutada[idx2], ruta_mutada[idx1]

        elif tipo_mutacion == 'inversion' and len(ruta_mutada) >= 2:
            start, end = sorted(random.sample(range(len(ruta_mutada)), 2))
            segmento = ruta_mutada[start:end+1]
            segmento.reverse()
            ruta_mutada[start:end+1] = segmento
        
        elif tipo_mutacion == 'agregar' and len(ruta_mutada) < len(lugares_turisticos):
            lugares_disponibles = [i for i in range(len(lugares_turisticos)) if i not in ruta_mutada]
            if lugares_disponibles:
                ruta_mutada.append(random.choice(lugares_disponibles))
        
        elif tipo_mutacion == 'quitar' and len(ruta_mutada) > 2:
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
    mejor_fitness_historico = -1
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
                hijo1, hijo2 = cruce_ordenado(padre1, padre2)
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

def algoritmo_genetico_estado_estacionario(generaciones: int = 100, tamaño_poblacion: int = 1000, 
                                           prob_cruce: float = 0.8, prob_mutacion: float = 0.3, 
                                           tiempo_disponible: int = tiempo_dia) -> dict:
    """
    Algoritmo genético con reemplazo de estado estacionario.
    Mantiene el 90% de los mejores individuos y reemplaza el 10% de los peores.
    """
    print(f"\n🧬 ALGORITMO GENÉTICO (ESTADO ESTACIONARIO)")
    print(f"Generaciones: {generaciones}, Población: {tamaño_poblacion}")
    print(f"Prob. cruce: {prob_cruce}, Prob. mutación: {prob_mutacion}")
    print("="*50)

    # 1. Crear población inicial
    poblacion = crear_poblacion_inicial(tamaño_poblacion, tiempo_disponible)
    mejor_fitness_historico = -1
    mejor_ruta_historica = []
    historial_fitness = []

    for generacion in range(generaciones):
        # 2. Evaluar población
        fitness_scores = [evaluar_ruta(ruta)["fitness"] for ruta in poblacion]

        # 3. Ordenar población por fitness (de mejor a peor)
        poblacion_ordenada = [ruta for _, ruta in sorted(zip(fitness_scores, poblacion), key=lambda x: x[0], reverse=True)]
        fitness_ordenado = sorted(fitness_scores, reverse=True)

        # 4. Mantener el 90% de los mejores individuos
        num_mejores = int(0.9 * tamaño_poblacion)
        nueva_poblacion = poblacion_ordenada[:num_mejores]

        # 5. Generar hijos para reemplazar el 10% de los peores
        num_hijos = tamaño_poblacion - num_mejores
        hijos = []
        while len(hijos) < num_hijos:
            padre1, padre2 = seleccion_ranking(poblacion, fitness_scores, 2)
            if random.random() < prob_cruce:
                hijo1, hijo2 = cruce_ordenado(padre1, padre2)
            else:
                hijo1, hijo2 = padre1.copy(), padre2.copy()

            hijo1 = mutacion(hijo1, prob_mutacion)
            hijo2 = mutacion(hijo2, prob_mutacion)
            hijos.extend([hijo1, hijo2])

        # 6. Evaluar hijos y reemplazar a los peores si son mejores
        hijos = hijos[:num_hijos]  # Asegurar que no haya más hijos de los necesarios
        for i, hijo in enumerate(hijos):
            evaluacion_hijo = evaluar_ruta(hijo)["fitness"]
            if evaluacion_hijo > fitness_ordenado[-(i + 1)]:  # Comparar con los peores
                nueva_poblacion.append(hijo)
            else:
                nueva_poblacion.append(poblacion_ordenada[-(i + 1)])

        # 7. Actualizar población
        poblacion = nueva_poblacion[:tamaño_poblacion]

        # 8. Actualizar el mejor histórico
        mejor_fitness_gen = max(fitness_scores)
        mejor_ruta_gen = poblacion_ordenada[0]
        if mejor_fitness_gen > mejor_fitness_historico:
            mejor_fitness_historico = mejor_fitness_gen
            mejor_ruta_historica = mejor_ruta_gen.copy()

        # 9. Guardar para histórico
        historial_fitness.append(mejor_fitness_gen)

        # 10. Mostrar progreso cada 5 generaciones
        if generacion % 5 == 0 or generacion == generaciones - 1:
            print(f"Gen {generacion:2d}: Mejor fitness = {mejor_fitness_gen:7.2f}, Promedio = {sum(fitness_scores)/len(fitness_scores):7.2f}")

    # Resultado final
    evaluacion_final = evaluar_ruta(mejor_ruta_historica)
    return {
        "mejor_ruta": mejor_ruta_historica,
        "evaluacion": evaluacion_final,
        "historial_fitness": historial_fitness,
        "algoritmo": "Genético Estado Estacionario"
    }

def algoritmo_genetico_reemplazo_mixto(generaciones: int = 100, tamaño_poblacion: int = 1000, 
                                        prob_cruce: float = 0.8, prob_mutacion: float = 0.3, 
                                        tiempo_disponible: int = tiempo_dia) -> dict:
    """
    Algoritmo genético con reemplazo mixto.
    Combina elitismo, hijos generados y nuevos individuos aleatorios.
    """
    print(f"\n🧬 ALGORITMO GENÉTICO (REEMPLAZO MIXTO)")
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
        fitness_scores = [evaluar_ruta(ruta)["fitness"] for ruta in poblacion]

        # 3. Ordenar población por fitness (de mejor a peor)
        poblacion_ordenada = [ruta for _, ruta in sorted(zip(fitness_scores, poblacion), key=lambda x: x[0], reverse=True)]

        # 4. Mantener el 40% de los mejores individuos (elitismo)
        num_elitismo = int(0.4 * tamaño_poblacion)
        nueva_poblacion = poblacion_ordenada[:num_elitismo]

        # 5. Generar el 40% de la población como hijos
        num_hijos = int(0.4 * tamaño_poblacion)
        hijos = []
        while len(hijos) < num_hijos:
            padre1, padre2 = seleccion_ranking(poblacion, fitness_scores, 2)
            if random.random() < prob_cruce:
                hijo1, hijo2 = cruce_ordenado(padre1, padre2)
            else:
                hijo1, hijo2 = padre1.copy(), padre2.copy()

            hijo1 = mutacion(hijo1, prob_mutacion)
            hijo2 = mutacion(hijo2, prob_mutacion)
            hijos.extend([hijo1, hijo2])

        nueva_poblacion.extend(hijos[:num_hijos])  # Asegurar que no haya más hijos de los necesarios

        # 6. Generar el 20% de la población como nuevos individuos aleatorios
        num_aleatorios = tamaño_poblacion - len(nueva_poblacion)
        nuevos_individuos = crear_poblacion_inicial(num_aleatorios, tiempo_disponible)
        nueva_poblacion.extend(nuevos_individuos)

        # 7. Actualizar población
        poblacion = nueva_poblacion[:tamaño_poblacion]

        # 8. Actualizar el mejor histórico
        mejor_fitness_gen = max(fitness_scores)
        mejor_ruta_gen = poblacion_ordenada[0]
        if mejor_fitness_gen > mejor_fitness_historico:
            mejor_fitness_historico = mejor_fitness_gen
            mejor_ruta_historica = mejor_ruta_gen.copy()

        # 9. Guardar para histórico
        historial_fitness.append(mejor_fitness_gen)

        # 10. Mostrar progreso cada 5 generaciones
        if generacion % 5 == 0 or generacion == generaciones - 1:
            print(f"Gen {generacion:2d}: Mejor fitness = {mejor_fitness_gen:7.2f}, Promedio = {sum(fitness_scores)/len(fitness_scores):7.2f}")

    # Resultado final
    evaluacion_final = evaluar_ruta(mejor_ruta_historica)
    return {
        "mejor_ruta": mejor_ruta_historica,
        "evaluacion": evaluacion_final,
        "historial_fitness": historial_fitness,
        "algoritmo": "Genético Reemplazo Mixto"
    }

def imprimir_ruta(ruta: List[int], evaluacion: dict, tiempo_disponible: int):
    """Imprime los detalles de una ruta"""
    print("\n" + "="*50)
    print("RUTA:")
    for i, lugar_idx in enumerate(ruta):
        lugar = lugares_turisticos[lugar_idx]
        print(f"{i+1}. {lugar['nombre']} (Puntos: {lugar['puntos']}, Tiempo: {lugar['tiempo_visita']}min)")
    
    print(f"\nRESULTADOS:")
    print(f"Puntos totales: {evaluacion['puntos']}")
    print(f"Distancia total: {evaluacion['distancia']}")
    print(f"Tiempo total: {evaluacion['tiempo']} minutos (de {tiempo_disponible} disponibles)")
    print(f"Válida: {'Sí' if evaluacion['valida'] else 'No'}")
    print(f"Fitness: {evaluacion['fitness']}")
    
# Ejemplo de uso
if __name__ == "__main__":
    print("OPTIMIZACIÓN CON ALGORITMO GENÉTICO")
    print("="*60)
    
    # Ejecutar algoritmo genético
    resultado = algoritmo_genetico_reemplazo_mixto(200, 1000, 0.9, 0.1)
    
    print(f"\n🏆 MEJOR SOLUCIÓN ENCONTRADA:")
    imprimir_ruta(resultado["mejor_ruta"], resultado["evaluacion"], tiempo_dia)
    
    print(f"\n📊 EVOLUCIÓN DEL FITNESS:")
    for i, fitness in enumerate(resultado["historial_fitness"]):
        if i % 4 == 0:  # Mostrar cada 4 generaciones
            print(f"Generación {i:2d}: {fitness:7.2f}")