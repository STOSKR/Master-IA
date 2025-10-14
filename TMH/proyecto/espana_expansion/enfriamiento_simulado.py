import random
import copy
import math
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

# Importar componentes reutilizables del algoritmo genético
from algoritmo_espana import (
    Individual,
    crear_individuo_aleatorio,
    evaluar_individuo,
    validar_restricciones_ciudades,
    reparar_individuo,
    analizar_solucion
)


def eliminar_duplicados_dia(individuo: Individual) -> Individual:
    """
    Elimina lugares duplicados en cada día, reemplazándolos por lugares únicos de la misma ciudad.
    
    Args:
        individuo: Individuo a limpiar
    
    Returns:
        Individuo sin lugares duplicados
    """
    for dia_idx in range(len(individuo.dias)):
        dia = individuo.dias[dia_idx]
        ciudad = individuo.ciudades[dia_idx]
        
        # Verificar si hay duplicados
        if len(dia) != len(set(dia)):
            # Hay duplicados, necesitamos reemplazarlos
            lugares_ciudad = get_lugares_ciudad(ciudad)
            lugares_unicos = []
            lugares_usados = set()
            
            for lugar_id in dia:
                if lugar_id not in lugares_usados:
                    lugares_unicos.append(lugar_id)
                    lugares_usados.add(lugar_id)
                else:
                    # Buscar un reemplazo que no esté usado
                    lugares_disponibles = [l["id"] for l in lugares_ciudad 
                                          if l["id"] not in lugares_usados]
                    if lugares_disponibles:
                        nuevo_lugar = random.choice(lugares_disponibles)
                        lugares_unicos.append(nuevo_lugar)
                        lugares_usados.add(nuevo_lugar)
                    else:
                        # Si no hay más lugares, mantener el duplicado (caso extremo)
                        lugares_unicos.append(lugar_id)
            
            individuo.dias[dia_idx] = lugares_unicos
    
    return individuo


def generar_vecino(solucion_actual: Individual) -> Individual:
    """
    Genera una solución vecina aplicando perturbaciones mixtas mejoradas:
    - 40% Swap de dos lugares en un día
    - 20% Reemplazar un lugar por otro de la misma ciudad
    - 15% Cambiar ciudad de un día (restricciones relajadas)
    - 15% Swap intercity (intercambiar dos días completos)
    - 10% 2-opt (optimizar orden dentro de un día)
    
    Args:
        solucion_actual: Solución actual
    
    Returns:
        Nueva solución vecina (copia profunda)
    """
    # Crear copia profunda para no modificar la original
    vecino = Individual(
        [dia[:] for dia in solucion_actual.dias],
        solucion_actual.ciudades[:]
    )
    
    # Elegir tipo de perturbación según probabilidades mejoradas
    tipo_perturbacion = random.choices(
        ["swap", "reemplazar", "cambiar_ciudad", "swap_intercity", "ruta_2opt"],
        weights=[0.40, 0.20, 0.15, 0.15, 0.10]
    )[0]
    
    if tipo_perturbacion == "swap":
        # Swap de dos lugares en un día aleatorio
        dia_idx = random.randint(0, len(vecino.dias) - 1)
        dia = vecino.dias[dia_idx]
        
        if len(dia) >= 2:
            i, j = random.sample(range(len(dia)), 2)
            dia[i], dia[j] = dia[j], dia[i]
    
    elif tipo_perturbacion == "reemplazar":
        # Reemplazar un lugar por otro de la misma ciudad
        dia_idx = random.randint(0, len(vecino.dias) - 1)
        ciudad = vecino.ciudades[dia_idx]
        lugares_ciudad = get_lugares_ciudad(ciudad)
        
        if lugares_ciudad and len(vecino.dias[dia_idx]) > 0:
            idx_lugar = random.randint(0, len(vecino.dias[dia_idx]) - 1)
            
            # Buscar un lugar que no esté ya en el día
            lugares_disponibles = [l["id"] for l in lugares_ciudad if l["id"] not in vecino.dias[dia_idx]]
            
            if lugares_disponibles:
                nuevo_lugar = random.choice(lugares_disponibles)
                vecino.dias[dia_idx][idx_lugar] = nuevo_lugar
    
    elif tipo_perturbacion == "cambiar_ciudad":
        # Cambiar ciudad de un día con restricciones relajadas
        dia_idx = random.randint(0, len(vecino.dias) - 1)
        ciudad_actual = vecino.ciudades[dia_idx]
        ciudades_disponibles = list(COORDENADAS_CIUDADES.keys())
        
        # Solo evitar la misma ciudad (restricciones relajadas)
        candidatas = [c for c in ciudades_disponibles if c != ciudad_actual]
        
        # Si hay candidatas, cambiar
        if candidatas:
            nueva_ciudad = random.choice(candidatas)
            vecino.ciudades[dia_idx] = nueva_ciudad
            
            # Reemplazar lugares del día con lugares de la nueva ciudad (sin repetir)
            lugares_nueva = get_lugares_ciudad(nueva_ciudad)
            if lugares_nueva:
                num_lugares = len(vecino.dias[dia_idx])
                # Usar sample para garantizar lugares únicos
                if len(lugares_nueva) >= num_lugares:
                    lugares_seleccionados = random.sample(lugares_nueva, num_lugares)
                    vecino.dias[dia_idx] = [l["id"] for l in lugares_seleccionados]
                else:
                    # Si no hay suficientes lugares, usar todos los disponibles
                    vecino.dias[dia_idx] = [l["id"] for l in lugares_nueva]
    
    elif tipo_perturbacion == "swap_intercity":
        # NUEVO: Intercambiar dos días completos (incluidas ciudades)
        if len(vecino.dias) >= 2:
            i, j = random.sample(range(len(vecino.dias)), 2)
            # Intercambiar días
            vecino.dias[i], vecino.dias[j] = vecino.dias[j], vecino.dias[i]
            # Intercambiar ciudades
            vecino.ciudades[i], vecino.ciudades[j] = vecino.ciudades[j], vecino.ciudades[i]
    
    elif tipo_perturbacion == "ruta_2opt":
        # NUEVO: Optimización 2-opt dentro de un día (invertir segmento)
        dia_idx = random.randint(0, len(vecino.dias) - 1)
        dia = vecino.dias[dia_idx]
        
        if len(dia) >= 4:
            # Elegir dos puntos de corte
            i = random.randint(0, len(dia) - 3)
            j = random.randint(i + 2, len(dia))
            # Invertir el segmento entre i y j
            vecino.dias[dia_idx] = dia[:i+1] + dia[i+1:j][::-1] + dia[j:]
    
    # Validar y reparar si es necesario
    if not validar_restricciones_ciudades(vecino):
        vecino = reparar_individuo(vecino)
    
    # Eliminar duplicados en cada día
    vecino = eliminar_duplicados_dia(vecino)
    
    return vecino


def calcular_temperatura_inicial(solucion_inicial: Individual, num_muestras: int = 100) -> float:
    """
    Calcula la temperatura inicial basada en la varianza de vecinos.
    
    Estrategia: Generar varios vecinos y calcular la desviación estándar
    de las diferencias de fitness. T0 = std(ΔE) * factor
    
    Args:
        solucion_inicial: Solución de partida
        num_muestras: Número de vecinos a generar para estimar
    
    Returns:
        Temperatura inicial sugerida
    """
    deltas = []
    
    for _ in range(num_muestras):
        vecino = generar_vecino(solucion_inicial)
        evaluar_individuo(vecino)
        delta = vecino.fitness - solucion_inicial.fitness
        deltas.append(abs(delta))
    
    if deltas:
        # Usar la desviación estándar como base
        import statistics
        std_delta = statistics.stdev(deltas) if len(deltas) > 1 else statistics.mean(deltas)
        # Factor multiplicador para asegurar exploración inicial
        T0 = std_delta * 2.0
        
        # Asegurar un mínimo y máximo razonable
        T0 = max(500, min(T0, 5000))
    else:
        T0 = 2000  # Valor por defecto
    
    return T0


def aceptar_solucion(delta_fitness: float, temperatura: float) -> bool:
    """
    Criterio de aceptación de Metropolis.
    
    - Si ΔE > 0: Aceptar (mejor solución)
    - Si ΔE ≤ 0: Aceptar con probabilidad P = exp(ΔE / T)
    
    Args:
        delta_fitness: Diferencia de fitness (nuevo - actual)
        temperatura: Temperatura actual del sistema
    
    Returns:
        True si se acepta la solución, False en caso contrario
    """
    if delta_fitness > 0:
        # Solución mejor: siempre aceptar
        return True
    else:
        # Solución peor: aceptar con probabilidad exponencial
        if temperatura > 0:
            probabilidad = math.exp(delta_fitness / temperatura)
            return random.random() < probabilidad
        else:
            return False


def enfriamiento_simulado(
    solucion_inicial: Individual = None,
    T_inicial: float = None,
    T_minima: float = 0.1,
    alpha: float = 0.95,
    max_iteraciones: int = 5000,
    iteraciones_sin_mejora_max: int = 1000,
    verbose: bool = True
) -> Dict:
    """
    Algoritmo de Enfriamiento Simulado (Simulated Annealing) para optimización de rutas.
    
    Estrategia híbrida recomendada:
    - Partir del mejor del genético (warm start) o generar solución aleatoria
    - Temperatura inicial adaptativa o fija (1000-2000)
    - Enfriamiento geométrico: T = T * alpha (0.95)
    - Perturbación mixta: 70% swap, 20% reemplazo, 10% cambio ciudad
    - Parada combinada: max_iteraciones O temperatura < T_minima O estancamiento
    
    Args:
        solucion_inicial: Solución de partida (si None, se genera aleatoria)
        T_inicial: Temperatura inicial (si None, se calcula adaptativamente)
        T_minima: Temperatura mínima de parada
        alpha: Factor de enfriamiento geométrico (0 < alpha < 1)
        max_iteraciones: Número máximo de iteraciones
        iteraciones_sin_mejora_max: Iteraciones sin mejora para parada temprana
        verbose: Mostrar progreso
    
    Returns:
        Dict con mejor solución encontrada y estadísticas
    """
    if verbose:
        print(f"\n{'='*80}")
        print(f"🔥 ALGORITMO DE ENFRIAMIENTO SIMULADO")
        print(f"{'='*80}")
    
    # Generar o usar solución inicial
    if solucion_inicial is None:
        if verbose:
            print(f"🎲 Generando solución inicial aleatoria...")
        # Usar parámetros por defecto
        solucion_inicial = crear_individuo_aleatorio(num_dias=20, lugares_por_dia=12)
    else:
        if verbose:
            print(f"🚀 Usando solución inicial proporcionada (warm start)...")
        # Hacer copia profunda para no modificar la original
        solucion_inicial = Individual(
            [dia[:] for dia in solucion_inicial.dias],
            solucion_inicial.ciudades[:]
        )
    
    # Eliminar duplicados de la solución inicial
    solucion_inicial = eliminar_duplicados_dia(solucion_inicial)
    
    # Evaluar solución inicial
    evaluar_individuo(solucion_inicial)
    
    # Calcular temperatura inicial si no se proporcionó
    if T_inicial is None:
        if verbose:
            print(f"🌡️  Calculando temperatura inicial adaptativa...")
        T_inicial = calcular_temperatura_inicial(solucion_inicial)
    
    if verbose:
        print(f"\n📊 Configuración:")
        print(f"  • Temperatura inicial: {T_inicial:.1f}")
        print(f"  • Temperatura mínima: {T_minima}")
        print(f"  • Factor de enfriamiento (α): {alpha}")
        print(f"  • Máx. iteraciones: {max_iteraciones:,}")
        print(f"  • Máx. iter. sin mejora: {iteraciones_sin_mejora_max:,}")
        print(f"  • Fitness inicial: {solucion_inicial.fitness:.1f}")
        print(f"  • Puntos iniciales: {solucion_inicial.puntos_totales}")
        print(f"{'='*80}\n")
    
    # Inicializar variables
    solucion_actual = solucion_inicial
    mejor_solucion = copy.deepcopy(solucion_inicial)
    temperatura = T_inicial
    
    # Estadísticas
    iteraciones_sin_mejora = 0
    total_aceptaciones = 0
    total_rechazos = 0
    mejoras_encontradas = 0
    historial_fitness = [solucion_actual.fitness]
    historial_mejor_fitness = [mejor_solucion.fitness]
    historial_temperatura = [temperatura]
    
    if verbose:
        print(f"🔄 Iniciando búsqueda...\n")
    
    # Bucle principal
    for iteracion in range(max_iteraciones):
        # Generar solución vecina
        vecino = generar_vecino(solucion_actual)
        
        # Evaluar vecino
        evaluar_individuo(vecino)
        
        # Calcular diferencia de fitness
        delta_fitness = vecino.fitness - solucion_actual.fitness
        
        # Decidir si aceptar
        if aceptar_solucion(delta_fitness, temperatura):
            solucion_actual = vecino
            total_aceptaciones += 1
            
            # Actualizar mejor global si es necesario
            if solucion_actual.fitness > mejor_solucion.fitness:
                mejor_solucion = copy.deepcopy(solucion_actual)
                iteraciones_sin_mejora = 0
                mejoras_encontradas += 1
                
                if verbose and (iteracion + 1) % 100 == 0:
                    print(f"  ✨ Nueva mejor solución en iteración {iteracion+1}: "
                          f"Fitness = {mejor_solucion.fitness:.1f} | "
                          f"Puntos = {mejor_solucion.puntos_totales} | "
                          f"T = {temperatura:.2f}")
            else:
                iteraciones_sin_mejora += 1
        else:
            total_rechazos += 1
            iteraciones_sin_mejora += 1
        
        # Guardar historial
        historial_fitness.append(solucion_actual.fitness)
        historial_mejor_fitness.append(mejor_solucion.fitness)
        historial_temperatura.append(temperatura)
        
        # Enfriar sistema (enfriamiento geométrico)
        temperatura = temperatura * alpha
        
        # Mostrar progreso periódicamente
        if verbose and (iteracion + 1) % 500 == 0:
            tasa_aceptacion = total_aceptaciones / (iteracion + 1) * 100
            print(f"  Iter {iteracion+1:5d}/{max_iteraciones} | "
                  f"T = {temperatura:8.2f} | "
                  f"Fitness = {solucion_actual.fitness:8.1f} | "
                  f"Mejor = {mejor_solucion.fitness:8.1f} | "
                  f"Aceptación = {tasa_aceptacion:5.1f}%")
        
        # Condiciones de parada
        if temperatura < T_minima:
            if verbose:
                print(f"\n❄️  Temperatura mínima alcanzada: {temperatura:.4f} < {T_minima}")
            break
        
        if iteraciones_sin_mejora >= iteraciones_sin_mejora_max:
            if verbose:
                print(f"\n⏸️  Estancamiento detectado: {iteraciones_sin_mejora} iteraciones sin mejora")
            break
    
    # Estadísticas finales
    iteraciones_realizadas = iteracion + 1
    tasa_aceptacion_final = total_aceptaciones / iteraciones_realizadas * 100
    mejora_absoluta = mejor_solucion.fitness - solucion_inicial.fitness
    mejora_porcentual = (mejora_absoluta / abs(solucion_inicial.fitness) * 100) if solucion_inicial.fitness != 0 else 0
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"✅ ENFRIAMIENTO SIMULADO COMPLETADO")
        print(f"{'='*80}")
        print(f"\n📈 Estadísticas:")
        print(f"  • Iteraciones realizadas: {iteraciones_realizadas:,}")
        print(f"  • Temperatura final: {temperatura:.4f}")
        print(f"  • Total aceptaciones: {total_aceptaciones:,} ({tasa_aceptacion_final:.1f}%)")
        print(f"  • Total rechazos: {total_rechazos:,}")
        print(f"  • Mejoras encontradas: {mejoras_encontradas}")
        print(f"\n🏆 Resultados:")
        print(f"  • Fitness inicial: {solucion_inicial.fitness:.1f}")
        print(f"  • Fitness final: {mejor_solucion.fitness:.1f}")
        print(f"  • Mejora absoluta: {mejora_absoluta:+.1f}")
        print(f"  • Mejora porcentual: {mejora_porcentual:+.2f}%")
        print(f"  • Puntos totales: {mejor_solucion.puntos_totales}")
        print(f"  • Tiempo total: {mejor_solucion.tiempo_total/60:.1f}h")
        print(f"  • Distancia total: {mejor_solucion.distancia_total:.1f}km")
        print(f"{'='*80}\n")
    
    return {
        "mejor_solucion": mejor_solucion,
        "solucion_inicial": solucion_inicial,
        "historial_fitness": historial_fitness,
        "historial_mejor_fitness": historial_mejor_fitness,
        "historial_temperatura": historial_temperatura,
        "estadisticas": {
            "iteraciones_realizadas": iteraciones_realizadas,
            "temperatura_final": temperatura,
            "total_aceptaciones": total_aceptaciones,
            "total_rechazos": total_rechazos,
            "tasa_aceptacion": tasa_aceptacion_final,
            "mejoras_encontradas": mejoras_encontradas,
            "fitness_inicial": solucion_inicial.fitness,
            "fitness_final": mejor_solucion.fitness,
            "mejora_absoluta": mejora_absoluta,
            "mejora_porcentual": mejora_porcentual
        }
    }


def enfriamiento_desde_genetico(
    resultados_genetico: Dict,
    usar_mejor: bool = True,
    T_inicial: float = 5000,  # Aumentado de 1000 a 5000 para mejor exploración
    alpha: float = 0.98,
    max_iteraciones: int = 5000
) -> Dict:
    """
    Ejecuta enfriamiento simulado usando la salida del algoritmo genético.
    
    Estrategia híbrida: GA (exploración global) + SA (refinamiento local)
    
    Args:
        resultados_genetico: Diccionario con resultados del GA
        usar_mejor: Si True, usa el mejor individuo; si False, usa uno del top 10
        T_inicial: Temperatura inicial (5000 para permitir exploración significativa)
        alpha: Factor de enfriamiento (más alto para convergencia más lenta)
        max_iteraciones: Iteraciones máximas
    
    Returns:
        Dict con resultados del enfriamiento simulado
    """
    print(f"\n{'='*80}")
    print(f"🔗 ENFRIAMIENTO SIMULADO DESDE ALGORITMO GENÉTICO (HÍBRIDO GA+SA)")
    print(f"{'='*80}\n")
    
    if usar_mejor:
        print(f"📍 Estrategia: Partir del MEJOR individuo del GA")
        solucion_inicial = resultados_genetico["mejor_individuo"]
    else:
        print(f"📍 Estrategia: Partir de un individuo del TOP 10 del GA")
        poblacion_final = resultados_genetico.get("poblacion_final", [])
        if poblacion_final:
            top_10 = sorted(poblacion_final, key=lambda x: x.fitness, reverse=True)[:10]
            solucion_inicial = random.choice(top_10)
            print(f"  • Seleccionado individuo con fitness: {solucion_inicial.fitness:.1f}")
        else:
            print(f"  ⚠️  No hay población final, usando mejor individuo")
            solucion_inicial = resultados_genetico["mejor_individuo"]
    
    print(f"\n💡 Configuración MEJORADA de refinamiento:")
    print(f"  • Temperatura inicial: {T_inicial} (alta para escapar de óptimos locales)")
    print(f"  • Factor α: {alpha} (enfriamiento lento para exploración cuidadosa)")
    print(f"  • Iteraciones: {max_iteraciones:,}")
    print(f"  • Vecindad mejorada: 5 tipos de perturbaciones (swap, reemplazar, cambiar ciudad, swap intercity, 2-opt)")
    
    # Ejecutar enfriamiento simulado
    resultados_sa = enfriamiento_simulado(
        solucion_inicial=solucion_inicial,
        T_inicial=T_inicial,
        alpha=alpha,
        max_iteraciones=max_iteraciones,
        verbose=True
    )
    
    return resultados_sa


def exportar_resultados_sa(resultados: Dict, archivo: str = "resultados_sa_espana.json"):
    """
    Exporta resultados del enfriamiento simulado a JSON.
    
    Args:
        resultados: Diccionario con resultados del SA
        archivo: Nombre del archivo de salida
    """
    import json
    
    mejor = resultados["mejor_solucion"]
    inicial = resultados["solucion_inicial"]
    stats = resultados["estadisticas"]
    
    data = {
        "algoritmo": "Enfriamiento Simulado",
        "mejor_solucion": {
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
            ]
        },
        "solucion_inicial": {
            "fitness": inicial.fitness,
            "puntos_totales": inicial.puntos_totales
        },
        "estadisticas": stats,
        "historial": {
            "fitness_actual": resultados["historial_fitness"],
            "mejor_fitness": resultados["historial_mejor_fitness"],
            "temperatura": resultados["historial_temperatura"]
        }
    }
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados exportados a: {archivo}")


def comparar_ga_vs_sa(resultados_ga: Dict, resultados_sa: Dict):
    """
    Compara los resultados del algoritmo genético vs enfriamiento simulado.
    
    Args:
        resultados_ga: Resultados del GA
        resultados_sa: Resultados del SA
    """
    mejor_ga = resultados_ga["mejor_individuo"]
    mejor_sa = resultados_sa["mejor_solucion"]
    
    print(f"\n{'='*80}")
    print(f"⚖️  COMPARACIÓN: ALGORITMO GENÉTICO vs ENFRIAMIENTO SIMULADO")
    print(f"{'='*80}\n")
    
    print(f"{'Métrica':<30} {'GA':<20} {'SA':<20} {'Diferencia':<20}")
    print(f"{'-'*80}")
    
    # Fitness
    diff_fitness = mejor_sa.fitness - mejor_ga.fitness
    print(f"{'Fitness':<30} {mejor_ga.fitness:<20.1f} {mejor_sa.fitness:<20.1f} {diff_fitness:+.1f}")
    
    # Puntos
    diff_puntos = mejor_sa.puntos_totales - mejor_ga.puntos_totales
    print(f"{'Puntos totales':<30} {mejor_ga.puntos_totales:<20} {mejor_sa.puntos_totales:<20} {diff_puntos:+d}")
    
    # Tiempo
    diff_tiempo = (mejor_sa.tiempo_total - mejor_ga.tiempo_total) / 60
    print(f"{'Tiempo total (h)':<30} {mejor_ga.tiempo_total/60:<20.1f} {mejor_sa.tiempo_total/60:<20.1f} {diff_tiempo:+.1f}")
    
    # Distancia
    diff_distancia = mejor_sa.distancia_total - mejor_ga.distancia_total
    print(f"{'Distancia total (km)':<30} {mejor_ga.distancia_total:<20.1f} {mejor_sa.distancia_total:<20.1f} {diff_distancia:+.1f}")
    
    print(f"{'-'*80}")
    
    if diff_fitness > 0:
        mejora_pct = (diff_fitness / abs(mejor_ga.fitness)) * 100
        print(f"\n🏆 El enfriamiento simulado MEJORÓ la solución del GA en {mejora_pct:.2f}%")
    elif diff_fitness < 0:
        empeora_pct = (abs(diff_fitness) / abs(mejor_ga.fitness)) * 100
        print(f"\n📉 El enfriamiento simulado empeoró ligeramente ({empeora_pct:.2f}%)")
    else:
        print(f"\n🤝 Ambos algoritmos encontraron soluciones de calidad similar")
    
    print(f"{'='*80}\n")


# Ejecución principal
if __name__ == "__main__":
    import sys
    
    modos = {
        "1": {
            "nombre": "SA desde CERO (Random start)",
            "descripcion": "Genera solución inicial aleatoria y ejecuta SA",
            "funcion": "standalone"
        },
        "2": {
            "nombre": "SA desde GA (Hybrid start)",
            "descripcion": "Primero ejecuta GA, luego refina con SA",
            "funcion": "hybrid"
        },
        "3": {
            "nombre": "SA con solución personalizada",
            "descripcion": "Carga solución desde JSON y ejecuta SA",
            "funcion": "custom"
        }
    }
    
    print(f"\n{'='*80}")
    print(f"🔥 ENFRIAMIENTO SIMULADO - RUTA POR ESPAÑA")
    print(f"{'='*80}\n")
    
    for key, modo in modos.items():
        print(f"[{key}] {modo['nombre']}")
        print(f"    📝 {modo['descripcion']}")
        print()
    
    print(f"{'='*80}")
    
    if len(sys.argv) > 1:
        seleccion = sys.argv[1]
    else:
        seleccion = input("👉 Selecciona modo (1/2/3): ").strip()
    
    if seleccion not in modos:
        print(f"\n❌ ERROR: Modo '{seleccion}' no válido. Usa: 1, 2 o 3")
        sys.exit(1)
    
    modo_elegido = modos[seleccion]["funcion"]
    
    if modo_elegido == "standalone":
        # Modo 1: SA desde cero
        print(f"\n🎲 Modo 1: Enfriamiento Simulado desde solución aleatoria\n")
        
        resultados = enfriamiento_simulado(
            solucion_inicial=None,  # Generará una aleatoria
            T_inicial=2000,
            T_minima=0.1,
            alpha=0.95,
            max_iteraciones=5000,
            iteraciones_sin_mejora_max=1000,
            verbose=True
        )
        
        analizar_solucion(resultados["mejor_solucion"])
        exportar_resultados_sa(resultados, archivo="resultados_sa_standalone.json")
    
    elif modo_elegido == "hybrid":
        # Modo 2: GA + SA (híbrido)
        print(f"\n🔗 Modo 2: Algoritmo Híbrido (GA + SA)\n")
        print(f"{'='*80}")
        print(f"FASE 1: ALGORITMO GENÉTICO (Exploración Global)")
        print(f"{'='*80}")
        
        from algoritmo_espana import algoritmo_genetico_espana
        
        # Ejecutar GA con configuración rápida
        resultados_ga = algoritmo_genetico_espana(
            num_dias=20,
            lugares_por_dia=12,
            tam_poblacion=5000,
            num_generaciones=300,
            tasa_elitismo=0.20
        )
        
        print(f"\n{'='*80}")
        print(f"FASE 2: ENFRIAMIENTO SIMULADO (Refinamiento Local)")
        print(f"{'='*80}")
        
        # Ejecutar SA desde el mejor del GA
        resultados_sa = enfriamiento_desde_genetico(
            resultados_genetico=resultados_ga,
            usar_mejor=True,
            T_inicial=5000,  # Temperatura alta para escapar de óptimos locales
            alpha=0.98,  # Enfriamiento lento
            max_iteraciones=5000
        )
        
        # Comparar resultados
        comparar_ga_vs_sa(resultados_ga, resultados_sa)
        
        # Analizar y exportar la mejor solución final
        print(f"\n{'='*80}")
        print(f"📋 ANÁLISIS DE LA SOLUCIÓN FINAL (POST-SA)")
        print(f"{'='*80}")
        analizar_solucion(resultados_sa["mejor_solucion"])
        
        exportar_resultados_sa(resultados_sa, archivo="resultados_sa_hybrid.json")
    
    elif modo_elegido == "custom":
        # Modo 3: Cargar desde JSON
        print(f"\n📂 Modo 3: SA desde solución personalizada\n")
        
        archivo_json = input("📄 Introduce la ruta del archivo JSON: ").strip()
        
        try:
            import json
            with open(archivo_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Reconstruir individuo desde JSON
            itinerario = data.get("itinerario", data.get("mejor_individuo", {}).get("itinerario", []))
            
            dias = [item["lugares_ids"] for item in itinerario]
            ciudades = [item["ciudad"] for item in itinerario]
            
            solucion_custom = Individual(dias, ciudades)
            evaluar_individuo(solucion_custom)
            
            print(f"✅ Solución cargada correctamente")
            print(f"  • Fitness: {solucion_custom.fitness:.1f}")
            print(f"  • Puntos: {solucion_custom.puntos_totales}")
            print(f"  • Días: {len(dias)}")
            
            resultados = enfriamiento_simulado(
                solucion_inicial=solucion_custom,
                T_inicial=1500,
                alpha=0.95,
                max_iteraciones=5000,
                verbose=True
            )
            
            analizar_solucion(resultados["mejor_solucion"])
            exportar_resultados_sa(resultados, archivo="resultados_sa_custom.json")
        
        except Exception as e:
            print(f"\n❌ ERROR al cargar archivo: {e}")
            sys.exit(1)
    
    print(f"\n✅ Ejecución completada exitosamente!")
