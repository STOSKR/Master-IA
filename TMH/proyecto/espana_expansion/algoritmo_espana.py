import random
import copy
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
    validar_limite_ciudad
)

class Individual:
    def __init__(self, dias: List[List[int]], ciudades: List[str]):
        # COPIAS DEFENSIVAS: Evitar referencias compartidas
        self.dias = [dia[:] if isinstance(dia, list) else dia for dia in dias]
        self.ciudades = ciudades[:] if isinstance(ciudades, list) else ciudades
        self.fitness = 0
        self.tiempo_total = 0
        self.puntos_totales = 0
        self.distancia_total = 0
        self.transportes_intercity = []  # [(dia_idx, origen, destino, tipo, tiempo, costo)]

def obtener_ciudad_mas_cercana(ciudad_actual: str, ciudades_visitadas: set, dias_consecutivos_actual: int) -> str:
    
    ciudades_disponibles = list(COORDENADAS_CIUDADES.keys())
    
    # Verificar si debemos forzar cambio por MAX_DIAS_POR_CIUDAD
    debe_cambiar = dias_consecutivos_actual >= MAX_DIAS_POR_CIUDAD
    
    # Filtrar ciudades candidatas
    candidatas = []
    for ciudad in ciudades_disponibles:
        # No puede ser la misma ciudad si debe cambiar
        if debe_cambiar and ciudad == ciudad_actual:
            continue
        # No puede ser una ciudad ya visitada completamente
        if ciudad in ciudades_visitadas:
            continue
        candidatas.append(ciudad)
    
    # Si no hay candidatas sin visitar, permitir revisar ciudades visitadas
    # (esto evita el problema de quedarse bloqueado)
    if not candidatas:
        candidatas = [c for c in ciudades_disponibles if c != ciudad_actual]
    
    # Si aún no hay candidatas, quedarse en la actual (caso extremo)
    if not candidatas:
        return ciudad_actual
    
    # Calcular distancias y elegir la más cercana
    coord_actual = COORDENADAS_CIUDADES[ciudad_actual]
    distancias = []
    
    from math import radians, sin, cos, sqrt, atan2
    
    for ciudad_candidata in candidatas:
        coord_candidata = COORDENADAS_CIUDADES[ciudad_candidata]
        # Calcular distancia usando fórmula de Haversine
        lat1 = float(coord_actual["lat"])
        lon1 = float(coord_actual["lon"])
        lat2 = float(coord_candidata["lat"])
        lon2 = float(coord_candidata["lon"])
        
        R = 6371  # Radio de la Tierra en km
        
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distancia = R * c
        
        distancias.append((ciudad_candidata, distancia))
    
    # Ordenar por distancia y devolver la más cercana
    distancias.sort(key=lambda x: x[1])
    return distancias[0][0]

def validar_restricciones_ciudades(individuo: Individual) -> bool:
    """
    Valida que un individuo cumple con las restricciones de ciudades:
    1. No regresar a una ciudad ya visitada
    2. No más de MAX_DIAS_POR_CIUDAD días consecutivos en la misma ciudad
    
    Returns:
        True si cumple todas las restricciones, False en caso contrario
    """
    ciudades = individuo.ciudades
    
    # Restricción 1: No regresar a ciudades visitadas
    ciudades_vistas = set()
    for i, ciudad in enumerate(ciudades):
        if ciudad in ciudades_vistas:
            # Verificar si es continuación (no hay problema)
            if i > 0 and ciudades[i-1] == ciudad:
                continue
            else:
                return False
        
        # Si cambiamos de ciudad, agregar la anterior al conjunto
        if i > 0 and ciudades[i-1] != ciudad:
            ciudades_vistas.add(ciudades[i-1])
    
    # Restricción 2: No más de MAX_DIAS_POR_CIUDAD días consecutivos
    dias_consecutivos = 1
    ciudad_actual_check = ciudades[0]
    for i in range(1, len(ciudades)):
        if ciudades[i] == ciudad_actual_check:
            dias_consecutivos += 1
            if dias_consecutivos > MAX_DIAS_POR_CIUDAD:
                return False
        else:
            ciudad_actual_check = ciudades[i]
            dias_consecutivos = 1
    
    return True

def reparar_individuo(individuo: Individual) -> Individual:
    """
    Repara un individuo que viola las restricciones de ciudades.
    """
    ciudades_disponibles = list(COORDENADAS_CIUDADES.keys())
    ciudades_visitadas = set()
    
    for dia_idx in range(len(individuo.ciudades)):
        ciudad_actual = individuo.ciudades[dia_idx]
        
        # Verificar días consecutivos
        dias_consecutivos = 1
        for i in range(dia_idx - 1, -1, -1):
            if individuo.ciudades[i] == ciudad_actual:
                dias_consecutivos += 1
            else:
                break
        
        # Verificar si regresa a ciudad visitada
        es_regreso = False
        if dia_idx > 0:
            if ciudad_actual in ciudades_visitadas and individuo.ciudades[dia_idx-1] != ciudad_actual:
                es_regreso = True
        
        # Reparar si es necesario
        if dias_consecutivos > MAX_DIAS_POR_CIUDAD or es_regreso:
            # Obtener ciudad más cercana válida
            ciudad_anterior = individuo.ciudades[dia_idx-1] if dia_idx > 0 else ciudad_actual
            nueva_ciudad = obtener_ciudad_mas_cercana(ciudad_anterior, ciudades_visitadas, dias_consecutivos)
            
            individuo.ciudades[dia_idx] = nueva_ciudad
            
            # Actualizar lugares
            lugares_nueva = get_lugares_ciudad(nueva_ciudad)
            if lugares_nueva:
                num_lugares = len(individuo.dias[dia_idx])
                individuo.dias[dia_idx] = [
                    random.choice(lugares_nueva)["id"] for _ in range(num_lugares)
                ]
        
        # Actualizar conjunto de visitadas
        if dia_idx > 0 and individuo.ciudades[dia_idx] != individuo.ciudades[dia_idx-1]:
            ciudades_visitadas.add(individuo.ciudades[dia_idx-1])
    
    return individuo

def crear_individuo_aleatorio(num_dias: int, lugares_por_dia: int) -> Individual:
    ciudades_disponibles = list(COORDENADAS_CIUDADES.keys())
    dias = []
    ciudades_plan = []
    ciudades_visitadas = set()  # Para rastrear ciudades ya visitadas completamente
    
    if AGRUPAR:
        dia_actual = 0
        ciudad_actual = random.choice(ciudades_disponibles)  # Primera ciudad aleatoria
        
        while dia_actual < num_dias:
            dias_restantes = num_dias - dia_actual
            
            # Limitar días en esta ciudad: máximo MAX_DIAS_POR_CIUDAD
            if dias_restantes == 1:
                dias_en_ciudad = 1
            else:
                dias_en_ciudad = random.randint(1, min(MAX_DIAS_POR_CIUDAD, dias_restantes))
            
            lugares_ciudad = get_lugares_ciudad(ciudad_actual)
            if len(lugares_ciudad) < lugares_por_dia:
                lugares_ciudad = lugares_turisticos_espana
            
            for _ in range(dias_en_ciudad):
                if dia_actual >= num_dias:
                    break
                
                lugares_dia = random.sample(lugares_ciudad, min(lugares_por_dia, len(lugares_ciudad)))
                ids_dia = [l["id"] for l in lugares_dia]
                random.shuffle(ids_dia)
                
                dias.append(ids_dia)
                ciudades_plan.append(ciudad_actual)
                dia_actual += 1
            
            # Marcar ciudad como visitada al salir de ella
            ciudades_visitadas.add(ciudad_actual)
            
            # Elegir siguiente ciudad MÁS CERCANA (si quedan días)
            if dia_actual < num_dias:
                ciudad_actual = obtener_ciudad_mas_cercana(ciudad_actual, ciudades_visitadas, MAX_DIAS_POR_CIUDAD)
    else:
        # Modo sin agrupar: cada día puede ser diferente
        ciudad_actual = random.choice(ciudades_disponibles)  # Primera ciudad aleatoria
        dias_consecutivos = 0
        
        for dia_idx in range(num_dias):
            # Incrementar contador de días consecutivos
            if dia_idx > 0 and ciudades_plan[-1] == ciudad_actual:
                dias_consecutivos += 1
            else:
                dias_consecutivos = 1
            
            # Si alcanzamos MAX_DIAS_POR_CIUDAD, cambiar a ciudad más cercana
            if dias_consecutivos >= MAX_DIAS_POR_CIUDAD:
                ciudades_visitadas.add(ciudad_actual)
                ciudad_actual = obtener_ciudad_mas_cercana(ciudad_actual, ciudades_visitadas, dias_consecutivos)
                dias_consecutivos = 1
            
            lugares_ciudad = get_lugares_ciudad(ciudad_actual)
            if len(lugares_ciudad) < lugares_por_dia:
                lugares_ciudad = lugares_turisticos_espana
            
            lugares_dia = random.sample(lugares_ciudad, min(lugares_por_dia, len(lugares_ciudad)))
            ids_dia = [l["id"] for l in lugares_dia]
            random.shuffle(ids_dia)
            
            dias.append(ids_dia)
            ciudades_plan.append(ciudad_actual)

    
    individuo = Individual(dias, ciudades_plan)
    
    # Validar y reparar si es necesario
    if not validar_restricciones_ciudades(individuo):
        individuo = reparar_individuo(individuo)
    
    return individuo

def crear_poblacion_inicial(tam_poblacion: int, num_dias: int, lugares_por_dia: int) -> List[Individual]:
    return [crear_individuo_aleatorio(num_dias, lugares_por_dia) for _ in range(tam_poblacion)]


def eliminar_duplicados_dia(individuo: Individual) -> Individual:
    """
    Elimina lugares duplicados en cada día, reemplazándolos por lugares únicos de la misma ciudad.
    
    Args:
        individuo: Individuo a limpiar
    
    Returns:
        Individuo sin lugares duplicados (modifica el individuo in-place y lo retorna)
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
                    # Si no hay más lugares disponibles, simplemente no añadimos nada
                    # (el día tendrá menos lugares, pero sin duplicados)
            
            individuo.dias[dia_idx] = lugares_unicos
    
    return individuo


def calcular_tiempo_dia(individuo: Individual, dia_idx: int) -> Tuple[int, int, float]:
    dia = individuo.dias[dia_idx]
    
    if not dia:
        return 0, 0, 0
    
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
        tiempo_total += dist / VELOCIDAD_MEDIA * 60
    
    return tiempo_total, distancia_total, puntos_total

def elegir_mejor_transporte(ciudad_origen: str, ciudad_destino: str, presupuesto_restante: float) -> Tuple[str, int, float]:
    opciones = []
    
    for tipo in ["avion", "tren", "bus"]:
        tiempo, costo = calcular_transporte_intercity(ciudad_origen, ciudad_destino, tipo)
        if tiempo is not None and costo is not None:
            opciones.append((tipo, tiempo, costo))
    
    if not opciones:
        return "tren", 0, 0
    
    if presupuesto_restante > 100:
        opciones.sort(key=lambda x: x[1])
    else:
        opciones.sort(key=lambda x: x[2])
    
    mejor = opciones[0]
    return mejor[0], mejor[1], mejor[2]

def evaluar_individuo(individuo: Individual) -> float:
    fitness = 0
    tiempo_acum = 0
    distancia_acum = 0
    puntos_acum = 0
    gasto_acumulado = 0
    individuo.transportes_intercity = []
    
    for dia_idx in range(len(individuo.dias)):
        tiempo_dia, dist_dia, puntos_dia = calcular_tiempo_dia(individuo, dia_idx)
        lugares_dia = get_lugares_por_ids(individuo.dias[dia_idx])
        
        if AGRUPAR and dia_idx > 0:
            ciudad_actual = individuo.ciudades[dia_idx]
            ciudad_anterior = individuo.ciudades[dia_idx - 1]
            
            if ciudad_actual != ciudad_anterior:
                # Penalizar solo si vuelve a una ciudad reciente (últimos 5 días)
                ciudades_recientes = individuo.ciudades[max(0, dia_idx-5):dia_idx]
                if ciudad_actual in ciudades_recientes:
                    fitness -= PENALIZACION_CAMBIO_CIUDAD_INNECESARIO
        
        if dia_idx > 0 and individuo.ciudades[dia_idx] != individuo.ciudades[dia_idx - 1]:
            dias_restantes = len(individuo.dias) - dia_idx
            presupuesto_restante = (PRESUPUESTO_DIARIO * dias_restantes) - gasto_acumulado
            
            tipo_elegido, tiempo_trans, costo_trans = elegir_mejor_transporte(
                individuo.ciudades[dia_idx - 1],
                individuo.ciudades[dia_idx],
                presupuesto_restante
            )
            
            individuo.transportes_intercity.append((
                dia_idx,
                individuo.ciudades[dia_idx - 1],
                individuo.ciudades[dia_idx],
                tipo_elegido,
                tiempo_trans,
                costo_trans
            ))
            
            if tiempo_trans:
                tiempo_dia += tiempo_trans
            gasto_acumulado += costo_trans
        
        # Penalizaciones básicas (fatiga, etc.)
        # pen_fatiga = aplicar_restricciones_basicas(individuo.dias[dia_idx], tiempo_dia)
        # fitness -= pen_fatiga

        if not validar_limite_ciudad(individuo.ciudades[:dia_idx + 1], individuo.ciudades[dia_idx])[0]:
            fitness -= PENALIZACION_LIMITE_CIUDAD
        
        if tiempo_dia > TIEMPO_DIA:
            exceso = tiempo_dia - TIEMPO_DIA
            if exceso > 0 and exceso <= 120:
                fitness -= PENALIZACION_EXCESO_TIEMPO * exceso
            elif exceso > 120:
                # Penalización más gradual en lugar de catastrófica
                fitness -= PENALIZACION_EXCESO_TIEMPO * 120  # Máximo 120 min
                fitness -= (exceso - 120) * 2  # 2 pts por minuto adicional
        
        hora_actual = HORA_INICIO
        
        # Si hay transporte intercity, añadir tiempo de transporte a hora_actual
        if dia_idx > 0 and individuo.ciudades[dia_idx] != individuo.ciudades[dia_idx - 1]:
            transporte_dia = next((t for t in individuo.transportes_intercity if t[0] == dia_idx), None)
            if transporte_dia and transporte_dia[4]:  # transporte_dia[4] = tiempo_trans
                hora_actual += transporte_dia[4]
        
        tiene_almuerzo = False
        tiene_cena = False
        gasto_dia = 0
        restaurantes_consecutivos = 0
        max_consecutivos = 0
        
        for lugar in lugares_dia:
            tipo = lugar.get('tipo', '')
            
            # Validar horario de apertura/cierre
            if tipo in HORARIOS_TIPO:
                apertura = HORARIOS_TIPO[tipo]["apertura"]
                cierre = HORARIOS_TIPO[tipo]["cierre"]
                
                if tipo == "bar" and cierre < apertura:
                    cierre = 26 * 60
                
                if hora_actual < apertura or hora_actual > cierre:
                    fitness -= PENALIZACION_FUERA_HORARIO_APERTURA
            
            if tipo in PRECIOS_TIPO:
                gasto_dia += PRECIOS_TIPO[tipo]
            else:
                gasto_dia += 10  # Precio por defecto (antes era 20)
            
            # Verificar si es restaurante/bar/cafetería en hora de comida
            if tipo in ['restaurante', 'bar', 'cafetería']:
                if HORA_ALMUERZO_MIN <= hora_actual <= HORA_ALMUERZO_MAX:
                    tiene_almuerzo = True
                elif HORA_CENA_MIN <= hora_actual <= HORA_CENA_MAX:
                    tiene_cena = True
                
                # Contar restaurantes consecutivos
                restaurantes_consecutivos += 1
                max_consecutivos = max(max_consecutivos, restaurantes_consecutivos)
            else:
                restaurantes_consecutivos = 0
            
            hora_actual += lugar['tiempo_visita']
        
        # Acumular gasto del día al acumulado
        gasto_acumulado += gasto_dia
        
        # Validar presupuesto diario
        if gasto_dia > PRESUPUESTO_DIARIO:
            exceso_presupuesto = gasto_dia - PRESUPUESTO_DIARIO
            fitness -= PENALIZACION_EXCESO_PRESUPUESTO * exceso_presupuesto
        
        # Penalizar si no hay almuerzo
        if not tiene_almuerzo:
            fitness -= PENALIZACION_COMIDA_FALTA
        
        # Penalizar si no hay cena
        if not tiene_cena:
            fitness -= PENALIZACION_CENA_FALTA
        
        # Penalizar muchos restaurantes consecutivos
        if max_consecutivos > 3:
            fitness -= PENALIZACION_RESTAURANTES_CONSECUTIVOS * (max_consecutivos - 3)
        
        # Acumular métricas
        tiempo_acum += tiempo_dia
        distancia_acum += dist_dia
        puntos_acum += puntos_dia
    
    # Fitness = puntos - penalizaciones - penalización por distancia
    fitness += puntos_acum
    
    # Penalizar distancia excesiva (0.3 puntos por km - más gradual)
    fitness -= distancia_acum * 0.3
    
    # Guardar métricas
    individuo.tiempo_total = tiempo_acum
    individuo.distancia_total = distancia_acum
    individuo.puntos_totales = puntos_acum
    individuo.fitness = fitness
    
    return fitness

# Operadores genéticos

def seleccion_torneo(poblacion: List[Individual], k: int = 3) -> Individual:
    """Selección por torneo"""
    torneo = random.sample(poblacion, k)
    return max(torneo, key=lambda ind: ind.fitness)

def crossover_dos_puntos(padre1: Individual, padre2: Individual) -> Tuple[Individual, Individual]:
    """Cruce de dos puntos por día"""
    if random.random() > PROBABILIDAD_CRUCE:
        # ¡IMPORTANTE! Devolver COPIAS, no referencias (sino la mutación afecta a los padres)
        hijo1 = Individual([dia[:] for dia in padre1.dias], padre1.ciudades[:])
        hijo2 = Individual([dia[:] for dia in padre2.dias], padre2.ciudades[:])
        return hijo1, hijo2
    
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
                dia[i:j+1] = list(reversed(dia[i:j+1]))
            
            elif tipo == "replace":
                lugares_ciudad = get_lugares_ciudad(ciudad)
                if lugares_ciudad:
                    idx = random.randint(0, len(dia) - 1)
                    nuevo = random.choice(lugares_ciudad)["id"]
                    if nuevo not in dia:
                        dia[idx] = nuevo
        
        # Mutación de ciudad (baja probabilidad) - USANDO CIUDAD MÁS CERCANA
        if random.random() < 0.05:
            # Restricción 1: No regresar a ciudades ya visitadas
            ciudades_visitadas = set(individuo.ciudades[:dia_idx])  # Ciudades antes de este día
            
            # Restricción 2: No más de MAX_DIAS_POR_CIUDAD días consecutivos
            dias_consecutivos_actual = 1
            for i in range(dia_idx - 1, -1, -1):
                if individuo.ciudades[i] == ciudad:
                    dias_consecutivos_actual += 1
                else:
                    break
            
            # Obtener ciudad más cercana válida
            nueva_ciudad = obtener_ciudad_mas_cercana(ciudad, ciudades_visitadas, dias_consecutivos_actual)
            
            # Solo mutar si la nueva ciudad es diferente
            if nueva_ciudad != ciudad:
                individuo.ciudades[dia_idx] = nueva_ciudad
                
                # Reemplazar lugares del día con lugares de nueva ciudad
                lugares_nueva = get_lugares_ciudad(nueva_ciudad)
                if lugares_nueva:
                    individuo.dias[dia_idx] = [
                        random.choice(lugares_nueva)["id"] for _ in range(len(dia))
                    ]
    
    # Validar y reparar después de mutar
    if not validar_restricciones_ciudades(individuo):
        individuo = reparar_individuo(individuo)


def algoritmo_genetico_espana(
    num_dias: int ,
    lugares_por_dia: int,
    tam_poblacion: int,
    num_generaciones: int,
    tasa_elitismo: float
) -> Dict:
    print(f"\n{'='*80}")
    print(f"ALGORITMO GENÉTICO")
    print(f"{'='*80}")
    print(f"Días: {num_dias}")
    print(f"Lugares/día: {lugares_por_dia}")
    print(f"Población: {tam_poblacion}")
    print(f"Generaciones: {num_generaciones}")
    print(f"Elitismo: {tasa_elitismo*100:.0f}%")
    print(f"Dataset: {len(lugares_turisticos_espana)} lugares en 10 ciudades")
    print(f"{'='*80}\n")
    
    print("Creando población inicial")
    poblacion = crear_poblacion_inicial(tam_poblacion, num_dias, lugares_por_dia)
    
    # Evaluar población inicial
    print("📊 Evaluando población inicial...")
    for ind in poblacion:
        evaluar_individuo(ind)
    
    # IMPORTANTE: Hacer copia profunda del mejor para evitar que las mutaciones lo afecten
    mejor_global = copy.deepcopy(max(poblacion, key=lambda ind: ind.fitness))
    historial_fitness = [mejor_global.fitness]
    historial_mejor_gen = [mejor_global.fitness]  # Nuevo: fitness del mejor de cada gen
    
    num_elite = int(tam_poblacion * tasa_elitismo)
    
    # Evolución
    print(f"\n🔄 Iniciando evolución ({num_generaciones} generaciones)...\n")
    
    for gen in range(num_generaciones):
        # Ordenar por fitness
        poblacion.sort(key=lambda ind: ind.fitness, reverse=True)
        
        # Elitismo - IMPORTANTE: Copiar profundamente para que no se muten
        nueva_poblacion = [copy.deepcopy(ind) for ind in poblacion[:num_elite]]
        
        # Generar descendencia
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = seleccion_torneo(poblacion)
            padre2 = seleccion_torneo(poblacion)
            
            hijo1, hijo2 = crossover_dos_puntos(padre1, padre2)
            
            mutar(hijo1)
            mutar(hijo2)
            
            # CRÍTICO: Eliminar duplicados ANTES de evaluar
            # Esto garantiza que el fitness siempre refleje soluciones válidas
            eliminar_duplicados_dia(hijo1)
            eliminar_duplicados_dia(hijo2)
            
            evaluar_individuo(hijo1)
            evaluar_individuo(hijo2)
            
            nueva_poblacion.extend([hijo1, hijo2])
        
        poblacion = nueva_poblacion[:tam_poblacion]
        
        # Actualizar mejor - IMPORTANTE: Hacer copia profunda para evitar mutaciones
        mejor_gen = max(poblacion, key=lambda ind: ind.fitness)
        historial_mejor_gen.append(mejor_gen.fitness)  # Guardar mejor de esta generación
        
        if mejor_gen.fitness > mejor_global.fitness:
            mejor_global = copy.deepcopy(mejor_gen)  # Copia profunda!
        
        historial_fitness.append(mejor_global.fitness)  # Siempre debe crecer o mantenerse
        
        # Progreso
        if (gen + 1) % 50 == 0 or gen == 0:
            print(f"  Gen {gen+1:4d}/{num_generaciones} | "
                  f"Mejor fitness: {mejor_global.fitness:8.1f} | "
                  f"Puntos: {mejor_global.puntos_totales:5d} | "
                  f"Tiempo: {mejor_global.tiempo_total/60:6.1f}h | "
                  f"Dist: {mejor_global.distancia_total:7.1f}km")
    
    print(f"\n✅ Evolución completada!")
    print(f"🏆 Mejor fitness global: {mejor_global.fitness:.1f}")
    
    return {
        "mejor_individuo": mejor_global,
        "historial_fitness": historial_fitness,  # Mejor global (siempre crece)
        "historial_mejor_gen": historial_mejor_gen,  # Mejor de cada gen (puede variar)
        "poblacion_final": poblacion
    }

# Utilidades de análisis

def analizar_solucion(individuo: Individual):
    """Muestra análisis detallado de una solución con itinerario completo"""
    print(f"\n{'='*80}")
    print(f"📋 ANÁLISIS DE LA MEJOR SOLUCIÓN")
    print(f"{'='*80}\n")
    
    print(f"🎯 Métricas Globales:")
    print(f"  • Fitness total: {individuo.fitness:.1f}")
    print(f"  • Puntos totales: {individuo.puntos_totales}")
    print(f"  • Tiempo total: {individuo.tiempo_total/60:.1f} horas ({individuo.tiempo_total:.0f} minutos)")
    print(f"  • Tiempo promedio/día: {(individuo.tiempo_total/len(individuo.dias))/60:.1f} horas")
    print(f"  • Distancia total: {individuo.distancia_total:.1f} km")
    print(f"  • Ciudades visitadas: {len(set(individuo.ciudades))}")
    
    print(f"\n📅 ITINERARIO DETALLADO POR DÍAS:")
    print(f"{'='*80}\n")
    
    for dia_idx, (dia, ciudad) in enumerate(zip(individuo.dias, individuo.ciudades), 1):
        lugares_dia = get_lugares_por_ids(dia)
        tiempo_dia, dist_dia, puntos_dia = calcular_tiempo_dia(individuo, dia_idx - 1)
        
        # Calcular gasto del día
        gasto_dia = 0
        for lugar in lugares_dia:
            tipo = lugar.get('tipo', '')
            if tipo in PRECIOS_TIPO:
                gasto_dia += PRECIOS_TIPO[tipo]
            else:
                gasto_dia += 10
        
        print(f"{'─'*80}")
        print(f"DÍA {dia_idx} - {ciudad.upper()}")
        print(f"{'─'*80}")
        
        # Mostrar transporte intercity si aplica
        transport_info = next((t for t in individuo.transportes_intercity if t[0] == dia_idx - 1), None)
        if transport_info:
            _, origen, destino, tipo_elegido, tiempo_trans, costo_trans = transport_info
            tipo_icons = {"avion": "✈️", "tren": "🚄", "bus": "🚌"}
            icon = tipo_icons.get(tipo_elegido, "🚗")
            print(f"{icon} Transporte: {origen} → {destino} | "
                  f"{tipo_elegido.upper()} ({tiempo_trans} min, {costo_trans}€)")
            print(f"")
        
        # Indicador de presupuesto
        if gasto_dia > PRESUPUESTO_DIARIO:
            presupuesto_str = f"💰 {gasto_dia}€ ⚠️ EXCEDE ({PRESUPUESTO_DIARIO}€)"
        else:
            presupuesto_str = f"💰 {gasto_dia}€ / {PRESUPUESTO_DIARIO}€"
        
        print(f"📊 Resumen: {len(lugares_dia)} lugares | "
              f"{puntos_dia} puntos | "
              f"{tiempo_dia/60:.2f}h ({tiempo_dia:.0f} min) | "
              f"{dist_dia:.1f} km | "
              f"{presupuesto_str}")
        print(f"")
        
        # Simular el recorrido del día mostrando horarios
        hora_actual = HORA_INICIO  # 9:00 AM en minutos
        ciudad_anterior = None
        
        for i, lugar in enumerate(lugares_dia, 1):
            # Calcular tiempo de tránsito
            tiempo_transito = 0
            if i > 1:
                lugar_anterior = lugares_dia[i-2]
                ciudad_anterior_lugar = lugar_anterior.get('ciudad', ciudad)
                ciudad_actual_lugar = lugar.get('ciudad', ciudad)
                
                if ciudad_anterior_lugar == ciudad_actual_lugar:
                    # Mismo ciudad: calcular distancia usando haversine
                    dist = distancia_haversine(lugar_anterior, lugar)
                    tiempo_transito = dist / VELOCIDAD_MEDIA * 60  # minutos
                else:
                    # Cambio de ciudad
                    tiempo_transito = calcular_transporte_intercity(ciudad_anterior_lugar, ciudad_actual_lugar)
                
                hora_actual += tiempo_transito
            
            # Formatear hora de llegada
            horas_llegada = int(hora_actual // 60)
            mins_llegada = int(hora_actual % 60)
            hora_str_llegada = f"{horas_llegada:02d}:{mins_llegada:02d}"
            
            # Calcular hora de salida
            hora_salida = hora_actual + lugar['tiempo_visita']
            horas_salida = int(hora_salida // 60)
            mins_salida = int(hora_salida % 60)
            hora_str_salida = f"{horas_salida:02d}:{mins_salida:02d}"
            
            # Detectar si es comida
            tipo_lugar = lugar.get('tipo', '')
            es_restaurante = tipo_lugar in ['restaurante', 'bar', 'cafetería']
            
            # Validar horario de apertura
            fuera_horario = ""
            if tipo_lugar in HORARIOS_TIPO:
                apertura = HORARIOS_TIPO[tipo_lugar]["apertura"]
                cierre = HORARIOS_TIPO[tipo_lugar]["cierre"]
                
                if tipo_lugar == "bar" and cierre < apertura:
                    cierre = 26 * 60
                
                if hora_actual < apertura or hora_actual > cierre:
                    fuera_horario = " ⚠️ FUERA HORARIO"
            
            icono_comida = ""
            if es_restaurante:
                # Desayuno: 8:00 - 10:00
                if HORA_DESAYUNO_MIN <= hora_actual <= HORA_DESAYUNO_MAX:
                    icono_comida = " ☕ DESAYUNO"
                # Almuerzo: 13:00 - 15:00
                elif HORA_ALMUERZO_MIN <= hora_actual <= HORA_ALMUERZO_MAX:
                    icono_comida = " 🍴 ALMUERZO"
                # Cena: 20:00 - 22:00
                elif HORA_CENA_MIN <= hora_actual <= HORA_CENA_MAX:
                    icono_comida = " 🍽️  CENA"
            
            # Imprimir el lugar con detalles
            nombre_corto = lugar['nombre'][:40]
            if len(lugar['nombre']) > 40:
                nombre_corto += "..."
            
            # Calcular precio del lugar
            if tipo_lugar in PRECIOS_TIPO:
                precio = PRECIOS_TIPO[tipo_lugar]
            else:
                precio = 10
            
            print(f"  {i:2d}. {hora_str_llegada} - {hora_str_salida} │ {nombre_corto:43s} │ {tipo_lugar:12s} │ {lugar['puntos']:3d} pts │ {precio:2d}€{icono_comida}{fuera_horario}")
            
            # Mostrar tiempo de tránsito si existe
            if tiempo_transito > 0:
                if tiempo_transito > 60:
                    print(f"      {'':13s} └─ Tránsito: {tiempo_transito/60:.1f}h ({tiempo_transito:.0f} min)")
                else:
                    print(f"      {'':13s} └─ Tránsito: {tiempo_transito:.0f} min")
            
            # Actualizar hora para el siguiente lugar
            hora_actual += lugar['tiempo_visita']
        
        # Mostrar hora de finalización del día
        horas_fin = int(hora_actual // 60)
        mins_fin = int(hora_actual % 60)
        hora_str_fin = f"{horas_fin:02d}:{mins_fin:02d}"
        
        # Verificar si se superó el tiempo límite
        exceso = max(0, tiempo_dia - TIEMPO_DIA)
        if exceso > 0:
            print(f"\n  ⚠️  DÍA FINALIZADO: {hora_str_fin} | EXCESO: {exceso:.0f} min ({exceso/60:.1f}h) | PENALIZACIÓN: -{PENALIZACION_EXCESO_TIEMPO * exceso:.0f} pts")
            if exceso > 120:
                print(f"      ❌ EXCESO CRÍTICO (>2h): Penalización adicional de -10,000 pts")
        else:
            print(f"\n  ✅ DÍA FINALIZADO: {hora_str_fin} | Dentro del límite ({TIEMPO_DIA/60:.0f}h)")
        
        print(f"")
    
    # Resumen de transportes intercity
    if individuo.transportes_intercity:
        print(f"{'='*80}")
        print(f"🚊 RESUMEN DE TRANSPORTES INTERCITY")
        print(f"{'='*80}\n")
        
        # Contar por tipo
        transportes_summary = {"avion": 0, "tren": 0, "bus": 0}
        costo_total_transporte = 0
        tiempo_total_transporte = 0
        
        for t in individuo.transportes_intercity:
            tipo = t[3]
            costo = t[5]
            tiempo = t[4]
            transportes_summary[tipo] += 1
            costo_total_transporte += costo
            tiempo_total_transporte += tiempo
        
        print(f"📊 Estadísticas:")
        print(f"  ✈️  Avión: {transportes_summary['avion']} viajes")
        print(f"  🚄 Tren:  {transportes_summary['tren']} viajes")
        print(f"  🚌 Bus:   {transportes_summary['bus']} viajes")
        print(f"\n💰 Costo total transportes: {costo_total_transporte}€")
        print(f"⏱️  Tiempo total transportes: {tiempo_total_transporte} min ({tiempo_total_transporte/60:.1f}h)")
        print(f"")
    
    print(f"{'='*80}")
    print(f"✅ ANÁLISIS COMPLETO")
    print(f"{'='*80}\n")


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
        "historial_fitness": resultados["historial_fitness"],  # Mejor global
        "historial_mejor_gen": resultados.get("historial_mejor_gen", resultados["historial_fitness"])  # Mejor por gen
    }
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados exportados a: {archivo}")

# Ejecución principal

if __name__ == "__main__":
    import sys
    
    configuraciones = {
        "1": {
            "nombre": "RÁPIDA (10-15 min)",
            "num_dias": 20,
            "lugares_por_dia": 12,
            "tam_poblacion": 1000,
            "num_generaciones": 500,
            "tasa_elitismo": 0.20,
            "descripcion": "Testing y validación rápida"
        },
        "2": {
            "nombre": "INTENSIVA (45-60 min)",
            "num_dias": 25,
            "lugares_por_dia": 12,  # Reducido de 15 a 12 (más realista)
            "tam_poblacion": 15000,
            "num_generaciones": 800,
            "tasa_elitismo": 0.15,
            "descripcion": "Mayor exploración y convergencia"
        },
        "3": {
            "nombre": "ULTRA-COMPLEJA (1.5-2 horas)",
            "num_dias": 30,
            "lugares_por_dia": 12,  # Reducido de 15 a 12 (más realista)
            "tam_poblacion": 20000,
            "num_generaciones": 1000,
            "tasa_elitismo": 0.10,
            "descripcion": "Máxima calidad de solución"
        }
    }
    
    if len(sys.argv) > 1:
        modo = sys.argv[1]
    else:
        print(f"\n{'='*80}")
        print(f"🎯 SELECCIONA MODO DE EJECUCIÓN")
        print(f"{'='*80}\n")
        
        for key, config in configuraciones.items():
            print(f"[{key}] {config['nombre']}")
            print(f"    📊 {config['descripcion']}")
            print(f"    ⚙️  {config['num_dias']} días | {config['lugares_por_dia']} lugares/día | "
                  f"{config['tam_poblacion']:,} población | {config['num_generaciones']} gen")
            print()
        
        print(f"{'='*80}")
        modo = input("👉 Selecciona modo (1/2/3): ").strip()
    
    if modo not in configuraciones:
        print(f"\n❌ ERROR: Modo '{modo}' no válido. Usa: 1, 2 o 3")
        print(f"💡 Uso: python algoritmo_espana.py [1|2|3]")
        sys.exit(1)
    
    config = configuraciones[modo]
    
    resultados = algoritmo_genetico_espana(
        num_dias=config["num_dias"],
        lugares_por_dia=config["lugares_por_dia"],
        tam_poblacion=config["tam_poblacion"],
        num_generaciones=config["num_generaciones"],
        tasa_elitismo=config["tasa_elitismo"]
    )
    
    analizar_solucion(resultados["mejor_individuo"])
    exportar_resultados(resultados, archivo=f"ag_{modo}.json")
