# Análisis comparativo de diferentes tamaños de POBLACIÓN

import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Crear carpeta de salida si no existe
output_dir = ".\graficas_generadas"
os.makedirs(output_dir, exist_ok=True)

# Directorio con los archivos JSON
data_dir = ".\data\json"

# Cargar solo los archivos JSON que empiezan con "Pob"
datos_experimentos = []

for archivo in os.listdir(data_dir):
    if archivo.startswith("Pob") and archivo.endswith(".json"):
        ruta = os.path.join(data_dir, archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
            
            # Extraer información relevante
            config = datos.get("configuracion", {})
            resultados = datos.get("resultados", {})
            
            experimento = {
                "nombre": datos.get("nombre", ""),
                "timestamp": datos.get("timestamp", ""),
                "fecha": datos.get("fecha", ""),
                # Configuración
                "poblacion": config.get("poblacion", 0),
                "elitismo": config.get("elitismo", 0),
                "generaciones": config.get("generaciones", None),
                "tiempo_limite_horas": config.get("tiempo_limite_horas", 0),
                "modo": config.get("modo", ""),
                # Resultados
                "fitness": resultados.get("fitness", 0),
                "puntos": resultados.get("puntos", 0),
                "distancia": resultados.get("distancia", 0),
                "tiempo_viaje": resultados.get("tiempo_viaje", 0),
                "generaciones_ejecutadas": resultados.get("generaciones_ejecutadas", 0),
                "tiempo_ejecucion_segundos": resultados.get("tiempo_ejecucion", 0),
                "tiempo_ejecucion_minutos": resultados.get("tiempo_ejecucion", 0) / 60,
                "fitness_por_segundo": resultados.get("fitness_por_segundo", 0),
                # Historial
                "historial_fitness": datos.get("historial_fitness", []),
                "historial_tiempos": datos.get("historial_tiempos", []),
                "archivo": archivo
            }
            
            datos_experimentos.append(experimento)

# Crear DataFrame con los resultados
df = pd.DataFrame(datos_experimentos)

# Ordenar por tamaño de población
df = df.sort_values("poblacion")

print("\n" + "="*120)
print("ANÁLISIS COMPARATIVO: IMPACTO DEL TAMAÑO DE POBLACIÓN")
print("="*120)
print(f"\nTotal de experimentos analizados: {len(df)}")
print(f"Rango de población: {df['poblacion'].min()} - {df['poblacion'].max()}")
print(f"Configuración común: Elitismo={df['elitismo'].iloc[0]*100:.0f}%, Tiempo límite={df['tiempo_limite_horas'].iloc[0]:.1f}h")

# ============================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================
print("\n" + "="*120)
print("ANÁLISIS ESTADÍSTICO")
print("="*120)

mejor_idx = df['fitness'].idxmax()
peor_idx = df['fitness'].idxmin()

# ============================================================
# GRÁFICAS: Comparativas dos a dos
# ============================================================

# Definir las comparaciones
comparaciones = [
    ([100, 500], "100 vs 500", "poblacion_100_vs_500.png"),
    ([750, 1000], "750 vs 1000", "poblacion_750_vs_1000.png"),
    ([3000, 5000], "3000 vs 5000", "poblacion_3000_vs_5000.png")
]

for poblaciones, titulo_comp, nombre_archivo in comparaciones:
    plt.figure(figsize=(12, 7))
    
    # Filtrar solo las poblaciones de esta comparación
    df_comp = df[df['poblacion'].isin(poblaciones)]
    
    # Colores distintivos
    colores = ['#1f77b4', '#ff7f0e']
    
    print(f"\n{'='*80}")
    print(f"COMPARACIÓN: {titulo_comp}")
    print(f"{'='*80}")
    
    for idx, (_, exp) in enumerate(df_comp.iterrows()):
        if exp["historial_fitness"] and exp["historial_tiempos"]:
            tiempos_min = [t / 60 for t in exp["historial_tiempos"]]
            fitness = exp["historial_fitness"]
            
            # Asegurar que ambos arrays tengan la misma longitud
            min_len = min(len(tiempos_min), len(fitness))
            tiempos_min = tiempos_min[:min_len]
            fitness = fitness[:min_len]
            
            # Obtener el mejor fitness (último valor ya que es histórico)
            mejor_fitness = fitness[-1] if fitness else 0
            
            print(f"\n  Población {exp['poblacion']:>5}: Mejor Fitness = {mejor_fitness:.2f}")
            
            plt.plot(tiempos_min, fitness, 
                    label=f"Población {exp['poblacion']} (Fitness: {mejor_fitness:.2f})", 
                    linewidth=2.5, alpha=0.9, color=colores[idx])
    
    plt.xlabel("Tiempo (minutos)", fontsize=12)
    plt.ylabel("Mejor Fitness histórico", fontsize=12)
    plt.title(f"Evolución del Fitness - Comparación Población {titulo_comp}", fontsize=14, fontweight='bold')
    plt.legend(loc="lower right", fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, nombre_archivo), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Gráfica generada: {nombre_archivo}")

print("\n" + "="*120)
print("ARCHIVOS GENERADOS")
print("="*120)
print(f"\nDirectorio: {output_dir}")
print("\nGráficas:")
print("  - poblacion_100_vs_500.png (Comparación poblaciones pequeñas)")
print("  - poblacion_750_vs_1000.png (Comparación poblaciones medias)")
print("  - poblacion_3000_vs_5000.png (Comparación poblaciones grandes)")
print("\n" + "="*120 + "\n")