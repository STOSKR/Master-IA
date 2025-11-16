# Análisis de ejecuciones de Simulated Annealing (SA)

import json
import os
import matplotlib.pyplot as plt

# Crear carpeta de salida si no existe
output_dir = "./graficas_generadas"
os.makedirs(output_dir, exist_ok=True)

# Directorio con los archivos JSON
data_dir = "./data/sa"

# Cargar los archivos JSON
datos_experimentos = []

# Buscar todos los archivos JSON en la carpeta
archivos_json = [f for f in os.listdir(data_dir) if f.endswith(".json")]
archivos_json.sort()  # Ordenar alfabéticamente

for archivo in archivos_json:
    ruta = os.path.join(data_dir, archivo)
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
            
            config = datos.get("configuracion", {})
            mejor_sol = datos.get("mejor_solucion", {})
            estadisticas = datos.get("estadisticas", {})
            
            # Nombre basado en el archivo
            nombre = archivo.replace('.json', '').replace('_', ' ').title()
            
            # Extraer historial
            historial = datos.get("historial", {})
            historial_fitness = historial.get("mejor_fitness", historial.get("fitness_actual", []))
            historial_tiempos = historial.get("tiempos", historial.get("tiempos_segundos", []))
            
            # Si no hay tiempos, generar sintéticamente basado en el tiempo total
            if not historial_tiempos and historial_fitness:
                tiempo_total = estadisticas.get("tiempo_ejecucion_segundos", 7200)
                num_puntos = len(historial_fitness)
                # Generar tiempos lineales
                historial_tiempos = [(i * tiempo_total / num_puntos) for i in range(num_puntos)]
            
            experimento = {
                "nombre": nombre,
                "fitness": mejor_sol.get("fitness", 0),
                "puntos": mejor_sol.get("puntos_totales", 0),
                "distancia": mejor_sol.get("distancia_total_km", 0),
                "iteraciones": estadisticas.get("iteraciones_realizadas", 0),
                "mejoras": estadisticas.get("mejoras_encontradas", 0),
                "tiempo_min": estadisticas.get("tiempo_ejecucion_minutos", 0),
                "historial_fitness": historial_fitness,
                "historial_tiempos": historial_tiempos,
                "archivo": archivo
            }
            
            datos_experimentos.append(experimento)
            print(f"✅ Cargado: {archivo}")
            print(f"   - Nombre: {nombre}")
            print(f"   - Mejor fitness: {experimento['fitness']:.2f}")
            print(f"   - Puntos: {experimento['puntos']}")
            print(f"   - Mejoras: {experimento['mejoras']}")
            print(f"   - Datos en historial: {len(experimento['historial_fitness'])}")
    except Exception as e:
        print(f"❌ Error cargando {archivo}: {str(e)}")

print("\n" + "="*120)
print("ANÁLISIS COMPARATIVO: EJECUCIONES DE SIMULATED ANNEALING")
print("="*120)
print(f"\nTotal de ejecuciones analizadas: {len(datos_experimentos)}")

# ============================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================
if datos_experimentos:
    print("\n" + "="*120)
    print("ANÁLISIS ESTADÍSTICO")
    print("="*120)
    
    mejor_exp = max(datos_experimentos, key=lambda x: x['fitness'])
    peor_exp = min(datos_experimentos, key=lambda x: x['fitness'])
    
    print(f"\n🏆 MEJOR RESULTADO:")
    print(f"   Ejecución: {mejor_exp['nombre']}")
    print(f"   Fitness: {mejor_exp['fitness']:.2f}")
    print(f"   Puntos: {mejor_exp['puntos']}")
    print(f"   Distancia: {mejor_exp['distancia']:.2f} km")
    print(f"   Mejoras: {mejor_exp['mejoras']}")
    
    print(f"\n❌ PEOR RESULTADO:")
    print(f"   Ejecución: {peor_exp['nombre']}")
    print(f"   Fitness: {peor_exp['fitness']:.2f}")
    print(f"   Puntos: {peor_exp['puntos']}")
    print(f"   Distancia: {peor_exp['distancia']:.2f} km")
    print(f"   Mejoras: {peor_exp['mejoras']}")
    
    fitness_promedio = sum(exp['fitness'] for exp in datos_experimentos) / len(datos_experimentos)
    puntos_promedio = sum(exp['puntos'] for exp in datos_experimentos) / len(datos_experimentos)
    
    print(f"\n📊 ESTADÍSTICAS GENERALES:")
    print(f"   Fitness promedio: {fitness_promedio:.2f}")
    print(f"   Puntos promedio: {puntos_promedio:.0f}")
    
    if len(datos_experimentos) > 1:
        mejora_porcentual = ((mejor_exp['fitness'] - peor_exp['fitness']) / peor_exp['fitness'] * 100)
        print(f"   Mejora del mejor vs peor: {mejora_porcentual:.2f}%")
        
        # Desviación estándar
        import statistics
        fitness_vals = [exp['fitness'] for exp in datos_experimentos]
        if len(fitness_vals) > 1:
            desv_std = statistics.stdev(fitness_vals)
            print(f"   Desviación estándar fitness: {desv_std:.2f}")

# ============================================================
# GRÁFICA: Evolución del fitness comparativa
# ============================================================
if datos_experimentos:
    plt.figure(figsize=(12, 7))
    
    # Colores distintos para cada ejecución
    colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for idx, exp in enumerate(datos_experimentos):
        if exp["historial_fitness"] and exp["historial_tiempos"]:
            # Convertir tiempos a minutos
            tiempos_min = [t / 60 for t in exp["historial_tiempos"]]
            
            # Asegurar que las listas tengan la misma longitud
            min_len = min(len(tiempos_min), len(exp["historial_fitness"]))
            tiempos_min = tiempos_min[:min_len]
            fitness = exp["historial_fitness"][:min_len]
            
            mejor_fitness = exp['fitness']
            
            plt.plot(tiempos_min, fitness, 
                    label=f"{exp['nombre']} (Fitness: {mejor_fitness:.2f})", 
                    linewidth=2, alpha=0.8, 
                    color=colores[idx % len(colores)])
            
            # Imprimir en consola
            print(f"\n{exp['nombre']}:")
            print(f"  Mejor Fitness: {mejor_fitness:.2f}")
    
    plt.xlabel("Tiempo (minutos)", fontsize=12)
    plt.ylabel("Mejor Fitness histórico", fontsize=12)
    plt.title("Evolución del Fitness - Ejecuciones de Simulated Annealing", fontsize=14, fontweight='bold')
    plt.xlim(0, 120)  # Limitar a 120 minutos
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "comparacion_sa_ejecuciones.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n" + "="*120)
    print("ARCHIVO GENERADO")
    print("="*120)
    print(f"✅ comparacion_sa_ejecuciones.png")
    print(f"\n📁 Ubicación: {os.path.abspath(output_dir)}")
else:
    print("\n⚠️ No se encontraron archivos JSON válidos para procesar")
