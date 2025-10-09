import random
from typing import List, Tuple, Dict, Optional
from utils import lugares_turisticos as lt, distancia_haversine
import json
try:
    from restricciones_complejas import (
        validar_incompatibilidades,
        calcular_bonus_sinergia,
        calcular_bonus_eventos,
        validar_presupuesto,
        calcular_costo_transporte,
        aplicar_perfil_usuario,
        aplicar_condiciones_climaticas,
        calcular_factor_fatiga,
        generar_clima_dias,
        EVENTOS_ESPECIALES,
        calcular_complejidad
    )
    RESTRICCIONES_ACTIVAS = True
except ImportError:
    print("⚠️  Módulo 'restricciones_complejas' no encontrado. Ejecutando sin restricciones avanzadas.")
    RESTRICCIONES_ACTIVAS = False

t_dia = 16 * 60  # 16 horas disponibles por día (960 minutos)
tm_visita = 75   # 75 minutos promedio por lugar
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

def crear_ruta(t_dia: int = t_dia, n_lugares: int = len(lt), vetos: List[int] = None) -> List[int]:
    if vetos is None:
        vetos = []
    
    # Filtrar lugares disponibles excluyendo los vetados
    lugares_disponibles = [i for i in range(len(lt)) if i not in vetos]
    
    if not lugares_disponibles:
        return []
    
    max_lugares_dinamico = min(len(lugares_disponibles), t_dia // tm_visita)
    if max_lugares_dinamico < 4:
        max_lugares_dinamico = min(len(lugares_disponibles), 4)
    
    n_lugares_seleccion = random.randint(min(4, len(lugares_disponibles)), max_lugares_dinamico)
    ruta = random.sample(lugares_disponibles, n_lugares_seleccion)
    
    # Asegurar que hay al menos un restaurante
    if not any(lt[i]['tipo'] == 'restaurante' for i in ruta):
        rest = [i for i in lugares_disponibles if lt[i]['tipo'] == 'restaurante']
        if rest:
            ruta[0] = random.choice(rest)
    return ruta

def crear_poblacion_inicial(tamaño_poblacion: int, tiempo_disponible: int, vetos: List[int] = None) -> List[List[int]]:
    if vetos is None:
        vetos = []
    
    poblacion = []

    while len(poblacion) < tamaño_poblacion:
        ruta = crear_ruta(tiempo_disponible, vetos=vetos)
        if ruta and ruta not in poblacion:
            poblacion.append(ruta)

    return poblacion

def evaluar_ruta(ruta: List[int], tiempo_max: int = t_dia, hora_actual: int = 9 * 60, 
                 dia: int = 1, perfil_usuario: str = "balanceado", clima: str = "soleado",
                 usar_restricciones: bool = True) -> dict:
    """
    Evalúa una ruta considerando múltiples restricciones complejas.
    
    Args:
        ruta: Lista de índices de lugares a visitar
        tiempo_max: Tiempo máximo disponible en minutos
        hora_actual: Hora de inicio en minutos desde las 00:00
        dia: Día del viaje (para eventos especiales)
        perfil_usuario: Perfil de preferencias del usuario
        clima: Condiciones climáticas del día
        usar_restricciones: Si True, aplica restricciones complejas
        
    Returns:
        dict con métricas de evaluación
    """
    if not ruta:
        return {"puntos": 0, "distancia": 0, "tiempo": 0, "fitness": 0, "valida": False, 
                "costo": 0, "bonus_sinergia": 0, "bonus_eventos": 0}

    puntos_t, distancia_t, tiempo_total = 0, 0, 0
    penalizacion = 0
    almuerzo_tomado, cena_tomada = False, False
    costo_total = 0
    bonus_sinergia = 0
    bonus_eventos = 0
    detalles_transporte = []

    # ===== VALIDACIONES CON RESTRICCIONES COMPLEJAS =====
    if RESTRICCIONES_ACTIVAS and usar_restricciones:
        # 1. Validar incompatibilidades
        es_compatible, pen_incomp = validar_incompatibilidades(ruta, lt)
        penalizacion += pen_incomp
        
        # 2. Calcular bonus por sinergias
        bonus_sinergia = calcular_bonus_sinergia(ruta, lt)
        
        # 3. Calcular bonus por eventos especiales
        bonus_eventos = calcular_bonus_eventos(ruta, lt, dia)
        
        # 4. Validar presupuesto
        dentro_presupuesto, costo_ruta, pen_presupuesto = validar_presupuesto(ruta, lt)
        costo_total = costo_ruta
        penalizacion += pen_presupuesto

    # ===== EVALUACIÓN ESTÁNDAR =====
    for i, lugar_idx in enumerate(ruta):
        lugar = lt[lugar_idx]
        
        if i > 0:
            lugar_anterior = lt[ruta[i-1]]
            distancia = distancia_haversine(lugar_anterior, lugar)
            distancia_t += distancia
            
            # Usar transporte inteligente si las restricciones están activas
            if RESTRICCIONES_ACTIVAS and usar_restricciones:
                tipo_trans, t_traslado, costo_trans = calcular_costo_transporte(distancia, priorizar_economia=True)
                costo_total += costo_trans
                detalles_transporte.append({"tipo": tipo_trans, "distancia": distancia, "costo": costo_trans})
            else:
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

        # Penalización/bonus por comidas
        penalizacion_comida, almuerzo_tomado, cena_tomada = calcular_penalizacion_comida(
            hora_actual, lugar["tipo"], almuerzo_tomado, cena_tomada
        )
        penalizacion += penalizacion_comida

        # Calcular puntos ajustados
        puntos_lugar = lugar["puntos"]
        
        if RESTRICCIONES_ACTIVAS and usar_restricciones:
            # Aplicar factor de fatiga
            factor_fatiga = calcular_factor_fatiga(hora_actual)
            puntos_lugar *= factor_fatiga
            
            # Aplicar perfil de usuario
            puntos_lugar = aplicar_perfil_usuario(puntos_lugar, lugar["tipo"], perfil_usuario)
            
            # Aplicar condiciones climáticas
            puntos_lugar = aplicar_condiciones_climaticas(puntos_lugar, lugar["tipo"], clima)
        
        puntos_t += puntos_lugar
        
        # Actualizar tiempo
        tiempo_visita = lugar["tiempo_visita"]
        tiempo_total += tiempo_visita
        hora_actual += tiempo_visita

    # Penalizaciones finales
    if not almuerzo_tomado:
        penalizacion += 100
    if not cena_tomada:
        penalizacion += 100

    # Añadir bonus
    puntos_t += bonus_sinergia + bonus_eventos

    fitness = calcular_fitness(1, 1, puntos_t, distancia_t, tiempo_total, tiempo_max, penalizacion)

    return {
        "puntos": round(puntos_t, 2),
        "distancia": round(distancia_t, 2),
        "tiempo": round(tiempo_total, 2),
        "fitness": max(0, round(fitness, 2)),
        "valida": tiempo_total <= tiempo_max and (not RESTRICCIONES_ACTIVAS or costo_total <= 150),
        "comida_penalizacion": penalizacion,
        "tiempo_penalizacion": 0,
        "costo": round(costo_total, 2) if RESTRICCIONES_ACTIVAS else 0,
        "bonus_sinergia": round(bonus_sinergia, 2) if RESTRICCIONES_ACTIVAS else 0,
        "bonus_eventos": round(bonus_eventos, 2) if RESTRICCIONES_ACTIVAS else 0,
        "detalles_transporte": detalles_transporte if RESTRICCIONES_ACTIVAS else [],
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

def mutacion(ruta: List[int], prob_mutacion: float = 0.1, vetos: List[int] = None) -> List[int]:
    if vetos is None:
        vetos = []
    
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
            # Filtrar lugares disponibles excluyendo los ya en la ruta y los vetados
            lugares_disponibles = [i for i in range(len(lt)) if i not in ruta_mutada and i not in vetos]
            if lugares_disponibles:
                ruta_mutada.append(random.choice(lugares_disponibles))
        
        elif tipo_mutacion == 'quitar' and len(ruta_mutada) > 2:
            idx = random.randint(0, len(ruta_mutada) - 1)
            ruta_mutada.pop(idx)
    
    return ruta_mutada

def inicializar_poblacion_y_evaluar(tamaño_poblacion: int, tiempo_disponible: int, vetos: List[int] = None, w_puntos: float = 1, w_distancia: float = 1):
    if vetos is None:
        vetos = []
    
    poblacion = crear_poblacion_inicial(tamaño_poblacion, tiempo_disponible, vetos)
    fitness_scores = []
    for ruta in poblacion:
        ev = evaluar_ruta(ruta, tiempo_disponible)
        fitness = calcular_fitness(w_puntos, w_distancia, ev["puntos"], ev["distancia"], ev["tiempo"], tiempo_disponible, ev["comida_penalizacion"])
        fitness_scores.append(fitness)
    return poblacion, fitness_scores

def evolucionar_poblacion(poblacion: List[List[int]], fitness_scores: List[float], tamaño_poblacion: int, prob_cruce: float, prob_mutacion: float, tamaño_seleccion: int = 200, vetos: List[int] = None):
    if vetos is None:
        vetos = []
    
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

        hijos.extend([mutacion(hijo1, prob_mutacion, vetos), mutacion(hijo2, prob_mutacion, vetos)])

    nueva_poblacion.extend(hijos)
    return nueva_poblacion[:tamaño_poblacion]

def algoritmo_genetico_reemplazo_mixto(generaciones: int = 100, tamaño_poblacion: int = 1000, 
                                        prob_cruce: float = 0.8, prob_mutacion: float = 0.3, 
                                        tiempo_disponible: int = t_dia, w_puntos: float = 1, w_distancia: float = 1,
                                        vetos: List[int] = None, 
                                        dia: int = 1, 
                                        perfil_usuario: str = "estandar", 
                                        clima: str = "soleado",
                                        usar_restricciones: bool = True) -> dict:
    if vetos is None:
        vetos = []
    
    print(f"\n🧬 ALGORITMO GENÉTICO (REEMPLAZO MIXTO)")
    print(f"Generaciones: {generaciones}, Población: {tamaño_poblacion}")
    print(f"Prob. cruce: {prob_cruce}, Prob. mutación: {prob_mutacion}")
    print(f"Pesos: Puntos={w_puntos:.2f}, Distancia={w_distancia:.2f}")
    print("="*50)

    poblacion, fitness_scores = inicializar_poblacion_y_evaluar(tamaño_poblacion, tiempo_disponible, vetos, w_puntos, w_distancia)
    
    mejor_fitness_global = 0
    mejor_ruta_global = []
    mejor_generacion_fitness = []
    mejor_generacion_pareto = []

    mejor_fitness_era = 0
    generaciones_estancadas = 0
    umbral_estancamiento = 30  # Reset tras 30 generaciones sin mejora

    historial_fitness = []
    historial_promedio = []
    soluciones_pareto = []
    fitness_final = []

    for generacion in range(generaciones):
        evaluaciones = [
            evaluar_ruta(ruta, tiempo_disponible, dia=dia, perfil_usuario=perfil_usuario, clima=clima, usar_restricciones=usar_restricciones) 
            for ruta in poblacion
        ]
        fitness_scores = [calcular_fitness(w_puntos, w_distancia, ev["puntos"], ev["distancia"], ev["tiempo"], tiempo_disponible, ev["comida_penalizacion"]) for ev in evaluaciones]

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
            poblacion, fitness_scores = inicializar_poblacion_y_evaluar(tamaño_poblacion, tiempo_disponible, vetos, w_puntos, w_distancia)
            generaciones_estancadas = 0
            mejor_fitness_era = 0 
            continue

        tamaño_seleccion = int(tamaño_poblacion * 0.2)
        # 4. Evolucionar la población usando la nueva estrategia
        poblacion = evolucionar_poblacion(poblacion, fitness_scores, tamaño_poblacion, prob_cruce, prob_mutacion, tamaño_seleccion, vetos)

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
    evaluacion_final = evaluar_ruta(mejor_ruta_global, tiempo_disponible, dia=dia, perfil_usuario=perfil_usuario, clima=clima, usar_restricciones=usar_restricciones)
    imprimir_mejor_ruta(mejor_ruta_global, evaluacion_final)
    return {
        "mejor_ruta": mejor_ruta_global,
        "evaluacion": evaluacion_final,
        "historial_fitness": historial_fitness,
        "algoritmo": "Genético Reemplazo Mixto"
    }

def algoritmo_genetico_multidias(generaciones: int = 100, tamaño_poblacion: int = 1000, 
                                 prob_cruce: float = 0.8, prob_mutacion: float = 0.3, 
                                 dias: int = 5, tiempo_disponible: int = t_dia,
                                 perfil_usuario: str = "balanceado",
                                 usar_restricciones: bool = True) -> dict:
    """
    Algoritmo genético para optimizar rutas de múltiples días.
    Ejecuta el algoritmo de UN DÍA múltiples veces, acumulando vetos de lugares visitados.
    
    Args:
        generaciones: Número de generaciones por día
        tamaño_poblacion: Tamaño de la población
        prob_cruce: Probabilidad de cruce
        prob_mutacion: Probabilidad de mutación
        dias: Número de días del viaje
        tiempo_disponible: Tiempo disponible por día en minutos
        perfil_usuario: Perfil de preferencias del usuario
        usar_restricciones: Si True, aplica restricciones complejas
    """
    print(f"\n🧬 ALGORITMO GENÉTICO MULTIDÍAS {'CON RESTRICCIONES COMPLEJAS' if usar_restricciones and RESTRICCIONES_ACTIVAS else 'BÁSICO'}")
    print(f"Días: {dias}, Generaciones por día: {generaciones}, Población: {tamaño_poblacion}")
    print(f"Prob. cruce: {prob_cruce}, Prob. mutación: {prob_mutacion}")
    print(f"Perfil de usuario: {perfil_usuario}")
    
    # Mostrar estadísticas de complejidad si las restricciones están activas
    if RESTRICCIONES_ACTIVAS and usar_restricciones:
        print("\n" + "="*70)
        print("📊 ANÁLISIS DE COMPLEJIDAD DEL PROBLEMA")
        print("="*70)
        complejidad = calcular_complejidad(len(lt), dias)
        print(f"Lugares totales disponibles: {complejidad['num_lugares_total']}")
        print(f"Combinaciones posibles por día: {complejidad['combinaciones_por_dia']:,.0f}")
        print(f"Espacio de búsqueda total: {complejidad['espacio_busqueda_total']:.2e}")
        print(f"Espacio de búsqueda válido (con restricciones): {complejidad['espacio_busqueda_valido']:.2e}")
        print(f"\n🔒 Restricciones activas:")
        for nombre, valor in complejidad['restricciones'].items():
            print(f"   - {nombre.replace('_', ' ').title()}: {valor}")
    
    print("="*70)

    # Generar clima para cada día si las restricciones están activas
    climas = generar_clima_dias(dias) if RESTRICCIONES_ACTIVAS and usar_restricciones else {d: "soleado" for d in range(1, dias+1)}

    vetos = []
    resultados_dias = []
    historial_completo = {
        "dias": [],
        "mejor_fitness_total": 0,
        "distancia_total": 0,
        "puntos_totales": 0,
        "tiempo_total": 0,
        "costo_total": 0,
        "bonus_sinergia_total": 0,
        "bonus_eventos_total": 0,
    }

    for dia in range(1, dias + 1):
        print(f"\n{'='*70}")
        print(f"🌅 DÍA {dia} / {dias}")
        if RESTRICCIONES_ACTIVAS and usar_restricciones:
            clima_dia = climas[dia]
            print(f"🌤️  Clima: {clima_dia.upper()}")
        print(f"{'='*70}")
        print(f"Lugares vetados hasta ahora: {len(vetos)}")
        
        # Ajustar pesos: más importancia a la distancia cada día
        w_distancia = 1 + (dia - 1) * 0.25 / 2
        w_puntos = 0.9 - ((dia - 1) * 0.05) / 2
        
        print(f"Pesos del día: Puntos={w_puntos:.2f}, Distancia={w_distancia:.2f}")

        # ✅ LLAMAR AL ALGORITMO DE UN DÍA con los vetos actuales
        resultado_dia_ag = algoritmo_genetico_reemplazo_mixto(
            generaciones=generaciones,
            tamaño_poblacion=tamaño_poblacion,
            prob_cruce=prob_cruce,
            prob_mutacion=prob_mutacion,
            tiempo_disponible=tiempo_disponible,
            vetos=vetos.copy(),  # Pasar copia de vetos
            w_puntos=w_puntos,
            w_distancia=w_distancia,
            dia=dia,  # Pasar el día
            perfil_usuario=perfil_usuario,  # Pasar el perfil
            clima=climas.get(dia, "soleado"),  # Pasar el clima del día
            usar_restricciones=usar_restricciones  # Pasar si usar restricciones
        )
        
        # Extraer la mejor ruta y evaluación del resultado
        mejor_ruta_global = resultado_dia_ag["mejor_ruta"]
        mejor_evaluacion = evaluar_ruta(
            mejor_ruta_global, tiempo_disponible,
            dia=dia,
            perfil_usuario=perfil_usuario,
            clima=climas.get(dia, "soleado"),
            usar_restricciones=usar_restricciones
        )

        # Actualizar vetos con los lugares visitados en la mejor ruta del día
        vetos.extend(mejor_ruta_global)
        
        # Guardar resultados del día
        resultado_dia = {
            "dia": dia,
            "mejor_ruta": mejor_ruta_global,
            "evaluacion": mejor_evaluacion,
            "fitness": mejor_evaluacion["fitness"],
            "puntos": mejor_evaluacion["puntos"],
            "distancia": mejor_evaluacion["distancia"],
            "tiempo": mejor_evaluacion["tiempo"],
            "costo": mejor_evaluacion.get("costo", 0),
            "bonus_sinergia": mejor_evaluacion.get("bonus_sinergia", 0),
            "bonus_eventos": mejor_evaluacion.get("bonus_eventos", 0),
            "w_puntos": w_puntos,
            "w_distancia": w_distancia,
            "clima": climas.get(dia, "soleado") if RESTRICCIONES_ACTIVAS else "soleado",
        }
        resultados_dias.append(resultado_dia)

        # Acumular totales
        historial_completo["dias"].append({
            "dia": dia,
            "fitness": mejor_evaluacion["fitness"],
            "puntos": mejor_evaluacion["puntos"],
            "distancia": mejor_evaluacion["distancia"],
            "tiempo": mejor_evaluacion["tiempo"],
            "costo": mejor_evaluacion.get("costo", 0),
            "clima": climas.get(dia, "soleado") if RESTRICCIONES_ACTIVAS else "soleado",
        })
        historial_completo["mejor_fitness_total"] += mejor_evaluacion["fitness"]
        historial_completo["distancia_total"] += mejor_evaluacion["distancia"]
        historial_completo["puntos_totales"] += mejor_evaluacion["puntos"]
        historial_completo["tiempo_total"] += mejor_evaluacion["tiempo"]
        historial_completo["costo_total"] += mejor_evaluacion.get("costo", 0)
        historial_completo["bonus_sinergia_total"] += mejor_evaluacion.get("bonus_sinergia", 0)
        historial_completo["bonus_eventos_total"] += mejor_evaluacion.get("bonus_eventos", 0)

        # Resumen del día
        print(f"\n✅ Día {dia} completado:")
        print(f"   Fitness: {mejor_evaluacion['fitness']:.2f}")
        print(f"   Puntos: {mejor_evaluacion['puntos']:.2f}")
        print(f"   Distancia: {mejor_evaluacion['distancia']:.2f} km")
        if RESTRICCIONES_ACTIVAS and usar_restricciones:
            print(f"   Costo: {mejor_evaluacion.get('costo', 0):.2f} €")
            print(f"   Bonus sinergia: {mejor_evaluacion.get('bonus_sinergia', 0):.2f}")
            print(f"   Bonus eventos: {mejor_evaluacion.get('bonus_eventos', 0):.2f}")
        print(f"   Lugares visitados: {len(mejor_ruta_global)}")
        print(f"   Total lugares vetados: {len(vetos)}")

    # Guardar resultados en archivo JSON
    try:
        nombre_archivo = f"resultados_ag_multidias_{'complejo' if usar_restricciones else 'basico'}.json"
        with open(nombre_archivo, "w", encoding='utf-8') as f:
            json.dump({
                "configuracion": {
                    "dias": dias,
                    "generaciones": generaciones,
                    "tamaño_poblacion": tamaño_poblacion,
                    "prob_cruce": prob_cruce,
                    "prob_mutacion": prob_mutacion,
                    "perfil_usuario": perfil_usuario,
                    "restricciones_activas": usar_restricciones and RESTRICCIONES_ACTIVAS,
                },
                "resultados_por_dia": resultados_dias,
                "resumen_total": historial_completo,
                "climas": climas if RESTRICCIONES_ACTIVAS else {},
            }, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Resultados guardados en '{nombre_archivo}'.")
    except Exception as e:
        print(f"❌ Error al guardar los resultados: {e}")

    # Imprimir resumen final
    imprimir_resumen_multidias(resultados_dias, historial_completo, usar_restricciones and RESTRICCIONES_ACTIVAS)
    
    return {
        "resultados_dias": resultados_dias,
        "historial_completo": historial_completo,
        "algoritmo": f"Genético Multidías {'con Restricciones Complejas' if usar_restricciones and RESTRICCIONES_ACTIVAS else 'Básico'}"
    }

def imprimir_resumen_multidias(resultados_dias: List[dict], historial_completo: dict, con_restricciones: bool = False):
    """Imprime un resumen de todos los días del viaje"""
    print("\n" + "="*70)
    print("🎯 RESUMEN COMPLETO DEL VIAJE")
    print("="*70)
    
    for resultado in resultados_dias:
        dia = resultado["dia"]
        print(f"\n📅 DÍA {dia}:")
        if con_restricciones:
            print(f"   Clima: {resultado.get('clima', 'soleado').title()}")
        print(f"   Pesos utilizados: Puntos={resultado['w_puntos']:.2f}, Distancia={resultado['w_distancia']:.2f}")
        print(f"   Lugares visitados: {len(resultado['mejor_ruta'])}")
        print(f"   Puntos: {resultado['puntos']:.2f}")
        print(f"   Distancia: {resultado['distancia']:.2f} km")
        print(f"   Tiempo: {resultado['tiempo']:.2f} min")
        if con_restricciones:
            print(f"   Costo: {resultado.get('costo', 0):.2f} €")
            print(f"   Bonus sinergia: {resultado.get('bonus_sinergia', 0):.2f}")
            print(f"   Bonus eventos: {resultado.get('bonus_eventos', 0):.2f}")
        print(f"   Fitness: {resultado['fitness']:.2f}")
        
        # Mostrar los lugares
        print(f"   Ruta:")
        for i, lugar_idx in enumerate(resultado['mejor_ruta']):
            lugar = lt[lugar_idx]
            print(f"      {i+1}. {lugar['nombre']} ({lugar['puntos']} pts)")
    
    print("\n" + "="*70)
    print("📊 TOTALES DEL VIAJE:")
    print(f"   Fitness total acumulado: {historial_completo['mejor_fitness_total']:.2f}")
    print(f"   Puntos totales: {historial_completo['puntos_totales']:.2f}")
    print(f"   Distancia total recorrida: {historial_completo['distancia_total']:.2f} km")
    print(f"   Tiempo total: {historial_completo['tiempo_total']:.2f} min ({historial_completo['tiempo_total']/60:.2f} horas)")
    if con_restricciones:
        print(f"   Costo total: {historial_completo.get('costo_total', 0):.2f} €")
        print(f"   Bonus sinergia total: {historial_completo.get('bonus_sinergia_total', 0):.2f}")
        print(f"   Bonus eventos total: {historial_completo.get('bonus_eventos_total', 0):.2f}")
    print(f"   Lugares únicos visitados: {sum(len(r['mejor_ruta']) for r in resultados_dias)}")
    print("="*70)

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
    
    # Opción para elegir el modo
    import sys
    
    modo = "un_dia"  # Cambiar a "multidias" para ejecutar el algoritmo de múltiples días
    
    if len(sys.argv) > 1:
        modo = sys.argv[1]
    
    if modo == "multidias":
        print("\n🗓️  MODO: PLANIFICACIÓN DE VIAJE DE MÚLTIPLES DÍAS")
        print("="*60)
        
        resultado = algoritmo_genetico_multidias(
            generaciones=300,      # Menos generaciones por día
            tamaño_poblacion=10000,  # Población reducida
            prob_cruce=0.8,
            prob_mutacion=0.2,
            dias=5                  # Número de días
        )
        
        print(f"\n🏆 VIAJE DE {len(resultado['resultados_dias'])} DÍAS COMPLETADO")
        print(f"Fitness total: {resultado['historial_completo']['mejor_fitness_total']:.2f}")
        print(f"Lugares únicos visitados: {sum(len(r['mejor_ruta']) for r in resultado['resultados_dias'])}")
        
    else:
        print("\n📅 MODO: PLANIFICACIÓN DE UN DÍA")
        print("="*60)
        
        resultado = algoritmo_genetico_reemplazo_mixto(600, 10000, 0.8, 0.2)

        print(f"\n🏆 MEJOR SOLUCIÓN ENCONTRADA:")
        imprimir_mejor_ruta(resultado["mejor_ruta"], resultado["evaluacion"])