import random
import copy
import math
import logging
from datetime import datetime
from typing import Dict, Tuple
from config import *
from utils_espana import (
    COORDENADAS_CIUDADES,
    get_lugares_ciudad,
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
tiempo_ejecucion = 4 # en horas (2 horas)
# tiempo_ejecucion = 0.01 # en horas (36 segundos)
# Configurar logging
def configurar_logging_sa(nombre_archivo: str = None):
    """Configura el sistema de logging para enfriamiento simulado"""
    import os
    
    # Crear carpeta de logs si no existe
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    if nombre_archivo is None:
        timestamp = datetime.now().strftime("%d_%H_%M")
        nombre_archivo = f"{timestamp}_sa.log"
    
    # Guardar el log en la carpeta logs
    ruta_log = os.path.join(logs_dir, nombre_archivo)
    
    # Crear logger
    logger = logging.getLogger('EnfriamientoSimulado')
    logger.setLevel(logging.DEBUG)
    
    # Limpiar handlers existentes
    logger.handlers.clear()
    
    # Handler para archivo
    fh = logging.FileHandler(ruta_log, encoding='utf-8')
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
    
    return logger, ruta_log

# Inicializar logger global
sa_logger = None


def eliminar_duplicados_dia(individuo: Individual) -> Individual:
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


def generar_vecino(solucion_actual: Individual, tiempo_transcurrido: float = 0.0, max_tiempo_segundos: float = 3600.0, usar_2opt: bool = True,   
                    fase_anterior: str = "") -> Tuple[Individual, str]:
    # Crear copia profunda para no modificar la original
    vecino = Individual(
        [dia[:] for dia in solucion_actual.dias],
        solucion_actual.ciudades[:]
    )

    # AJUSTE CLAVE: Calcular progreso basado en tiempo
    progreso = tiempo_transcurrido / max_tiempo_segundos if max_tiempo_segundos > 0 else 0
    # Asegurarse de que el progreso no supere 1.0 (por si acaso)
    progreso = min(progreso, 1.0)
    
    # Determinar fase actual con 3 etapas claras
    fase_actual = ""
    if progreso < 0.3:  # Primeros 30% del tiempo
        fase_actual = "Inicial (Exploración)"
    elif progreso < 0.7:  # 30-70% del tiempo
        fase_actual = "Intermedia (Balance)"
    else:  # Últimos 30% del tiempo
        fase_actual = "Final (Refinamiento)"

    # --- IMPRIMIR SOLO SI LA FASE CAMBIA ---
    if fase_actual != fase_anterior:
        sa_logger.info(f"--- Cambiando a Fase: {fase_actual} (Progreso: {progreso:.1%}) ---")
    # ----------------------------------------
    
    if usar_2opt:
        if fase_actual == "Inicial (Exploración)":
            # Exploración agresiva: más cambios grandes
            # swap, 2opt, reemplazar, swap_intercity, cambiar_ciudad
            probabilidades = [0.25, 0.20, 0.25, 0.20, 0.10] 
        elif fase_actual == "Intermedia (Balance)":
            # Balance: reducir cambios drásticos
            probabilidades = [0.35, 0.25, 0.25, 0.10, 0.05]
        else: # Final (Refinamiento)
            # Solo ajustes finos: swap y 2opt
            probabilidades = [0.50, 0.40, 0.10, 0.0, 0.0]
    else:
        if fase_actual == "Inicial (Exploración)":
            # Sin 2opt: compensar con más swaps
            probabilidades = [0.40, 0.0, 0.25, 0.20, 0.15]
        elif fase_actual == "Intermedia (Balance)":
            probabilidades = [0.55, 0.0, 0.25, 0.12, 0.08]
        else: # Final
            probabilidades = [0.70, 0.0, 0.20, 0.10, 0.0]
    
    tipo_perturbacion = random.choices(
        ["swap", "ruta_2opt", "reemplazar", "swap_intercity", "cambiar_ciudad"],
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
    elif tipo_perturbacion == "cambiar_ciudad":
        # PERTURBACIÓN MEDIA/ALTA: Cambiar la ciudad de un día
        if len(vecino.dias) > 0:
            dia_idx = random.randint(0, len(vecino.dias) - 1)
            ciudad_actual_del_dia = vecino.ciudades[dia_idx]

            # Obtener una nueva ciudad (que no sea la misma)
            candidatas = [c for c in COORDENADAS_CIUDADES.keys() if c != ciudad_actual_del_dia]
            if candidatas:
                nueva_ciudad = random.choice(candidatas)
                vecino.ciudades[dia_idx] = nueva_ciudad
                
                # Reconstruir el día con lugares de la nueva ciudad
                lugares_nueva = get_lugares_ciudad(nueva_ciudad)
                if lugares_nueva:
                    # Asegurarse de que el día tenga el mismo número de lugares
                    num_lugares = len(vecino.dias[dia_idx])
                    if num_lugares == 0: num_lugares = 12 # Default si el día estaba vacío
                    
                    # Usar choices para permitir repetición si no hay suficientes lugares únicos
                    vecino.dias[dia_idx] = [
                        random.choice(lugares_nueva)["id"] for _ in range(num_lugares)
                    ]
    
    # Validar y reparar si es necesario
    if not validar_restricciones_ciudades(vecino):
        vecino = reparar_individuo(vecino)
    
    # Eliminar duplicados en cada día
    vecino = eliminar_duplicados_dia(vecino)

    return vecino, fase_actual


def calcular_temperatura_inicial(solucion_inicial: Individual, num_muestras: int = 100) -> float:
    deltas = []
    
    for _ in range(num_muestras):
        vecino, _ = generar_vecino(solucion_inicial)
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
        T0 = max(10, min(T0, 100))  # Rango ajustado: 10-100 (antes 500-5000)
    else:
        T0 = 50  # Valor por defecto más bajo
    
    return T0


def calcular_temperatura_adaptativa(tiempo_transcurrido: float, max_tiempo: float, 
                                     T_inicial: float, T_final: float = 0.1) -> float:
    """
    Calcula temperatura usando enfriamiento NO-LINEAL basado en tiempo.
    Usa una curva exponencial para enfriar más rápido al inicio.
    
    Args:
        tiempo_transcurrido: Tiempo en segundos desde el inicio
        max_tiempo: Tiempo máximo de ejecución en segundos
        T_inicial: Temperatura inicial
        T_final: Temperatura final mínima
    
    Returns:
        Temperatura actual
    """
    if max_tiempo <= 0:
        return T_final
    
    progreso = min(tiempo_transcurrido / max_tiempo, 1.0)
    
    # Enfriamiento EXPONENCIAL: enfría rápido al inicio, lento al final
    # Esto permite explorar al inicio y refinar al final
    import math
    factor_exp = math.exp(-3 * progreso)  # e^(-3*p): 1.0 → 0.05
    
    # Interpolación con curva exponencial
    temperatura = T_final + (T_inicial - T_final) * factor_exp
    
    return max(temperatura, T_final)


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
    iteraciones_sin_mejora_max: int = 999999,
    usar_2opt: bool = True,  # Nuevo parámetro para controlar 2-opt
    usar_temp_adaptativa: bool = True,  # NUEVO: usar temperatura adaptativa
    verbose: bool = True,
    debug_saltos: bool = True  # Nuevo: activar detección de saltos anormales
) -> Dict:
    global sa_logger
    
    # Configurar logging
    if sa_logger is None:
        sa_logger, log_file = configurar_logging_sa()
        sa_logger.info(f"📝 Log guardándose en: {log_file}")
    
    sa_logger.info("="*80)
    sa_logger.info("🔥 INICIANDO ENFRIAMIENTO SIMULADO")
    sa_logger.info("="*80)
    
    # Importar time para medir tiempo de ejecución
    import time
    tiempo_inicio = time.time()
    
    # Generar o usar solución inicial
    if solucion_inicial is None:
        sa_logger.info("🎲 Generando solución inicial aleatoria...")
        # Usar parámetros por defecto
        solucion_inicial = crear_individuo_aleatorio(num_dias=20, lugares_por_dia=12)
        # Evaluar solución inicial aleatoria
        evaluar_individuo(solucion_inicial)
        sa_logger.info(f"Solución inicial creada - Fitness: {solucion_inicial.fitness:.1f}, Puntos: {solucion_inicial.puntos_totales}")
    else:
        sa_logger.info("🚀 Usando solución inicial proporcionada (warm start)...")
        sa_logger.info(f"  • Fitness reportado por el GA: {solucion_inicial.fitness:.1f}")
        sa_logger.info(f"  • Puntos reportados por el GA: {solucion_inicial.puntos_totales}")
        
        sa_logger.info(f"Usando solución inicial proporcionada - Fitness: {solucion_inicial.fitness:.1f}, Puntos: {solucion_inicial.puntos_totales}")
        
        # CRÍTICO: Hacer copia profunda SIN perder el fitness
        # El módulo copy ya está importado al inicio del archivo
        solucion_inicial = copy.deepcopy(solucion_inicial)
        
        sa_logger.debug(f"  • Fitness después de copia (sin cambios): {solucion_inicial.fitness:.1f}")
        
        sa_logger.debug(f"Copia profunda realizada - Fitness: {solucion_inicial.fitness:.1f}")
    
    # Eliminar duplicados de la solución inicial (si los hay)
    # IMPORTANTE: Solo si realmente hay duplicados, para no re-evaluar
    tiene_duplicados = False
    for dia in solucion_inicial.dias:
        if len(dia) != len(set(dia)):
            tiene_duplicados = True
            break
    
    if tiene_duplicados:
        sa_logger.warning("⚠️  ¡ATENCIÓN! La solución del GA contiene lugares duplicados en el mismo día.")
        sa_logger.warning("Esto infla artificialmente el fitness del GA porque no los penaliza.")
        sa_logger.warning("Procedo a limpiar la solución y a re-evaluarla para obtener el fitness REAL.")
        solucion_inicial = eliminar_duplicados_dia(solucion_inicial)
        # Re-evaluar solo si modificamos
        evaluar_individuo(solucion_inicial)
        sa_logger.info(f"  • Fitness REAL después de limpiar duplicados: {solucion_inicial.fitness:.1f}")
    else:
        sa_logger.info("  ✅ La solución del GA es válida (sin duplicados).")
    
    # Calcular temperatura inicial si no se proporcionó
    if T_inicial is None:
        sa_logger.info("🌡️  Calculando temperatura inicial adaptativa...")
        T_inicial = calcular_temperatura_inicial(solucion_inicial)
    
    # AJUSTE CRÍTICO: Si usa temperatura adaptativa, la temperatura inicial
    # debe ser proporcional al tiempo disponible para evitar sobre-exploración
    if usar_temp_adaptativa and max_tiempo_segundos > 0:
        # Regla empírica: T_inicial óptima depende del tiempo
        # Para 2h (7200s): T=5-10 es suficiente
        # Para 1h (3600s): T=3-5
        # Para 30min (1800s): T=2-3
        factor_tiempo = max_tiempo_segundos / 3600  # Normalizar por 1 hora
        T_inicial_sugerida = 5 * factor_tiempo  # Escala lineal
        
        if T_inicial > T_inicial_sugerida * 3:  # Si es más de 3x lo sugerido
            T_vieja = T_inicial
            T_inicial = T_inicial_sugerida
            sa_logger.warning(f"⚠️  T_inicial={T_vieja:.1f} es muy alta para temp. adaptativa con {max_tiempo_segundos/60:.0f}min")
            sa_logger.warning(f"   Ajustada automáticamente a T_inicial={T_inicial:.1f} para evitar sobre-exploración")
    
    sa_logger.info("📊 Configuración para Enfriamiento Simulado:")
    sa_logger.info(f"  • Temperatura inicial: {T_inicial:.1f}")
    sa_logger.info(f"  • Temperatura mínima: {T_minima}")
    sa_logger.info(f"  • Tipo de enfriamiento: {'🔄 ADAPTATIVO (lineal por tiempo)' if usar_temp_adaptativa else f'🌡️  GEOMÉTRICO (α={alpha})'}")
    if not usar_temp_adaptativa:
        sa_logger.info(f"  • Factor de enfriamiento (α): {alpha}")
    if max_iteraciones:
        sa_logger.info(f"  • Máx. iteraciones: {max_iteraciones:,}")
    sa_logger.info(f"  • Máx. tiempo: {max_tiempo_segundos/60:.1f} minutos ({max_tiempo_segundos/3600:.1f} horas)")
    sa_logger.info(f"  • Máx. iter. sin mejora: {iteraciones_sin_mejora_max:,}")
    sa_logger.info(f"  • Usar optimización 2-opt: {'✅ SÍ' if usar_2opt else '❌ NO'}")
    sa_logger.info(f"  • Fitness inicial (REAL): {solucion_inicial.fitness:.1f}")
    sa_logger.info(f"  • Puntos iniciales (REAL): {solucion_inicial.puntos_totales}")
    sa_logger.info("="*80)
    
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
    ax.set_ylabel("Fitness (escala logarítmica)")
    ax.set_yscale('log')  # Escala logarítmica en eje Y
    line_actual, = ax.plot([], [], label="Fitness actual")
    line_mejor, = ax.plot([], [], label="Mejor fitness global")
    ax.legend()
    ax.grid(True, alpha=0.3, which='both', linestyle='--')  # Grid para ambas escalas
    
    
    
    
    
    sa_logger.info("🔄 Iniciando búsqueda...")
    
    sa_logger.info("Iniciando búsqueda por vecindario")
    sa_logger.info(f"Configuración: T_inicial={T_inicial}, alpha={alpha}, max_tiempo={max_tiempo_segundos}s, usar_2opt={usar_2opt}")
    
    # Bucle principal
    iteracion = 0
    fitness_anterior = solucion_actual.fitness  # Para detectar saltos
    fase_actual_sa = ""
    
    # NUEVO: Detección de degradación
    ultima_mejora_iter = 0
    fitness_medio_reciente = []  # Ventana deslizante de fitness
    VENTANA_DEGRADACION = 50  # Cada 50 iteraciones (más frecuente)
    UMBRAL_DEGRADACION = 20   # Si cae más de 20 puntos (más estricto)
    
    while True:
        # Verificar tiempo transcurrido
        tiempo_transcurrido = time.time() - tiempo_inicio
        
        # Verificar límite de tiempo
        if tiempo_transcurrido >= max_tiempo_segundos:
            sa_logger.info(f"⏰ Tiempo máximo alcanzado: {tiempo_transcurrido/60:.1f} minutos")
            break
        
        tiempo_transcurrido = time.time() - tiempo_inicio
        
        # NUEVO: Detección de degradación cada VENTANA_DEGRADACION iteraciones
        if iteracion > 0 and iteracion % VENTANA_DEGRADACION == 0:
            if len(fitness_medio_reciente) > 0:
                fitness_promedio = sum(fitness_medio_reciente) / len(fitness_medio_reciente)
                
                # Si el fitness promedio es muy bajo comparado con el mejor
                degradacion = mejor_solucion.fitness - fitness_promedio
                
                # Si hay degradación significativa y hace mucho que no mejora
                iteraciones_sin_mejora_real = iteracion - ultima_mejora_iter
                if degradacion > UMBRAL_DEGRADACION and iteraciones_sin_mejora_real > 100:
                    sa_logger.warning(f"⚠️  DEGRADACIÓN DETECTADA en iter {iteracion}:")
                    sa_logger.warning(f"   Mejor fitness: {mejor_solucion.fitness:.1f}")
                    sa_logger.warning(f"   Fitness promedio reciente: {fitness_promedio:.1f}")
                    sa_logger.warning(f"   Degradación: {degradacion:.1f}")
                    sa_logger.warning(f"   🔄 RESTAURANDO mejor solución...")
                    
                    # Restaurar la mejor solución encontrada
                    solucion_actual = copy.deepcopy(mejor_solucion)
                    fitness_medio_reciente.clear()
            
            fitness_medio_reciente.clear()
        
        # Guardar fitness actual en ventana
        fitness_medio_reciente.append(solucion_actual.fitness)
        
        # Generar solución vecina
        vecino, fase_actual_sa = generar_vecino(
            solucion_actual,
            tiempo_transcurrido,
            max_tiempo_segundos,
            usar_2opt,
            fase_anterior=fase_actual_sa # Pasa la fase guardada
        )
        evaluar_individuo(vecino)
        
        # Log detallado cada 100 iteraciones
        if iteracion % 100 == 0:
            sa_logger.debug(f"Iter {iteracion}: T={temperatura:.2f}, Fitness_actual={solucion_actual.fitness:.1f}, Mejor={mejor_solucion.fitness:.1f}")
        
        # Calcular diferencia de fitness
        delta_fitness = vecino.fitness - solucion_actual.fitness
        
        # DETECCIÓN DE SALTOS GRANDES (más de 20 en fitness escalado ~ 2000 en fitness original)
        if debug_saltos and abs(delta_fitness) > 20:
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
                sa_logger.warning(f"⚠️  SALTO ANORMAL DETECTADO en iteración {iteracion}")
                sa_logger.warning(f"   Fitness: {solucion_actual.fitness:.1f} → {vecino.fitness:.1f} (Δ={delta_fitness:+.1f})")
                sa_logger.warning(f"   Ver detalles en archivo de log")
        
        # Decidir si aceptar
        aceptado = aceptar_solucion(delta_fitness, temperatura)
        
        if aceptado:
            # Actualizar solución actual (puede ser peor que la anterior)
            fitness_antes_actualizar = solucion_actual.fitness
            puntos_antes = solucion_actual.puntos_totales
            tiempo_antes = solucion_actual.tiempo_total
            distancia_antes = solucion_actual.distancia_total
            
            solucion_actual = vecino
            total_aceptaciones += 1
            
            # Log si hubo un cambio significativo (>10 en fitness escalado ~ 1000 original)
            if debug_saltos and abs(delta_fitness) > 10:
                sa_logger.info(f"Iter {iteracion}: Aceptada solución con delta={delta_fitness:+.1f} (T={temperatura:.2f})")
                
                # Detalles del cambio
                delta_puntos_cambio = solucion_actual.puntos_totales - puntos_antes
                delta_tiempo_cambio = solucion_actual.tiempo_total - tiempo_antes
                delta_distancia_cambio = solucion_actual.distancia_total - distancia_antes
                
                sa_logger.info(f"  📊 Desglose del cambio:")
                sa_logger.info(f"     Puntos: {delta_puntos_cambio:+d} → {solucion_actual.puntos_totales} total")
                sa_logger.info(f"     Tiempo: {delta_tiempo_cambio:+.1f}min → {solucion_actual.tiempo_total:.1f}min total")
                sa_logger.info(f"     Distancia: {delta_distancia_cambio:+.1f}km → {solucion_actual.distancia_total:.1f}km total")
                
                # Verificar duplicados
                duplicados_despues = sum(1 for dia in solucion_actual.dias if len(dia) != len(set(dia)))
                if duplicados_despues > 0:
                    sa_logger.warning(f"     ⚠️ Nueva solución tiene duplicados en {duplicados_despues} día(s)")
            
            # Verificar si es la MEJOR GLOBAL encontrada hasta ahora
            if solucion_actual.fitness > mejor_solucion.fitness:
                mejora_sobre_mejor = solucion_actual.fitness - mejor_solucion.fitness
                
                # Log detallado para mejoras grandes (>10 en fitness escalado ~ 1000 original)
                if mejora_sobre_mejor > 10:
                    sa_logger.info(f"="*80)
                    sa_logger.info(f"🎯 GRAN MEJORA DETECTADA: +{mejora_sobre_mejor:.1f} puntos de fitness")
                    sa_logger.info(f"  ANTES (mejor anterior):")
                    sa_logger.info(f"    • Fitness: {mejor_solucion.fitness:.1f}")
                    sa_logger.info(f"    • Puntos: {mejor_solucion.puntos_totales}")
                    sa_logger.info(f"    • Tiempo: {mejor_solucion.tiempo_total:.1f}min")
                    sa_logger.info(f"    • Distancia: {mejor_solucion.distancia_total:.1f}km")
                    
                    sa_logger.info(f"  DESPUÉS (nueva mejor):")
                    sa_logger.info(f"    • Fitness: {solucion_actual.fitness:.1f}")
                    sa_logger.info(f"    • Puntos: {solucion_actual.puntos_totales}")
                    sa_logger.info(f"    • Tiempo: {solucion_actual.tiempo_total:.1f}min")
                    sa_logger.info(f"    • Distancia: {solucion_actual.distancia_total:.1f}km")
                    
                    sa_logger.info(f"  DIFERENCIAS:")
                    delta_puntos = solucion_actual.puntos_totales - mejor_solucion.puntos_totales
                    delta_tiempo = solucion_actual.tiempo_total - mejor_solucion.tiempo_total
                    delta_distancia = solucion_actual.distancia_total - mejor_solucion.distancia_total
                    
                    sa_logger.info(f"    • Δ Puntos: {delta_puntos:+d}")
                    sa_logger.info(f"    • Δ Tiempo: {delta_tiempo:+.1f}min")
                    sa_logger.info(f"    • Δ Distancia: {delta_distancia:+.1f}km")
                    
                    # Calcular contribución de cada componente al fitness
                    # Fitness = (puntos - distancia * 0.3) / FITNESS_SCALE_FACTOR
                    contrib_puntos = delta_puntos / FITNESS_SCALE_FACTOR
                    contrib_distancia = -delta_distancia * 0.3 / FITNESS_SCALE_FACTOR
                    
                    sa_logger.info(f"  CONTRIBUCIÓN AL FITNESS:")
                    sa_logger.info(f"    • Puntos: {contrib_puntos:+.1f} (Δ{delta_puntos:+d} × 1.0 ÷ {FITNESS_SCALE_FACTOR})")
                    sa_logger.info(f"    • Distancia: {contrib_distancia:+.1f} (Δ{delta_distancia:+.1f}km × 0.3 ÷ {FITNESS_SCALE_FACTOR})")
                    sa_logger.info(f"    • TOTAL calculado: {contrib_puntos + contrib_distancia:+.2f}")
                    sa_logger.info(f"    • TOTAL real: {mejora_sobre_mejor:+.2f}")
                    diferencia_calc = abs((contrib_puntos + contrib_distancia) - mejora_sobre_mejor)
                    if diferencia_calc > 1:  # Ajustado a escala (era 10)
                        sa_logger.warning(f"    ⚠️ Discrepancia de {diferencia_calc:.2f} (probablemente por penalizaciones)")
                    
                    # Verificar duplicados
                    for dia_idx, dia in enumerate(solucion_actual.dias):
                        if len(dia) != len(set(dia)):
                            duplicados = [x for x in dia if dia.count(x) > 1]
                            sa_logger.warning(f"    ⚠️ Día {dia_idx+1} tiene duplicados: {set(duplicados)}")
                    
                    sa_logger.info(f"="*80)
                
                mejor_solucion = copy.deepcopy(solucion_actual)
                iteraciones_sin_mejora = 0
                mejoras_encontradas += 1
                ultima_mejora_iter = iteracion  # NUEVO: Actualizar última mejora
                
                sa_logger.info(f"🌟 MEJORA #{mejoras_encontradas} en iter {iteracion}: Fitness={mejor_solucion.fitness:.1f} (+{mejora_sobre_mejor:.1f}), Puntos={mejor_solucion.puntos_totales}")
                
                if verbose and mejoras_encontradas % 5 == 0:
                    sa_logger.info(f"  ✨ Mejora #{mejoras_encontradas} en iteración {iteracion+1}: "
                          f"Fitness = {mejor_solucion.fitness:.1f} | "
                          f"Puntos = {mejor_solucion.puntos_totales} | "
                          f"T = {temperatura:.2f}")
            else:
                iteraciones_sin_mejora += 1
        else:
            # Solución rechazada, mantener la actual
            total_rechazos += 1
            iteraciones_sin_mejora += 1
            
            # Log rechazos significativos (>20 en fitness escalado ~ 2000 original)
            if debug_saltos and delta_fitness > 20:
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
        
        # Actualizar temperatura según el método elegido
        if usar_temp_adaptativa:
            # Enfriamiento adaptativo (lineal por tiempo)
            temperatura = calcular_temperatura_adaptativa(
                tiempo_transcurrido, 
                max_tiempo_segundos, 
                T_inicial, 
                T_minima
            )
        else:
            # Enfriamiento geométrico tradicional
            temperatura = temperatura * alpha
        
        # Mostrar progreso periódicamente
        if verbose and (iteracion + 1) % 500 == 0:
            tasa_aceptacion = total_aceptaciones / (iteracion + 1) * 100
            tiempo_transcurrido = time.time() - tiempo_inicio
            progreso_tiempo = (tiempo_transcurrido / max_tiempo_segundos) * 100
            sa_logger.info(f"  Iter {iteracion+1:5d} | "
                  f"Tiempo: {tiempo_transcurrido/60:6.1f}min ({progreso_tiempo:4.1f}%) | "
                  f"T = {temperatura:8.2f} | "
                  f"Fitness = {solucion_actual.fitness:8.1f} | "
                  f"Mejor = {mejor_solucion.fitness:8.1f} | "
                  f"Aceptación = {tasa_aceptacion:5.1f}%")
            
            sa_logger.info(f"Progreso iter {iteracion+1}: T={temperatura:.2f}, Fitness={solucion_actual.fitness:.1f}, "
                          f"Mejor={mejor_solucion.fitness:.1f}, Tasa_acept={tasa_aceptacion:.1f}%")
        
        # Condiciones de parada
        if not usar_temp_adaptativa and temperatura < T_minima:
            sa_logger.info(f"❄️  Temperatura mínima alcanzada: {temperatura:.4f} < {T_minima}")
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
    
    # Crear carpeta de graficas si no existe
    graficas_dir = "graficas"
    if not os.path.exists(graficas_dir):
        os.makedirs(graficas_dir)
    
    timestamp = datetime.now().strftime("%d_%H_%M")
    fig_filename = os.path.join(graficas_dir, f"evolucion_fitness_sa_{timestamp}.png")
    plt.savefig(fig_filename, dpi=150, bbox_inches='tight')
    sa_logger.info(f"💾 Gráfica guardada: {fig_filename}")
    
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
    
    sa_logger.info("="*80)
    sa_logger.info("✅ ENFRIAMIENTO SIMULADO COMPLETADO")
    sa_logger.info("="*80)
    sa_logger.info("")
    sa_logger.info("📈 Estadísticas:")
    sa_logger.info(f"  • Iteraciones realizadas: {iteraciones_realizadas:,}")
    sa_logger.info(f"  • Tiempo de ejecución: {tiempo_total_ejecucion/60:.2f} minutos ({tiempo_total_ejecucion/3600:.2f} horas)")
    sa_logger.info(f"  • Temperatura final: {temperatura:.4f}")
    sa_logger.info(f"  • Total aceptaciones: {total_aceptaciones:,} ({tasa_aceptacion_final:.1f}%)")
    sa_logger.info(f"  • Total rechazos: {total_rechazos:,}")
    sa_logger.info(f"  • Mejoras encontradas: {mejoras_encontradas}")
    sa_logger.info("")
    sa_logger.info("🏆 Resultados:")
    sa_logger.info(f"  • Fitness inicial: {solucion_inicial.fitness:.1f}")
    sa_logger.info(f"  • Fitness final: {mejor_solucion.fitness:.1f}")
    sa_logger.info(f"  • Mejora absoluta: {mejora_absoluta:+.1f}")
    sa_logger.info(f"  • Mejora porcentual: {mejora_porcentual:+.2f}%")
    sa_logger.info(f"  • Puntos totales: {mejor_solucion.puntos_totales}")
    sa_logger.info(f"  • Tiempo total: {mejor_solucion.tiempo_total/60:.1f}h")
    sa_logger.info(f"  • Distancia total: {mejor_solucion.distancia_total:.1f}km")
    sa_logger.info("="*80)
    
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
    T_inicial: float = 10,  # Temperatura baja para refinamiento (era 20)
    alpha: float = 0.98,    # Solo usado si no se usa temp. adaptativa
    max_tiempo_segundos: float = 3600,  # 1 hora por defecto
    usar_temp_adaptativa: bool = True  # NUEVO: usar temperatura adaptativa
) -> Dict:
    sa_logger.info("="*80)
    sa_logger.info("🔗 ENFRIAMIENTO SIMULADO DESDE ALGORITMO GENÉTICO (HÍBRIDO GA+SA)")
    sa_logger.info("="*80)
    
    if usar_mejor:
        sa_logger.info("📍 Estrategia: Partir del MEJOR individuo del GA")
        solucion_inicial = resultados_genetico["mejor_individuo"]
    else:
        sa_logger.info("📍 Estrategia: Partir de un individuo del TOP 10 del GA")
        poblacion_final = resultados_genetico.get("poblacion_final", [])
        if poblacion_final:
            top_10 = sorted(poblacion_final, key=lambda x: x.fitness, reverse=True)[:10]
            solucion_inicial = random.choice(top_10)
            sa_logger.info(f"  • Seleccionado individuo con fitness: {solucion_inicial.fitness:.1f}")
        else:
            sa_logger.warning("  ⚠️  No hay población final, usando mejor individuo")
            solucion_inicial = resultados_genetico["mejor_individuo"]
    
    sa_logger.info("")
    sa_logger.info("💡 Configuración OPTIMIZADA de refinamiento:")
    sa_logger.info(f"  • Temperatura inicial: {T_inicial} (baja para refinamiento local)")
    sa_logger.info(f"  • Enfriamiento: {'Adaptativo (lineal por tiempo)' if usar_temp_adaptativa else f'Geométrico (α={alpha})'}")
    sa_logger.info(f"  • Tiempo máximo: {max_tiempo_segundos/60:.1f} minutos ({max_tiempo_segundos/3600:.1f} horas)")
    sa_logger.info(f"  • Vecindad adaptativa: 5 tipos de perturbaciones con probabilidades dinámicas")
    sa_logger.info(f"  • Estrategia: Perturbaciones conservadoras que preservan calidad del GA")
    
    # Ejecutar enfriamiento simulado
    resultados_sa = enfriamiento_simulado(
        solucion_inicial=solucion_inicial,
        T_inicial=T_inicial,
        alpha=alpha,
        max_tiempo_segundos=max_tiempo_segundos,
        usar_2opt=True,
        usar_temp_adaptativa=usar_temp_adaptativa,
        verbose=True
    )
    
    return resultados_sa


def exportar_resultados_sa(resultados: Dict, archivo: str = None, config: Dict = None):
    import json
    from datetime import datetime
    
    # Generar nombre de archivo automáticamente si no se proporciona
    if archivo is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo = f"resultados_sa_{timestamp}.json"
    
    mejor = resultados["mejor_solucion"]
    inicial = resultados["solucion_inicial"]
    stats = resultados["estadisticas"]
    
    # Contar tipos de transporte
    transportes_summary = {"avion": 0, "tren": 0, "tren_ave": 0, "bus": 0, "coche": 0, "ferry": 0}
    costo_total_transporte = 0
    tiempo_total_transporte = 0
    
    if hasattr(mejor, 'transportes_intercity') and mejor.transportes_intercity:
        for t in mejor.transportes_intercity:
            tipo = t[3]
            costo = t[5]
            tiempo = t[4]
            if tipo in transportes_summary:
                transportes_summary[tipo] += 1
            costo_total_transporte += costo
            tiempo_total_transporte += tiempo
    
    data = {
        "algoritmo": "Enfriamiento Simulado",
        "timestamp": datetime.now().isoformat(),
        "mejor_solucion": {
            "fitness": mejor.fitness,
            "puntos_totales": mejor.puntos_totales,
            "tiempo_total_min": mejor.tiempo_total,
            "tiempo_total_horas": mejor.tiempo_total / 60,
            "distancia_total_km": mejor.distancia_total,
            "num_dias": len(mejor.dias),
            "lugares_totales": sum(len(dia) for dia in mejor.dias),
            "ciudades_visitadas": list(set(mejor.ciudades)),
            "num_ciudades": len(set(mejor.ciudades)),
            "transportes": {
                "avion": transportes_summary["avion"],
                "tren": transportes_summary["tren"],
                "tren_ave": transportes_summary["tren_ave"],
                "bus": transportes_summary["bus"],
                "coche": transportes_summary["coche"],
                "ferry": transportes_summary["ferry"],
                "costo_total_euros": costo_total_transporte,
                "tiempo_total_min": tiempo_total_transporte,
                "tiempo_total_horas": tiempo_total_transporte / 60
            }
        },
        "solucion_inicial": {
            "fitness": inicial.fitness,
            "puntos_totales": inicial.puntos_totales,
            "tiempo_total_min": inicial.tiempo_total,
            "distancia_total_km": inicial.distancia_total
        },
        "configuracion": {
            "T_inicial": config.get("T_inicial") if config else stats.get("T_inicial", "auto"),
            "T_minima": config.get("T_minima") if config else 0.1,
            "alpha": config.get("alpha") if config else 0.95,
            "max_tiempo_segundos": config.get("max_tiempo_segundos") if config else None,
            "max_tiempo_minutos": config.get("max_tiempo_segundos", 3600) / 60 if config else None,
            "usar_2opt": config.get("usar_2opt", True) if config else True,
            "max_dias_por_ciudad": MAX_DIAS_POR_CIUDAD,
            "agrupar": AGRUPAR
        },
        "estadisticas": {
            "iteraciones_realizadas": stats["iteraciones_realizadas"],
            "tiempo_ejecucion_segundos": stats["tiempo_ejecucion_segundos"],
            "tiempo_ejecucion_minutos": stats["tiempo_ejecucion_minutos"],
            "tiempo_ejecucion_horas": stats["tiempo_ejecucion_segundos"] / 3600,
            "temperatura_inicial": config.get("T_inicial") if config else "auto",
            "temperatura_final": stats["temperatura_final"],
            "total_aceptaciones": stats["total_aceptaciones"],
            "total_rechazos": stats["total_rechazos"],
            "tasa_aceptacion_pct": stats["tasa_aceptacion"],
            "mejoras_encontradas": stats["mejoras_encontradas"],
            "fitness_inicial": stats["fitness_inicial"],
            "fitness_final": stats["fitness_final"],
            "mejora_absoluta": stats["mejora_absoluta"],
            "mejora_porcentual": stats["mejora_porcentual"]
        },
        "itinerario": [
            {
                "dia": i + 1,
                "ciudad": ciudad,
                "lugares_ids": dia,
                "num_lugares": len(dia)
            }
            for i, (dia, ciudad) in enumerate(zip(mejor.dias, mejor.ciudades))
        ],
        "historial": {
            "fitness_actual": resultados["historial_fitness"],
            "mejor_fitness": resultados["historial_mejor_fitness"],
            "temperatura": resultados["historial_temperatura"]
        }
    }
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    if sa_logger:
        sa_logger.info(f"💾 Resultados exportados a: {archivo}")
    
    return archivo


def comparar_con_sin_2opt(
    solucion_inicial: Individual,
    T_inicial: float = 2000,
    alpha: float = 0.97,
    max_tiempo_segundos: float = 1800,  # 30 minutos cada uno
    verbose: bool = True
) -> Dict:
    import copy
    
    sa_logger.info("="*80)
    sa_logger.info("🔬 EXPERIMENTO: COMPARACIÓN CON/SIN OPTIMIZACIÓN 2-OPT")
    sa_logger.info("="*80)
    
    # Hacer copias de la solución inicial
    solucion_con = copy.deepcopy(solucion_inicial)
    solucion_sin = copy.deepcopy(solucion_inicial)
    
    sa_logger.info("📋 Configuración del experimento:")
    sa_logger.info(f"  • Temperatura inicial: {T_inicial}")
    sa_logger.info(f"  • Factor α: {alpha}")
    sa_logger.info(f"  • Tiempo máximo por ejecución: {max_tiempo_segundos/60:.1f} minutos")
    sa_logger.info(f"  • Fitness inicial: {solucion_inicial.fitness:.1f}")
    
    # Ejecución CON 2-opt
    sa_logger.info("="*80)
    sa_logger.info("🟢 EJECUCIÓN 1: CON Optimización 2-opt")
    sa_logger.info("="*80)
    
    resultados_con = enfriamiento_simulado(
        solucion_inicial=solucion_con,
        T_inicial=T_inicial,
        alpha=alpha,
        max_tiempo_segundos=max_tiempo_segundos,
        usar_2opt=True,
        verbose=verbose
    )
    
    # Ejecución SIN 2-opt
    sa_logger.info("="*80)
    sa_logger.info("🔴 EJECUCIÓN 2: SIN Optimización 2-opt")
    sa_logger.info("="*80)
    
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
    
    sa_logger.info("="*80)
    sa_logger.info("📊 RESULTADOS DE LA COMPARACIÓN 2-OPT")
    sa_logger.info("="*80)
    
    sa_logger.info(f"{'Métrica':<35} {'CON 2-opt':<20} {'SIN 2-opt':<20} {'Diferencia':<20}")
    sa_logger.info("-"*95)
    
    # Fitness final
    diff_fitness = mejor_con.fitness - mejor_sin.fitness
    simbolo_fitness = "✅ CON" if diff_fitness > 0 else "✅ SIN" if diff_fitness < 0 else "="
    sa_logger.info(f"{'Fitness final':<35} {mejor_con.fitness:<20.1f} {mejor_sin.fitness:<20.1f} {diff_fitness:+.1f} {simbolo_fitness}")
    
    # Puntos
    diff_puntos = mejor_con.puntos_totales - mejor_sin.puntos_totales
    sa_logger.info(f"{'Puntos totales':<35} {mejor_con.puntos_totales:<20} {mejor_sin.puntos_totales:<20} {diff_puntos:+d}")
    
    # Iteraciones
    diff_iter = stats_con["iteraciones_realizadas"] - stats_sin["iteraciones_realizadas"]
    sa_logger.info(f"{'Iteraciones realizadas':<35} {stats_con['iteraciones_realizadas']:<20,} {stats_sin['iteraciones_realizadas']:<20,} {diff_iter:+,}")
    
    # Mejoras encontradas
    diff_mejoras = stats_con["mejoras_encontradas"] - stats_sin["mejoras_encontradas"]
    simbolo_mejoras = "✅ CON" if diff_mejoras > 0 else "✅ SIN" if diff_mejoras < 0 else "="
    sa_logger.info(f"{'Mejoras encontradas':<35} {stats_con['mejoras_encontradas']:<20} {stats_sin['mejoras_encontradas']:<20} {diff_mejoras:+d} {simbolo_mejoras}")
    
    # Tasa de aceptación
    diff_tasa = stats_con["tasa_aceptacion"] - stats_sin["tasa_aceptacion"]
    sa_logger.info(f"{'Tasa de aceptación (%)':<35} {stats_con['tasa_aceptacion']:<20.2f} {stats_sin['tasa_aceptacion']:<20.2f} {diff_tasa:+.2f}")
    
    # Tiempo
    diff_tiempo = stats_con["tiempo_ejecucion_minutos"] - stats_sin["tiempo_ejecucion_minutos"]
    sa_logger.info(f"{'Tiempo de ejecución (min)':<35} {stats_con['tiempo_ejecucion_minutos']:<20.2f} {stats_sin['tiempo_ejecucion_minutos']:<20.2f} {diff_tiempo:+.2f}")
    
    sa_logger.info("-"*95)
    
    # Conclusiones
    if diff_fitness > 0:
        mejora_pct = (diff_fitness / abs(mejor_sin.fitness)) * 100 if mejor_sin.fitness != 0 else 0
        sa_logger.info(f"🏆 CONCLUSIÓN: El uso de 2-opt MEJORÓ el resultado en {mejora_pct:.2f}%")
        sa_logger.info(f"   La optimización 2-opt ayuda a encontrar mejores rutas locales.")
    elif diff_fitness < 0:
        empeora_pct = (abs(diff_fitness) / abs(mejor_con.fitness)) * 100 if mejor_con.fitness != 0 else 0
        sa_logger.info(f"⚠️  CONCLUSIÓN: El uso de 2-opt EMPEORÓ el resultado en {empeora_pct:.2f}%")
        sa_logger.info(f"   Esto puede indicar que 2-opt consume tiempo que podría usarse en más iteraciones.")
    else:
        sa_logger.info(f"🤝 CONCLUSIÓN: Ambas configuraciones produjeron resultados similares")
    
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
    axes[0, 0].set_ylabel('Fitness (escala logarítmica)')
    axes[0, 0].set_yscale('log')  # Escala logarítmica
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3, which='both', linestyle='--')
    
    # Gráfica 2: Fitness final
    axes[0, 1].bar(['Con 2-opt', 'Sin 2-opt'], [mejor_con.fitness, mejor_sin.fitness], 
                   color=['green', 'red'], alpha=0.7)
    axes[0, 1].set_title('Fitness Final')
    axes[0, 1].set_ylabel('Fitness (escala logarítmica)')
    axes[0, 1].set_yscale('log')  # Escala logarítmica
    axes[0, 1].grid(axis='y', alpha=0.3, which='both', linestyle='--')
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
    import os
    
    # Crear carpeta de graficas si no existe
    graficas_dir = "graficas"
    if not os.path.exists(graficas_dir):
        os.makedirs(graficas_dir)
    
    timestamp = datetime.now().strftime("%d_%H_%M")
    fig_filename = os.path.join(graficas_dir, f"comparacion_2opt_{timestamp}.png")
    plt.savefig(fig_filename, dpi=150, bbox_inches='tight')
    sa_logger.info(f"💾 Gráfica comparativa guardada: {fig_filename}")
    plt.show()
    
    sa_logger.info("="*80)
    
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
    
    sa_logger.info("="*80)
    sa_logger.info("⚖️  COMPARACIÓN: ALGORITMO GENÉTICO vs ENFRIAMIENTO SIMULADO")
    sa_logger.info("="*80)
    
    sa_logger.info(f"{'Métrica':<30} {'GA':<20} {'SA':<20} {'Diferencia':<20}")
    sa_logger.info("-"*90)
    
    # Fitness
    diff_fitness = mejor_sa.fitness - mejor_ga.fitness
    simbolo_fitness = "✅" if diff_fitness > 0 else "⚠️" if diff_fitness < 0 else "="
    sa_logger.info(f"{'Fitness':<30} {mejor_ga.fitness:<20.1f} {mejor_sa.fitness:<20.1f} {diff_fitness:+.1f} {simbolo_fitness}")
    
    # Puntos
    diff_puntos = mejor_sa.puntos_totales - mejor_ga.puntos_totales
    simbolo_puntos = "✅" if diff_puntos > 0 else "⚠️" if diff_puntos < 0 else "="
    sa_logger.info(f"{'Puntos totales':<30} {mejor_ga.puntos_totales:<20} {mejor_sa.puntos_totales:<20} {diff_puntos:+d} {simbolo_puntos}")
    
    # Tiempo
    diff_tiempo = (mejor_sa.tiempo_total - mejor_ga.tiempo_total) / 60
    simbolo_tiempo = "⚠️" if diff_tiempo > 0 else "✅" if diff_tiempo < 0 else "="
    sa_logger.info(f"{'Tiempo total (h)':<30} {mejor_ga.tiempo_total/60:<20.1f} {mejor_sa.tiempo_total/60:<20.1f} {diff_tiempo:+.1f} {simbolo_tiempo}")
    
    # Distancia
    diff_distancia = mejor_sa.distancia_total - mejor_ga.distancia_total
    simbolo_distancia = "⚠️" if diff_distancia > 0 else "✅" if diff_distancia < 0 else "="
    sa_logger.info(f"{'Distancia total (km)':<30} {mejor_ga.distancia_total:<20.1f} {mejor_sa.distancia_total:<20.1f} {diff_distancia:+.1f} {simbolo_distancia}")
    
    sa_logger.info("-"*90)
    
    # Tiempo de ejecución de algoritmos
    tiempo_ga = resultados_ga.get("tiempo_ejecucion_segundos", 0) / 60
    tiempo_sa = resultados_sa["estadisticas"]["tiempo_ejecucion_minutos"]
    sa_logger.info("")
    sa_logger.info("⏱️  Tiempo de ejecución de algoritmos:")
    sa_logger.info(f"  • GA: {tiempo_ga:.2f} minutos")
    sa_logger.info(f"  • SA: {tiempo_sa:.2f} minutos")
    sa_logger.info(f"  • Total híbrido: {tiempo_ga + tiempo_sa:.2f} minutos")
    
    if diff_fitness > 0:
        mejora_pct = (diff_fitness / abs(mejor_ga.fitness)) * 100
        sa_logger.info(f"🏆 El enfriamiento simulado MEJORÓ la solución del GA en {mejora_pct:.2f}%")
    elif diff_fitness < 0:
        empeora_pct = (abs(diff_fitness) / abs(mejor_ga.fitness)) * 100
        sa_logger.info(f"📉 El enfriamiento simulado empeoró ligeramente ({empeora_pct:.2f}%)")
    else:
        sa_logger.info(f"🤝 Ambos algoritmos encontraron soluciones de calidad similar")
    
    # Crear gráfica comparativa
    import matplotlib.pyplot as plt
    from datetime import datetime
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Comparación GA vs SA', fontsize=16, fontweight='bold')
    
    # Gráfica 1: Fitness
    axes[0, 0].bar(['GA', 'SA'], [mejor_ga.fitness, mejor_sa.fitness], color=['#3498db', '#e74c3c'])
    axes[0, 0].set_title('Fitness Final')
    axes[0, 0].set_ylabel('Fitness (escala logarítmica)')
    axes[0, 0].set_yscale('log')  # Escala logarítmica
    axes[0, 0].grid(axis='y', alpha=0.3, which='both', linestyle='--')
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
    import os
    
    # Crear carpeta de graficas si no existe
    graficas_dir = "graficas"
    if not os.path.exists(graficas_dir):
        os.makedirs(graficas_dir)
    
    timestamp = datetime.now().strftime("%d_%H_%M")
    fig_filename = os.path.join(graficas_dir, f"comparacion_ga_vs_sa_{timestamp}.png")
    plt.savefig(fig_filename, dpi=150, bbox_inches='tight')
    sa_logger.info(f"💾 Gráfica comparativa guardada: {fig_filename}")
    plt.show()
    
    sa_logger.info("="*80)


# Ejecución principal
if __name__ == "__main__":
    import sys
    
    # Inicializar logger global al inicio del programa
    sa_logger, log_file = configurar_logging_sa()
    sa_logger.info(f"📝 Log iniciado: {log_file}")
    
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
        sa_logger.info("🎲 Modo 1: Enfriamiento Simulado desde solución aleatoria")
        
        # Configuración ULTRA-CONSERVADORA para minimizar caídas
        # Con T_inicial=2-3, solo aceptará cambios pequeños (~20% prob para Δ=-2)
        config_sa = {
            "T_inicial": 3,            # MUY BAJA: minimiza aceptación de soluciones malas
            "T_minima": 0.1,
            "alpha": 0.9995,           # Solo usado si usar_temp_adaptativa=False
            "max_tiempo_segundos": tiempo_ejecucion * 3600,
            "usar_2opt": True,
            "usar_temp_adaptativa": True  # Usar enfriamiento adaptativo exponencial
        }
        
        resultados = enfriamiento_simulado(
            solucion_inicial=None,  # Generará una aleatoria
            T_inicial=config_sa["T_inicial"],
            T_minima=config_sa["T_minima"],
            alpha=config_sa["alpha"],
            max_tiempo_segundos=config_sa["max_tiempo_segundos"],
            iteraciones_sin_mejora_max=999999,
            usar_2opt=config_sa["usar_2opt"],
            usar_temp_adaptativa=config_sa["usar_temp_adaptativa"],
            verbose=True,
            debug_saltos=True
        )
        
        # Analizar solución
        sa_logger.info("="*80)
        sa_logger.info("📋 ANÁLISIS DE LA SOLUCIÓN FINAL")
        sa_logger.info("="*80)
        analizar_solucion(resultados["mejor_solucion"])
        
        # Guardar resultados con timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_json = exportar_resultados_sa(resultados, archivo=f"resultados_sa_standalone_{timestamp}.json", config=config_sa)
        
        sa_logger.info("")
        sa_logger.info("✅ Resultados guardados exitosamente:")
        sa_logger.info(f"   • JSON: {archivo_json}")
        sa_logger.info(f"   • Log: {log_file}")
        sa_logger.info(f"   • Gráfica: graficas/evolucion_fitness_sa_*.png")
    
    elif modo_elegido == "hybrid":
        # Modo 2: GA + SA (híbrido)
        sa_logger.info("🔗 Modo 2: Algoritmo Híbrido (GA + SA)")
        sa_logger.info("="*80)
        sa_logger.info("FASE 1: ALGORITMO GENÉTICO (Exploración Global)")
        sa_logger.info("="*80)
        
        from algoritmo_espana import algoritmo_genetico_espana
        
        # Ejecutar GA con configuración rápida
        resultados_ga = algoritmo_genetico_espana(
            num_dias=20,
            lugares_por_dia=12,
            tam_poblacion=1000,
            tiempo_limite_horas= tiempo_ejecucion,
            tasa_elitismo=0.10
        )
        
        sa_logger.info("="*80)
        sa_logger.info("FASE 2: ENFRIAMIENTO SIMULADO (Refinamiento Local)")
        sa_logger.info("="*80)
        
        # Configuración SA MEJORADA - Para refinamiento desde GA
        config_sa = {
            "T_inicial": 10,           # Temperatura baja para refinamiento
            "T_minima": 0.1,
            "alpha": 0.98,             # Solo usado si usar_temp_adaptativa=False
            "max_tiempo_segundos": tiempo_ejecucion * 3600,
            "usar_2opt": True,
            "usar_temp_adaptativa": True  # Enfriamiento adaptativo
        }
        
        # Ejecutar SA desde el mejor del GA
        resultados_sa = enfriamiento_desde_genetico(
            resultados_genetico=resultados_ga,
            usar_mejor=True,
            T_inicial=config_sa["T_inicial"],
            alpha=config_sa["alpha"],
            max_tiempo_segundos=config_sa["max_tiempo_segundos"]
        )
        
        # Comparar resultados
        comparar_ga_vs_sa(resultados_ga, resultados_sa)
        
        # Analizar y exportar la mejor solución final
        sa_logger.info("="*80)
        sa_logger.info("📋 ANÁLISIS DE LA SOLUCIÓN FINAL (POST-SA)")
        sa_logger.info("="*80)
        analizar_solucion(resultados_sa["mejor_solucion"])
        
        # Guardar resultados automáticamente con timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_json = exportar_resultados_sa(resultados_sa, archivo=f"resultados_sa_hybrid_{timestamp}.json", config=config_sa)
        
        sa_logger.info("")
        sa_logger.info("✅ Resultados guardados exitosamente:")
        sa_logger.info(f"   • JSON: {archivo_json}")
        sa_logger.info(f"   • Gráfica comparativa: graficas/comparacion_ga_vs_sa_*.png")
        sa_logger.info(f"   • Gráfica evolución: graficas/evolucion_fitness_sa_*.png")
        sa_logger.info(f"   • Log: {log_file}")
    
    elif modo_elegido == "comparar_2opt":
        # Modo 3: Comparar con/sin 2-opt
        sa_logger.info("🔬 Modo 3: Comparación del impacto de 2-opt")
        
        # Generar solución inicial común
        sa_logger.info("🎲 Generando solución inicial aleatoria...")
        solucion_inicial = crear_individuo_aleatorio(num_dias=20, lugares_por_dia=12)
        evaluar_individuo(solucion_inicial)
        
        # Configuración común
        config_base = {
            "T_inicial": 20,
            "T_minima": 0.1,
            "alpha": 0.999,
            "max_tiempo_segundos": tiempo_ejecucion * 3600  # 30 minutos cada uno
        }
        
        # Ejecutar comparación
        resultados_comp = comparar_con_sin_2opt(
            solucion_inicial=solucion_inicial,
            T_inicial=config_base["T_inicial"],
            alpha=config_base["alpha"],
            max_tiempo_segundos=config_base["max_tiempo_segundos"],
            verbose=True
        )
        
        # Guardar resultados con timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        sa_logger.info("💾 Guardando resultados...")
        
        config_con = config_base.copy()
        config_con["usar_2opt"] = True
        archivo_con = exportar_resultados_sa(
            resultados_comp["con_2opt"], 
            archivo=f"resultados_con_2opt_{timestamp}.json",
            config=config_con
        )
        
        config_sin = config_base.copy()
        config_sin["usar_2opt"] = False
        archivo_sin = exportar_resultados_sa(
            resultados_comp["sin_2opt"], 
            archivo=f"resultados_sin_2opt_{timestamp}.json",
            config=config_sin
        )
        
        sa_logger.info(f"✅ Comparación completada. Mejor configuración: {resultados_comp['mejor_configuracion']}")
        sa_logger.info("")
        sa_logger.info("📊 Archivos generados:")
        sa_logger.info(f"   • JSON con 2-opt: {archivo_con}")
        sa_logger.info(f"   • JSON sin 2-opt: {archivo_sin}")
        sa_logger.info(f"   • Gráfica comparativa: graficas/comparacion_2opt_{timestamp}.png")
        sa_logger.info(f"   • Logs: {log_file}")
    
    sa_logger.info("✅ Ejecución completada exitosamente!")
