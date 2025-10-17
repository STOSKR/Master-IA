import random
import copy
import logging
import os
from datetime import datetime
from typing import List, Dict, Tuple
from math import radians, sin, cos, sqrt, atan2
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
def configurar_logging(output_dir="logs", prefijo="ag_espana"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%d_%H_%M")
    log_filename = os.path.join(output_dir, f"{prefijo}_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler() 
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"{'='*80}")
    logger.info(f"INICIO DE EJECUCIÓN - Algoritmo Genético España")
    logger.info(f"Log guardado en: {log_filename}")
    logger.info(f"{'='*80}")
    
    return log_filename

def log(mensaje):
    logging.info(mensaje)

class Individual:
    def __init__(self, dias: List[List[int]], ciudades: List[str]):
        self.dias = [dia[:] if isinstance(dia, list) else dia for dia in dias]
        self.ciudades = ciudades[:] if isinstance(ciudades, list) else ciudades
        self.fitness = 0
        self.tiempo_total = 0
        self.puntos_totales = 0
        self.distancia_total = 0
        self.transportes_intercity = []


def eliminar_duplicados_globales(individuo: Individual) -> Individual:
    lugares_visitados_global = set()
    
    for dia_idx in range(len(individuo.dias)):
        dia = individuo.dias[dia_idx]
        ciudad = individuo.ciudades[dia_idx]
        lugares_ciudad = get_lugares_ciudad(ciudad)
        
        dia_limpio = []
        for lugar_id in dia:
            if lugar_id not in lugares_visitados_global:
                dia_limpio.append(lugar_id)
                lugares_visitados_global.add(lugar_id)
            else:
                lugares_disponibles = [
                    l["id"] for l in lugares_ciudad 
                    if l["id"] not in lugares_visitados_global
                ]
                
                if lugares_disponibles:
                    nuevo_lugar = random.choice(lugares_disponibles)
                    dia_limpio.append(nuevo_lugar)
                    lugares_visitados_global.add(nuevo_lugar)
        
        individuo.dias[dia_idx] = dia_limpio
    
    return individuo


def obtener_ciudad_mas_cercana(ciudad_actual: str, ciudades_visitadas: set, dias_consecutivos_actual: int) -> str:
    """
    Obtiene la ciudad más cercana respetando MAX_DIAS_POR_CIUDAD.
    NUNCA debe quedarse más de MAX_DIAS_POR_CIUDAD días en una misma ciudad.
    """
    ciudades_disponibles = list(COORDENADAS_CIUDADES.keys())
    
    debe_cambiar = dias_consecutivos_actual >= MAX_DIAS_POR_CIUDAD
    
    # PRIORIDAD 1: Buscar ciudades no visitadas (excluyendo actual si debe_cambiar)
    candidatas = []
    for ciudad in ciudades_disponibles:
        if debe_cambiar and ciudad == ciudad_actual:
            continue
        if ciudad in ciudades_visitadas:
            continue
        candidatas.append(ciudad)
    
    # PRIORIDAD 2: Si no hay ciudades nuevas, revisar ciudades YA visitadas (excepto la actual si debe cambiar)
    if not candidatas:
        candidatas = [c for c in ciudades_disponibles if c != ciudad_actual]
    
    # PRIORIDAD 3: Si aún no hay candidatas (caso extremo), forzar cualquier ciudad diferente
    if not candidatas:
        # Esto fuerza cambiar a CUALQUIER otra ciudad
        candidatas = [c for c in ciudades_disponibles if c != ciudad_actual]
        if not candidatas:  # Solo si hay UNA ciudad (imposible con 10 ciudades)
            return random.choice(ciudades_disponibles)

    coord_actual = COORDENADAS_CIUDADES[ciudad_actual]
    distancias = []
    
    for ciudad_candidata in candidatas:
        coord_candidata = COORDENADAS_CIUDADES[ciudad_candidata]
        lat1 = float(coord_actual["lat"])
        lon1 = float(coord_actual["lon"])
        lat2 = float(coord_candidata["lat"])
        lon2 = float(coord_candidata["lon"])
        
        R = 6371
        
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distancia = R * c
        
        distancias.append((ciudad_candidata, distancia))
    
    distancias.sort(key=lambda x: x[1])
    return distancias[0][0]

def validar_restricciones_ciudades(individuo: Individual) -> bool:
    """
    Valida que un individuo respete las restricciones de ciudades:
    1. No regresar a una ciudad ya visitada (sin agrupar días consecutivos)
    2. NO quedarse más de MAX_DIAS_POR_CIUDAD días consecutivos en una ciudad
    """
    ciudades = individuo.ciudades
    
    # Validar que no se repitan ciudades sin agrupar (no regresar)
    ciudades_vistas = set()
    for i, ciudad in enumerate(ciudades):
        if ciudad in ciudades_vistas:
            # Si ya se visitó, debe ser consecutiva
            if i > 0 and ciudades[i-1] == ciudad:
                continue  # OK: Días consecutivos en la misma ciudad
            else:
                return False  # ERROR: Regreso a ciudad ya visitada
        if i > 0 and ciudades[i-1] != ciudad:
            ciudades_vistas.add(ciudades[i-1])
    
    # VALIDACIÓN CRÍTICA: Verificar que NUNCA se quede más de MAX_DIAS_POR_CIUDAD días consecutivos
    dias_consecutivos = 1
    ciudad_actual_check = ciudades[0]
    for i in range(1, len(ciudades)):
        if ciudades[i] == ciudad_actual_check:
            dias_consecutivos += 1
            if dias_consecutivos > MAX_DIAS_POR_CIUDAD:
                return False  # PROHIBIDO: Más de MAX_DIAS_POR_CIUDAD días en una ciudad
        else:
            # Cambió de ciudad, resetear contador
            ciudad_actual_check = ciudades[i]
            dias_consecutivos = 1
    
    return True

def reparar_individuo(individuo: Individual) -> Individual:
    ciudades_disponibles = list(COORDENADAS_CIUDADES.keys())
    
    DEBUG_REPARAR = False  # ⚠️ DEBUG DESACTIVADO
    
    if DEBUG_REPARAR:
        print(f"\n🔧 [DEBUG] INICIANDO REPARACIÓN")
        print(f"   Total días: {len(individuo.ciudades)}")
    
    # Paso 1: Corregir bloques que exceden MAX_DIAS_POR_CIUDAD
    i = 0
    while i < len(individuo.ciudades):
        ciudad_actual = individuo.ciudades[i]
        inicio_bloque = i
        
        while i < len(individuo.ciudades) and individuo.ciudades[i] == ciudad_actual:
            i += 1
        
        dias_consecutivos = i - inicio_bloque
        
        if DEBUG_REPARAR:
            simbolo = "✅" if dias_consecutivos <= MAX_DIAS_POR_CIUDAD else "❌"
            print(f"   {simbolo} Bloque: {ciudad_actual} (días {inicio_bloque+1}-{i}, {dias_consecutivos} días)")
        
        if dias_consecutivos > MAX_DIAS_POR_CIUDAD:
            if DEBUG_REPARAR:
                print(f"      ⚠️  EXCEDE LÍMITE! Reparando...")
            
            # ⚠️ IMPORTANTE: Analizar cuántos días tiene cada ciudad hasta este punto
            contador_dias_ciudad = {}
            for idx in range(inicio_bloque):
                c = individuo.ciudades[idx]
                contador_dias_ciudad[c] = contador_dias_ciudad.get(c, 0) + 1
            
            ciudades_previas = set(contador_dias_ciudad.keys())
            
            # ⚠️ CORRECCIÓN: Dividir en pedazos, cada pedazo de ciudad diferente
            pedazos_necesarios = (dias_consecutivos + MAX_DIAS_POR_CIUDAD - 1) // MAX_DIAS_POR_CIUDAD
            
            if DEBUG_REPARAR:
                print(f"      🔪 Dividiendo en {pedazos_necesarios} pedazos")
                print(f"      � Días por ciudad hasta ahora: {contador_dias_ciudad}")
            
            for pedazo_idx in range(1, pedazos_necesarios):
                dia_inicio_pedazo = inicio_bloque + (pedazo_idx * MAX_DIAS_POR_CIUDAD)
                dia_fin_pedazo = min(dia_inicio_pedazo + MAX_DIAS_POR_CIUDAD, i)
                dias_pedazo = dia_fin_pedazo - dia_inicio_pedazo
                
                if DEBUG_REPARAR:
                    print(f"      🔄 Pedazo {pedazo_idx+1}: días {dia_inicio_pedazo+1}-{dia_fin_pedazo} ({dias_pedazo} días a repartir)")
                
                # 📊 ESTRATEGIA DE REPARTO CON INSERCIÓN:
                # 1. Identificar ciudades incompletas y su última posición
                ciudades_incompletas = []
                for c in ciudades_disponibles:
                    if c != ciudad_actual:
                        dias_actuales = contador_dias_ciudad.get(c, 0)
                        if dias_actuales < MAX_DIAS_POR_CIUDAD:
                            # Buscar la última posición donde aparece esta ciudad
                            ultima_pos = -1
                            for idx in range(inicio_bloque - 1, -1, -1):
                                if individuo.ciudades[idx] == c:
                                    ultima_pos = idx
                                    break
                            
                            espacio = MAX_DIAS_POR_CIUDAD - dias_actuales
                            ciudades_incompletas.append({
                                'ciudad': c,
                                'dias_actuales': dias_actuales,
                                'espacio': espacio,
                                'ultima_posicion': ultima_pos
                            })
                
                # Ordenar por última posición (para insertar en orden)
                ciudades_incompletas.sort(key=lambda x: x['ultima_posicion'])
                
                if DEBUG_REPARAR:
                    print(f"         📋 Ciudades incompletas disponibles:")
                    for info in ciudades_incompletas:
                        pos_str = f"posición {info['ultima_posicion']+1}" if info['ultima_posicion'] >= 0 else "nueva"
                        print(f"            - {info['ciudad']}: {info['dias_actuales']} días (espacio: {info['espacio']}, {pos_str})")
                
                # 2. Reemplazar los días del pedazo con ciudades incompletas (reparto cíclico)
                dias_a_repartir = []
                idx_ciudad = 0
                
                for _ in range(dias_pedazo):
                    if not ciudades_incompletas:
                        break
                    
                    info_ciudad = ciudades_incompletas[idx_ciudad % len(ciudades_incompletas)]
                    dias_a_repartir.append({
                        'ciudad': info_ciudad['ciudad'],
                        'insertar_despues': info_ciudad['ultima_posicion']
                    })
                    
                    # Actualizar contadores
                    info_ciudad['dias_actuales'] += 1
                    info_ciudad['espacio'] -= 1
                    
                    # Actualizar última posición (se desplaza por las inserciones previas)
                    info_ciudad['ultima_posicion'] += 1
                    
                    # Si se completó, quitar de la lista
                    if info_ciudad['dias_actuales'] >= MAX_DIAS_POR_CIUDAD:
                        ciudades_incompletas.pop(idx_ciudad % len(ciudades_incompletas))
                    else:
                        idx_ciudad += 1
                
                # 3. Reemplazar los días en el pedazo con las ciudades elegidas
                for idx_pedazo, info_dia in enumerate(dias_a_repartir):
                    dia_idx = dia_inicio_pedazo + idx_pedazo
                    ciudad_elegida = info_dia['ciudad']
                    
                    individuo.ciudades[dia_idx] = ciudad_elegida
                    contador_dias_ciudad[ciudad_elegida] = contador_dias_ciudad.get(ciudad_elegida, 0) + 1
                    ciudades_previas.add(ciudad_elegida)
                    
                    # Actualizar lugares del día
                    lugares_nueva = get_lugares_ciudad(ciudad_elegida)
                    if lugares_nueva and individuo.dias[dia_idx]:
                        individuo.dias[dia_idx] = [
                            random.choice(lugares_nueva)["id"] 
                            for _ in range(len(individuo.dias[dia_idx]))
                        ]
                    
                    if DEBUG_REPARAR:
                        print(f"            Día {dia_idx+1} → {ciudad_elegida}")
                
                # Si faltan días por asignar, crear regresos
                if len(dias_a_repartir) < dias_pedazo:
                    if DEBUG_REPARAR:
                        print(f"         ⚠️  Faltan {dias_pedazo - len(dias_a_repartir)} días, creando regresos...")
                    
                    for idx_pedazo in range(len(dias_a_repartir), dias_pedazo):
                        dia_idx = dia_inicio_pedazo + idx_pedazo
                        candidatas = [c for c in ciudades_disponibles if c != ciudad_actual]
                        if candidatas:
                            ciudad_regreso = random.choice(candidatas)
                            individuo.ciudades[dia_idx] = ciudad_regreso
                            contador_dias_ciudad[ciudad_regreso] = contador_dias_ciudad.get(ciudad_regreso, 0) + 1
                            
                            lugares_nueva = get_lugares_ciudad(ciudad_regreso)
                            if lugares_nueva and individuo.dias[dia_idx]:
                                individuo.dias[dia_idx] = [
                                    random.choice(lugares_nueva)["id"] 
                                    for _ in range(len(individuo.dias[dia_idx]))
                                ]
                            
                            if DEBUG_REPARAR:
                                print(f"            Día {dia_idx+1} → {ciudad_regreso} (REGRESO)")
                    for dia_idx in range(dia_inicio_pedazo, dia_fin_pedazo):
                        individuo.ciudades[dia_idx] = nueva_ciudad
                        
                        lugares_nueva = get_lugares_ciudad(nueva_ciudad)
                        if lugares_nueva and individuo.dias[dia_idx]:
                            individuo.dias[dia_idx] = [
                                random.choice(lugares_nueva)["id"] 
                                for _ in range(len(individuo.dias[dia_idx]))
                            ]
    
    # Paso 2: Eliminar TODOS los regresos (intentar múltiples veces)
    # ⚠️ IMPORTANTE: Solo si AGRUPAR=False, porque con AGRUPAR=True 
    # el Paso 1 ya garantiza que no hay bloques > MAX_DIAS_POR_CIUDAD
    if not AGRUPAR:
        if DEBUG_REPARAR:
            print(f"\n🔄 [DEBUG] PASO 2: Eliminar regresos...")
        
        for intento in range(3):
            ciudades_vistas = set()
            cambios = False
            
            if DEBUG_REPARAR:
                print(f"\n   Intento {intento+1}/3")
            
            i = 0
            while i < len(individuo.ciudades):
                ciudad_actual = individuo.ciudades[i]
                
                # Detectar regreso
                es_regreso = (ciudad_actual in ciudades_vistas and 
                             (i == 0 or individuo.ciudades[i-1] != ciudad_actual))
                
                if es_regreso:
                    if DEBUG_REPARAR:
                        print(f"      ⚠️  Día {i+1}: {ciudad_actual} es REGRESO (ya visitada)")
                    
                    # Buscar ciudad NO visitada
                    candidatas = [c for c in ciudades_disponibles 
                                 if c not in ciudades_vistas]
                    
                    if not candidatas and i > 0:
                        candidatas = [c for c in ciudades_disponibles 
                                     if c != individuo.ciudades[i-1]]
                    
                    if candidatas:
                        nueva_ciudad = random.choice(candidatas)
                        individuo.ciudades[i] = nueva_ciudad
                        cambios = True
                        
                        if DEBUG_REPARAR:
                            print(f"         🔄 Cambiando a {nueva_ciudad}")
                        
                        lugares_nueva = get_lugares_ciudad(nueva_ciudad)
                        if lugares_nueva:
                            individuo.dias[i] = [
                                random.choice(lugares_nueva)["id"] 
                                for _ in range(len(individuo.dias[i]))
                            ]
                        
                        ciudad_actual = nueva_ciudad
                
                if i > 0 and individuo.ciudades[i] != individuo.ciudades[i-1]:
                    ciudades_vistas.add(individuo.ciudades[i-1])
                
                i += 1
            
            if not cambios:
                break
    else:
        if DEBUG_REPARAR:
            print(f"\n🔄 [DEBUG] PASO 2: OMITIDO (AGRUPAR=True, Paso 1 suficiente)")
    
    return individuo

def crear_individuo_aleatorio(num_dias: int, lugares_por_dia: int) -> Individual:
    ciudades_disponibles = list(COORDENADAS_CIUDADES.keys())
    dias = []
    ciudades_plan = []
    ciudades_visitadas = set()
    lugares_visitados_global = set()
    
    if AGRUPAR:
        dia_actual = 0
        ciudad_actual = random.choice(ciudades_disponibles)
        dias_consecutivos_ciudad = 0
        ciudades_usadas = []  # Lista ordenada de ciudades ya visitadas
        
        while dia_actual < num_dias:
            dias_restantes = num_dias - dia_actual
            
            # Calcular cuántos días PUEDE quedarse en esta ciudad (máximo MAX_DIAS_POR_CIUDAD)
            max_permitido = MAX_DIAS_POR_CIUDAD - dias_consecutivos_ciudad
            
            # Si llegó al límite, DEBE cambiar de ciudad
            if max_permitido <= 0:
                ciudades_usadas.append(ciudad_actual)
                # Buscar ciudad NO visitada
                candidatas = [c for c in ciudades_disponibles if c not in ciudades_usadas]
                if not candidatas:
                    # Si todas fueron visitadas, reiniciar (permitir reutilizar ciudades)
                    candidatas = [c for c in ciudades_disponibles if c != ciudad_actual]
                
                ciudad_actual = random.choice(candidatas) if candidatas else ciudad_actual
                dias_consecutivos_ciudad = 0
                max_permitido = MAX_DIAS_POR_CIUDAD
            
            # Calcular días a asignar: mínimo entre max_permitido y días_restantes
            dias_en_ciudad = random.randint(1, min(max_permitido, dias_restantes))
            
            # Asignar días
            lugares_ciudad = get_lugares_ciudad(ciudad_actual)
            
            # ⚠️ CRÍTICO: Si no hay suficientes lugares, permitir repeticiones
            # NO usar lugares de otras ciudades (causaría distancias intercity enormes)
            permitir_repeticiones = len(lugares_ciudad) < lugares_por_dia
            
            for _ in range(dias_en_ciudad):
                if dia_actual >= num_dias:
                    break
                
                lugares_disponibles = [
                    l for l in lugares_ciudad 
                    if l["id"] not in lugares_visitados_global
                ]
                
                if len(lugares_disponibles) < lugares_por_dia:
                    lugares_disponibles = lugares_ciudad
                
                # Si hay suficientes lugares, usar sample (sin repetición)
                # Si no, usar choices (con repetición permitida)
                if len(lugares_disponibles) >= lugares_por_dia:
                    lugares_dia = random.sample(lugares_disponibles, lugares_por_dia)
                else:
                    # Con repetición: podemos elegir el mismo lugar varias veces si es necesario
                    lugares_dia = random.choices(lugares_disponibles, k=lugares_por_dia)
                
                ids_dia = [l["id"] for l in lugares_dia]
                
                lugares_visitados_global.update(ids_dia)
                random.shuffle(ids_dia)
                
                dias.append(ids_dia)
                ciudades_plan.append(ciudad_actual)
                dia_actual += 1
                dias_consecutivos_ciudad += 1
            
            # Si quedan días y estamos cerca del límite o terminamos los días de esta ciudad
            # cambiar proactivamente
            if dia_actual < num_dias and dias_consecutivos_ciudad >= MAX_DIAS_POR_CIUDAD:
                ciudades_usadas.append(ciudad_actual)
                # Buscar ciudad NO visitada
                candidatas = [c for c in ciudades_disponibles if c not in ciudades_usadas]
                if not candidatas:
                    candidatas = [c for c in ciudades_disponibles if c != ciudad_actual]
                
                ciudad_actual = random.choice(candidatas) if candidatas else ciudad_actual
                dias_consecutivos_ciudad = 0
            elif dia_actual < num_dias and random.random() < 0.5:  # 50% probabilidad de cambiar voluntariamente
                ciudades_usadas.append(ciudad_actual)
                candidatas = [c for c in ciudades_disponibles if c not in ciudades_usadas]
                if candidatas:
                    ciudad_actual = random.choice(candidatas)
                    dias_consecutivos_ciudad = 0
    else:
        ciudad_actual = random.choice(ciudades_disponibles)
        dias_consecutivos = 0
        
        for dia_idx in range(num_dias):
            if dia_idx > 0 and ciudades_plan[-1] == ciudad_actual:
                dias_consecutivos += 1
            else:
                dias_consecutivos = 1
            
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
    
    if not validar_restricciones_ciudades(individuo):
        individuo = reparar_individuo(individuo)
    
    # Intentar reparar horarios desde el inicio
    individuo = reparar_horarios_individuo(individuo, max_intentos=1)
    
    return individuo

def crear_poblacion_inicial(tam_poblacion: int, num_dias: int, lugares_por_dia: int) -> List[Individual]:
    return [crear_individuo_aleatorio(num_dias, lugares_por_dia) for _ in range(tam_poblacion)]

def calcular_tiempo_dia(individuo: Individual, dia_idx: int) -> Tuple[int, int, float]:
    dia = individuo.dias[dia_idx]
    
    if not dia:
        return 0, 0, 0
    
    lugares_dia = get_lugares_por_ids(dia)
    tiempo_total = 0
    distancia_total = 0
    puntos_total = 0
    
    for lugar in lugares_dia:
        tiempo_total += lugar["tiempo_visita"]
        puntos_total += lugar["puntos"]
    
    for i in range(len(lugares_dia) - 1):
        dist = distancia_haversine(lugares_dia[i], lugares_dia[i + 1])
        distancia_total += dist
        tiempo_total += dist / VELOCIDAD_MEDIA * 60
    
    return tiempo_total, distancia_total, puntos_total

def verificar_lugar_en_horario(lugar: Dict, hora_inicio: int, hora_fin: int) -> bool:
    """
    Verifica si un lugar puede ser visitado en el rango de tiempo especificado.
    
    Args:
        lugar: Diccionario con información del lugar (debe incluir 'tipo')
        hora_inicio: Hora de inicio de la visita en minutos desde medianoche
        hora_fin: Hora de fin de la visita en minutos desde medianoche
    
    Returns:
        True si el lugar está abierto durante todo el periodo de visita
    """
    tipo = lugar.get('tipo', '')
    
    if tipo not in HORARIOS_TIPO:
        return True  # Si no tiene horario definido, se considera siempre disponible
    
    apertura = HORARIOS_TIPO[tipo]["apertura"]
    cierre = HORARIOS_TIPO[tipo]["cierre"]
    
    # Caso especial: bares abiertos después de medianoche
    if tipo == "bar" and cierre < apertura:
        cierre = 26 * 60
    
    # El lugar debe estar abierto al inicio Y al final de la visita
    return hora_inicio >= apertura and hora_fin <= cierre

def intentar_intercambio_horarios(individuo: Individual, dia_idx: int) -> bool:
    """
    Intenta intercambiar lugares dentro del mismo día para que todos queden dentro de horario.
    
    Args:
        individuo: El individuo a reparar
        dia_idx: Índice del día a reparar
    
    Returns:
        True si se logró hacer algún intercambio que mejore los horarios
    """
    dia = individuo.dias[dia_idx]
    if len(dia) < 2:
        return False
    
    lugares_dia = get_lugares_por_ids(dia)
    ciudad = individuo.ciudades[dia_idx]
    
    # Calcular hora inicial considerando transporte intercity si es necesario
    hora_actual = HORA_INICIO
    if dia_idx > 0 and individuo.ciudades[dia_idx] != individuo.ciudades[dia_idx - 1]:
        for transporte in individuo.transportes_intercity:
            if transporte[0] == dia_idx:
                hora_actual += transporte[4]
                break
    
    # Identificar lugares fuera de horario
    lugares_problematicos = []
    hora_simulada = hora_actual
    
    for idx, lugar in enumerate(lugares_dia):
        tiempo_visita = lugar['tiempo_visita']
        hora_fin_visita = hora_simulada + tiempo_visita
        
        if not verificar_lugar_en_horario(lugar, hora_simulada, hora_fin_visita):
            lugares_problematicos.append(idx)
        
        hora_simulada += tiempo_visita
        
        # Añadir tiempo de desplazamiento al siguiente lugar
        if idx < len(lugares_dia) - 1:
            dist = distancia_haversine(lugar, lugares_dia[idx + 1])
            hora_simulada += dist / VELOCIDAD_MEDIA * 60
    
    if not lugares_problematicos:
        return False  # No hay problemas
    
    # Intentar intercambios: probar swaps entre lugares problemáticos y otros
    for idx_problema in lugares_problematicos:
        for idx_otro in range(len(dia)):
            if idx_otro == idx_problema:
                continue
            
            # Crear copia temporal para probar el intercambio
            dia_temp = dia[:]
            dia_temp[idx_problema], dia_temp[idx_otro] = dia_temp[idx_otro], dia_temp[idx_problema]
            
            # Verificar si el intercambio mejora la situación
            lugares_temp = get_lugares_por_ids(dia_temp)
            hora_simulada = hora_actual
            problemas_nuevos = 0
            
            for idx, lugar in enumerate(lugares_temp):
                tiempo_visita = lugar['tiempo_visita']
                hora_fin_visita = hora_simulada + tiempo_visita
                
                if not verificar_lugar_en_horario(lugar, hora_simulada, hora_fin_visita):
                    problemas_nuevos += 1
                
                hora_simulada += tiempo_visita
                
                if idx < len(lugares_temp) - 1:
                    dist = distancia_haversine(lugar, lugares_temp[idx + 1])
                    hora_simulada += dist / VELOCIDAD_MEDIA * 60
            
            # Si hay menos problemas, aplicar el intercambio
            if problemas_nuevos < len(lugares_problematicos):
                individuo.dias[dia_idx] = dia_temp
                return True
    
    return False

def buscar_lugar_alternativo_horario(individuo: Individual, dia_idx: int, lugar_idx: int, 
                                     hora_visita: int) -> bool:
    """
    Busca un lugar alternativo de la misma ciudad que esté disponible en el horario especificado.
    
    Args:
        individuo: El individuo a reparar
        dia_idx: Índice del día
        lugar_idx: Índice del lugar problemático dentro del día
        hora_visita: Hora en minutos a la que se visitaría el lugar
    
    Returns:
        True si se encontró y aplicó un reemplazo
    """
    ciudad = individuo.ciudades[dia_idx]
    dia = individuo.dias[dia_idx]
    lugar_actual_id = dia[lugar_idx]
    lugar_actual = get_lugares_por_ids([lugar_actual_id])[0]
    
    # Obtener todos los lugares de la ciudad
    lugares_ciudad = get_lugares_ciudad(ciudad)
    
    # Filtrar lugares ya visitados en este viaje (no solo este día)
    lugares_visitados_global = set()
    for d in individuo.dias:
        lugares_visitados_global.update(d)
    
    # Buscar lugares alternativos que estén dentro del horario
    candidatos = []
    for lugar in lugares_ciudad:
        if lugar["id"] in lugares_visitados_global and lugar["id"] != lugar_actual_id:
            continue  # Ya visitado
        
        tiempo_visita = lugar["tiempo_visita"]
        hora_fin = hora_visita + tiempo_visita
        
        if verificar_lugar_en_horario(lugar, hora_visita, hora_fin):
            candidatos.append(lugar)
    
    if not candidatos:
        return False
    
    # Elegir el mejor candidato (por puntos o aleatoriamente)
    # Priorizar lugares con puntos similares al original
    puntos_original = lugar_actual.get("puntos", 0)
    candidatos.sort(key=lambda x: abs(x.get("puntos", 0) - puntos_original))
    
    mejor_candidato = candidatos[0]
    individuo.dias[dia_idx][lugar_idx] = mejor_candidato["id"]
    
    return True

def reparar_horarios_individuo(individuo: Individual, max_intentos: int = 3) -> Individual:
    """
    Repara un individuo intentando corregir lugares visitados fuera de horario.
    
    Estrategia:
    1. Intentar intercambiar lugares dentro del mismo día
    2. Si no funciona, buscar lugares alternativos en la misma ciudad
    
    Args:
        individuo: El individuo a reparar
        max_intentos: Número máximo de intentos de reparación por día
    
    Returns:
        El individuo reparado
    """
    for dia_idx in range(len(individuo.dias)):
        # Intentar reparar este día
        for intento in range(max_intentos):
            # Calcular hora inicial del día
            hora_actual = HORA_INICIO
            if dia_idx > 0 and individuo.ciudades[dia_idx] != individuo.ciudades[dia_idx - 1]:
                for transporte in individuo.transportes_intercity:
                    if transporte[0] == dia_idx:
                        hora_actual += transporte[4]
                        break
            
            # Identificar lugares problemáticos
            lugares_dia = get_lugares_por_ids(individuo.dias[dia_idx])
            hora_simulada = hora_actual
            indices_problematicos = []
            horas_problematicas = []
            
            for idx, lugar in enumerate(lugares_dia):
                tiempo_visita = lugar['tiempo_visita']
                hora_fin_visita = hora_simulada + tiempo_visita
                
                if not verificar_lugar_en_horario(lugar, hora_simulada, hora_fin_visita):
                    indices_problematicos.append(idx)
                    horas_problematicas.append(hora_simulada)
                
                hora_simulada += tiempo_visita
                
                if idx < len(lugares_dia) - 1:
                    dist = distancia_haversine(lugar, lugares_dia[idx + 1])
                    hora_simulada += dist / VELOCIDAD_MEDIA * 60
            
            if not indices_problematicos:
                break  # Este día está bien, pasar al siguiente
            
            # Estrategia 1: Intentar intercambios
            if intentar_intercambio_horarios(individuo, dia_idx):
                continue  # Volver a verificar con el nuevo orden
            
            # Estrategia 2: Buscar lugares alternativos
            se_hizo_cambio = False
            for idx_problema, hora_problema in zip(indices_problematicos, horas_problematicas):
                if buscar_lugar_alternativo_horario(individuo, dia_idx, idx_problema, hora_problema):
                    se_hizo_cambio = True
                    break  # Hacer un cambio a la vez y volver a verificar
            
            if not se_hizo_cambio:
                break  # No se pudo hacer más, continuar con el siguiente día
    
    return individuo

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
    
    # ⚠️ CONTADOR DE VIOLACIONES CRÍTICAS
    violaciones_ciudades = 0
    violaciones_horarios = 0
    
    # ⚠️ VALIDACIÓN: Si el individuo viola restricciones de ciudades
    if not validar_restricciones_ciudades(individuo):
        violaciones_ciudades += 1
    
    for dia_idx in range(len(individuo.dias)):
        tiempo_dia, dist_dia, puntos_dia = calcular_tiempo_dia(individuo, dia_idx)
        lugares_dia = get_lugares_por_ids(individuo.dias[dia_idx])
        
        if AGRUPAR and dia_idx > 0:
            ciudad_actual = individuo.ciudades[dia_idx]
            ciudad_anterior = individuo.ciudades[dia_idx - 1]
            
            if ciudad_actual != ciudad_anterior:
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

        if not validar_limite_ciudad(individuo.ciudades[:dia_idx + 1], individuo.ciudades[dia_idx])[0]:
            fitness -= PENALIZACION_LIMITE_CIUDAD
        
        # Calcular tiempo sin transporte para verificar límite del día
        tiempo_dia_sin_transporte = tiempo_dia
        if dia_idx > 0 and individuo.ciudades[dia_idx] != individuo.ciudades[dia_idx - 1]:
            transporte_dia = next((t for t in individuo.transportes_intercity if t[0] == dia_idx), None)
            if transporte_dia and transporte_dia[4]:
                tiempo_dia_sin_transporte -= transporte_dia[4]
        
        if tiempo_dia_sin_transporte > TIEMPO_DIA:
            exceso = tiempo_dia_sin_transporte - TIEMPO_DIA
            if exceso > 0 and exceso <= 120:
                fitness -= PENALIZACION_EXCESO_TIEMPO * exceso
            elif exceso > 120:
                fitness -= PENALIZACION_EXCESO_TIEMPO * 120 
                fitness -= (exceso - 120) * 2
        
        hora_actual = HORA_INICIO
        
        if dia_idx > 0 and individuo.ciudades[dia_idx] != individuo.ciudades[dia_idx - 1]:
            transporte_dia = next((t for t in individuo.transportes_intercity if t[0] == dia_idx), None)
            if transporte_dia and transporte_dia[4]:
                hora_actual += transporte_dia[4]
        
        tiene_almuerzo = False
        tiene_cena = False
        gasto_dia = 0
        restaurantes_consecutivos = 0
        max_consecutivos = 0
        
        for lugar in lugares_dia:
            tipo = lugar.get('tipo', '')
            tiempo_visita = lugar['tiempo_visita']
            hora_fin_visita = hora_actual + tiempo_visita
            
            if tipo in HORARIOS_TIPO:
                apertura = HORARIOS_TIPO[tipo]["apertura"]
                cierre = HORARIOS_TIPO[tipo]["cierre"]
                
                # Caso especial: bares abiertos después de medianoche
                if tipo == "bar" and cierre < apertura:
                    cierre = 26 * 60
                
                if hora_actual < apertura or hora_fin_visita > cierre:
                    # Contar violación en lugar de retornar inmediatamente
                    violaciones_horarios += 1
                    fitness -= PENALIZACION_FUERA_HORARIO_APERTURA
            
            if tipo in PRECIOS_TIPO:
                gasto_dia += PRECIOS_TIPO[tipo]
            else:
                gasto_dia += 10
            
            if tipo in ['restaurante', 'bar', 'cafetería']:
                if HORA_ALMUERZO_MIN <= hora_actual <= HORA_ALMUERZO_MAX:
                    tiene_almuerzo = True
                elif HORA_CENA_MIN <= hora_actual <= HORA_CENA_MAX:
                    tiene_cena = True
                
                restaurantes_consecutivos += 1
                max_consecutivos = max(max_consecutivos, restaurantes_consecutivos)
            else:
                restaurantes_consecutivos = 0
            
            hora_actual += tiempo_visita  # Usar la variable local
        
        gasto_acumulado += gasto_dia
        
        if gasto_dia > PRESUPUESTO_DIARIO:
            exceso_presupuesto = gasto_dia - PRESUPUESTO_DIARIO
            fitness -= PENALIZACION_EXCESO_PRESUPUESTO * exceso_presupuesto
        
        if not tiene_almuerzo:
            fitness -= PENALIZACION_COMIDA_FALTA
        
        if not tiene_cena:
            fitness -= PENALIZACION_CENA_FALTA
        
        if max_consecutivos > 3:
            fitness -= PENALIZACION_RESTAURANTES_CONSECUTIVOS * (max_consecutivos - 3)
        
        tiempo_acum += tiempo_dia
        distancia_acum += dist_dia
        puntos_acum += puntos_dia
    
    fitness += puntos_acum
    fitness -= distancia_acum * 0.3
    
    individuo.tiempo_total = tiempo_acum
    individuo.distancia_total = distancia_acum
    individuo.puntos_totales = puntos_acum
    individuo.fitness = fitness
    
    # ⚠️ NUEVO: Si hay violaciones de horario, intentar reparar
    if violaciones_horarios > 0:
        # Guardar fitness actual para comparar
        fitness_antes = fitness
        
        # Intentar reparar horarios
        individuo_reparado = reparar_horarios_individuo(individuo, max_intentos=2)
        
        # Re-evaluar después de reparar (llamada recursiva, pero solo una vez)
        # Para evitar recursión infinita, marcamos que ya se intentó reparar
        if not hasattr(individuo, '_reparacion_horarios_intentada'):
            individuo._reparacion_horarios_intentada = True
            individuo.dias = individuo_reparado.dias
            individuo.ciudades = individuo_reparado.ciudades
            # Re-evaluar con los cambios
            return evaluar_individuo(individuo)
    
    return fitness

def seleccion_torneo(poblacion: List[Individual], k: int = 3) -> Individual:
    torneo = random.sample(poblacion, k)
    return max(torneo, key=lambda ind: ind.fitness)

def crossover_dos_puntos(padre1: Individual, padre2: Individual) -> Tuple[Individual, Individual]:
    if random.random() > PROBABILIDAD_CRUCE:
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
    
    hijo1 = Individual(hijo1_dias, hijo1_ciudades)
    hijo2 = Individual(hijo2_dias, hijo2_ciudades)
    
    if not validar_restricciones_ciudades(hijo1):
        hijo1 = reparar_individuo(hijo1)
    if not validar_restricciones_ciudades(hijo2):
        hijo2 = reparar_individuo(hijo2)
    
    return hijo1, hijo2

def mutar(individuo: Individual):
    for dia_idx in range(len(individuo.dias)):
        dia = individuo.dias[dia_idx]
        ciudad = individuo.ciudades[dia_idx]

        if not dia:  # Evitar mutaciones en días vacíos
            continue

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
        
        if random.random() < 0.05:
            ciudades_visitadas = set(individuo.ciudades[:dia_idx])
            dias_consecutivos_actual = 1
            for i in range(dia_idx - 1, -1, -1):
                if individuo.ciudades[i] == ciudad:
                    dias_consecutivos_actual += 1
                else:
                    break
            nueva_ciudad = obtener_ciudad_mas_cercana(ciudad, ciudades_visitadas, dias_consecutivos_actual)
            if nueva_ciudad != ciudad:
                individuo.ciudades[dia_idx] = nueva_ciudad
                lugares_nueva = get_lugares_ciudad(nueva_ciudad)
                if lugares_nueva:
                    individuo.dias[dia_idx] = [
                        random.choice(lugares_nueva)["id"] for _ in range(len(dia))
                    ]
    
    # ⚠️ CRÍTICO: Validar y reparar después de mutar
    if not validar_restricciones_ciudades(individuo):
        # La reparación devuelve un nuevo individuo, hay que copiarlo
        individuo_reparado = reparar_individuo(individuo)
        individuo.dias = individuo_reparado.dias
        individuo.ciudades = individuo_reparado.ciudades
    
    # Intentar reparar horarios después de mutar
    individuo_reparado = reparar_horarios_individuo(individuo, max_intentos=1)
    individuo.dias = individuo_reparado.dias
    individuo.ciudades = individuo_reparado.ciudades


def reiniciar_poblacion(tam_poblacion: int, num_dias: int, lugares_por_dia: int, mejor_individuo: Individual) -> List[Individual]:
    log(f"\n REINICIANDO POBLACIÓN (manteniendo mejor individuo)...")
    
    nueva_poblacion = [copy.deepcopy(mejor_individuo)]
    
    for _ in range(tam_poblacion - 1):
        nuevo_ind = crear_individuo_aleatorio(num_dias, lugares_por_dia)
        evaluar_individuo(nuevo_ind)
        nueva_poblacion.append(nuevo_ind)
    
    log(f"Nueva población creada ({tam_poblacion} individuos)\n")
    return nueva_poblacion


def algoritmo_genetico_espana(
    num_dias: int ,
    lugares_por_dia: int,
    tam_poblacion: int,
    num_generaciones: int = None,
    tasa_elitismo: float = 0.15,
    tiempo_limite_horas: float = None
) -> Dict:
    import time as time_module
    
    tiempo_limite_segundos = None
    if tiempo_limite_horas is not None:
        tiempo_limite_segundos = int(tiempo_limite_horas * 3600)
    
    if num_generaciones is None and tiempo_limite_horas is None:
        raise ValueError("Debe especificar num_generaciones o tiempo_limite_horas")
    
    modo_tiempo = tiempo_limite_segundos is not None
    
    log(f"\n{'='*80}")
    log(f"ALGORITMO GENÉTICO")
    log(f"{'='*80}")
    log(f"Días: {num_dias}")
    log(f"Lugares/día: {lugares_por_dia}")
    log(f"Población: {tam_poblacion}")
    if modo_tiempo:
        horas = int(tiempo_limite_horas)
        minutos = int((tiempo_limite_horas - horas) * 60)
        log(f"Tiempo límite: {horas}h {minutos}m ({tiempo_limite_horas:.2f}h)")
    else:
        log(f"Generaciones: {num_generaciones}")
    log(f"Elitismo: {tasa_elitismo*100:.0f}%")
    log(f"Dataset: {len(lugares_turisticos_espana)} lugares en 10 ciudades")
    log(f"{'='*80}\n")
    
    tiempo_inicio_total = time_module.time()
    
    log("Creando población inicial")
    poblacion = crear_poblacion_inicial(tam_poblacion, num_dias, lugares_por_dia)
    
    log("Evaluando población inicial")
    for ind in poblacion:
        evaluar_individuo(ind)
    
    mejor_global = copy.deepcopy(max(poblacion, key=lambda ind: ind.fitness))
    historial_fitness = [mejor_global.fitness]
    historial_mejor_gen = [mejor_global.fitness]
    historial_tiempos = [0]  # Tiempo acumulado
    
    num_elite = int(tam_poblacion * tasa_elitismo)
    
    # Variables para control de estancamiento
    mejor_fitness_era = mejor_global.fitness
    generaciones_estancadas = 0
    umbral_estancamiento = 100
    
    if modo_tiempo:
        log(f"\nIniciando evolución (hasta {tiempo_limite_segundos}s)...\n")
    else:
        log(f"\nIniciando evolución ({num_generaciones} generaciones)...\n")
    
    gen = 0
    ultimo_reporte = time_module.time()
    
    while True:
        # Verificar criterio de parada
        tiempo_transcurrido = time_module.time() - tiempo_inicio_total
        
        if modo_tiempo:
            if tiempo_transcurrido >= tiempo_limite_segundos:
                log(f"\n⏱️  Tiempo límite alcanzado: {tiempo_transcurrido:.1f}s")
                break
        else:
            if gen >= num_generaciones:
                break
        
        poblacion.sort(key=lambda ind: ind.fitness, reverse=True)
        nueva_poblacion = [copy.deepcopy(ind) for ind in poblacion[:num_elite]]
        
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = seleccion_torneo(poblacion)
            padre2 = seleccion_torneo(poblacion)
            
            hijo1, hijo2 = crossover_dos_puntos(padre1, padre2)
            mutar(hijo1)
            mutar(hijo2)

            eliminar_duplicados_globales(hijo1)
            eliminar_duplicados_globales(hijo2)
            
            evaluar_individuo(hijo1)
            evaluar_individuo(hijo2)
            
            nueva_poblacion.extend([hijo1, hijo2])
        
        poblacion = nueva_poblacion[:tam_poblacion]
        
        mejor_gen = max(poblacion, key=lambda ind: ind.fitness)
        historial_mejor_gen.append(mejor_gen.fitness) 
        
        if mejor_gen.fitness > mejor_global.fitness:
            mejor_global = copy.deepcopy(mejor_gen)
        
        historial_fitness.append(mejor_global.fitness)
        historial_tiempos.append(tiempo_transcurrido)
        
        # Comprobar estancamiento
        if mejor_gen.fitness > mejor_fitness_era:
            mejor_fitness_era = mejor_gen.fitness
            generaciones_estancadas = 0
        else:
            generaciones_estancadas += 1
        
        # Reiniciar población si hay estancamiento prolongado
        if generaciones_estancadas >= umbral_estancamiento:
            log(f"\n⚠️  ESTANCAMIENTO DETECTADO: {generaciones_estancadas} generaciones sin mejora")
            log(f"   Mejor fitness actual: {mejor_fitness_era:.1f}")
            poblacion = reiniciar_poblacion(tam_poblacion, num_dias, lugares_por_dia, mejor_global)
            generaciones_estancadas = 0
            mejor_fitness_era = mejor_global.fitness
        
        gen += 1
        
        tiempo_desde_reporte = time_module.time() - ultimo_reporte
        if (gen % 50 == 0) or (tiempo_desde_reporte >= 60):
            if modo_tiempo:
                tiempo_restante = tiempo_limite_segundos - tiempo_transcurrido
                mins_restantes = int(tiempo_restante // 60)
                log(f"  Gen {gen:4d} | Tiempo: {tiempo_transcurrido/60:6.1f}m (resta: {mins_restantes}m) | "
                      f"Fitness: {mejor_global.fitness:8.1f} | "
                      f"Puntos: {mejor_global.puntos_totales:5d} | "
                      f"Dist: {mejor_global.distancia_total:7.1f}km")
            else:
                log(f"  Gen {gen:4d}/{num_generaciones} | "
                      f"Mejor fitness: {mejor_global.fitness:8.1f} | "
                      f"Puntos: {mejor_global.puntos_totales:5d} | "
                      f"Tiempo: {mejor_global.tiempo_total/60:6.1f}h | "
                      f"Dist: {mejor_global.distancia_total:7.1f}km")
            ultimo_reporte = time_module.time()
    
    tiempo_total_ejecucion = time_module.time() - tiempo_inicio_total
    
    log(f"\n✅ Evolución completada!")
    log(f"🏆 Mejor fitness global: {mejor_global.fitness:.1f}")
    log(f"📊 Generaciones ejecutadas: {gen}")
    log(f"⏱️  Tiempo total: {tiempo_total_ejecucion:.2f}s ({tiempo_total_ejecucion/60:.2f}m)")
    
    return {
        "mejor_individuo": mejor_global,
        "historial_fitness": historial_fitness,
        "historial_mejor_gen": historial_mejor_gen,
        "historial_tiempos": historial_tiempos,
        "poblacion_final": poblacion,
        "generaciones_ejecutadas": gen,
        "tiempo_ejecucion": tiempo_total_ejecucion
    }


def analizar_solucion(individuo: Individual):
    """Muestra análisis detallado de una solución con itinerario completo"""
    log(f"\n{'='*80}")
    log(f"ANÁLISIS DE LA MEJOR SOLUCIÓN")
    log(f"{'='*80}\n")
    
    log(f"Métricas Globales:")
    log(f"- Fitness total: {individuo.fitness:.1f}")
    log(f"- Puntos totales: {individuo.puntos_totales}")
    log(f"- Tiempo total: {individuo.tiempo_total/60:.1f} horas ({individuo.tiempo_total:.0f} minutos)")
    log(f"- Tiempo promedio/día: {(individuo.tiempo_total/len(individuo.dias))/60:.1f} horas")
    log(f"- Distancia total: {individuo.distancia_total:.1f} km")
    log(f"- Ciudades visitadas: {len(set(individuo.ciudades))}")
    
    log(f"\nITINERARIO DETALLADO POR DÍAS:")
    log(f"{'='*80}\n")
    
    for dia_idx, (dia, ciudad) in enumerate(zip(individuo.dias, individuo.ciudades), 1):
        lugares_dia = get_lugares_por_ids(dia)
        tiempo_dia, dist_dia, puntos_dia = calcular_tiempo_dia(individuo, dia_idx - 1)
        
        gasto_dia = 0
        for lugar in lugares_dia:
            tipo = lugar.get('tipo', '')
            if tipo in PRECIOS_TIPO:
                gasto_dia += PRECIOS_TIPO[tipo]
            else:
                gasto_dia += 10
        
        log(f"{'─'*80}")
        log(f"DÍA {dia_idx} - {ciudad.upper()}")
        log(f"{'─'*80}")
        
        transport_info = next((t for t in individuo.transportes_intercity if t[0] == dia_idx - 1), None)
        if transport_info:
            _, origen, destino, tipo_elegido, tiempo_trans, costo_trans = transport_info
            tipo_icons = {"avion": "✈️", "tren": "🚄", "bus": "🚌"}
            icon = tipo_icons.get(tipo_elegido, "🚗")
            log(f"{icon} Transporte: {origen} → {destino} | "
                  f"{tipo_elegido.upper()} ({tiempo_trans} min, {costo_trans}€)")
            log(f"")
        
        if gasto_dia > PRESUPUESTO_DIARIO:
            presupuesto_str = f"💰 {gasto_dia}€ ⚠️ EXCEDE ({PRESUPUESTO_DIARIO}€)"
        else:
            presupuesto_str = f"💰 {gasto_dia}€ / {PRESUPUESTO_DIARIO}€"
        
        log(f"📊 Resumen: {len(lugares_dia)} lugares | "
              f"{puntos_dia} puntos | "
              f"{tiempo_dia/60:.2f}h ({tiempo_dia:.0f} min) | "
              f"{dist_dia:.1f} km | "
              f"{presupuesto_str}")
        log(f"")
        
        hora_actual = HORA_INICIO
        
        for i, lugar in enumerate(lugares_dia, 1):
            tiempo_transito = 0
            if i > 1:
                lugar_anterior = lugares_dia[i-2]
                ciudad_anterior_lugar = lugar_anterior.get('ciudad', ciudad)
                ciudad_actual_lugar = lugar.get('ciudad', ciudad)
                
                if ciudad_anterior_lugar == ciudad_actual_lugar:
                    dist = distancia_haversine(lugar_anterior, lugar)
                    tiempo_transito = dist / VELOCIDAD_MEDIA * 60
                else:
                    # calcular_transporte_intercity devuelve (tiempo, costo), necesitamos solo tiempo
                    tiempo_trans, _ = calcular_transporte_intercity(ciudad_anterior_lugar, ciudad_actual_lugar, "tren")
                    tiempo_transito = tiempo_trans if tiempo_trans is not None else 60
                
                hora_actual += tiempo_transito
            
            horas_llegada = int(hora_actual // 60)
            mins_llegada = int(hora_actual % 60)
            hora_str_llegada = f"{horas_llegada:02d}:{mins_llegada:02d}"
            
            hora_salida = hora_actual + lugar['tiempo_visita']
            horas_salida = int(hora_salida // 60)
            mins_salida = int(hora_salida % 60)
            hora_str_salida = f"{horas_salida:02d}:{mins_salida:02d}"
            
            tipo_lugar = lugar.get('tipo', '')
            es_restaurante = tipo_lugar in ['restaurante', 'bar', 'cafetería']
            
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
                if HORA_DESAYUNO_MIN <= hora_actual <= HORA_DESAYUNO_MAX:
                    icono_comida = " DESAYUNO"
                elif HORA_ALMUERZO_MIN <= hora_actual <= HORA_ALMUERZO_MAX:
                    icono_comida = " COMIDA"
                elif HORA_CENA_MIN <= hora_actual <= HORA_CENA_MAX:
                    icono_comida = " CENA"

            nombre_corto = lugar['nombre'][:40]
            if len(lugar['nombre']) > 40:
                nombre_corto += "..."
            
            if tipo_lugar in PRECIOS_TIPO:
                precio = PRECIOS_TIPO[tipo_lugar]
            else:
                precio = 10
            
            log(f"  {i:2d}. {hora_str_llegada} - {hora_str_salida} │ {nombre_corto:43s} │ {tipo_lugar:12s} │ {lugar['puntos']:3d} pts │ {precio:2d}€{icono_comida}{fuera_horario}")
            
            if tiempo_transito > 0:
                if tiempo_transito > 60:
                    log(f"      {'':13s} └─ Tránsito: {tiempo_transito/60:.1f}h ({tiempo_transito:.0f} min)")
                else:
                    log(f"      {'':13s} └─ Tránsito: {tiempo_transito:.0f} min")
            
            hora_actual += lugar['tiempo_visita']
        
        horas_fin = int(hora_actual // 60)
        mins_fin = int(hora_actual % 60)
        hora_str_fin = f"{horas_fin:02d}:{mins_fin:02d}"
        
        exceso = max(0, tiempo_dia - TIEMPO_DIA)
        if exceso > 0:
            log(f"\n  ⚠️  DÍA FINALIZADO: {hora_str_fin} | EXCESO: {exceso:.0f} min ({exceso/60:.1f}h) | PENALIZACIÓN: -{PENALIZACION_EXCESO_TIEMPO * exceso:.0f} pts")
            if exceso > 120:
                log(f"      ❌ EXCESO CRÍTICO (>2h): Penalización adicional de -10,000 pts")
        else:
            log(f"\n  ✅ DÍA FINALIZADO: {hora_str_fin} | Dentro del límite ({TIEMPO_DIA/60:.0f}h)")
        
        log(f"")
    
    if individuo.transportes_intercity:
        log(f"{'='*80}")
        log(f"🚊 RESUMEN DE TRANSPORTES INTERCITY")
        log(f"{'='*80}\n")
        
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
        
        log(f"📊 Estadísticas:")
        log(f"  ✈️  Avión: {transportes_summary['avion']} viajes")
        log(f"  🚄 Tren:  {transportes_summary['tren']} viajes")
        log(f"  🚌 Bus:   {transportes_summary['bus']} viajes")
        log(f"\n💰 Costo total transportes: {costo_total_transporte}€")
        log(f"⏱️  Tiempo total transportes: {tiempo_total_transporte} min ({tiempo_total_transporte/60:.1f}h)")
        log(f"")
    
    log(f"{'='*80}")
    log(f"✅ ANÁLISIS COMPLETO")
    log(f"{'='*80}\n")


def exportar_resultados(resultados: Dict, archivo: str = "resultados_espana.json", config: Dict = None):
    """Exporta resultados a JSON incluyendo configuración del algoritmo"""
    import json
    
    mejor = resultados["mejor_individuo"]
    
    data = {
        "fitness": mejor.fitness,
        "puntos_totales": mejor.puntos_totales,
        "tiempo_total_min": mejor.tiempo_total,
        "distancia_total_km": mejor.distancia_total,
        "num_dias": len(mejor.dias),
        "ciudades_visitadas": list(set(mejor.ciudades)),
        "configuracion": {
            "poblacion": config.get("tam_poblacion") if config else None,
            "generaciones": config.get("num_generaciones") if config else resultados.get("generaciones_ejecutadas"),
            "num_dias": config.get("num_dias") if config else len(mejor.dias),
            "lugares_por_dia": config.get("lugares_por_dia") if config else None,
            "tasa_elitismo": config.get("tasa_elitismo") if config else None,
            "max_dias_por_ciudad": MAX_DIAS_POR_CIUDAD,
            "agrupar": AGRUPAR
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
        "historial_fitness": resultados["historial_fitness"],  # Mejor global
        "historial_mejor_gen": resultados.get("historial_mejor_gen", resultados["historial_fitness"])  # Mejor por gen
    }
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    log(f"💾 Resultados exportados a: {archivo}")

# Ejecución principal

if __name__ == "__main__":
    import sys
    
    # CONFIGURAR LOGGING AL INICIO
    log_file = configurar_logging(output_dir="logs", prefijo="ag_espana")
    
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
            "num_dias": 20,
            "lugares_por_dia": 12,
            "tam_poblacion": 15000,
            "num_generaciones": 800,
            "tasa_elitismo": 0.15,
            "descripcion": "Mayor exploración y convergencia"
        },
        "3": {
            "nombre": "ULTRA-COMPLEJA (1.5-2 horas)",
            "num_dias": 20,
            "lugares_por_dia": 12,
            "tam_poblacion": 1000,
            "num_generaciones": 600,
            "tasa_elitismo": 0.10,
            "descripcion": "Máxima calidad de solución"
        }
    }
    
    if len(sys.argv) > 1:
        modo = sys.argv[1]
    else:
        # Estos prints SÍ van a consola para interacción del usuario
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
    
    # Registrar configuración elegida en el log
    log(f"\n{'='*80}")
    log(f"CONFIGURACIÓN SELECCIONADA: Modo {modo}")
    log(f"Nombre: {config['nombre']}")
    log(f"Descripción: {config['descripcion']}")
    log(f"{'='*80}\n")
    
    resultados = algoritmo_genetico_espana(
        num_dias=config["num_dias"],
        lugares_por_dia=config["lugares_por_dia"],
        tam_poblacion=config["tam_poblacion"],
        num_generaciones=config["num_generaciones"],
        tasa_elitismo=config["tasa_elitismo"],
        tiempo_limite_horas=None
    )
    
    analizar_solucion(resultados["mejor_individuo"])
    exportar_resultados(resultados, archivo=f"ag_{modo}.json", config=config)
    
    log(f"\n{'='*80}")
    log(f"EJECUCIÓN COMPLETADA - Log guardado en: {log_file}")
    log(f"{'='*80}")
