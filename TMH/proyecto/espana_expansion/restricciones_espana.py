from typing import List, Dict, Tuple
from math import factorial, comb, log10

MAX_DIAS_POR_CIUDAD = 4
PRESUPUESTO_DIARIO = 150

def validar_limite_ciudad(historial_ciudades: List[str], nueva_ciudad: str) -> Tuple[bool, int]:
    if not historial_ciudades:
        return True, 0
    
    dias_consecutivos = 1
    for ciudad in reversed(historial_ciudades):
        if ciudad == nueva_ciudad:
            dias_consecutivos += 1
        else:
            break
    
    es_valido = dias_consecutivos < MAX_DIAS_POR_CIUDAD
    return es_valido, dias_consecutivos

def calcular_penalizacion_cambio_ciudad(historial_ciudades: List[str]) -> float:
    if len(historial_ciudades) < 2:
        return 0
    
    if historial_ciudades[-1] != historial_ciudades[-2]:
        return 20  # Penalización moderada por cambio
    return 0

def calcular_complejidad_espana(num_lugares: int, num_ciudades: int, num_dias: int) -> Dict:
    """
    Calcula la complejidad del problema de España con restricción de ciudad
    
    Args:
        num_lugares: Total de lugares disponibles (~1,293)
        num_ciudades: Número de ciudades (10)
        num_dias: Días totales del viaje
        
    Returns:
        Diccionario con métricas de complejidad
    """
    lugares_por_dia = 12
    
    try:
        # Combinaciones por día
        combinaciones_por_dia = comb(num_lugares, lugares_por_dia)
    except:
        log_comb = lugares_por_dia * (log10(num_lugares) - log10(lugares_por_dia)) + lugares_por_dia * 0.434
        combinaciones_por_dia = 10 ** log_comb
    
    try:
        # Permutaciones por día
        log_fact = sum(log10(i) for i in range(1, lugares_por_dia + 1))
        permutaciones_por_dia = combinaciones_por_dia * (10 ** log_fact)
    except:
        permutaciones_por_dia = float('inf')
    
    # Combinaciones de ciudades
    # Con máx. 4 días/ciudad, necesitas al menos num_dias/4 ciudades
    min_ciudades = (num_dias + MAX_DIAS_POR_CIUDAD - 1) // MAX_DIAS_POR_CIUDAD
    
    # Calcular combinaciones posibles de ciudades
    try:
        combinaciones_ciudades = 0
        for k in range(min_ciudades, min(num_ciudades, num_dias) + 1):
            combinaciones_ciudades += comb(num_ciudades, k) * factorial(k)
    except:
        # Aproximación
        k_promedio = (min_ciudades + num_ciudades) // 2
        combinaciones_ciudades = comb(num_ciudades, k_promedio) * factorial(k_promedio)
    
    # Espacio de búsqueda total
    try:
        log_espacio_rutas = num_dias * log10(permutaciones_por_dia)
        log_espacio_total = log_espacio_rutas + log10(combinaciones_ciudades)
        
        if log_espacio_total > 308:  # Límite de float
            espacio_busqueda_total = float('inf')
            complejidad_total = float('inf')
        else:
            espacio_busqueda_total = 10 ** log_espacio_rutas
            complejidad_total = 10 ** log_espacio_total
    except:
        espacio_busqueda_total = float('inf')
        complejidad_total = float('inf')
    
    return {
        "num_lugares_total": num_lugares,
        "num_ciudades": num_ciudades,
        "num_dias": num_dias,
        "lugares_por_dia_promedio": lugares_por_dia,
        "max_dias_por_ciudad": MAX_DIAS_POR_CIUDAD,
        "min_ciudades_necesarias": min_ciudades,
        "combinaciones_por_dia": combinaciones_por_dia,
        "permutaciones_por_dia": permutaciones_por_dia,
        "combinaciones_ciudades": combinaciones_ciudades,
        "espacio_busqueda_total": espacio_busqueda_total,
        "complejidad_total_real": complejidad_total,
        "log10_complejidad": log_espacio_total if 'log_espacio_total' in locals() else float('inf'),
    }

# Restricciones simplificadas (sin todas las complejas de Madrid)
def aplicar_restricciones_basicas(lugares_ids: List[int], tiempo_total: int) -> float:
    hora_inicio = 9 * 60  # 9 AM
    hora_fin = 23 * 60    # 11 PM
    
    hora_actual = hora_inicio + tiempo_total
    
    if hora_actual < hora_inicio or tiempo_total == 0:
        return 0
    
    # Factor de fatiga: aumenta con el tiempo
    progreso = min(1.0, (hora_actual - hora_inicio) / (hora_fin - hora_inicio))
    penalizacion_fatiga = progreso * 50  # Máximo 50 puntos de penalización
    
    return penalizacion_fatiga

if __name__ == "__main__":
    import math
    
    print("\n" + "="*80)
    print("📊 CÁLCULO DE COMPLEJIDAD - ESPAÑA")
    print("="*80)
    
    # Configuración: 20 días, 1293 lugares, 10 ciudades
    comp = calcular_complejidad_espana(1293, 10, 20)
    
    print(f"\n🔢 Configuración:")
    print(f"  Lugares totales: {comp['num_lugares_total']}")
    print(f"  Ciudades: {comp['num_ciudades']}")
    print(f"  Días de viaje: {comp['num_dias']}")
    print(f"  Lugares por día: {comp['lugares_por_dia_promedio']}")
    print(f"  Máx. días por ciudad: {comp['max_dias_por_ciudad']}")
    print(f"  Mín. ciudades a visitar: {comp['min_ciudades_necesarias']}")
    
    print(f"\n📈 Espacio de búsqueda:")
    print(f"  Combinaciones por día: {comp['combinaciones_por_dia']:.4e}")
    print(f"  Permutaciones por día: {comp['permutaciones_por_dia']:.4e}")
    print(f"  Combinaciones de ciudades: {comp['combinaciones_ciudades']:.4e}")
    
    print(f"\n⭐ COMPLEJIDAD TOTAL: {comp['complejidad_total_real']:.6e}")
    if comp['log10_complejidad'] != float('inf'):
        print(f"   📍 Equivalente a: 10^{comp['log10_complejidad']:.1f}")
    
    print("\n" + "="*80)
    print("💡 COMPARACIÓN:")
    print("="*80)
    print(f"  Madrid (7 días, 253 lugares):     10^251.5")
    if comp['log10_complejidad'] != float('inf'):
        print(f"  España (20 días, 1293 lugares):   10^{comp['log10_complejidad']:.1f}")
        print(f"  Diferencia: {comp['log10_complejidad'] - 251.5:.1f} órdenes de magnitud")
    print("="*80)
    
    # Test de validación de ciudades
    print("\n🧪 TEST DE VALIDACIÓN DE LÍMITE DE CIUDAD:")
    print("="*80)
    historial = ["Madrid", "Madrid", "Madrid"]
    valido, dias = validar_limite_ciudad(historial, "Madrid")
    print(f"  Historial: {historial}")
    print(f"  Nueva ciudad: Madrid")
    print(f"  ¿Válido?: {valido} (días consecutivos: {dias})")
    
    historial = ["Madrid", "Madrid", "Madrid", "Madrid"]
    valido, dias = validar_limite_ciudad(historial, "Madrid")
    print(f"\n  Historial: {historial}")
    print(f"  Nueva ciudad: Madrid")
    print(f"  ¿Válido?: {valido} (días consecutivos: {dias}) ❌ EXCEDE LÍMITE")
    
    historial = ["Madrid", "Madrid", "Madrid"]
    valido, dias = validar_limite_ciudad(historial, "Barcelona")
    print(f"\n  Historial: {historial}")
    print(f"  Nueva ciudad: Barcelona")
    print(f"  ¿Válido?: {valido} (días consecutivos: {dias}) ✅ CAMBIO VÁLIDO")
    print("="*80)
