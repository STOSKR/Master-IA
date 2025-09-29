# Algoritmo Genético para Optimización de Rutas Turísticas
import random
from typing import List, Tuple
from utils import lugares_turisticos, distancia_haversine

tiempo_dia = 14 * 60  # 14 horas

def calcular_penalizacion_comida(hora_actual: int, tipo: str, almuerzo_tomado: bool, cena_tomada: bool) -> Tuple[float, bool, bool]:
    penalizacion = 0
    if not almuerzo_tomado and hora_actual >= 13.5 * 60:
        if tipo == "restaurante":
            almuerzo_tomado = True
        else:
            penalizacion += 50
    elif not cena_tomada and hora_actual >= 20.5 * 60:
        if tipo == "restaurante":
            cena_tomada = True
        else:
            penalizacion += 50
    return penalizacion, almuerzo_tomado, cena_tomada

def calcular_fitness(puntos_total: float, distancia_total: float, tiempo_total: float, tiempo_max: int, penalizacion_comida: float) -> float:
    exceso_tiempo = max(0, tiempo_total - tiempo_max)
    penalizacion_tiempo = exceso_tiempo * 3
    return max(0, (puntos_total) - (distancia_total * 100) - penalizacion_tiempo - penalizacion_comida)

def crear_ruta(tiempo_dia: int = tiempo_dia, num_lugares: int = len(lugares_turisticos)) -> List[int]:
    max_lugares_dinamico = max(3, min(num_lugares, tiempo_dia // 90))
    num_lugares = random.randint(2, max_lugares_dinamico)
    ruta = random.sample(range(len(lugares_turisticos)), num_lugares)
    # Asegurar que haya al menos un restaurante
    if not any(lugares_turisticos[i]['tipo'] == 'restaurante' for i in ruta):
        restaurantes = [i for i, lugar in enumerate(lugares_turisticos) if lugar['tipo'] == 'restaurante']
        if restaurantes:
            ruta[0] = random.choice(restaurantes)
    return ruta

def crear_poblacion_inicial(tamaño_poblacion: int, tiempo_disponible: int) -> List[List[int]]:
    poblacion = []

    while len(poblacion) < tamaño_poblacion:
        ruta = crear_ruta(tiempo_disponible)
        if ruta not in poblacion:
            poblacion.append(ruta)

    return poblacion

def evaluar_ruta(ruta: List[int], tiempo_max: int = tiempo_dia) -> dict:
    if not ruta:
        return {"puntos": 0, "distancia": 0, "tiempo": 0, "fitness": 0, "valida": False}

    puntos_total, distancia_total, tiempo_total = 0, 0, 0
    hora_actual = 9 * 60  # Empezamos a las 9:00
    almuerzo_tomado, cena_tomada = False, False
    penalizacion_comida = 0

    # Iterar sobre la ruta para calcular tiempo, distancia y puntos
    for i, lugar_idx in enumerate(ruta):
        lugar = lugares_turisticos[lugar_idx]
        
        # Calcular tiempo de traslado desde el lugar anterior
        if i > 0:
            lugar_anterior = lugares_turisticos[ruta[i-1]]
            distancia = distancia_haversine(lugar_anterior, lugar)
            distancia_total += distancia
            tiempo_traslado = distancia * 25  # 25 min/km
            # Redondear el tiempo de traslado al múltiplo de 5 más cercano hacia arriba
            tiempo_traslado = ((int(tiempo_traslado) + 4) // 5) * 5
            tiempo_total += tiempo_traslado
            hora_actual += tiempo_traslado

        # Penalización por horario de apertura/cierre
        apertura = int(lugar["apertura"].split(":")[0]) * 60 + int(lugar["apertura"].split(":")[1])
        cierre = int(lugar["cierre"].split(":")[0]) * 60 + int(lugar["cierre"].split(":")[1])

        if hora_actual < apertura:
            tiempo_espera = apertura - hora_actual
            tiempo_total += tiempo_espera
            hora_actual += tiempo_espera
        
        if hora_actual + lugar["tiempo_visita"] > cierre:
            penalizacion_comida += 200  # Penalización moderada por violar horarios

        # Lógica para comidas
        # Almuerzo
        if not almuerzo_tomado and hora_actual >= 13.5 * 60:
            if lugar["tipo"] == "restaurante":
                puntos_lugar = lugar["puntos"]
                if 13.5 * 60 <= hora_actual <= 14.5 * 60:
                    puntos_total += puntos_lugar * 1.5  # Bonificación
                else:
                    puntos_total += puntos_lugar * 0.5  # Penalización
                almuerzo_tomado = True
            else:
                # Penalización si no es un restaurante y es hora de comer
                penalizacion_comida += 50 
        
        # Cena
        elif not cena_tomada and hora_actual >= 20.5 * 60:
            if lugar["tipo"] == "restaurante":
                puntos_lugar = lugar["puntos"]
                if 20.5 * 60 <= hora_actual <= 22 * 60:
                    puntos_total += puntos_lugar * 1.5  # Bonificación
                else:
                    puntos_total += puntos_lugar * 0.5  # Penalización
                cena_tomada = True
            else:
                # Penalización si no es un restaurante y es hora de cenar
                penalizacion_comida += 50
        else:
            puntos_total += lugar["puntos"]

        # Actualizar tiempo total y hora actual
        tiempo_visita = lugar["tiempo_visita"]
        tiempo_total += tiempo_visita
        hora_actual += tiempo_visita

    # Penalización si no se ha comido o cenado
    if not almuerzo_tomado:
        penalizacion_comida += 100  # Penalización reducida
    if not cena_tomada:
        penalizacion_comida += 100  # Penalización reducida

    # Calcular fitness final
    fitness = calcular_fitness(puntos_total, distancia_total, tiempo_total, tiempo_max, penalizacion_comida)

    return {
        "puntos": puntos_total,
        "distancia": round(distancia_total, 2),
        "tiempo": round(tiempo_total, 2),
        "fitness": max(0, round(fitness, 2)),
        "valida": tiempo_total <= tiempo_max,
        "comida_penalizacion": penalizacion_comida,
        "tiempo_penalizacion": 0,  # Se eliminó la penalización de tiempo individual
    }

def seleccion_ranking(poblacion: List[List[int]], fitness_scores: List[float], tamaño_seleccion: int = 200) -> List[List[int]]:
    """
    Selección por ranking con elitismo: selecciona un porcentaje fijo de los mejores individuos
    y el resto basándose en el ranking de fitness.
    """
    # Ordenar población por fitness (mayor a menor)
    ranking = sorted(zip(poblacion, fitness_scores), key=lambda x: x[1], reverse=True)

    # Determinar el número de individuos para elitismo (10% de tamaño_seleccion)
    num_elitismo = max(1, tamaño_seleccion // 5)  # Al menos 1 individuo
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

def inicializar_poblacion_y_evaluar(tamaño_poblacion: int, tiempo_disponible: int):
    poblacion = crear_poblacion_inicial(tamaño_poblacion, tiempo_disponible)
    fitness_scores = [evaluar_ruta(ruta)["fitness"] for ruta in poblacion]
    return poblacion, fitness_scores

def evolucionar_poblacion(poblacion: List[List[int]], fitness_scores: List[float], tamaño_poblacion: int, prob_cruce: float, prob_mutacion: float):
    nueva_poblacion = []
    while len(nueva_poblacion) < tamaño_poblacion:
        padre1, padre2 = seleccion_ranking(poblacion, fitness_scores, 2)
        if random.random() < prob_cruce:
            hijo1, hijo2 = cruce_ordenado(padre1, padre2)
        else:
            hijo1, hijo2 = padre1.copy(), padre2.copy()
        nueva_poblacion.extend([mutacion(hijo1, prob_mutacion), mutacion(hijo2, prob_mutacion)])
    return nueva_poblacion[:tamaño_poblacion]

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
    poblacion, fitness_scores = inicializar_poblacion_y_evaluar(tamaño_poblacion, tiempo_disponible)
    mejor_fitness_historico, mejor_ruta_historica = -1, []
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
        
        # 6. Mostrar progreso cada 20 generaciones
        if generacion % 20 == 0 or generacion == generaciones - 1:
            print(f"| Gen {generacion:3d} | Mejor Fitness: {mejor_fitness_gen:8.2f} | Fitness Promedio: {sum(fitness_scores)/len(fitness_scores):8.2f} | Mejor Histórico: {mejor_fitness_historico:8.2f} |")
        
        # 7. Crear nueva población
        poblacion = evolucionar_poblacion(poblacion, fitness_scores, tamaño_poblacion, prob_cruce, prob_mutacion)

    # Resultado final
    evaluacion_final = evaluar_ruta(mejor_ruta_historica)
    imprimir_mejor_ruta(mejor_ruta_historica, evaluacion_final)
    
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
    poblacion, fitness_scores = inicializar_poblacion_y_evaluar(tamaño_poblacion, tiempo_disponible)
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

        # 10. Mostrar progreso cada 20 generaciones
        if generacion % 20 == 0 or generacion == generaciones - 1:
            print(f"Gen {generacion:2d}: Mejor fitness = {mejor_fitness_gen:7.2f}, Promedio = {sum(fitness_scores)/len(fitness_scores):7.2f}")

    # Resultado final
    evaluacion_final = evaluar_ruta(mejor_ruta_historica)
    imprimir_mejor_ruta(mejor_ruta_historica, evaluacion_final)
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
    poblacion, fitness_scores = inicializar_poblacion_y_evaluar(tamaño_poblacion, tiempo_disponible)
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

        # 5. Generar el 60% de la población como hijos
        num_hijos = int(0.6 * tamaño_poblacion)
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

        # 10. Mostrar progreso cada 20 generaciones
        if generacion % 20 == 0 or generacion == generaciones - 1:
            print(f"Gen {generacion:2d}: Mejor fitness = {mejor_fitness_gen:7.2f}, Promedio = {sum(fitness_scores)/len(fitness_scores):7.2f}")

    # Resultado final
    evaluacion_final = evaluar_ruta(mejor_ruta_historica)
    imprimir_mejor_ruta(mejor_ruta_historica, evaluacion_final)
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

def imprimir_mejor_ruta(ruta: List[int], evaluacion: dict):
    print("\n" + "="*50)
    print("🏆 MEJOR RUTA ENCONTRADA 🏆")
    print("="*50)

    hora_actual = 9 * 60  # 9:00 AM
    almuerzo_tomado = False
    cena_tomada = False

    for i, lugar_idx in enumerate(ruta):
        lugar = lugares_turisticos[lugar_idx]
        
        # Tiempo de traslado
        if i > 0:
            lugar_anterior = lugares_turisticos[ruta[i-1]]
            distancia = distancia_haversine(lugar_anterior, lugar)
            tiempo_traslado = distancia * 25
            # Redondear el tiempo de traslado al múltiplo de 5 más cercano hacia arriba
            tiempo_traslado = ((int(tiempo_traslado) + 4) // 5) * 5
            hora_actual += tiempo_traslado
            print(f"  -> Traslado: {tiempo_traslado:.0f} min")

        # Hora de llegada y espera
        apertura = int(lugar["apertura"].split(":")[0]) * 60 + int(lugar["apertura"].split(":")[1])
        hora_llegada = hora_actual
        if hora_llegada < apertura:
            hora_actual = apertura
        
        # Determinar si es comida/cena
        etiqueta_comida = ""
        if not almuerzo_tomado and lugar["tipo"] == "restaurante" and hora_actual >= 13.5 * 60:
            etiqueta_comida = " (Almuerzo)"
            almuerzo_tomado = True
        elif not cena_tomada and lugar["tipo"] == "restaurante" and hora_actual >= 20.5 * 60:
            etiqueta_comida = " (Cena)"
            cena_tomada = True

        print(f"{i+1}. {lugar['nombre']}{etiqueta_comida}")
        print(f"   - Llegada: {int(hora_llegada // 60):02d}:{int(hora_llegada % 60):02d} | Visita: {lugar['tiempo_visita']} min | Puntos: {lugar['puntos']}")
        
        hora_actual += lugar['tiempo_visita']

    print("="*50)
    print("📊 RESUMEN DE LA RUTA:")
    print(f"  - Puntos totales: {evaluacion['puntos']:.2f}")
    print(f"  - Distancia total: {evaluacion['distancia']:.2f} km")
    print(f"  - Tiempo total: {evaluacion['tiempo']:.2f} min (de {tiempo_dia} disponibles)")
    print(f"  - Penalización por tiempo: {evaluacion.get('tiempo_penalizacion', 0):.2f}")
    print(f"  - Penalización por comidas: {evaluacion.get('comida_penalizacion', 0):.2f}")
    print(f"  - Fitness final: {evaluacion['fitness']:.2f}")
    print(f"  - Ruta válida: {'Sí' if evaluacion['valida'] else 'No'}")
    print("="*50)
    
# Ejemplo de uso
if __name__ == "__main__":
    print("OPTIMIZACIÓN CON ALGORITMO GENÉTICO")
    print("="*60)

    # Ejecutar algoritmo genético
    resultado = algoritmo_genetico_reemplazo_mixto(300, 1000, 0.9, 0.2)

    print(f"\n🏆 MEJOR SOLUCIÓN ENCONTRADA:")
    imprimir_mejor_ruta(resultado["mejor_ruta"], resultado["evaluacion"])