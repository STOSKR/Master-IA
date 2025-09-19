import random
import math
from typing import List, Tuple

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
    {"nombre": "Museo Reina Sofía", "x": 40.4087, "y": -3.6947, "puntos": 92, "tiempo_visita": 110},
    {"nombre": "Zoo Aquarium de Madrid", "x": 40.4017, "y": -3.7611, "puntos": 85, "tiempo_visita": 150}
]

tiempo_maximo_dia = 12 * 60  # 12 horas en minutos

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
    # Redondea un tiempo dado a la franja de 15 minutos más cercana hacia arriba.
    return math.ceil(tiempo / 15) * 15

def evaluar_ruta_multiobjetivo(ruta: List[int], tiempo_max: int = tiempo_maximo_dia, w_puntos: float = 1.0, w_distancia: float = 1.0) -> dict:
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

    # Calcular distancia total y tiempo de traslado
    for i in range(len(ruta) - 1):
        lugar_actual = lugares_turisticos[ruta[i]]
        lugar_siguiente = lugares_turisticos[ruta[i + 1]]
        distancia = distancia_haversine(lugar_actual, lugar_siguiente)
        distancia_total += distancia

        # Convertir distancia a tiempo de traslado (en minutos)
        tiempo_traslado = distancia * 20  # 20 minutos por kilómetro
        tiempo_traslado_redondeado = redondear_a_franja_15(tiempo_traslado)
        tiempo_total += tiempo_traslado_redondeado

    # Verificar si la ruta es válida (dentro del tiempo máximo)
    valida = tiempo_total <= tiempo_max

    # Calcular fitness: maximizar puntos, minimizar distancia
    if valida:
        fitness = (w_puntos * puntos_total) - (w_distancia * distancia_total)
    else:
        fitness = 0  # Ruta inválida

    return {
        "puntos": puntos_total,
        "distancia": round(distancia_total, 2),
        "tiempo": round(tiempo_total, 2),
        "fitness": round(fitness, 2),
        "valida": valida
    }

def crear_ruta_aleatoria(max_lugares: int = len(lugares_turisticos)) -> List[int]:
    """Crea una ruta aleatoria seleccionando lugares al azar."""
    num_lugares = random.randint(2, max_lugares)
    return random.sample(range(len(lugares_turisticos)), num_lugares)

def imprimir_ruta(ruta: List[int], evaluacion: dict):
    """Imprime los detalles de una ruta"""
    print("\n" + "="*50)
    print("RUTA:")
    for i, lugar_idx in enumerate(ruta):
        lugar = lugares_turisticos[lugar_idx]
        print(f"{i+1}. {lugar['nombre']} (Puntos: {lugar['puntos']}, Tiempo: {lugar['tiempo_visita']}min)")
    
    print(f"\nRESULTADOS:")
    print(f"Puntos totales: {evaluacion['puntos']}")
    print(f"Distancia total: {evaluacion['distancia']}")
    print(f"Tiempo total: {evaluacion['tiempo']} minutos")
    print(f"Válida: {'Sí' if evaluacion['valida'] else 'No'}")
    print(f"Fitness: {evaluacion['fitness']}")
    
"""
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

# Ejemplo de uso básico
if __name__ == "__main__":
    print("OPTIMIZACIÓN DE RUTAS TURÍSTICAS - MULTIOBJETIVO")
    print("="*60)
    
    print("\nLugares disponibles:")
    for i, lugar in enumerate(lugares_turisticos):
        print(f"{i}. {lugar['nombre']} - Puntos: {lugar['puntos']}, Tiempo: {lugar['tiempo_visita']}min, Posición: ({lugar['x']}, {lugar['y']})")
    
    print("\n" + "="*60)
    print("PROBANDO RUTAS ALEATORIAS CON ENFOQUE MULTIOBJETIVO:")
    
    mejor_fitness = -999999
    mejor_ruta = []
    mejor_evaluacion = {}
    
    for i in range(5):
        ruta = crear_ruta_aleatoria()
        evaluacion = evaluar_ruta_multiobjetivo(ruta, w_puntos=1.0, w_distancia=0.5)
        
        print(f"\n--- RUTA {i+1} ---")
        imprimir_ruta(ruta, evaluacion)
        
        # Guardar la mejor ruta
        if evaluacion["fitness"] > mejor_fitness:
            mejor_fitness = evaluacion["fitness"]
            mejor_ruta = ruta
            mejor_evaluacion = evaluacion
    
    print("\n" + "="*60)
    print("MEJOR RUTA ENCONTRADA (MULTIOBJETIVO):")
    imprimir_ruta(mejor_ruta, mejor_evaluacion)