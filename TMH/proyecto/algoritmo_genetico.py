import random
from typing import List, Tuple
from utils import lugares_turisticos as lt, distancia_haversine
import json  # Add this import at the top

t_dia = 14 * 60
tm_visita = 90
hora_actual = 9 * 60

def calcular_penalizacion_comida(hora_actual: int, tipo: str, almuerzo_tomado: bool, cena_tomada: bool) -> Tuple[float, bool, bool]:
    penalizacion = 0
    if not almuerzo_tomado and hora_actual >= 13.5 * 60 and hora_actual < 14.5 * 60:
        if tipo == "restaurante":
            almuerzo_tomado = True
            penalizacion -= 100
        else:
            penalizacion += 50
    elif not cena_tomada and hora_actual >= 20.5 * 60 and hora_actual < 22 * 60:
        if tipo == "restaurante":
            cena_tomada = True
            penalizacion -= 100
        else:
            penalizacion += 50
    return penalizacion, almuerzo_tomado, cena_tomada

def calcular_fitness(w_puntos, w_distancia, puntos_t: float, distancia_t: float, tiempo_total: float, tiempo_max: int, penalizacion: float) -> float:
    exceso_tiempo = max(0, tiempo_total - tiempo_max)
    penalizacion_tiempo = exceso_tiempo * 3
    return max(0, (puntos_t * w_puntos) - (distancia_t * 100 * w_distancia) - penalizacion_tiempo - penalizacion)

def crear_ruta(t_dia: int = t_dia, n_lugares: int = len(lt)) -> List[int]:
    max_lugares_dinamico = min(n_lugares, t_dia // tm_visita)
    n_lugares = random.randint(4, max_lugares_dinamico)
    ruta = random.sample(range(len(lt)), n_lugares)
    
    if not any(lt[i]['tipo'] == 'restaurante' for i in ruta):
        rest = [i for i, l in enumerate(lt) if l['tipo'] == 'restaurante']
        if rest:
            ruta[0] = random.choice(rest)
    return ruta

def crear_poblacion_inicial(tamaño_poblacion: int, tiempo_disponible: int) -> List[List[int]]:
    poblacion = []

    while len(poblacion) < tamaño_poblacion:
        ruta = crear_ruta(tiempo_disponible)
        if ruta not in poblacion:
            poblacion.append(ruta)

    return poblacion

def evaluar_ruta(ruta: List[int], tiempo_max: int = t_dia, hora_actual: int = 9 * 60) -> dict:
    if not ruta:
        return {"puntos": 0, "distancia": 0, "tiempo": 0, "fitness": 0, "valida": False}

    puntos_t, distancia_t, tiempo_total = 0, 0, 0
    penalizacion = 0
    almuerzo_tomado, cena_tomada = False, False

    for i, lugar_idx in enumerate(ruta):
        lugar = lt[lugar_idx]
        
        if i > 0:
            lugar_anterior = lt[ruta[i-1]]
            distancia = distancia_haversine(lugar_anterior, lugar)
            distancia_t += distancia
            t_traslado = distancia * 25
            
            # Redondear a múltiplo de 5 más cercano superior
            t_traslado = ((int(t_traslado)) // 5 + 1) * 5
            tiempo_total += t_traslado
            hora_actual += t_traslado

        # Penalización por horario de apertura/cierre
        apertura = int(lugar["apertura"].split(":")[0]) * 60 + int(lugar["apertura"].split(":")[1])
        cierre = int(lugar["cierre"].split(":")[0]) * 60 + int(lugar["cierre"].split(":")[1])

        if hora_actual < apertura:
            tiempo_espera = apertura - hora_actual
            tiempo_total += tiempo_espera
            hora_actual += tiempo_espera
        
        if hora_actual + lugar["tiempo_visita"] > cierre:
            penalizacion += 200

        penalizacion_comida, almuerzo_tomado, cena_tomada = calcular_penalizacion_comida(
            hora_actual, lugar["tipo"], almuerzo_tomado, cena_tomada
        )
        penalizacion += penalizacion_comida

        # Actualizar puntos y tiempo
        puntos_t += lugar["puntos"]
        tiempo_visita = lugar["tiempo_visita"]
        tiempo_total += tiempo_visita
        hora_actual += tiempo_visita

    if not almuerzo_tomado:
        penalizacion += 100
    if not cena_tomada:
        penalizacion += 100

    fitness = calcular_fitness(1, 1, puntos_t, distancia_t, tiempo_total, tiempo_max, penalizacion)

    return {
        "puntos": puntos_t,
        "distancia": round(distancia_t, 2),
        "tiempo": round(tiempo_total, 2),
        "fitness": max(0, round(fitness, 2)),
        "valida": tiempo_total <= tiempo_max,
        "comida_penalizacion": penalizacion,
        "tiempo_penalizacion": 0, 
    }

def seleccion_ranking(poblacion: List[List[int]], fitness_scores: List[float], tamaño_seleccion: int = 200) -> List[List[int]]:
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
        
        elif tipo_mutacion == 'agregar' and len(ruta_mutada) < len(lt):
            lugares_disponibles = [i for i in range(len(lt)) if i not in ruta_mutada]
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

def evolucionar_poblacion(poblacion: List[List[int]], fitness_scores: List[float], tamaño_poblacion: int, prob_cruce: float, prob_mutacion: float, tamaño_seleccion: int = 200):
    # 1. Crear el "mating pool" una sola vez
    mating_pool = seleccion_ranking(poblacion, fitness_scores, tamaño_seleccion)

    # 2. Mantener el 20% de los mejores individuos (elitismo)
    num_elitismo = int(0.2 * tamaño_poblacion)
    nueva_poblacion = poblacion[:num_elitismo]

    # 3. Generar el 80% de la población como hijos
    num_hijos = tamaño_poblacion - num_elitismo
    hijos = []
    while len(hijos) < num_hijos:
        padre1 = random.choice(mating_pool)
        padre2 = random.choice(mating_pool)

        if random.random() < prob_cruce:
            hijo1, hijo2 = cruce_ordenado(padre1, padre2)
        else:
            hijo1, hijo2 = padre1.copy(), padre2.copy()

        hijos.extend([mutacion(hijo1, prob_mutacion), mutacion(hijo2, prob_mutacion)])

    nueva_poblacion.extend(hijos)
    return nueva_poblacion[:tamaño_poblacion]

def algoritmo_genetico_reemplazo_mixto(generaciones: int = 100, tamaño_poblacion: int = 1000, 
                                        prob_cruce: float = 0.8, prob_mutacion: float = 0.3, 
                                        tiempo_disponible: int = t_dia) -> dict:
    print(f"\n🧬 ALGORITMO GENÉTICO (REEMPLAZO MIXTO)")
    print(f"Generaciones: {generaciones}, Población: {tamaño_poblacion}")
    print(f"Prob. cruce: {prob_cruce}, Prob. mutación: {prob_mutacion}")
    print("="*50)

    poblacion, fitness_scores = inicializar_poblacion_y_evaluar(tamaño_poblacion, tiempo_disponible)
    
    mejor_fitness_global = 0
    mejor_ruta_global = []
    mejor_generacion_fitness = []
    mejor_generacion_pareto = []

    mejor_fitness_era = 0
    generaciones_estancadas = 0
    umbral_estancamiento = 50

    historial_fitness = []
    historial_promedio = []
    soluciones_pareto = []
    fitness_final = []

    for generacion in range(generaciones):
        evaluaciones = [evaluar_ruta(ruta) for ruta in poblacion]
        fitness_scores = [ev["fitness"] for ev in evaluaciones]

        if generacion == generaciones - 1:
            soluciones_pareto = [{"puntos": ev["puntos"], "distancia": ev["distancia"]} for ev in evaluaciones]
            fitness_final = fitness_scores

        poblacion = [ruta for _, ruta in sorted(zip(fitness_scores, poblacion), key=lambda item: item[0], reverse=True)]
        fitness_ordenado = sorted(fitness_scores, reverse=True)

        mejor_fitness_gen = fitness_ordenado[0]
        if mejor_fitness_gen > mejor_fitness_global:
            mejor_fitness_global = mejor_fitness_gen
            mejor_ruta_global = poblacion[0]
            mejor_generacion_fitness = fitness_scores
            mejor_generacion_pareto = [{"puntos": ev["puntos"], "distancia": ev["distancia"]} for ev in evaluaciones]

        # Comprobar estancamiento en la "era" actual
        if mejor_fitness_gen > mejor_fitness_era:
            mejor_fitness_era = mejor_fitness_gen
            generaciones_estancadas = 0
        else:
            generaciones_estancadas += 1

        if generaciones_estancadas >= umbral_estancamiento:
            print(f"\nReiniciando población en generación {generacion} debido a estancamiento.")
            poblacion, fitness_scores = inicializar_poblacion_y_evaluar(tamaño_poblacion, tiempo_disponible)
            generaciones_estancadas = 0
            mejor_fitness_era = 0 
            continue

        tamaño_seleccion = int(tamaño_poblacion * 0.2)
        # 4. Evolucionar la población usando la nueva estrategia
        poblacion = evolucionar_poblacion(poblacion, fitness_scores, tamaño_poblacion, prob_cruce, prob_mutacion, tamaño_seleccion)

        # 9. Guardar para histórico
        historial_fitness.append(mejor_fitness_gen)
        historial_promedio.append(sum(fitness_scores) / len(fitness_scores))

        # 10. Mostrar progreso cada 5 generaciones
        if generacion % 5 == 0 or generacion == generaciones - 1:
            print(f"Gen {generacion:2d}: Mejor fitness = {mejor_fitness_gen:7.2f}, Promedio = {sum(fitness_scores)/len(fitness_scores):7.2f}")

    # Guardar resultados en un archivo JSON
    try:
        with open("resultados_ag.json", "w") as f:
            json.dump({
                "historial_fitness": historial_fitness,
                "historial_promedio": historial_promedio,
                "soluciones_pareto": mejor_generacion_pareto,
                "fitness_final": mejor_generacion_fitness,
                "mejor_ruta": mejor_ruta_global
            }, f, indent=4)
        print("\nResultados guardados en 'resultados_ag.json'.")
    except Exception as e:
        print(f"Error al guardar los resultados: {e}")

    # Resultado final
    evaluacion_final = evaluar_ruta(mejor_ruta_global)
    imprimir_mejor_ruta(mejor_ruta_global, evaluacion_final)
    return {
        "mejor_ruta": mejor_ruta_global,
        "evaluacion": evaluacion_final,
        "historial_fitness": historial_fitness,
        "algoritmo": "Genético Reemplazo Mixto"
    }

def imprimir_mejor_ruta(ruta: List[int], evaluacion: dict):
    print("\n" + "="*50)
    print("🏆 MEJOR RUTA ENCONTRADA 🏆")
    print("="*50)

    hora_actual = 9 * 60  # 9:00 AM
    almuerzo_tomado = False
    cena_tomada = False

    for i, lugar_idx in enumerate(ruta):
        lugar = lt[lugar_idx]
        
        # Tiempo de traslado
        if i > 0:
            lugar_anterior = lt[ruta[i-1]]
            distancia = distancia_haversine(lugar_anterior, lugar)
            t_traslado = distancia * 25
            # Redondear el tiempo de traslado al múltiplo de 5 más cercano hacia arriba
            t_traslado = ((int(t_traslado) + 4) // 5) * 5
            hora_actual += t_traslado
            print(f"  -> Traslado: {t_traslado:.0f} min")

        # Hora de llegada y espera
        apertura = int(lugar["apertura"].split(":")[0]) * 60 + int(lugar["apertura"].split(":")[1])
        hora_llegada = hora_actual
        if hora_llegada < apertura:
            hora_actual = apertura
        
        # Determinar si es comida/cena
        etiqueta_comida = ""
        if not almuerzo_tomado and lugar["tipo"] == "restaurante" and hora_actual >= 13.5 * 60:
            etiqueta_comida = " (Comida)"
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
    print(f"  - Tiempo total: {evaluacion['tiempo']:.2f} min (de {t_dia} disponibles)")
    print(f"  - Penalización por tiempo: {evaluacion.get('tiempo_penalizacion', 0):.2f}")
    print(f"  - Penalización por comidas: {evaluacion.get('comida_penalizacion', 0):.2f}")
    print(f"  - Fitness final: {evaluacion['fitness']:.2f}")
    print(f"  - Ruta válida: {'Sí' if evaluacion['valida'] else 'No'}")
    print("="*50)
    
# Ejemplo de uso
if __name__ == "__main__":
    print("OPTIMIZACIÓN CON ALGORITMO GENÉTICO")
    print("="*60)

    resultado = algoritmo_genetico_reemplazo_mixto(600, 10000, 0.8, 0.2)

    print(f"\n🏆 MEJOR SOLUCIÓN ENCONTRADA:")
    imprimir_mejor_ruta(resultado["mejor_ruta"], resultado["evaluacion"])