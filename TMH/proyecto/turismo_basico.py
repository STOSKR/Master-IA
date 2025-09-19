import random
import math
from typing import List, Tuple

# Datos básicos: lugares turísticos con coordenadas reales y puntos ajustados
lugares_turisticos = [
    {"nombre": "Museo del Prado", "x": 40.4138, "y": -3.6921, "puntos": 95, "tiempo_visita": 120},
    {"nombre": "Palacio Real", "x": 40.4179, "y": -3.7143, "puntos": 90, "tiempo_visita": 90},
    {"nombre": "Plaza Mayor", "x": 40.4155, "y": -3.7074, "puntos": 85, "tiempo_visita": 45},
    {"nombre": "Puerta del Sol", "x": 40.4169, "y": -3.7038, "puntos": 80, "tiempo_visita": 30},
    {"nombre": "Parque del Retiro", "x": 40.4153, "y": -3.6846, "puntos": 88, "tiempo_visita": 60},
    {"nombre": "Gran Vía", "x": 40.4203, "y": -3.7058, "puntos": 75, "tiempo_visita": 45}
]

def distancia_entre_puntos(lugar1: dict, lugar2: dict) -> float:
    return math.sqrt((lugar1["x"] - lugar2["x"])**2 + (lugar1["y"] - lugar2["y"])**2)

def redondear_a_franja_15(tiempo: float) -> int:
    # Redondea un tiempo dado a la franja de 15 minutos más cercana hacia arriba.
    return math.ceil(tiempo / 15) * 15

def evaluar_ruta(ruta: List[int], tiempo_max: int = 400) -> dict:
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

def evaluar_ruta_multiobjetivo(ruta: List[int], tiempo_max: int = 12 * 60, w_puntos: float = 1.0, w_distancia: float = 1.0) -> dict:
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
        distancia = distancia_entre_puntos(lugar_actual, lugar_siguiente)
        distancia_total += distancia

        # Convertir distancia a tiempo de traslado (en minutos)
        tiempo_traslado = distancia * 50 * 30  # Factor de conversión: 1 unidad de distancia ≈ 30 minutos
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