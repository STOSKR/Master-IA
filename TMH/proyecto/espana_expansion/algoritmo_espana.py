import random
from typing import List, Dict, Tuple
from config import *
from utils_espana import (
    lugares_turisticos_espana,
    get_lugares_ciudad,
    get_lugares_por_ids,
    calcular_transporte_intercity,
    distancia_haversine,
    COORDENADAS_CIUDADES
)
from restricciones_espana import (
    validar_limite_ciudad,
    calcular_penalizacion_cambio_ciudad,
    aplicar_restricciones_basicas
)

class Individual:
    def __init__(self, dias: List[List[int]], ciudades: List[str]):
        self.dias = dias
        self.ciudades = ciudades
        self.fitness = 0
        self.tiempo_total = 0
        self.puntos_totales = 0
        self.distancia_total = 0

def crear_individuo_aleatorio(num_dias: int, lugares_por_dia: int) -> Individual:
    ciudades_disponibles = list(COORDENADAS_CIUDADES.keys())
    dias = []
    ciudades_plan = []
    historial_ciudad = []
    
    for dia in range(num_dias):
        # Seleccionar ciudad válida
        if historial_ciudad and len(historial_ciudad) >= MAX_DIAS_POR_CIUDAD:
            ultimos = historial_ciudad[-MAX_DIAS_POR_CIUDAD:]
            if len(set(ultimos)) == 1:  # Todos iguales
                ciudad_actual = random.choice([c for c in ciudades_disponibles if c != ultimos[0]])
            else:
                ciudad_actual = random.choice(ciudades_disponibles)
        else:
            ciudad_actual = random.choice(ciudades_disponibles)
        
        # Generar lugares del día
        lugares_ciudad = get_lugares_ciudad(ciudad_actual)
        if len(lugares_ciudad) < lugares_por_dia:
            lugares_ciudad = lugares_turisticos_espana
        
        lugares_dia = random.sample(lugares_ciudad, min(lugares_por_dia, len(lugares_ciudad)))
        ids_dia = [l["id"] for l in lugares_dia]
        random.shuffle(ids_dia)
        
        dias.append(ids_dia)
        ciudades_plan.append(ciudad_actual)
        historial_ciudad.append(ciudad_actual)
    
    return Individual(dias, ciudades_plan)

def crear_poblacion_inicial(tam_poblacion: int, num_dias: int, lugares_por_dia: int) -> List[Individual]:
    """Genera población inicial con diversidad"""
    return [crear_individuo_aleatorio(num_dias, lugares_por_dia) for _ in range(tam_poblacion)]

# ============================================================================
# EVALUACIÓN DE FITNESS
# ============================================================================

def calcular_tiempo_dia(individuo: Individual, dia_idx: int) -> Tuple[int, int, float]:
    """Calcula tiempo, distancia y puntos para un día específico"""
    dia = individuo.dias[dia_idx]
    ciudad = individuo.ciudades[dia_idx]
    
    if not dia:
        return 0, 0, 0
    
    # Usar función optimizada O(n) en lugar de O(n²)
    lugares_dia = get_lugares_por_ids(dia)
    tiempo_total = 0
    distancia_total = 0
    puntos_total = 0
    
    # Tiempo de visitas
    for lugar in lugares_dia:
        tiempo_total += lugar["tiempo_visita"]
        puntos_total += lugar["puntos"]
    
    # Distancias entre lugares
    for i in range(len(lugares_dia) - 1):
        dist = distancia_haversine(lugares_dia[i], lugares_dia[i + 1])
        distancia_total += dist
        tiempo_total += dist / VELOCIDAD_MEDIA_KMH * 60
    
    # Tiempo comida
    if tiempo_total > 180:
        tiempo_total += TIEMPO_COMIDA_MIN
    if tiempo_total > 480:
        tiempo_total += TIEMPO_CENA_MIN
    
    return tiempo_total, distancia_total, puntos_total

def evaluar_individuo(individuo: Individual) -> float:
    """Calcula fitness considerando restricciones, transporte intercity y cambios de ciudad"""
    fitness = 0
    tiempo_acum = 0
    distancia_acum = 0
    puntos_acum = 0
    
    for dia_idx in range(len(individuo.dias)):
        tiempo_dia, dist_dia, puntos_dia = calcular_tiempo_dia(individuo, dia_idx)
        
        # Transporte intercity si cambia de ciudad
        if dia_idx > 0 and individuo.ciudades[dia_idx] != individuo.ciudades[dia_idx - 1]:
            tiempo_trans, _ = calcular_transporte_intercity(
                individuo.ciudades[dia_idx - 1],
                individuo.ciudades[dia_idx],
                "tren"
            )
            if tiempo_trans:
                tiempo_dia += tiempo_trans
            
            # Penalización leve por cambio
            pen_cambio = calcular_penalizacion_cambio_ciudad(
                individuo.ciudades[:dia_idx + 1]
            )
            fitness -= pen_cambio
        
        # Penalizaciones básicas
        pen_fatiga = aplicar_restricciones_basicas(individuo.dias[dia_idx], tiempo_dia)
        fitness -= pen_fatiga
        
        # Validar límite de ciudad
        if not validar_limite_ciudad(individuo.ciudades[:dia_idx + 1], individuo.ciudades[dia_idx]):
            fitness -= PENALIZACION_LIMITE_CIUDAD
        
        # Penalizar exceso de tiempo
        if tiempo_dia > TIEMPO_DIA:
            fitness -= PENALIZACION_EXCESO_TIEMPO * (tiempo_dia - TIEMPO_DIA) / 60
        
        # Acumular métricas
        tiempo_acum += tiempo_dia
        distancia_acum += dist_dia
        puntos_acum += puntos_dia
    
    # Fitness = puntos - penalizaciones
    fitness += puntos_acum
    
    # Guardar métricas
    individuo.tiempo_total = tiempo_acum
    individuo.distancia_total = distancia_acum
    individuo.puntos_totales = puntos_acum
    individuo.fitness = fitness
    
    return fitness

# ============================================================================
# OPERADORES GENÉTICOS
# ============================================================================

def seleccion_torneo(poblacion: List[Individual], k: int = 3) -> Individual:
    """Selección por torneo"""
    torneo = random.sample(poblacion, k)
    return max(torneo, key=lambda ind: ind.fitness)

def crossover_dos_puntos(padre1: Individual, padre2: Individual) -> Tuple[Individual, Individual]:
    """Cruce de dos puntos por día"""
    if random.random() > PROBABILIDAD_CRUCE:
        return padre1, padre2
    
    num_dias = len(padre1.dias)
    hijo1_dias = []
    hijo2_dias = []
    hijo1_ciudades = []
    hijo2_ciudades = []
    
    for dia_idx in range(num_dias):
        dia1 = padre1.dias[dia_idx]
        dia2 = padre2.dias[dia_idx]
        
        if len(dia1) < 2 or len(dia2) < 2:
            hijo1_dias.append(dia1[:])
            hijo2_dias.append(dia2[:])
            hijo1_ciudades.append(padre1.ciudades[dia_idx])
            hijo2_ciudades.append(padre2.ciudades[dia_idx])
            continue
        
        punto1 = random.randint(1, len(dia1) - 1)
        punto2 = random.randint(punto1, len(dia1))
        
        nuevo_dia1 = dia1[:punto1] + dia2[punto1:punto2] + dia1[punto2:]
        nuevo_dia2 = dia2[:punto1] + dia1[punto1:punto2] + dia2[punto2:]
        
        hijo1_dias.append(nuevo_dia1)
        hijo2_dias.append(nuevo_dia2)
        hijo1_ciudades.append(padre1.ciudades[dia_idx])
        hijo2_ciudades.append(padre2.ciudades[dia_idx])
    
    return Individual(hijo1_dias, hijo1_ciudades), Individual(hijo2_dias, hijo2_ciudades)

def mutar(individuo: Individual):
    """Aplica múltiples tipos de mutación"""
    for dia_idx in range(len(individuo.dias)):
        dia = individuo.dias[dia_idx]
        ciudad = individuo.ciudades[dia_idx]
        
        if random.random() < PROBABILIDAD_MUTACION:
            tipo = random.choices(
                ["swap", "insert", "reverse", "replace"],
                weights=[0.3, 0.2, 0.2, 0.3]
            )[0]
            
            if tipo == "swap" and len(dia) >= 2:
                i, j = random.sample(range(len(dia)), 2)
                dia[i], dia[j] = dia[j], dia[i]
            
            elif tipo == "insert" and len(dia) >= 2:
                i = random.randint(0, len(dia) - 1)
                j = random.randint(0, len(dia) - 1)
                dia.insert(j, dia.pop(i))
            
            elif tipo == "reverse" and len(dia) >= 2:
                i, j = sorted(random.sample(range(len(dia)), 2))
                dia[i:j+1] = reversed(dia[i:j+1])
            
            elif tipo == "replace":
                lugares_ciudad = get_lugares_ciudad(ciudad)
                if lugares_ciudad:
                    idx = random.randint(0, len(dia) - 1)
                    nuevo = random.choice(lugares_ciudad)["id"]
                    if nuevo not in dia:
                        dia[idx] = nuevo
        
        # Mutación de ciudad (baja probabilidad)
        if random.random() < 0.05:
            ciudades_disponibles = list(COORDENADAS_CIUDADES.keys())
            nueva_ciudad = random.choice([c for c in ciudades_disponibles if c != ciudad])
            individuo.ciudades[dia_idx] = nueva_ciudad
            
            # Reemplazar lugares del día con lugares de nueva ciudad
            lugares_nueva = get_lugares_ciudad(nueva_ciudad)
            if lugares_nueva:
                individuo.dias[dia_idx] = [
                    random.choice(lugares_nueva)["id"] for _ in range(len(dia))
                ]

# ============================================================================
# ALGORITMO PRINCIPAL
# ============================================================================

def algoritmo_genetico_espana(
    num_dias: int = 20,
    lugares_por_dia: int = 12,
    tam_poblacion: int = 8000,
    num_generaciones: int = 500,
    tasa_elitismo: float = 0.20
) -> Dict:
    """
    Ejecuta el algoritmo genético para España
    
    Args:
        num_dias: Días totales de viaje (default: 20)
        lugares_por_dia: Lugares a visitar por día (default: 12)
        tam_poblacion: Tamaño de la población (default: 8000)
        num_generaciones: Generaciones a evolucionar (default: 500)
        tasa_elitismo: % de mejores que pasan directamente (default: 0.20)
    
    Returns:
        Dict con mejor solución y estadísticas
    """
    print(f"\n{'='*80}")
    print(f"🇪🇸 ALGORITMO GENÉTICO - RUTA POR ESPAÑA")
    print(f"{'='*80}")
    print(f"📊 Configuración:")
    print(f"  • Días de viaje: {num_dias}")
    print(f"  • Lugares/día: {lugares_por_dia}")
    print(f"  • Población: {tam_poblacion}")
    print(f"  • Generaciones: {num_generaciones}")
    print(f"  • Elitismo: {tasa_elitismo*100:.0f}%")
    print(f"  • Dataset: {len(lugares_turisticos_espana)} lugares en 10 ciudades")
    print(f"{'='*80}\n")
    
    # Crear población inicial
    print("🧬 Creando población inicial...")
    poblacion = crear_poblacion_inicial(tam_poblacion, num_dias, lugares_por_dia)
    
    # Evaluar población inicial
    print("📊 Evaluando población inicial...")
    for ind in poblacion:
        evaluar_individuo(ind)
    
    mejor_global = max(poblacion, key=lambda ind: ind.fitness)
    historial_fitness = [mejor_global.fitness]
    
    num_elite = int(tam_poblacion * tasa_elitismo)
    
    # Evolución
    print(f"\n🔄 Iniciando evolución ({num_generaciones} generaciones)...\n")
    
    for gen in range(num_generaciones):
        # Ordenar por fitness
        poblacion.sort(key=lambda ind: ind.fitness, reverse=True)
        
        # Elitismo
        nueva_poblacion = poblacion[:num_elite]
        
        # Generar descendencia
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = seleccion_torneo(poblacion)
            padre2 = seleccion_torneo(poblacion)
            
            hijo1, hijo2 = crossover_dos_puntos(padre1, padre2)
            
            mutar(hijo1)
            mutar(hijo2)
            
            evaluar_individuo(hijo1)
            evaluar_individuo(hijo2)
            
            nueva_poblacion.extend([hijo1, hijo2])
        
        poblacion = nueva_poblacion[:tam_poblacion]
        
        # Actualizar mejor
        mejor_gen = max(poblacion, key=lambda ind: ind.fitness)
        if mejor_gen.fitness > mejor_global.fitness:
            mejor_global = mejor_gen
        
        historial_fitness.append(mejor_global.fitness)
        
        # Progreso
        if (gen + 1) % 50 == 0 or gen == 0:
            print(f"  Gen {gen+1:4d}/{num_generaciones} | "
                  f"Mejor fitness: {mejor_global.fitness:8.1f} | "
                  f"Puntos: {mejor_global.puntos_totales:5d} | "
                  f"Tiempo: {mejor_global.tiempo_total/60:6.1f}h | "
                  f"Dist: {mejor_global.distancia_total:7.1f}km")
    
    print(f"\n{'='*80}")
    print(f"✅ OPTIMIZACIÓN COMPLETADA")
    print(f"{'='*80}\n")
    
    return {
        "mejor_individuo": mejor_global,
        "historial_fitness": historial_fitness,
        "poblacion_final": poblacion
    }

# ============================================================================
# UTILIDADES DE ANÁLISIS
# ============================================================================

def analizar_solucion(individuo: Individual):
    """Muestra análisis detallado de una solución"""
    print(f"\n{'='*80}")
    print(f"📋 ANÁLISIS DE LA MEJOR SOLUCIÓN")
    print(f"{'='*80}\n")
    
    print(f"🎯 Métricas Globales:")
    print(f"  • Fitness total: {individuo.fitness:.1f}")
    print(f"  • Puntos totales: {individuo.puntos_totales}")
    print(f"  • Tiempo total: {individuo.tiempo_total/60:.1f} horas")
    print(f"  • Distancia total: {individuo.distancia_total:.1f} km")
    print(f"  • Ciudades visitadas: {len(set(individuo.ciudades))}")
    
    print(f"\n📅 Itinerario por Días:")
    print(f"{'-'*80}")
    
    for dia_idx, (dia, ciudad) in enumerate(zip(individuo.dias, individuo.ciudades), 1):
        lugares_dia = get_lugares_por_ids(dia)
        tiempo_dia, dist_dia, puntos_dia = calcular_tiempo_dia(individuo, dia_idx - 1)
        
        print(f"\n  DÍA {dia_idx} - {ciudad}")
        print(f"  {'─'*76}")
        print(f"    Lugares: {len(lugares_dia)} | "
              f"Puntos: {puntos_dia} | "
              f"Tiempo: {tiempo_dia/60:.1f}h | "
              f"Dist: {dist_dia:.1f}km")
        
        for i, lugar in enumerate(lugares_dia[:5], 1):  # Mostrar primeros 5
            print(f"      {i}. {lugar['nombre'][:45]} ({lugar['tipo']})")
        
        if len(lugares_dia) > 5:
            print(f"      ... y {len(lugares_dia)-5} lugares más")
    
    print(f"\n{'='*80}")

def exportar_resultados(resultados: Dict, archivo: str = "resultados_espana.json"):
    """Exporta resultados a JSON"""
    import json
    
    mejor = resultados["mejor_individuo"]
    
    data = {
        "fitness": mejor.fitness,
        "puntos_totales": mejor.puntos_totales,
        "tiempo_total_min": mejor.tiempo_total,
        "distancia_total_km": mejor.distancia_total,
        "num_dias": len(mejor.dias),
        "ciudades_visitadas": list(set(mejor.ciudades)),
        "itinerario": [
            {
                "dia": i + 1,
                "ciudad": ciudad,
                "lugares_ids": dia,
                "num_lugares": len(dia)
            }
            for i, (dia, ciudad) in enumerate(zip(mejor.dias, mejor.ciudades))
        ],
        "historial_fitness": resultados["historial_fitness"]
    }
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados exportados a: {archivo}")

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    # Ejecutar algoritmo
    resultados = algoritmo_genetico_espana(
        num_dias=20,
        lugares_por_dia=12,
        tam_poblacion=8000,
        num_generaciones=500,
        tasa_elitismo=0.20
    )
    
    # Analizar y exportar
    analizar_solucion(resultados["mejor_individuo"])
    exportar_resultados(resultados)
