"""
RESTRICCIONES COMPLEJAS PARA EL ALGORITMO GENÉTICO
Este módulo añade múltiples capas de complejidad que hacen que el problema
tenga una explosión combinatoria significativa.
"""

import random
from typing import List, Dict, Tuple

# =============================================================================
# 1. RESTRICCIONES DE INCOMPATIBILIDAD
# =============================================================================
# Algunos lugares NO pueden visitarse el mismo día
# Razones: competencia, fatiga, saturación del mismo tipo, etc.

INCOMPATIBILIDADES = {
    # No visitar 2 museos grandes el mismo día (fatiga cultural)
    "museos_grandes": [
        ["Museo Nacional del Prado", "Museo Nacional Centro de Arte Reina Sofía"],
        ["Museo Nacional del Prado", "Museo Nacional Thyssen-Bornemisza"],
        ["Museo Nacional Centro de Arte Reina Sofía", "Museo Nacional Thyssen-Bornemisza"],
    ],
    
    # No visitar parques grandes consecutivamente (saturación de naturaleza)
    "parques_grandes": [
        ["Parque de El Retiro", "Casa de Campo"],
        ["Real Jardín Botánico de Madrid", "Casa de Campo"],
    ],
    
    # No visitar restaurantes caros el mismo día (presupuesto)
    "restaurantes_caros": [
        ["DiverXO", "Amazónico"],
        ["DiverXO", "StreetXO"],
        ["Amazónico", "StreetXO"],
        ["Casa Botín", "DiverXO"],
    ],
    
    # Incompatibilidad de zonas lejanas (demasiado tiempo de traslado)
    "zonas_lejanas": [
        ["Estadio Santiago Bernabéu", "Parque Cerro del Tío Pío (Parque de las Siete Tetas)"],
        ["Faro de Moncloa", "Estación de Atocha"],
    ],
}

# =============================================================================
# 2. GRUPOS DE LUGARES RELACIONADOS (SINERGIAS)
# =============================================================================
# Bonus por visitar lugares relacionados el mismo día

GRUPOS_SINERGICOS = {
    "triangulo_del_arte": {
        "lugares": ["Museo Nacional del Prado", "Museo Nacional Centro de Arte Reina Sofía", "Museo Nacional Thyssen-Bornemisza"],
        "bonus_puntos": 100,
        "min_lugares": 2  # Mínimo 2 para activar bonus
    },
    "madrid_de_los_austrias": {
        "lugares": ["Plaza Mayor de Madrid", "Palacio Real de Madrid", "Catedral de Santa María la Real de la Almudena", "Mercado de San Miguel"],
        "bonus_puntos": 80,
        "min_lugares": 3
    },
    "shopping_lujo": {
        "lugares": ["Calle de Serrano", "Ten con Ten", "Amazónico", "Zara (Plaza de España)"],
        "bonus_puntos": 60,
        "min_lugares": 2
    },
    "gastronomia_tradicional": {
        "lugares": ["Casa Botín", "Casa Lucio", "La Bola Taberna", "Sobrino de Botín", "Mercado de San Miguel"],
        "bonus_puntos": 70,
        "min_lugares": 2
    },
    "parques_y_naturaleza": {
        "lugares": ["Parque de El Retiro", "Real Jardín Botánico de Madrid", "Templo de Debod"],
        "bonus_puntos": 50,
        "min_lugares": 2
    },
    "gran_via_centro": {
        "lugares": ["Gran Vía", "Puerta del Sol", "Plaza Mayor de Madrid", "WOW Concept"],
        "bonus_puntos": 60,
        "min_lugares": 3
    },
}

# =============================================================================
# 3. EVENTOS ESPECIALES POR DÍA
# =============================================================================
# Ciertos lugares tienen bonus o están disponibles solo ciertos días

EVENTOS_ESPECIALES = {
    1: {  # Día 1
        "bonus_lugares": ["Palacio Real de Madrid", "Museo Nacional del Prado"],
        "bonus_multiplicador": 1.5,  # 50% más puntos
        "restricciones": []
    },
    2: {  # Día 2
        "bonus_lugares": ["Gran Vía", "Puerta del Sol", "Plaza Mayor de Madrid"],
        "bonus_multiplicador": 1.3,
        "restricciones": []
    },
    3: {  # Día 3
        "bonus_lugares": ["Parque de El Retiro", "Templo de Debod"],
        "bonus_multiplicador": 1.4,
        "restricciones": ["El Rastro de Madrid"]  # Solo domingos, supongamos día 3 no es domingo
    },
    4: {  # Día 4
        "bonus_lugares": ["Estadio Santiago Bernabéu", "Casa de Campo"],
        "bonus_multiplicador": 1.3,
        "restricciones": []
    },
    5: {  # Día 5
        "bonus_lugares": ["Barrio de La Latina", "Mercado de San Miguel", "El Rastro de Madrid"],
        "bonus_multiplicador": 1.5,
        "restricciones": []
    },
}

# =============================================================================
# 4. COSTOS DE LUGARES (PRESUPUESTO LIMITADO)
# =============================================================================
# Presupuesto máximo por día: 150 euros

COSTOS_LUGARES = {
    # Museos premium
    "Museo Nacional del Prado": 15,
    "Museo Nacional Centro de Arte Reina Sofía": 12,
    "Museo Nacional Thyssen-Bornemisza": 13,
    "Palacio Real de Madrid": 18,
    
    # Museos económicos
    "Museo Arqueológico Nacional de España": 8,
    "Museo Sorolla": 6,
    "Museo del Robot": 12,
    "Museo geominero": 0,  # Gratis
    
    # Restaurantes caros
    "DiverXO": 250,  # Menú degustación
    "Amazónico": 80,
    "StreetXO": 70,
    "Casa Botín": 60,
    "Sala de Despiece": 50,
    "Ten con Ten": 65,
    
    # Restaurantes medios
    "Casa Lucio": 45,
    "La Bola Taberna": 35,
    "Yakitoro": 40,
    "Mercado de San Miguel": 30,
    "Running sushi in Akihabara": 35,
    "Secretos de Lola": 35,
    "Inclán brutal bar": 40,
    
    # Restaurantes económicos
    "Filippo Pizza": 20,
    "Le Petit Dinsum": 25,
    "El Tigre Sidrería": 15,
    "Juana La Loca": 25,
    "Chocolateria San Gines": 10,
    
    # Atracciones con entrada
    "Estadio Santiago Bernabéu": 25,
    "Faro de Moncloa": 4,
    "Teatro Real": 30,
    "Sweet Space": 18,
    
    # Tiendas (costo estimado de compras)
    "El Corte Inglés (Preciados)": 40,
    "Primark Gran Vía": 25,
    "Zara (Plaza de España)": 30,
    "Fnac Callao": 20,
    
    # Gratis o muy barato
    "Puerta del Sol": 0,
    "Plaza Mayor de Madrid": 0,
    "Plaza de Cibeles": 0,
    "Plaza de España": 0,
    "Gran Vía": 0,
    "Parque de El Retiro": 0,
    "Templo de Debod": 0,
    "Real Jardín Botánico de Madrid": 6,
}

PRESUPUESTO_DIARIO = 150  # euros

# =============================================================================
# 5. TIPOS DE TRANSPORTE
# =============================================================================
# Diferentes medios de transporte afectan tiempo y costo

TIPOS_TRANSPORTE = {
    "andando": {
        "velocidad_km_h": 4,  # 4 km/h
        "costo_por_km": 0,
        "max_distancia": 2,  # Solo para distancias < 2km
    },
    "metro": {
        "velocidad_km_h": 20,  # Considerando esperas
        "costo_por_km": 0.5,  # Aproximado
        "max_distancia": float('inf'),
    },
    "taxi": {
        "velocidad_km_h": 25,
        "costo_por_km": 1.5,
        "max_distancia": float('inf'),
    },
    "bus": {
        "velocidad_km_h": 15,
        "costo_por_km": 0.4,
        "max_distancia": float('inf'),
    },
}

# =============================================================================
# 6. FACTOR DE FATIGA
# =============================================================================
# Los puntos de los lugares disminuyen conforme avanza el día

def calcular_factor_fatiga(hora_actual: int) -> float:
    """
    Calcula el factor de fatiga basado en la hora del día.
    
    Args:
        hora_actual: Hora en minutos desde las 00:00
        
    Returns:
        Factor multiplicador (1.0 = sin fatiga, <1.0 = con fatiga)
    """
    # 9:00 AM (540 min) = factor 1.0 (energía máxima)
    # 14:00 PM (840 min) = factor 0.9 (ligera fatiga)
    # 18:00 PM (1080 min) = factor 0.7 (fatiga moderada)
    # 22:00 PM (1320 min) = factor 0.5 (muy cansado)
    
    hora_inicio = 9 * 60  # 9:00 AM
    hora_fin = 23 * 60    # 11:00 PM
    
    if hora_actual < hora_inicio:
        return 1.0
    
    progreso = (hora_actual - hora_inicio) / (hora_fin - hora_inicio)
    factor = 1.0 - (progreso * 0.5)  # Disminuye hasta 0.5
    
    return max(0.5, factor)

# =============================================================================
# 7. PREFERENCIAS DE USUARIO (PERFILES)
# =============================================================================

PERFILES_USUARIO = {
    "cultural": {
        "tipos_favoritos": ["museo", "palacio", "catedral", "teatro"],
        "multiplicador": 1.5,
    },
    "gastronomico": {
        "tipos_favoritos": ["restaurante", "mercado", "bar"],
        "multiplicador": 1.4,
    },
    "naturaleza": {
        "tipos_favoritos": ["parque", "jardin", "mirador"],
        "multiplicador": 1.6,
    },
    "shopping": {
        "tipos_favoritos": ["tienda", "calle_comercial", "centro_comercial"],
        "multiplicador": 1.5,
    },
    "balanceado": {
        "tipos_favoritos": [],
        "multiplicador": 1.0,
    },
}

# =============================================================================
# 8. CLIMA Y CONDICIONES
# =============================================================================

CONDICIONES_CLIMATICAS = {
    "soleado": {
        "bonus_tipos": ["parque", "jardin", "plaza", "mirador"],
        "penalizacion_tipos": [],
        "multiplicador_bonus": 1.3,
        "multiplicador_penalizacion": 1.0,
    },
    "lluvioso": {
        "bonus_tipos": ["museo", "tienda", "restaurante", "centro_comercial"],
        "penalizacion_tipos": ["parque", "jardin", "plaza"],
        "multiplicador_bonus": 1.2,
        "multiplicador_penalizacion": 0.6,
    },
    "nublado": {
        "bonus_tipos": [],
        "penalizacion_tipos": [],
        "multiplicador_bonus": 1.0,
        "multiplicador_penalizacion": 1.0,
    },
}

# Asignar clima aleatorio a cada día (se puede personalizar)
def generar_clima_dias(num_dias: int) -> Dict[int, str]:
    """Genera condiciones climáticas aleatorias para cada día"""
    climas = ["soleado", "lluvioso", "nublado"]
    return {dia: random.choice(climas) for dia in range(1, num_dias + 1)}

# =============================================================================
# 9. CATEGORÍAS DE LUGARES
# =============================================================================
# Clasificación más detallada para aplicar restricciones

CATEGORIAS = {
    "Museo Nacional del Prado": ["museo", "cultura", "arte", "interior"],
    "Museo Nacional Centro de Arte Reina Sofía": ["museo", "cultura", "arte", "interior"],
    "Museo Nacional Thyssen-Bornemisza": ["museo", "cultura", "arte", "interior"],
    "Palacio Real de Madrid": ["palacio", "cultura", "historia", "interior"],
    "Parque de El Retiro": ["parque", "naturaleza", "exterior"],
    "Gran Vía": ["calle", "compras", "exterior"],
    "DiverXO": ["restaurante", "lujo", "gastronómico", "interior"],
    "Casa Botín": ["restaurante", "tradicional", "gastronómico", "interior"],
    "Estadio Santiago Bernabéu": ["deportivo", "cultura", "interior"],
    "Templo de Debod": ["monumento", "cultura", "exterior"],
    # ... (se pueden añadir más)
}

# =============================================================================
# FUNCIONES DE VALIDACIÓN Y CÁLCULO
# =============================================================================

def validar_incompatibilidades(ruta: List[int], lugares_turisticos: List[Dict]) -> Tuple[bool, float]:
    """
    Verifica si hay lugares incompatibles en la ruta.
    
    Returns:
        (es_valida, penalizacion)
    """
    nombres_ruta = [lugares_turisticos[i]["nombre"] for i in ruta]
    penalizacion = 0
    
    for categoria, incompatibilidades in INCOMPATIBILIDADES.items():
        for par_incompatible in incompatibilidades:
            if par_incompatible[0] in nombres_ruta and par_incompatible[1] in nombres_ruta:
                penalizacion += 500  # Penalización fuerte
    
    return penalizacion == 0, penalizacion


def calcular_bonus_sinergia(ruta: List[int], lugares_turisticos: List[Dict]) -> float:
    """
    Calcula bonus por visitar grupos de lugares relacionados.
    
    Returns:
        bonus_total en puntos
    """
    nombres_ruta = [lugares_turisticos[i]["nombre"] for i in ruta]
    bonus_total = 0
    
    for nombre_grupo, info_grupo in GRUPOS_SINERGICOS.items():
        lugares_grupo = info_grupo["lugares"]
        lugares_visitados = [l for l in lugares_grupo if l in nombres_ruta]
        
        if len(lugares_visitados) >= info_grupo["min_lugares"]:
            # Bonus progresivo: más lugares = más bonus
            multiplicador = len(lugares_visitados) / len(lugares_grupo)
            bonus = info_grupo["bonus_puntos"] * multiplicador
            bonus_total += bonus
    
    return bonus_total


def calcular_bonus_eventos(ruta: List[int], lugares_turisticos: List[Dict], dia: int) -> float:
    """
    Calcula bonus por eventos especiales del día.
    
    Returns:
        bonus_total en puntos
    """
    if dia not in EVENTOS_ESPECIALES:
        return 0
    
    eventos = EVENTOS_ESPECIALES[dia]
    nombres_ruta = [lugares_turisticos[i]["nombre"] for i in ruta]
    bonus_total = 0
    
    for nombre in nombres_ruta:
        if nombre in eventos["bonus_lugares"]:
            lugar = next(l for l in lugares_turisticos if l["nombre"] == nombre)
            bonus = lugar["puntos"] * (eventos["bonus_multiplicador"] - 1)
            bonus_total += bonus
    
    return bonus_total


def validar_presupuesto(ruta: List[int], lugares_turisticos: List[Dict]) -> Tuple[bool, float, float]:
    """
    Verifica si la ruta cumple con el presupuesto diario.
    
    Returns:
        (dentro_presupuesto, costo_total, penalizacion)
    """
    costo_total = 0
    
    for idx in ruta:
        nombre = lugares_turisticos[idx]["nombre"]
        costo_total += COSTOS_LUGARES.get(nombre, 0)
    
    if costo_total > PRESUPUESTO_DIARIO:
        exceso = costo_total - PRESUPUESTO_DIARIO
        penalizacion = exceso * 5  # 5 puntos por cada euro de exceso
        return False, costo_total, penalizacion
    
    return True, costo_total, 0


def calcular_costo_transporte(distancia_km: float, priorizar_economia: bool = False) -> Tuple[str, float, float]:
    """
    Elige el mejor tipo de transporte según la distancia.
    
    Returns:
        (tipo_transporte, tiempo_minutos, costo_euros)
    """
    # Elegir transporte según distancia
    if distancia_km < TIPOS_TRANSPORTE["andando"]["max_distancia"]:
        tipo = "andando"
    elif distancia_km < 5:
        tipo = "metro" if priorizar_economia else "taxi"
    else:
        tipo = "metro" if priorizar_economia else "taxi"
    
    info = TIPOS_TRANSPORTE[tipo]
    tiempo_horas = distancia_km / info["velocidad_km_h"]
    tiempo_minutos = tiempo_horas * 60
    costo = distancia_km * info["costo_por_km"]
    
    return tipo, tiempo_minutos, costo


def aplicar_perfil_usuario(puntos_base: float, tipo_lugar: str, perfil: str = "balanceado") -> float:
    """
    Ajusta los puntos según el perfil del usuario.
    
    Returns:
        puntos_ajustados
    """
    if perfil not in PERFILES_USUARIO:
        return puntos_base
    
    info_perfil = PERFILES_USUARIO[perfil]
    
    if tipo_lugar in info_perfil["tipos_favoritos"]:
        return puntos_base * info_perfil["multiplicador"]
    
    return puntos_base


def aplicar_condiciones_climaticas(puntos_base: float, tipo_lugar: str, clima: str) -> float:
    """
    Ajusta los puntos según las condiciones climáticas.
    
    Returns:
        puntos_ajustados
    """
    if clima not in CONDICIONES_CLIMATICAS:
        return puntos_base
    
    condiciones = CONDICIONES_CLIMATICAS[clima]
    
    if tipo_lugar in condiciones["bonus_tipos"]:
        return puntos_base * condiciones["multiplicador_bonus"]
    elif tipo_lugar in condiciones["penalizacion_tipos"]:
        return puntos_base * condiciones["multiplicador_penalizacion"]
    
    return puntos_base


# =============================================================================
# ESTADÍSTICAS DEL PROBLEMA
# =============================================================================

def calcular_complejidad(num_lugares: int, num_dias: int) -> Dict:
    """
    Calcula métricas de complejidad del problema.
    """
    # Combinaciones posibles por día (sin considerar orden)
    from math import factorial, comb
    
    lugares_por_dia_promedio = 8
    
    # Combinaciones simples (sin restricciones)
    combinaciones_por_dia = comb(num_lugares, lugares_por_dia_promedio) if num_lugares >= lugares_por_dia_promedio else factorial(num_lugares)
    
    # Permutaciones (considerando orden)
    permutaciones_por_dia = factorial(lugares_por_dia_promedio) * combinaciones_por_dia
    
    # Espacio de búsqueda total (aproximado)
    espacio_busqueda_total = permutaciones_por_dia ** num_dias
    
    # Con restricciones (reducción estimada del 60-80%)
    factor_reduccion = 0.3  # 70% de soluciones inválidas
    espacio_busqueda_valido = espacio_busqueda_total * factor_reduccion
    
    return {
        "num_lugares_total": num_lugares,
        "num_dias": num_dias,
        "lugares_por_dia_promedio": lugares_por_dia_promedio,
        "combinaciones_por_dia": combinaciones_por_dia,
        "permutaciones_por_dia": permutaciones_por_dia,
        "espacio_busqueda_total": espacio_busqueda_total,
        "espacio_busqueda_valido": espacio_busqueda_valido,
        "restricciones": {
            "incompatibilidades": sum(len(v) for v in INCOMPATIBILIDADES.values()),
            "grupos_sinergicos": len(GRUPOS_SINERGICOS),
            "eventos_especiales": len(EVENTOS_ESPECIALES),
            "presupuesto": PRESUPUESTO_DIARIO,
            "tipos_transporte": len(TIPOS_TRANSPORTE),
            "perfiles_usuario": len(PERFILES_USUARIO),
            "condiciones_climaticas": len(CONDICIONES_CLIMATICAS),
        }
    }


if __name__ == "__main__":
    # Prueba de complejidad
    complejidad = calcular_complejidad(100, 5)
    
    print("\n" + "="*70)
    print("📊 ANÁLISIS DE COMPLEJIDAD DEL PROBLEMA")
    print("="*70)
    print(f"Lugares totales: {complejidad['num_lugares_total']}")
    print(f"Días de viaje: {complejidad['num_dias']}")
    print(f"Lugares por día (promedio): {complejidad['lugares_por_dia_promedio']}")
    print(f"\nCombinaciones por día: {complejidad['combinaciones_por_dia']:,.0f}")
    print(f"Permutaciones por día: {complejidad['permutaciones_por_dia']:,.0e}")
    print(f"\nEspacio de búsqueda total: {complejidad['espacio_busqueda_total']:.2e}")
    print(f"Espacio de búsqueda válido: {complejidad['espacio_busqueda_valido']:.2e}")
    
    print(f"\n🔒 RESTRICCIONES ACTIVAS:")
    for nombre, valor in complejidad['restricciones'].items():
        print(f"   - {nombre.replace('_', ' ').title()}: {valor}")
    
    print("\n" + "="*70)
