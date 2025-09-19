# Algoritmo Genético Simple para Optimización de Rutas Turísticas

from turismo_basico import lugares_turisticos, evaluar_ruta, imprimir_ruta, distancia_entre_puntos
import random
from typing import List, Tuple

def crear_poblacion_inicial(tamaño_poblacion: int, max_lugares: int = 4) -> List[List[int]]:
    """Crea una población inicial de rutas aleatorias"""
    poblacion = []
    for _ in range(tamaño_poblacion):
        # Crear ruta aleatoria
        num_lugares = random.randint(2, min(max_lugares, len(lugares_turisticos)))
        ruta = random.sample(range(len(lugares_turisticos)), num_lugares)
        poblacion.append(ruta)
    return poblacion

def seleccion_torneo(poblacion: List[List[int]], fitness_scores: List[float], k: int = 3) -> List[int]:
    """Selecciona un individuo usando torneo de k individuos"""
    # Seleccionar k individuos aleatorios
    candidatos = random.sample(list(zip(poblacion, fitness_scores)), k)
    # Retornar el mejor (mayor fitness)
    mejor = max(candidatos, key=lambda x: x[1])
    return mejor[0].copy()

def cruce_simple(padre1: List[int], padre2: List[int]) -> Tuple[List[int], List[int]]:
    """
    Cruce simple: toma lugares del padre1 y algunos del padre2
    Evita duplicados manteniendo orden
    """
    # Tomar lugares únicos de ambos padres
    lugares_combinados = list(set(padre1 + padre2))
    
    # Crear dos hijos con longitudes aleatorias
    max_len = min(len(lugares_combinados), 4)  # máximo 4 lugares
    len_hijo1 = random.randint(2, max_len)
    len_hijo2 = random.randint(2, max_len)
    
    # Mezclar y seleccionar
    random.shuffle(lugares_combinados)
    hijo1 = lugares_combinados[:len_hijo1]
    hijo2 = lugares_combinados[:len_hijo2]
    
    return hijo1, hijo2

def mutacion(ruta: List[int], prob_mutacion: float = 0.1) -> List[int]:
    """
    Mutación simple: puede cambiar un lugar, agregar uno o quitar uno
    """
    ruta_mutada = ruta.copy()
    
    if random.random() < prob_mutacion:
        tipo_mutacion = random.choice(['cambiar', 'agregar', 'quitar'])
        
        if tipo_mutacion == 'cambiar' and len(ruta_mutada) > 0:
            # Cambiar un lugar por otro
            idx = random.randint(0, len(ruta_mutada) - 1)
            nuevo_lugar = random.randint(0, len(lugares_turisticos) - 1)
            if nuevo_lugar not in ruta_mutada:
                ruta_mutada[idx] = nuevo_lugar
        
        elif tipo_mutacion == 'agregar' and len(ruta_mutada) < 4:
            # Agregar un nuevo lugar
            lugares_disponibles = [i for i in range(len(lugares_turisticos)) if i not in ruta_mutada]
            if lugares_disponibles:
                ruta_mutada.append(random.choice(lugares_disponibles))
        
        elif tipo_mutacion == 'quitar' and len(ruta_mutada) > 2:
            # Quitar un lugar
            idx = random.randint(0, len(ruta_mutada) - 1)
            ruta_mutada.pop(idx)
    
    return ruta_mutada

def algoritmo_genetico_simple(generaciones: int = 20, tamaño_poblacion: int = 10, 
                             prob_cruce: float = 0.8, prob_mutacion: float = 0.1) -> dict:
    """
    Ejecuta el algoritmo genético simple
    """
    print(f"\n🧬 ALGORITMO GENÉTICO")
    print(f"Generaciones: {generaciones}, Población: {tamaño_poblacion}")
    print(f"Prob. cruce: {prob_cruce}, Prob. mutación: {prob_mutacion}")
    print("="*50)
    
    # 1. Crear población inicial
    poblacion = crear_poblacion_inicial(tamaño_poblacion)
    mejor_fitness_historico = -999999
    mejor_ruta_historica = []
    historial_fitness = []
    
    for generacion in range(generaciones):
        # 2. Evaluar población
        fitness_scores = []
        for ruta in poblacion:
            evaluacion = evaluar_ruta(ruta)
            fitness_scores.append(evaluacion["fitness"])
        
        # 3. Encontrar el mejor de esta generación
        mejor_idx = fitness_scores.index(max(fitness_scores))
        mejor_ruta_gen = poblacion[mejor_idx]
        mejor_fitness_gen = fitness_scores[mejor_idx]
        
        # 4. Actualizar el mejor histórico
        if mejor_fitness_gen > mejor_fitness_historico:
            mejor_fitness_historico = mejor_fitness_gen
            mejor_ruta_historica = mejor_ruta_gen.copy()
        
        # 5. Guardar para histórico
        historial_fitness.append(mejor_fitness_gen)
        
        # 6. Mostrar progreso cada 5 generaciones
        if generacion % 5 == 0 or generacion == generaciones - 1:
            print(f"Gen {generacion:2d}: Mejor fitness = {mejor_fitness_gen:7.2f}, "
                  f"Promedio = {sum(fitness_scores)/len(fitness_scores):7.2f}")
        
        # 7. Crear nueva población
        nueva_poblacion = []
        
        # Mantener el mejor (elitismo)
        nueva_poblacion.append(mejor_ruta_gen.copy())
        
        # Generar el resto
        while len(nueva_poblacion) < tamaño_poblacion:
            # Selección
            padre1 = seleccion_torneo(poblacion, fitness_scores)
            padre2 = seleccion_torneo(poblacion, fitness_scores)
            
            # Cruce
            if random.random() < prob_cruce:
                hijo1, hijo2 = cruce_simple(padre1, padre2)
            else:
                hijo1, hijo2 = padre1.copy(), padre2.copy()
            
            # Mutación
            hijo1 = mutacion(hijo1, prob_mutacion)
            hijo2 = mutacion(hijo2, prob_mutacion)
            
            # Agregar a nueva población
            nueva_poblacion.extend([hijo1, hijo2])
        
        # Ajustar tamaño si se pasó
        poblacion = nueva_poblacion[:tamaño_poblacion]
    
    # Resultado final
    evaluacion_final = evaluar_ruta(mejor_ruta_historica)
    
    return {
        "mejor_ruta": mejor_ruta_historica,
        "evaluacion": evaluacion_final,
        "historial_fitness": historial_fitness,
        "algoritmo": "Genético"
    }

# Ejemplo de uso
if __name__ == "__main__":
    print("OPTIMIZACIÓN CON ALGORITMO GENÉTICO")
    print("="*60)
    
    # Ejecutar algoritmo genético
    resultado = algoritmo_genetico_simple(generaciones=20, tamaño_poblacion=15)
    
    print(f"\n🏆 MEJOR SOLUCIÓN ENCONTRADA:")
    imprimir_ruta(resultado["mejor_ruta"], resultado["evaluacion"])
    
    print(f"\n📊 EVOLUCIÓN DEL FITNESS:")
    for i, fitness in enumerate(resultado["historial_fitness"]):
        if i % 4 == 0:  # Mostrar cada 4 generaciones
            print(f"Generación {i:2d}: {fitness:7.2f}")