# Enfriamiento Simulado (Simulated Annealing) para Optimización de Rutas Turísticas

from turismo_basico import lugares_turisticos, evaluar_ruta, imprimir_ruta, crear_ruta_aleatoria
import random
import math
from typing import List

def generar_vecino(ruta: List[int]) -> List[int]:
    """
    Genera una ruta vecina aplicando una pequeña modificación
    """
    vecino = ruta.copy()
    
    if len(vecino) == 0:
        return crear_ruta_aleatoria(3)
    
    # Tipos de modificaciones posibles
    modificaciones = ['intercambiar', 'agregar', 'quitar', 'reemplazar']
    modificacion = random.choice(modificaciones)
    
    if modificacion == 'intercambiar' and len(vecino) >= 2:
        # Intercambiar dos lugares de posición
        i, j = random.sample(range(len(vecino)), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
    
    elif modificacion == 'agregar' and len(vecino) < 4:
        # Agregar un nuevo lugar
        lugares_disponibles = [i for i in range(len(lugares_turisticos)) if i not in vecino]
        if lugares_disponibles:
            nuevo_lugar = random.choice(lugares_disponibles)
            posicion = random.randint(0, len(vecino))
            vecino.insert(posicion, nuevo_lugar)
    
    elif modificacion == 'quitar' and len(vecino) > 2:
        # Quitar un lugar
        idx = random.randint(0, len(vecino) - 1)
        vecino.pop(idx)
    
    elif modificacion == 'reemplazar' and len(vecino) > 0:
        # Reemplazar un lugar por otro
        idx = random.randint(0, len(vecino) - 1)
        lugares_disponibles = [i for i in range(len(lugares_turisticos)) if i not in vecino]
        if lugares_disponibles:
            vecino[idx] = random.choice(lugares_disponibles)
    
    return vecino

def probabilidad_aceptacion(fitness_actual: float, fitness_vecino: float, temperatura: float) -> float:
    """
    Calcula la probabilidad de aceptar una solución peor
    """
    if fitness_vecino > fitness_actual:
        return 1.0  # Siempre acepta mejores soluciones
    
    if temperatura <= 0:
        return 0.0
    
    # Fórmula de Boltzmann
    try:
        return math.exp((fitness_vecino - fitness_actual) / temperatura)
    except OverflowError:
        return 0.0

def enfriamiento_simulado(temperatura_inicial: float = 1000.0, 
                         temperatura_final: float = 0.1,
                         factor_enfriamiento: float = 0.95,
                         iteraciones_por_temp: int = 10) -> dict:
    """
    Ejecuta el algoritmo de enfriamiento simulado
    """
    print(f"\n🌡️ ENFRIAMIENTO SIMULADO")
    print(f"Temp. inicial: {temperatura_inicial}, Temp. final: {temperatura_final}")
    print(f"Factor enfriamiento: {factor_enfriamiento}, Iter. por temp: {iteraciones_por_temp}")
    print("="*50)
    
    # 1. Solución inicial aleatoria
    solucion_actual = crear_ruta_aleatoria(4)
    evaluacion_actual = evaluar_ruta(solucion_actual)
    fitness_actual = evaluacion_actual["fitness"]
    
    # Mejor solución encontrada
    mejor_solucion = solucion_actual.copy()
    mejor_evaluacion = evaluacion_actual.copy()
    mejor_fitness = fitness_actual
    
    # Historial
    historial_fitness = []
    historial_temperatura = []
    aceptadas = 0
    rechazadas = 0
    
    temperatura = temperatura_inicial
    iteracion_global = 0
    
    print(f"Solución inicial: Fitness = {fitness_actual:.2f}")
    
    # 2. Proceso de enfriamiento
    while temperatura > temperatura_final:
        
        for _ in range(iteraciones_por_temp):
            iteracion_global += 1
            
            # Generar vecino
            vecino = generar_vecino(solucion_actual)
            evaluacion_vecino = evaluar_ruta(vecino)
            fitness_vecino = evaluacion_vecino["fitness"]
            
            # Calcular probabilidad de aceptación
            prob_aceptacion = probabilidad_aceptacion(fitness_actual, fitness_vecino, temperatura)
            
            # Decidir si aceptar
            if random.random() < prob_aceptacion:
                solucion_actual = vecino
                evaluacion_actual = evaluacion_vecino
                fitness_actual = fitness_vecino
                aceptadas += 1
                
                # Actualizar mejor solución si es necesario
                if fitness_actual > mejor_fitness:
                    mejor_solucion = solucion_actual.copy()
                    mejor_evaluacion = evaluacion_actual.copy()
                    mejor_fitness = fitness_actual
            else:
                rechazadas += 1
            
            # Guardar historial
            historial_fitness.append(mejor_fitness)
            historial_temperatura.append(temperatura)
        
        # Mostrar progreso
        if iteracion_global % 50 == 0:
            print(f"Iter {iteracion_global:3d}: Temp = {temperatura:6.1f}, "
                  f"Fitness actual = {fitness_actual:7.2f}, "
                  f"Mejor = {mejor_fitness:7.2f}")
        
        # Enfriar
        temperatura *= factor_enfriamiento
    
    print(f"\nResultados finales:")
    print(f"Iteraciones totales: {iteracion_global}")
    print(f"Soluciones aceptadas: {aceptadas}")
    print(f"Soluciones rechazadas: {rechazadas}")
    print(f"Tasa de aceptación: {aceptadas/(aceptadas+rechazadas)*100:.1f}%")
    
    return {
        "mejor_ruta": mejor_solucion,
        "evaluacion": mejor_evaluacion,
        "historial_fitness": historial_fitness,
        "historial_temperatura": historial_temperatura,
        "iteraciones": iteracion_global,
        "tasa_aceptacion": aceptadas/(aceptadas+rechazadas)*100,
        "algoritmo": "Enfriamiento Simulado"
    }

# Ejemplo de uso
if __name__ == "__main__":
    print("OPTIMIZACIÓN CON ENFRIAMIENTO SIMULADO")
    print("="*60)
    
    # Ejecutar enfriamiento simulado
    resultado = enfriamiento_simulado(
        temperatura_inicial=1000.0,
        temperatura_final=0.1,
        factor_enfriamiento=0.95,
        iteraciones_por_temp=15
    )
    
    print(f"\n🏆 MEJOR SOLUCIÓN ENCONTRADA:")
    imprimir_ruta(resultado["mejor_ruta"], resultado["evaluacion"])
    
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"Iteraciones: {resultado['iteraciones']}")
    print(f"Tasa de aceptación: {resultado['tasa_aceptacion']:.1f}%")
    
    # Mostrar evolución del fitness (cada 20 iteraciones)
    print(f"\n📈 EVOLUCIÓN DEL MEJOR FITNESS:")
    historial = resultado["historial_fitness"]
    for i in range(0, len(historial), 20):
        print(f"Iteración {i:3d}: {historial[i]:7.2f}")