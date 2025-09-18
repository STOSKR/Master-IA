# Comparación entre Algoritmos Genéticos y Enfriamiento Simulado
# Para optimización de rutas turísticas

from algoritmo_genetico import algoritmo_genetico_simple
from enfriamiento_simulado import enfriamiento_simulado
from turismo_basico import imprimir_ruta
import time

def ejecutar_experimento(num_ejecuciones: int = 5):
    """
    Ejecuta múltiples experimentos con ambos algoritmos para comparar resultados
    """
    print("🔬 EXPERIMENTO COMPARATIVO")
    print("="*80)
    print(f"Ejecutando {num_ejecuciones} experimentos con cada algoritmo...")
    
    resultados_ga = []
    resultados_sa = []
    
    print(f"\n🧬 EJECUTANDO ALGORITMOS GENÉTICOS:")
    print("-" * 50)
    
    for i in range(num_ejecuciones):
        print(f"\nEjecución {i+1}/{num_ejecuciones}")
        inicio = time.time()
        resultado = algoritmo_genetico_simple(generaciones=20, tamaño_poblacion=15, 
                                            prob_cruce=0.8, prob_mutacion=0.1)
        tiempo_ejecucion = time.time() - inicio
        resultado["tiempo_ejecucion"] = tiempo_ejecucion
        resultados_ga.append(resultado)
        print(f"✅ Fitness: {resultado['evaluacion']['fitness']:.2f}, Tiempo: {tiempo_ejecucion:.2f}s")
    
    print(f"\n🌡️ EJECUTANDO ENFRIAMIENTO SIMULADO:")
    print("-" * 50)
    
    for i in range(num_ejecuciones):
        print(f"\nEjecución {i+1}/{num_ejecuciones}")
        inicio = time.time()
        resultado = enfriamiento_simulado(temperatura_inicial=1000.0, 
                                        temperatura_final=0.1,
                                        factor_enfriamiento=0.95,
                                        iteraciones_por_temp=10)
        tiempo_ejecucion = time.time() - inicio
        resultado["tiempo_ejecucion"] = tiempo_ejecucion
        resultados_sa.append(resultado)
        print(f"✅ Fitness: {resultado['evaluacion']['fitness']:.2f}, Tiempo: {tiempo_ejecucion:.2f}s")
    
    return resultados_ga, resultados_sa

def analizar_resultados(resultados_ga: list, resultados_sa: list):
    """
    Analiza y compara los resultados de ambos algoritmos
    """
    print("\n" + "="*80)
    print("📊 ANÁLISIS COMPARATIVO DE RESULTADOS")
    print("="*80)
    
    # Extraer métricas
    fitness_ga = [r["evaluacion"]["fitness"] for r in resultados_ga]
    fitness_sa = [r["evaluacion"]["fitness"] for r in resultados_sa]
    
    tiempo_ga = [r["tiempo_ejecucion"] for r in resultados_ga]
    tiempo_sa = [r["tiempo_ejecucion"] for r in resultados_sa]
    
    puntos_ga = [r["evaluacion"]["puntos"] for r in resultados_ga]
    puntos_sa = [r["evaluacion"]["puntos"] for r in resultados_sa]
    
    distancia_ga = [r["evaluacion"]["distancia"] for r in resultados_ga]
    distancia_sa = [r["evaluacion"]["distancia"] for r in resultados_sa]
    
    # Estadísticas descriptivas
    def estadisticas(datos, nombre):
        promedio = sum(datos) / len(datos)
        maximo = max(datos)
        minimo = min(datos)
        return f"{nombre:15} | Promedio: {promedio:7.2f} | Máximo: {maximo:7.2f} | Mínimo: {minimo:7.2f}"
    
    print(f"\n🧬 ALGORITMOS GENÉTICOS:")
    print(estadisticas(fitness_ga, "Fitness"))
    print(estadisticas(puntos_ga, "Puntos"))
    print(estadisticas(distancia_ga, "Distancia"))
    print(estadisticas(tiempo_ga, "Tiempo (s)"))
    
    print(f"\n🌡️ ENFRIAMIENTO SIMULADO:")
    print(estadisticas(fitness_sa, "Fitness"))
    print(estadisticas(puntos_sa, "Puntos"))
    print(estadisticas(distancia_sa, "Distancia"))
    print(estadisticas(tiempo_sa, "Tiempo (s)"))
    
    # Comparación directa
    print(f"\n🏆 COMPARACIÓN DIRECTA:")
    print("-" * 50)
    
    mejor_fitness_ga = max(fitness_ga)
    mejor_fitness_sa = max(fitness_sa)
    
    if mejor_fitness_ga > mejor_fitness_sa:
        ganador_fitness = "Algoritmos Genéticos"
        ventaja_fitness = mejor_fitness_ga - mejor_fitness_sa
    elif mejor_fitness_sa > mejor_fitness_ga:
        ganador_fitness = "Enfriamiento Simulado"
        ventaja_fitness = mejor_fitness_sa - mejor_fitness_ga
    else:
        ganador_fitness = "Empate"
        ventaja_fitness = 0
    
    print(f"Mejor fitness encontrado:")
    print(f"  🧬 AG: {mejor_fitness_ga:.2f}")
    print(f"  🌡️ SA: {mejor_fitness_sa:.2f}")
    print(f"  🏆 Ganador: {ganador_fitness}")
    if ventaja_fitness > 0:
        print(f"  📈 Ventaja: {ventaja_fitness:.2f}")
    
    # Tiempo promedio
    tiempo_prom_ga = sum(tiempo_ga) / len(tiempo_ga)
    tiempo_prom_sa = sum(tiempo_sa) / len(tiempo_sa)
    
    print(f"\nTiempo promedio de ejecución:")
    print(f"  🧬 AG: {tiempo_prom_ga:.2f}s")
    print(f"  🌡️ SA: {tiempo_prom_sa:.2f}s")
    
    if tiempo_prom_ga > 0 and tiempo_prom_sa > 0:
        if tiempo_prom_ga < tiempo_prom_sa:
            print(f"  ⚡ AG es {tiempo_prom_sa/tiempo_prom_ga:.1f}x más rápido")
        else:
            print(f"  ⚡ SA es {tiempo_prom_ga/tiempo_prom_sa:.1f}x más rápido")
    else:
        print(f"  ⚡ Tiempos muy similares (< 0.01s)")
    
    # Encontrar mejores soluciones
    mejor_idx_ga = fitness_ga.index(max(fitness_ga))
    mejor_idx_sa = fitness_sa.index(max(fitness_sa))
    
    print(f"\n🥇 MEJOR SOLUCIÓN - ALGORITMOS GENÉTICOS:")
    imprimir_ruta(resultados_ga[mejor_idx_ga]["mejor_ruta"], 
                  resultados_ga[mejor_idx_ga]["evaluacion"])
    
    print(f"\n🥈 MEJOR SOLUCIÓN - ENFRIAMIENTO SIMULADO:")
    imprimir_ruta(resultados_sa[mejor_idx_sa]["mejor_ruta"], 
                  resultados_sa[mejor_idx_sa]["evaluacion"])
    
    return {
        "ga": {
            "fitness_promedio": sum(fitness_ga) / len(fitness_ga),
            "mejor_fitness": max(fitness_ga),
            "tiempo_promedio": tiempo_prom_ga
        },
        "sa": {
            "fitness_promedio": sum(fitness_sa) / len(fitness_sa),
            "mejor_fitness": max(fitness_sa),
            "tiempo_promedio": tiempo_prom_sa
        },
        "ganador": ganador_fitness
    }

def main():
    """Función principal del experimento"""
    print("COMPARACIÓN: ALGORITMOS GENÉTICOS vs ENFRIAMIENTO SIMULADO")
    print("Problema: Optimización de Rutas Turísticas")
    print("="*80)
    
    # Ejecutar experimentos
    resultados_ga, resultados_sa = ejecutar_experimento(num_ejecuciones=3)
    
    # Analizar resultados
    resumen = analizar_resultados(resultados_ga, resultados_sa)
    
    print(f"\n📋 RESUMEN EJECUTIVO:")
    print("="*50)
    print(f"Ganador por fitness: {resumen['ganador']}")
    print(f"AG - Fitness promedio: {resumen['ga']['fitness_promedio']:.2f}")
    print(f"SA - Fitness promedio: {resumen['sa']['fitness_promedio']:.2f}")
    print(f"AG - Tiempo promedio: {resumen['ga']['tiempo_promedio']:.2f}s")
    print(f"SA - Tiempo promedio: {resumen['sa']['tiempo_promedio']:.2f}s")

if __name__ == "__main__":
    main()