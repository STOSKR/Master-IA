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
    
    if AGRUPAR_DIAS_POR_CIUDAD:
        dia_actual = 0
        
        while dia_actual < num_dias:
            ciudad = random.choice(ciudades_disponibles)
            
            dias_restantes = num_dias - dia_actual
            
            if dias_restantes == 1:
                dias_en_ciudad = 1
            else:
                dias_en_ciudad = random.randint(2, min(MAX_DIAS_POR_CIUDAD, dias_restantes))
            
            lugares_ciudad = get_lugares_ciudad(ciudad)
            if len(lugares_ciudad) < lugares_por_dia:
                lugares_ciudad = lugares_turisticos_espana
            
            for _ in range(dias_en_ciudad):
                if dia_actual >= num_dias:
                    break
                
                lugares_dia = random.sample(lugares_ciudad, min(lugares_por_dia, len(lugares_ciudad)))
                ids_dia = [l["id"] for l in lugares_dia]
                random.shuffle(ids_dia)
                
                dias.append(ids_dia)
                ciudades_plan.append(ciudad)
                dia_actual += 1
    else:
        historial_ciudad = []
        
        for _ in range(num_dias):
            if historial_ciudad and len(historial_ciudad) >= MAX_DIAS_POR_CIUDAD:
                ultimos = historial_ciudad[-MAX_DIAS_POR_CIUDAD:]
                if len(set(ultimos)) == 1:
                    ciudad_actual = random.choice([c for c in ciudades_disponibles if c != ultimos[0]])
                else:
                    ciudad_actual = random.choice(ciudades_disponibles)
            else:
                ciudad_actual = random.choice(ciudades_disponibles)
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
    return [crear_individuo_aleatorio(num_dias, lugares_por_dia) for _ in range(tam_poblacion)]

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
    
    # Tiempo comida
    if tiempo_total > 180:
        tiempo_total += TIEMPO_COMIDA_MIN
    if tiempo_total > 480:
        tiempo_total += TIEMPO_CENA_MIN
    
    return tiempo_total, distancia_total, puntos_total

def evaluar_individuo(individuo: Individual) -> float:
    """
    Calcula fitness con restricciones mejoradas:
    - Penalización FUERTE por exceder tiempo diario
    - Validación de comidas obligatorias (almuerzo y cena)
    - Penalización por muchos restaurantes consecutivos
    - NUEVO: Validación de horarios de apertura/cierre
    - NUEVO: Validación de presupuesto diario
    - NUEVO: Penalización por cambios innecesarios de ciudad
    """
    fitness = 0
    tiempo_acum = 0
    distancia_acum = 0
    puntos_acum = 0
    
    for dia_idx in range(len(individuo.dias)):
        tiempo_dia, dist_dia, puntos_dia = calcular_tiempo_dia(individuo, dia_idx)
        lugares_dia = get_lugares_por_ids(individuo.dias[dia_idx])
        
        # ============================================================
        # VALIDACIÓN: Días consecutivos en misma ciudad
        # ============================================================
        if AGRUPAR_DIAS_POR_CIUDAD and dia_idx > 0:
            ciudad_actual = individuo.ciudades[dia_idx]
            ciudad_anterior = individuo.ciudades[dia_idx - 1]
            
            # Verificar si hay cambio de ciudad
            if ciudad_actual != ciudad_anterior:
                # Contar cuántos días quedan
                dias_restantes = len(individuo.dias) - dia_idx
                
                # Buscar si vuelve a la ciudad anterior más adelante
                vuelve_ciudad_anterior = False
                for futuro_idx in range(dia_idx + 1, len(individuo.dias)):
                    if individuo.ciudades[futuro_idx] == ciudad_anterior:
                        vuelve_ciudad_anterior = True
                        break
                
                # Si vuelve a la ciudad anterior, es un cambio innecesario
                if vuelve_ciudad_anterior:
                    fitness -= PENALIZACION_CAMBIO_CIUDAD_INNECESARIO
        
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
        if not validar_limite_ciudad(individuo.ciudades[:dia_idx + 1], individuo.ciudades[dia_idx])[0]:
            fitness -= PENALIZACION_LIMITE_CIUDAD
        
        # ============================================================
        # PENALIZACIÓN FUERTE POR EXCESO DE TIEMPO
        # ============================================================
        if tiempo_dia > TIEMPO_DIA:
            exceso = tiempo_dia - TIEMPO_DIA
            fitness -= PENALIZACION_EXCESO_TIEMPO * exceso
            
            if exceso > 120:
                fitness -= 10000  # Penalización catastrófica
        
        # ============================================================
        # VALIDAR HORARIOS, COMIDAS Y PRESUPUESTO
        # ============================================================
        hora_actual = HORA_INICIO
        tiene_almuerzo = False
        tiene_cena = False
        gasto_dia = 0
        
        # Simular horarios del día
        for lugar in lugares_dia:
            tipo = lugar.get('tipo', '')
            
            # ============================================================
            # NUEVO: Validar horario de apertura/cierre
            # ============================================================
            if tipo in HORARIOS_TIPO:
                apertura = HORARIOS_TIPO[tipo]["apertura"]
                cierre = HORARIOS_TIPO[tipo]["cierre"]
                
                # Si es bar que cierra de madrugada (2:00), ajustar
                if tipo == "bar" and cierre < apertura:
                    cierre = 26 * 60  # 02:00 del día siguiente = 26:00
                
                # Verificar si la visita está dentro del horario
                if hora_actual < apertura or hora_actual > cierre:
                    fitness -= PENALIZACION_FUERA_HORARIO_APERTURA
            
            # ============================================================
            # NUEVO: Calcular gasto del día
            # ============================================================
            if tipo in PRECIOS_TIPO:
                gasto_dia += PRECIOS_TIPO[tipo]
            else:
                gasto_dia += 10  # Precio por defecto
            
            # Verificar si es restaurante/bar/cafetería en hora de comida
            if tipo in ['restaurante', 'bar', 'cafetería']:
                if HORA_ALMUERZO_MIN <= hora_actual <= HORA_ALMUERZO_MAX:
                    tiene_almuerzo = True
                elif HORA_CENA_MIN <= hora_actual <= HORA_CENA_MAX:
                    tiene_cena = True
            
            hora_actual += lugar['tiempo_visita']
        
        # ============================================================
        # NUEVO: Validar presupuesto diario
        # ============================================================
        if gasto_dia > PRESUPUESTO_DIARIO:
            exceso_presupuesto = gasto_dia - PRESUPUESTO_DIARIO
            fitness -= PENALIZACION_EXCESO_PRESUPUESTO * exceso_presupuesto
        
        # Penalizar si no hay almuerzo
        if not tiene_almuerzo:
            fitness -= PENALIZACION_COMIDA_FALTA
        
        # Penalizar si no hay cena
        if not tiene_cena:
            fitness -= PENALIZACION_CENA_FALTA
        
        # ============================================================
        # PENALIZAR MUCHOS RESTAURANTES CONSECUTIVOS
        # ============================================================
        restaurantes_consecutivos = 0
        max_consecutivos = 0
        
        for lugar in lugares_dia:
            tipo = lugar.get('tipo', '')
            if tipo in ['restaurante', 'bar', 'cafetería']:
                restaurantes_consecutivos += 1
                max_consecutivos = max(max_consecutivos, restaurantes_consecutivos)
            else:
                restaurantes_consecutivos = 0
        
        if max_consecutivos > 3:
            fitness -= PENALIZACION_RESTAURANTES_CONSECUTIVOS * (max_consecutivos - 3)
        
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
