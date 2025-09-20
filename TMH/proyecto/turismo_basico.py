import random
from typing import List
from utils import lugares_turisticos, distancia_haversine, redondear_a_franja_15

tiempo_maximo_dia = 12 * 60  # 12 horas en minutos

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

def crear_ruta_aleatoria(tiempo: int = tiempo_maximo_dia, max_lugares: int = len(lugares_turisticos)) -> List[int]:
    max_lugares_dinamico = min(max_lugares, tiempo // 90)
    num_lugares = random.randint(2, max_lugares_dinamico)
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