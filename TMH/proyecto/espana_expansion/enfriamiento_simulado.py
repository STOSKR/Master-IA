import random
import copy
import math
import logging
from datetime import datetime
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

# Configurar logging
def configurar_logging_sa(nombre_archivo: str = None):
    """Configura el sistema de logging para enfriamiento simulado"""
    if nombre_archivo is None:
        timestamp = datetime.now().strftime("%d_%H_%M")
        nombre_archivo = f"sa_log_{timestamp}.txt"
    
    # Crear logger
    logger = logging.getLogger('EnfriamientoSimulado')
    logger.setLevel(logging.DEBUG)
    
    # Limpiar handlers existentes
    logger.handlers.clear()
    
    # Handler para archivo
    fh = logging.FileHandler(nombre_archivo, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    # Handler para consola
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger, nombre_archivo

# Inicializar logger global
sa_logger = None


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


def generar_vecino(solucion_actual: Individual, iteracion: int = 0, max_iteraciones: int = 5000, usar_2opt: bool = True) -> Individual:
    """
    Genera una solución vecina aplicando perturbaciones mixtas mejoradas:
    - 40% Swap de dos lugares en un día (preserva fitness mejor)
    - 30% 2-opt (optimizar orden dentro de un día) - OPCIONAL
    - 20% Reemplazar un lugar por otro de la misma ciudad
    - 10% Swap intercity (intercambiar dos días completos - más disruptivo)
    
    Args:
        solucion_actual: Solución actual
        iteracion: Iteración actual (opcional)
        max_iteraciones: Iteraciones máximas (opcional)
        usar_2opt: Si True, incluye 2-opt en las perturbaciones
    
    Returns:
        Nueva solución vecina (copia profunda)
    """
    # Crear copia profunda para no modificar la original
    vecino = Individual(
        [dia[:] for dia in solucion_actual.dias],
        solucion_actual.ciudades[:]
    )
    
    # Ajustar probabilidades dinámicamente según si se usa 2-opt
    progreso = iteracion / max_iteraciones if max_iteraciones > 0 else 0
    
    if usar_2opt:
        # Configuración original con 2-opt
        if progreso < 0.3:
            # Etapa inicial: más exploración
            probabilidades = [0.30, 0.20, 0.20, 0.30]
        elif progreso < 0.7:
            # Etapa intermedia: balance
            probabilidades = [0.40, 0.30, 0.20, 0.10]
        else:
            # Etapa final: más refinamiento local
            probabilidades = [0.50, 0.35, 0.10, 0.05]
    else:
        # Sin 2-opt: redistribuir probabilidades
        if progreso < 0.3:
            probabilidades = [0.40, 0.0, 0.30, 0.30]
        elif progreso < 0.7:
            probabilidades = [0.55, 0.0, 0.30, 0.15]
        else:
            probabilidades = [0.65, 0.0, 0.25, 0.10]
    
    tipo_perturbacion = random.choices(
        ["swap", "ruta_2opt", "reemplazar", "swap_intercity"],
        weights=probabilidades
    )[0]
    
    if tipo_perturbacion == "swap":
        # Swap de dos lugares en un día aleatorio (MÍNIMA PERTURBACIÓN)
        dia_idx = random.randint(0, len(vecino.dias) - 1)
        dia = vecino.dias[dia_idx]
        
        if len(dia) >= 2:
            i, j = random.sample(range(len(dia)), 2)
            dia[i], dia[j] = dia[j], dia[i]
    
    elif tipo_perturbacion == "ruta_2opt" and usar_2opt:
        # Optimización 2-opt dentro de un día (MÍNIMA PERTURBACIÓN)
        dia_idx = random.randint(0, len(vecino.dias) - 1)
        dia = vecino.dias[dia_idx]
        
        if len(dia) >= 4:
            # Elegir dos puntos de corte
            i = random.randint(0, len(dia) - 3)
            j = random.randint(i + 2, len(dia))
            # Invertir el segmento entre i y j
            vecino.dias[dia_idx] = dia[:i+1] + dia[i+1:j][::-1] + dia[j:]
    
    elif tipo_perturbacion == "reemplazar":
        # Reemplazar un lugar por otro de la misma ciudad (PERTURBACIÓN MEDIA)
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
    
    elif tipo_perturbacion == "swap_intercity":
        # Intercambiar dos días completos (PERTURBACIÓN FUERTE - solo al inicio)
        if len(vecino.dias) >= 2:
            i, j = random.sample(range(len(vecino.dias)), 2)
            # Intercambiar días
            vecino.dias[i], vecino.dias[j] = vecino.dias[j], vecino.dias[i]
            # Intercambiar ciudades
            vecino.ciudades[i], vecino.ciudades[j] = vecino.ciudades[j], vecino.ciudades[i]
    
    # Validar y reparar si es necesario
    if not validar_restricciones_ciudades(vecino):
        vecino = reparar_individuo(vecino)
    
    # Eliminar duplicados en cada día
    vecino = eliminar_duplicados_dia(vecino)
    
    return vecino


def calcular_temperatura_inicial(solucion_inicial: Individual, num_muestras: int = 100) -> float:
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
    if delta_fitness > 0:
        # Solución MEJOR: siempre aceptar
        return True
    else:
        # Solución PEOR: aceptar con probabilidad exponencial
        # Cuanto mayor sea T, mayor probabilidad de aceptar
        if temperatura > 0:
            probabilidad = math.exp(delta_fitness / temperatura)
            return random.random() < probabilidad
        else:
            # Si T=0, nunca aceptar soluciones peores (comportamiento greedy)
            return False


def enfriamiento_simulado(
    solucion_inicial: Individual = None,
    T_inicial: float = None,
    T_minima: float = 0.1,
    alpha: float = 0.95,
    max_iteraciones: int = None,
    max_tiempo_segundos: float = 3600,  # 1 hora por defecto
    iteraciones_sin_mejora_max: int = 1000,
    usar_2opt: bool = True,  # Nuevo parámetro para controlar 2-opt
    verbose: bool = True,
    debug_saltos: bool = True  # Nuevo: activar detección de saltos anormales
) -> Dict:
    global sa_logger
    
    # Configurar logging
    if sa_logger is None:
        sa_logger, log_file = configurar_logging_sa()
        if verbose:
            print(f"📝 Log guardándose en: {log_file}")
    
    sa_logger.info("="*80)
    sa_logger.info("🔥 INICIANDO ENFRIAMIENTO SIMULADO")
    sa_logger.info("="*80)
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"🔥 ALGORITMO DE ENFRIAMIENTO SIMULADO")
        print(f"{'='*80}")
    
    # Importar time para medir tiempo de ejecución
    import time
    tiempo_inicio = time.time()
    
    # Generar o usar solución inicial
    if solucion_inicial is None:
        if verbose:
            print(f"🎲 Generando solución inicial aleatoria...")
        sa_logger.info("Generando solución inicial aleatoria")
        # Usar parámetros por defecto
        solucion_inicial = crear_individuo_aleatorio(num_dias=20, lugares_por_dia=12)
        # Evaluar solución inicial aleatoria
        evaluar_individuo(solucion_inicial)
        sa_logger.info(f"Solución inicial creada - Fitness: {solucion_inicial.fitness:.1f}, Puntos: {solucion_inicial.puntos_totales}")
    else:
        if verbose:
            print(f"🚀 Usando solución inicial proporcionada (warm start)...")
            print(f"  • Fitness reportado por el GA: {solucion_inicial.fitness:.1f}")
            print(f"  • Puntos reportados por el GA: {solucion_inicial.puntos_totales}")
        
        sa_logger.info(f"Usando solución inicial proporcionada - Fitness: {solucion_inicial.fitness:.1f}, Puntos: {solucion_inicial.puntos_totales}")
        
        # CRÍTICO: Hacer copia profunda SIN perder el fitness
        # El módulo copy ya está importado al inicio del archivo
        solucion_inicial = copy.deepcopy(solucion_inicial)
        
        if verbose:
            print(f"  • Fitness después de copia (sin cambios): {solucion_inicial.fitness:.1f}")
        
        sa_logger.debug(f"Copia profunda realizada - Fitness: {solucion_inicial.fitness:.1f}")
    
    # Eliminar duplicados de la solución inicial (si los hay)
    # IMPORTANTE: Solo si realmente hay duplicados, para no re-evaluar
    tiene_duplicados = False
    for dia in solucion_inicial.dias:
        if len(dia) != len(set(dia)):
            tiene_duplicados = True
            break
    
    if tiene_duplicados:
        if verbose:
            print(f"\n  ⚠️  ¡ATENCIÓN! La solución del GA contiene lugares duplicados en el mismo día.")
            print(f"      Esto infla artificialmente el fitness del GA porque no los penaliza.")
            print(f"      Procedo a limpiar la solución y a re-evaluarla para obtener el fitness REAL.")
        solucion_inicial = eliminar_duplicados_dia(solucion_inicial)
        # Re-evaluar solo si modificamos
        evaluar_individuo(solucion_inicial)
        if verbose:
            print(f"  • Fitness REAL después de limpiar duplicados: {solucion_inicial.fitness:.1f}")
    else:
        if verbose:
            print(f"  ✅ La solución del GA es válida (sin duplicados).")
    
    # Calcular temperatura inicial si no se proporcionó
    if T_inicial is None:
        if verbose:
            print(f"🌡️  Calculando temperatura inicial adaptativa...")
        T_inicial = calcular_temperatura_inicial(solucion_inicial)
    
    if verbose:
        print(f"\n📊 Configuración para Enfriamiento Simulado:")
        print(f"  • Temperatura inicial: {T_inicial:.1f}")
        print(f"  • Temperatura mínima: {T_minima}")
        print(f"  • Factor de enfriamiento (α): {alpha}")
        if max_iteraciones:
            print(f"  • Máx. iteraciones: {max_iteraciones:,}")
        print(f"  • Máx. tiempo: {max_tiempo_segundos/60:.1f} minutos ({max_tiempo_segundos/3600:.1f} horas)")
        print(f"  • Máx. iter. sin mejora: {iteraciones_sin_mejora_max:,}")
        print(f"  • Usar optimización 2-opt: {'✅ SÍ' if usar_2opt else '❌ NO'}")
        print(f"  • Fitness inicial (REAL): {solucion_inicial.fitness:.1f}")
        print(f"  • Puntos iniciales (REAL): {solucion_inicial.puntos_totales}")
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
    
    # Configuración de visualización en tiempo real
    import matplotlib.pyplot as plt
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title("Evolución del Fitness")
    ax.set_xlabel("Iteración")
    ax.set_ylabel("Fitness")
    line_actual, = ax.plot([], [], label="Fitness actual")
    line_mejor, = ax.plot([], [], label="Mejor fitness global")
    ax.legend()
    
    if verbose:
        print(f"🔄 Iniciando búsqueda...\n")
    
    sa_logger.info("Iniciando búsqueda por vecindario")
    sa_logger.info(f"Configuración: T_inicial={T_inicial}, alpha={alpha}, max_tiempo={max_tiempo_segundos}s, usar_2opt={usar_2opt}")
    
    # Bucle principal
    iteracion = 0
    fitness_anterior = solucion_actual.fitness  # Para detectar saltos
    
    while True:
        # Verificar tiempo transcurrido
        tiempo_transcurrido = time.time() - tiempo_inicio
        
        # Verificar límite de tiempo
        if tiempo_transcurrido >= max_tiempo_segundos:
            if verbose:
                print(f"\n⏰ Tiempo máximo alcanzado: {tiempo_transcurrido/60:.1f} minutos")
            sa_logger.info(f"Tiempo máximo alcanzado: {tiempo_transcurrido/60:.1f} minutos")
            break
        
        # Verificar límite de iteraciones (si se especificó)
        if max_iteraciones and iteracion >= max_iteraciones:
            if verbose:
                print(f"\n🔢 Iteraciones máximas alcanzadas: {iteracion}")
            sa_logger.info(f"Iteraciones máximas alcanzadas: {iteracion}")
            break
        
        # Generar solución vecina
        vecino = generar_vecino(solucion_actual, iteracion, max_iteraciones if max_iteraciones else 10000, usar_2opt)
        
        # Evaluar vecino
        fitness_antes_evaluar = vecino.fitness if hasattr(vecino, 'fitness') else None
        evaluar_individuo(vecino)
        
        # Log detallado cada 100 iteraciones
        if iteracion % 100 == 0:
            sa_logger.debug(f"Iter {iteracion}: T={temperatura:.2f}, Fitness_actual={solucion_actual.fitness:.1f}, Mejor={mejor_solucion.fitness:.1f}")
        
        # Calcular diferencia de fitness
        delta_fitness = vecino.fitness - solucion_actual.fitness
        
        # DETECCIÓN DE SALTOS ANORMALES
        if debug_saltos and abs(delta_fitness) > 5000:
            sa_logger.warning("="*80)
            sa_logger.warning(f"⚠️  SALTO ANORMAL DETECTADO en iteración {iteracion}")
            sa_logger.warning(f"   Fitness actual: {solucion_actual.fitness:.1f}")
            sa_logger.warning(f"   Fitness vecino: {vecino.fitness:.1f}")
            sa_logger.warning(f"   Delta: {delta_fitness:+.1f}")
            sa_logger.warning(f"   Temperatura: {temperatura:.2f}")
            sa_logger.warning(f"   Tipo perturbación aplicada: (ver generar_vecino)")
            
            # Detalles del vecino
            sa_logger.warning(f"   Vecino - Puntos: {vecino.puntos_totales}, Tiempo: {vecino.tiempo_total:.1f}min, Distancia: {vecino.distancia_total:.1f}km")
            sa_logger.warning(f"   Actual - Puntos: {solucion_actual.puntos_totales}, Tiempo: {solucion_actual.tiempo_total:.1f}min, Distancia: {solucion_actual.distancia_total:.1f}km")
            
            # Verificar si tiene duplicados
            tiene_duplicados_vecino = False
            for dia_idx, dia in enumerate(vecino.dias):
                if len(dia) != len(set(dia)):
                    tiene_duplicados_vecino = True
                    duplicados = [x for x in dia if dia.count(x) > 1]
                    sa_logger.warning(f"   ⚠️ Vecino tiene DUPLICADOS en día {dia_idx+1}: {set(duplicados)}")
            
            tiene_duplicados_actual = False
            for dia_idx, dia in enumerate(solucion_actual.dias):
                if len(dia) != len(set(dia)):
                    tiene_duplicados_actual = True
                    duplicados = [x for x in dia if dia.count(x) > 1]
                    sa_logger.warning(f"   ⚠️ Actual tiene DUPLICADOS en día {dia_idx+1}: {set(duplicados)}")
            
            # Verificar restricciones
            es_valido_vecino = validar_restricciones_ciudades(vecino)
            es_valido_actual = validar_restricciones_ciudades(solucion_actual)
            sa_logger.warning(f"   Validez restricciones - Vecino: {es_valido_vecino}, Actual: {es_valido_actual}")
            
            sa_logger.warning("="*80)
            
            # Imprimir en consola también
            if verbose:
                print(f"\n⚠️  SALTO ANORMAL DETECTADO en iteración {iteracion}")
                print(f"   Fitness: {solucion_actual.fitness:.1f} → {vecino.fitness:.1f} (Δ={delta_fitness:+.1f})")
                print(f"   Ver detalles en archivo de log\n")
        
        # Decidir si aceptar
        aceptado = aceptar_solucion(delta_fitness, temperatura)
        
        if aceptado:
            # Actualizar solución actual (puede ser peor que la anterior)
            fitness_antes_actualizar = solucion_actual.fitness
            solucion_actual = vecino
            total_aceptaciones += 1
            
            # Log si hubo un cambio significativo
            if debug_saltos and abs(delta_fitness) > 1000:
                sa_logger.info(f"Iter {iteracion}: Aceptada solución con delta={delta_fitness:+.1f} (T={temperatura:.2f})")
            
            # Verificar si es la MEJOR GLOBAL encontrada hasta ahora
            if solucion_actual.fitness > mejor_solucion.fitness:
                mejora_sobre_mejor = solucion_actual.fitness - mejor_solucion.fitness
                mejor_solucion = copy.deepcopy(solucion_actual)
                iteraciones_sin_mejora = 0
                mejoras_encontradas += 1
                
                sa_logger.info(f"🌟 MEJORA #{mejoras_encontradas} en iter {iteracion}: Fitness={mejor_solucion.fitness:.1f} (+{mejora_sobre_mejor:.1f}), Puntos={mejor_solucion.puntos_totales}")
                
                if verbose and mejoras_encontradas % 5 == 0:
                    print(f"  ✨ Mejora #{mejoras_encontradas} en iteración {iteracion+1}: "
                          f"Fitness = {mejor_solucion.fitness:.1f} | "
                          f"Puntos = {mejor_solucion.puntos_totales} | "
                          f"T = {temperatura:.2f}")
            else:
                iteraciones_sin_mejora += 1
        else:
            # Solución rechazada, mantener la actual
            total_rechazos += 1
            iteraciones_sin_mejora += 1
            
            # Log rechazos significativos
            if debug_saltos and delta_fitness > 2000:
                probabilidad = math.exp(delta_fitness / temperatura) if temperatura > 0 else 0
                sa_logger.debug(f"Iter {iteracion}: Rechazada mejora de {delta_fitness:+.1f} (prob={probabilidad:.4f}, T={temperatura:.2f})")
        
        # Actualizar fitness_anterior para próxima iteración
        fitness_anterior = solucion_actual.fitness
        
        # Guardar historial
        historial_fitness.append(solucion_actual.fitness)
        historial_mejor_fitness.append(mejor_solucion.fitness)
        historial_temperatura.append(temperatura)
        
        # Actualizar visualización en tiempo real
        line_actual.set_xdata(range(len(historial_fitness)))
        line_actual.set_ydata(historial_fitness)
        line_mejor.set_xdata(range(len(historial_mejor_fitness)))
        line_mejor.set_ydata(historial_mejor_fitness)
        ax.relim()
        ax.autoscale_view()
        plt.pause(0.01)
        
        # Enfriar sistema (enfriamiento geométrico)
        temperatura = temperatura * alpha
        
        # Mostrar progreso periódicamente
        if verbose and (iteracion + 1) % 500 == 0:
            tasa_aceptacion = total_aceptaciones / (iteracion + 1) * 100
            tiempo_transcurrido = time.time() - tiempo_inicio
            print(f"  Iter {iteracion+1:5d} | "
                  f"Tiempo: {tiempo_transcurrido/60:6.1f}min | "
                  f"T = {temperatura:8.2f} | "
                  f"Fitness = {solucion_actual.fitness:8.1f} | "
                  f"Mejor = {mejor_solucion.fitness:8.1f} | "
                  f"Aceptación = {tasa_aceptacion:5.1f}%")
            
            sa_logger.info(f"Progreso iter {iteracion+1}: T={temperatura:.2f}, Fitness={solucion_actual.fitness:.1f}, "
                          f"Mejor={mejor_solucion.fitness:.1f}, Tasa_acept={tasa_aceptacion:.1f}%")
        
        # Condiciones de parada
        if temperatura < T_minima:
            if verbose:
                print(f"\n❄️  Temperatura mínima alcanzada: {temperatura:.4f} < {T_minima}")
            sa_logger.info(f"Temperatura mínima alcanzada: {temperatura:.4f}")
            break
        
        if iteraciones_sin_mejora >= iteraciones_sin_mejora_max:
            if verbose:
                print(f"\n⏸️  Estancamiento detectado: {iteraciones_sin_mejora} iteraciones sin mejora")
            sa_logger.info(f"Estancamiento: {iteraciones_sin_mejora} iteraciones sin mejora")
            break
        
        # Incrementar contador de iteraciones
        iteracion += 1
    
    # Cerrar visualización y guardar
    plt.ioff()
    
    # Calcular tiempo total de ejecución
    tiempo_total_ejecucion = time.time() - tiempo_inicio
    
    # Guardar la figura antes de cerrarla
    import os
    from datetime import datetime
    timestamp = datetime.now().strftime("%d_%H_%M")
    fig_filename = f"evolucion_fitness_sa_{timestamp}.png"
    plt.savefig(fig_filename, dpi=150, bbox_inches='tight')
    if verbose:
        print(f"\n💾 Gráfica guardada: {fig_filename}")
    
    plt.show()
    
    # Estadísticas finales
    iteraciones_realizadas = iteracion + 1
    tasa_aceptacion_final = total_aceptaciones / iteraciones_realizadas * 100
    mejora_absoluta = mejor_solucion.fitness - solucion_inicial.fitness
    mejora_porcentual = (mejora_absoluta / abs(solucion_inicial.fitness) * 100) if solucion_inicial.fitness != 0 else 0
    
    sa_logger.info("="*80)
    sa_logger.info("✅ ENFRIAMIENTO SIMULADO COMPLETADO")
    sa_logger.info("="*80)
    sa_logger.info(f"Iteraciones: {iteraciones_realizadas:,}")
    sa_logger.info(f"Tiempo ejecución: {tiempo_total_ejecucion/60:.2f} minutos")
    sa_logger.info(f"Fitness inicial: {solucion_inicial.fitness:.1f}")
    sa_logger.info(f"Fitness final: {mejor_solucion.fitness:.1f}")
    sa_logger.info(f"Mejora: {mejora_absoluta:+.1f} ({mejora_porcentual:+.2f}%)")
    sa_logger.info(f"Mejoras encontradas: {mejoras_encontradas}")
    sa_logger.info(f"Tasa aceptación: {tasa_aceptacion_final:.2f}%")
    sa_logger.info("="*80)
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"✅ ENFRIAMIENTO SIMULADO COMPLETADO")
        print(f"{'='*80}")
        print(f"\n📈 Estadísticas:")
        print(f"  • Iteraciones realizadas: {iteraciones_realizadas:,}")
        print(f"  • Tiempo de ejecución: {tiempo_total_ejecucion/60:.2f} minutos ({tiempo_total_ejecucion/3600:.2f} horas)")
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
            "tiempo_ejecucion_segundos": tiempo_total_ejecucion,
            "tiempo_ejecucion_minutos": tiempo_total_ejecucion / 60,
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
    T_inicial: float = 20,  # Temperatura moderada para refinamiento
    alpha: float = 0.999,  # Enfriamiento más rápido para convergencia
    max_tiempo_segundos: float = 3600  # 1 hora por defecto
) -> Dict:
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
    
    print(f"\n💡 Configuración OPTIMIZADA de refinamiento:")
    print(f"  • Temperatura inicial: {T_inicial} (moderada para refinamiento inteligente)")
    print(f"  • Factor α: {alpha} (convergencia balanceada)")
    print(f"  • Tiempo máximo: {max_tiempo_segundos/60:.1f} minutos ({max_tiempo_segundos/3600:.1f} horas)")
    print(f"  • Vecindad adaptativa: 4 tipos de perturbaciones con probabilidades dinámicas")
    print(f"  • Estrategia: Perturbaciones conservadoras que preservan calidad")
    
    # Ejecutar enfriamiento simulado
    resultados_sa = enfriamiento_simulado(
        solucion_inicial=solucion_inicial,
        T_inicial=T_inicial,
        alpha=alpha,
        max_tiempo_segundos=max_tiempo_segundos,
        usar_2opt=True,
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


def comparar_con_sin_2opt(
    solucion_inicial: Individual,
    T_inicial: float = 2000,
    alpha: float = 0.97,
    max_tiempo_segundos: float = 1800,  # 30 minutos cada uno
    verbose: bool = True
) -> Dict:
    """
    Compara el rendimiento del SA con y sin optimización 2-opt.
    
    Args:
        solucion_inicial: Solución inicial común para ambas ejecuciones
        T_inicial: Temperatura inicial
        alpha: Factor de enfriamiento
        max_tiempo_segundos: Tiempo máximo para cada ejecución
        verbose: Mostrar progreso
    
    Returns:
        Dict con resultados de ambas ejecuciones y comparación
    """
    import copy
    
    print(f"\n{'='*80}")
    print(f"🔬 EXPERIMENTO: COMPARACIÓN CON/SIN OPTIMIZACIÓN 2-OPT")
    print(f"{'='*80}\n")
    
    # Hacer copias de la solución inicial
    solucion_con = copy.deepcopy(solucion_inicial)
    solucion_sin = copy.deepcopy(solucion_inicial)
    
    print(f"📋 Configuración del experimento:")
    print(f"  • Temperatura inicial: {T_inicial}")
    print(f"  • Factor α: {alpha}")
    print(f"  • Tiempo máximo por ejecución: {max_tiempo_segundos/60:.1f} minutos")
    print(f"  • Fitness inicial: {solucion_inicial.fitness:.1f}")
    
    # Ejecución CON 2-opt
    print(f"\n{'='*80}")
    print(f"🟢 EJECUCIÓN 1: CON Optimización 2-opt")
    print(f"{'='*80}")
    
    resultados_con = enfriamiento_simulado(
        solucion_inicial=solucion_con,
        T_inicial=T_inicial,
        alpha=alpha,
        max_tiempo_segundos=max_tiempo_segundos,
        usar_2opt=True,
        verbose=verbose
    )
    
    # Ejecución SIN 2-opt
    print(f"\n{'='*80}")
    print(f"🔴 EJECUCIÓN 2: SIN Optimización 2-opt")
    print(f"{'='*80}")
    
    resultados_sin = enfriamiento_simulado(
        solucion_inicial=solucion_sin,
        T_inicial=T_inicial,
        alpha=alpha,
        max_tiempo_segundos=max_tiempo_segundos,
        usar_2opt=False,
        verbose=verbose
    )
    
    # Comparación
    mejor_con = resultados_con["mejor_solucion"]
    mejor_sin = resultados_sin["mejor_solucion"]
    stats_con = resultados_con["estadisticas"]
    stats_sin = resultados_sin["estadisticas"]
    
    print(f"\n{'='*80}")
    print(f"📊 RESULTADOS DE LA COMPARACIÓN 2-OPT")
    print(f"{'='*80}\n")
    
    print(f"{'Métrica':<35} {'CON 2-opt':<20} {'SIN 2-opt':<20} {'Diferencia':<20}")
    print(f"{'-'*95}")
    
    # Fitness final
    diff_fitness = mejor_con.fitness - mejor_sin.fitness
    simbolo_fitness = "✅ CON" if diff_fitness > 0 else "✅ SIN" if diff_fitness < 0 else "="
    print(f"{'Fitness final':<35} {mejor_con.fitness:<20.1f} {mejor_sin.fitness:<20.1f} {diff_fitness:+.1f} {simbolo_fitness}")
    
    # Puntos
    diff_puntos = mejor_con.puntos_totales - mejor_sin.puntos_totales
    print(f"{'Puntos totales':<35} {mejor_con.puntos_totales:<20} {mejor_sin.puntos_totales:<20} {diff_puntos:+d}")
    
    # Iteraciones
    diff_iter = stats_con["iteraciones_realizadas"] - stats_sin["iteraciones_realizadas"]
    print(f"{'Iteraciones realizadas':<35} {stats_con['iteraciones_realizadas']:<20,} {stats_sin['iteraciones_realizadas']:<20,} {diff_iter:+,}")
    
    # Mejoras encontradas
    diff_mejoras = stats_con["mejoras_encontradas"] - stats_sin["mejoras_encontradas"]
    simbolo_mejoras = "✅ CON" if diff_mejoras > 0 else "✅ SIN" if diff_mejoras < 0 else "="
    print(f"{'Mejoras encontradas':<35} {stats_con['mejoras_encontradas']:<20} {stats_sin['mejoras_encontradas']:<20} {diff_mejoras:+d} {simbolo_mejoras}")
    
    # Tasa de aceptación
    diff_tasa = stats_con["tasa_aceptacion"] - stats_sin["tasa_aceptacion"]
    print(f"{'Tasa de aceptación (%)':<35} {stats_con['tasa_aceptacion']:<20.2f} {stats_sin['tasa_aceptacion']:<20.2f} {diff_tasa:+.2f}")
    
    # Tiempo
    diff_tiempo = stats_con["tiempo_ejecucion_minutos"] - stats_sin["tiempo_ejecucion_minutos"]
    print(f"{'Tiempo de ejecución (min)':<35} {stats_con['tiempo_ejecucion_minutos']:<20.2f} {stats_sin['tiempo_ejecucion_minutos']:<20.2f} {diff_tiempo:+.2f}")
    
    print(f"{'-'*95}")
    
    # Conclusiones
    if diff_fitness > 0:
        mejora_pct = (diff_fitness / abs(mejor_sin.fitness)) * 100 if mejor_sin.fitness != 0 else 0
        print(f"\n🏆 CONCLUSIÓN: El uso de 2-opt MEJORÓ el resultado en {mejora_pct:.2f}%")
        print(f"   La optimización 2-opt ayuda a encontrar mejores rutas locales.")
    elif diff_fitness < 0:
        empeora_pct = (abs(diff_fitness) / abs(mejor_con.fitness)) * 100 if mejor_con.fitness != 0 else 0
        print(f"\n⚠️  CONCLUSIÓN: El uso de 2-opt EMPEORÓ el resultado en {empeora_pct:.2f}%")
        print(f"   Esto puede indicar que 2-opt consume tiempo que podría usarse en más iteraciones.")
    else:
        print(f"\n🤝 CONCLUSIÓN: Ambas configuraciones produjeron resultados similares")
    
    # Crear gráficas comparativas
    import matplotlib.pyplot as plt
    from datetime import datetime
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Comparación: Con vs Sin Optimización 2-opt', fontsize=16, fontweight='bold')
    
    # Gráfica 1: Evolución del fitness
    axes[0, 0].plot(resultados_con["historial_mejor_fitness"], label='Con 2-opt', linewidth=2, color='green')
    axes[0, 0].plot(resultados_sin["historial_mejor_fitness"], label='Sin 2-opt', linewidth=2, color='red')
    axes[0, 0].set_title('Evolución del Mejor Fitness')
    axes[0, 0].set_xlabel('Iteración')
    axes[0, 0].set_ylabel('Fitness')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    
    # Gráfica 2: Fitness final
    axes[0, 1].bar(['Con 2-opt', 'Sin 2-opt'], [mejor_con.fitness, mejor_sin.fitness], 
                   color=['green', 'red'], alpha=0.7)
    axes[0, 1].set_title('Fitness Final')
    axes[0, 1].set_ylabel('Fitness')
    axes[0, 1].grid(axis='y', alpha=0.3)
    for i, v in enumerate([mejor_con.fitness, mejor_sin.fitness]):
        axes[0, 1].text(i, v, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfica 3: Mejoras encontradas
    axes[1, 0].bar(['Con 2-opt', 'Sin 2-opt'], 
                   [stats_con['mejoras_encontradas'], stats_sin['mejoras_encontradas']], 
                   color=['green', 'red'], alpha=0.7)
    axes[1, 0].set_title('Mejoras Encontradas')
    axes[1, 0].set_ylabel('Número de mejoras')
    axes[1, 0].grid(axis='y', alpha=0.3)
    for i, v in enumerate([stats_con['mejoras_encontradas'], stats_sin['mejoras_encontradas']]):
        axes[1, 0].text(i, v, f'{v}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfica 4: Iteraciones por segundo
    iter_por_seg_con = stats_con['iteraciones_realizadas'] / stats_con['tiempo_ejecucion_segundos']
    iter_por_seg_sin = stats_sin['iteraciones_realizadas'] / stats_sin['tiempo_ejecucion_segundos']
    axes[1, 1].bar(['Con 2-opt', 'Sin 2-opt'], [iter_por_seg_con, iter_por_seg_sin], 
                   color=['green', 'red'], alpha=0.7)
    axes[1, 1].set_title('Velocidad de Iteración')
    axes[1, 1].set_ylabel('Iteraciones por segundo')
    axes[1, 1].grid(axis='y', alpha=0.3)
    for i, v in enumerate([iter_por_seg_con, iter_por_seg_sin]):
        axes[1, 1].text(i, v, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Guardar gráfica
    timestamp = datetime.now().strftime("%d_%H_%M")
    fig_filename = f"comparacion_2opt_{timestamp}.png"
    plt.savefig(fig_filename, dpi=150, bbox_inches='tight')
    print(f"\n💾 Gráfica comparativa guardada: {fig_filename}")
    plt.show()
    
    print(f"{'='*80}\n")
    
    return {
        "con_2opt": resultados_con,
        "sin_2opt": resultados_sin,
        "mejor_configuracion": "con_2opt" if diff_fitness > 0 else "sin_2opt" if diff_fitness < 0 else "empate"
    }


def comparar_ga_vs_sa(resultados_ga: Dict, resultados_sa: Dict):
    """
    Compara los resultados del algoritmo genético vs enfriamiento simulado.
    Genera gráficas comparativas y tabla de resultados.
    
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
    print(f"{'-'*90}")
    
    # Fitness
    diff_fitness = mejor_sa.fitness - mejor_ga.fitness
    simbolo_fitness = "✅" if diff_fitness > 0 else "⚠️" if diff_fitness < 0 else "="
    print(f"{'Fitness':<30} {mejor_ga.fitness:<20.1f} {mejor_sa.fitness:<20.1f} {diff_fitness:+.1f} {simbolo_fitness}")
    
    # Puntos
    diff_puntos = mejor_sa.puntos_totales - mejor_ga.puntos_totales
    simbolo_puntos = "✅" if diff_puntos > 0 else "⚠️" if diff_puntos < 0 else "="
    print(f"{'Puntos totales':<30} {mejor_ga.puntos_totales:<20} {mejor_sa.puntos_totales:<20} {diff_puntos:+d} {simbolo_puntos}")
    
    # Tiempo
    diff_tiempo = (mejor_sa.tiempo_total - mejor_ga.tiempo_total) / 60
    simbolo_tiempo = "⚠️" if diff_tiempo > 0 else "✅" if diff_tiempo < 0 else "="
    print(f"{'Tiempo total (h)':<30} {mejor_ga.tiempo_total/60:<20.1f} {mejor_sa.tiempo_total/60:<20.1f} {diff_tiempo:+.1f} {simbolo_tiempo}")
    
    # Distancia
    diff_distancia = mejor_sa.distancia_total - mejor_ga.distancia_total
    simbolo_distancia = "⚠️" if diff_distancia > 0 else "✅" if diff_distancia < 0 else "="
    print(f"{'Distancia total (km)':<30} {mejor_ga.distancia_total:<20.1f} {mejor_sa.distancia_total:<20.1f} {diff_distancia:+.1f} {simbolo_distancia}")
    
    print(f"{'-'*90}")
    
    # Tiempo de ejecución de algoritmos
    tiempo_ga = resultados_ga.get("tiempo_ejecucion_segundos", 0) / 60
    tiempo_sa = resultados_sa["estadisticas"]["tiempo_ejecucion_minutos"]
    print(f"\n⏱️  Tiempo de ejecución de algoritmos:")
    print(f"  • GA: {tiempo_ga:.2f} minutos")
    print(f"  • SA: {tiempo_sa:.2f} minutos")
    print(f"  • Total híbrido: {tiempo_ga + tiempo_sa:.2f} minutos")
    
    if diff_fitness > 0:
        mejora_pct = (diff_fitness / abs(mejor_ga.fitness)) * 100
        print(f"\n🏆 El enfriamiento simulado MEJORÓ la solución del GA en {mejora_pct:.2f}%")
    elif diff_fitness < 0:
        empeora_pct = (abs(diff_fitness) / abs(mejor_ga.fitness)) * 100
        print(f"\n📉 El enfriamiento simulado empeoró ligeramente ({empeora_pct:.2f}%)")
    else:
        print(f"\n🤝 Ambos algoritmos encontraron soluciones de calidad similar")
    
    # Crear gráfica comparativa
    import matplotlib.pyplot as plt
    from datetime import datetime
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Comparación GA vs SA', fontsize=16, fontweight='bold')
    
    # Gráfica 1: Fitness
    axes[0, 0].bar(['GA', 'SA'], [mejor_ga.fitness, mejor_sa.fitness], color=['#3498db', '#e74c3c'])
    axes[0, 0].set_title('Fitness Final')
    axes[0, 0].set_ylabel('Fitness')
    axes[0, 0].grid(axis='y', alpha=0.3)
    for i, v in enumerate([mejor_ga.fitness, mejor_sa.fitness]):
        axes[0, 0].text(i, v, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfica 2: Puntos totales
    axes[0, 1].bar(['GA', 'SA'], [mejor_ga.puntos_totales, mejor_sa.puntos_totales], color=['#3498db', '#e74c3c'])
    axes[0, 1].set_title('Puntos Totales')
    axes[0, 1].set_ylabel('Puntos')
    axes[0, 1].grid(axis='y', alpha=0.3)
    for i, v in enumerate([mejor_ga.puntos_totales, mejor_sa.puntos_totales]):
        axes[0, 1].text(i, v, f'{v}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfica 3: Tiempo y distancia
    x = ['Tiempo (h)', 'Distancia (km)']
    ga_vals = [mejor_ga.tiempo_total/60, mejor_ga.distancia_total]
    sa_vals = [mejor_sa.tiempo_total/60, mejor_sa.distancia_total]
    
    x_pos = range(len(x))
    width = 0.35
    axes[1, 0].bar([p - width/2 for p in x_pos], ga_vals, width, label='GA', color='#3498db')
    axes[1, 0].bar([p + width/2 for p in x_pos], sa_vals, width, label='SA', color='#e74c3c')
    axes[1, 0].set_title('Tiempo y Distancia')
    axes[1, 0].set_xticks(x_pos)
    axes[1, 0].set_xticklabels(x)
    axes[1, 0].legend()
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Gráfica 4: Mejora porcentual
    metricas = ['Fitness', 'Puntos', 'Tiempo', 'Distancia']
    mejoras = [
        (diff_fitness / abs(mejor_ga.fitness)) * 100 if mejor_ga.fitness != 0 else 0,
        (diff_puntos / mejor_ga.puntos_totales) * 100 if mejor_ga.puntos_totales != 0 else 0,
        -(diff_tiempo / (mejor_ga.tiempo_total/60)) * 100 if mejor_ga.tiempo_total != 0 else 0,  # Negativo porque menos tiempo es mejor
        -(diff_distancia / mejor_ga.distancia_total) * 100 if mejor_ga.distancia_total != 0 else 0  # Negativo porque menos distancia es mejor
    ]
    
    colores = ['green' if m > 0 else 'red' if m < 0 else 'gray' for m in mejoras]
    axes[1, 1].barh(metricas, mejoras, color=colores, alpha=0.7)
    axes[1, 1].set_title('Mejora SA vs GA (%)')
    axes[1, 1].set_xlabel('% Mejora (verde=mejor)')
    axes[1, 1].axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    axes[1, 1].grid(axis='x', alpha=0.3)
    for i, v in enumerate(mejoras):
        axes[1, 1].text(v, i, f'{v:+.2f}%', va='center', fontweight='bold')
    
    plt.tight_layout()
    
    # Guardar gráfica
    timestamp = datetime.now().strftime("%d_%H_%M")
    fig_filename = f"comparacion_ga_vs_sa_{timestamp}.png"
    plt.savefig(fig_filename, dpi=150, bbox_inches='tight')
    print(f"\n💾 Gráfica comparativa guardada: {fig_filename}")
    plt.show()
    
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
            "nombre": "Comparar CON vs SIN 2-opt",
            "descripcion": "Ejecuta SA dos veces para comparar el impacto de 2-opt",
            "funcion": "comparar_2opt"
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
            alpha=0.97,
            max_tiempo_segundos=3600,  # 1 hora
            iteraciones_sin_mejora_max=1000,
            usar_2opt=True,
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
            num_dias=30,
            lugares_por_dia=12,
            tam_poblacion=1000,
            num_generaciones=600,
            tasa_elitismo=0.20
        )
        
        print(f"\n{'='*80}")
        print(f"FASE 2: ENFRIAMIENTO SIMULADO (Refinamiento Local)")
        print(f"{'='*80}")
        
        # Ejecutar SA desde el mejor del GA
        resultados_sa = enfriamiento_desde_genetico(
            resultados_genetico=resultados_ga,
            usar_mejor=True,
            T_inicial=2000,  # Temperatura moderada para refinamiento
            alpha=0.97,  # Convergencia balanceada
            max_tiempo_segundos=3600  # 1 hora
        )
        
        # Comparar resultados
        comparar_ga_vs_sa(resultados_ga, resultados_sa)
        
        # Analizar y exportar la mejor solución final
        print(f"\n{'='*80}")
        print(f"📋 ANÁLISIS DE LA SOLUCIÓN FINAL (POST-SA)")
        print(f"{'='*80}")
        analizar_solucion(resultados_sa["mejor_solucion"])
        
        # Guardar resultados automáticamente
        from datetime import datetime
        timestamp = datetime.now().strftime("%d_%H_%M")
        archivo_resultados = f"resultados_sa_hybrid_{timestamp}.json"
        exportar_resultados_sa(resultados_sa, archivo=archivo_resultados)
        print(f"\n💾 Resultados guardados en: {archivo_resultados}")
    
    elif modo_elegido == "comparar_2opt":
        # Modo 3: Comparar con/sin 2-opt
        print(f"\n🔬 Modo 3: Comparación del impacto de 2-opt\n")
        
        # Generar solución inicial común
        print(f"🎲 Generando solución inicial aleatoria...")
        solucion_inicial = crear_individuo_aleatorio(num_dias=20, lugares_por_dia=12)
        evaluar_individuo(solucion_inicial)
        
        # Ejecutar comparación
        resultados_comp = comparar_con_sin_2opt(
            solucion_inicial=solucion_inicial,
            T_inicial=2000,
            alpha=0.97,
            max_tiempo_segundos=1800,  # 30 minutos cada uno
            verbose=True
        )
        
        # Guardar resultados
        from datetime import datetime
        timestamp = datetime.now().strftime("%d_%H_%M")
        
        print(f"\n💾 Guardando resultados...")
        exportar_resultados_sa(resultados_comp["con_2opt"], archivo=f"resultados_con_2opt_{timestamp}.json")
        exportar_resultados_sa(resultados_comp["sin_2opt"], archivo=f"resultados_sin_2opt_{timestamp}.json")
        
        print(f"\n✅ Comparación completada. Mejor configuración: {resultados_comp['mejor_configuracion']}")
    
    print(f"\n✅ Ejecución completada exitosamente!")
