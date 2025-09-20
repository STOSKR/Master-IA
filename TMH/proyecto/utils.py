import math
import random

lugares_turisticos = [
    {"nombre": "Museo del Prado", "x": 40.4138, "y": -3.6921, "puntos": 95, "tiempo_visita": 120},
    {"nombre": "Palacio Real", "x": 40.4179, "y": -3.7143, "puntos": 90, "tiempo_visita": 90},
    {"nombre": "Plaza Mayor", "x": 40.4155, "y": -3.7074, "puntos": 85, "tiempo_visita": 45},
    {"nombre": "Puerta del Sol", "x": 40.4169, "y": -3.7038, "puntos": 80, "tiempo_visita": 30},
    {"nombre": "Parque del Retiro", "x": 40.4153, "y": -3.6846, "puntos": 88, "tiempo_visita": 60},
    {"nombre": "Gran Vía", "x": 40.4203, "y": -3.7058, "puntos": 75, "tiempo_visita": 45},
    {"nombre": "Templo de Debod", "x": 40.4240, "y": -3.7170, "puntos": 70, "tiempo_visita": 40},
    {"nombre": "Catedral de la Almudena", "x": 40.4153, "y": -3.7145, "puntos": 85, "tiempo_visita": 50},
    {"nombre": "Mercado de San Miguel", "x": 40.4154, "y": -3.7089, "puntos": 80, "tiempo_visita": 35},
    {"nombre": "Estadio Santiago Bernabéu", "x": 40.4531, "y": -3.6883, "puntos": 90, "tiempo_visita": 120},
    {"nombre": "Museo Reina Sofía", "x": 40.4087, "y": -3.6947, "puntos": 92, "tiempo_visita": 110}
]

def distancia_haversine(lugar1: dict, lugar2: dict) -> float:
    
    R = 6371.0

    # Convertir latitudes y longitudes de grados a radianes
    lat1, lon1 = math.radians(lugar1["x"]), math.radians(lugar1["y"])
    lat2, lon2 = math.radians(lugar2["x"]), math.radians(lugar2["y"])

    # Diferencias de latitud y longitud
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # Fórmula de Haversine
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c

    return distancia

def redondear_a_franja_15(tiempo: float) -> int:
    return math.ceil(tiempo / 15) * 15

"""
def crear_ruta_aleatoria(max_lugares: int = len(lugares_turisticos)) -> List[int]:
    num_lugares = random.randint(2, max_lugares)
    return random.sample(range(len(lugares_turisticos)), num_lugares)

def evaluar_ruta(ruta: List[int], tiempo_max: int = tiempo_maximo_dia) -> dict:
    if len(ruta) == 0:
        return {"puntos": 0, "distancia": 0, "tiempo": 0, "fitness": 0, "valida": False}
    
    puntos_total = 0
    distancia_total = 0
    tiempo_total = 0
    
    # Calcular puntos y tiempo de visita
    for i in ruta:
        lugar = lugares_turisticos[i]
        puntos_total += lugar["puntos"]
        tiempo_total += lugar["tiempo_visita"]
    
    # Calcular distancia total del recorrido
    for i in range(len(ruta) - 1):
        lugar_actual = lugares_turisticos[ruta[i]]
        lugar_siguiente = lugares_turisticos[ruta[i + 1]]
        distancia_total += distancia_entre_puntos(lugar_actual, lugar_siguiente)
    
    # Agregar tiempo de viaje (asumiendo velocidad constante)
    tiempo_viaje = distancia_total * 20  # 20 minutos por unidad de distancia
    tiempo_total += tiempo_viaje
    
    # Verificar si la ruta es válida (dentro del tiempo máximo)
    valida = tiempo_total <= tiempo_max
    
    # Calcular fitness: maximizar puntos, minimizar distancia
    if valida:
        fitness = puntos_total - (distancia_total * 10)  # Penalizar distancia
    else:
        fitness = 0  # Ruta inválida
    
    return {
        "puntos": puntos_total,
        "distancia": round(distancia_total, 2),
        "tiempo": round(tiempo_total, 2),
        "fitness": round(fitness, 2),
        "valida": valida
    }
"""
