# Análisis comparativo de diferentes ejecuciones

import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Crear carpeta de salida si no existe
output_dir = ".\graficas_generadas"
os.makedirs(output_dir, exist_ok=True)

# Directorio con los archivos JSON de ejecuciones
data_dir = ".\data\ejecuciones"

# Función para extraer datos de archivos .log
def extraer_datos_log(ruta_log):
    import re
    
    historial_fitness = []
    historial_tiempos = []
    
    poblacion = 0
    elitismo = 0
    mejor_fitness = 0
    mejor_puntos = 0
    mejor_distancia = 0
    generaciones = 0
    
    with open(ruta_log, "r", encoding="utf-8") as f:
        for line in f:
            # Extraer configuración
            if "Población:" in line:
                match = re.search(r"Población:\s+(\d+)", line)
                if match:
                    poblacion = int(match.group(1))
            
            if "Elitismo:" in line:
                match = re.search(r"Elitismo:\s+(\d+)%", line)
                if match:
                    elitismo = int(match.group(1)) / 100
            
            # Extraer datos de progreso: Gen X | Tiempo: Xm | Fitness: X | Puntos: X | Dist: X
            match = re.search(r"Gen\s+(\d+)\s+\|\s+Tiempo:\s+([\d.]+)m.*Fitness:\s+([\d.]+)\s+\|\s+Puntos:\s+(\d+)\s+\|\s+Dist:\s+([\d.]+)km", line)
            if match:
                gen = int(match.group(1))
                tiempo_min = float(match.group(2))
                fitness = float(match.group(3))
                puntos = int(match.group(4))
                distancia = float(match.group(5))
                
                historial_tiempos.append(tiempo_min * 60)  # Convertir a segundos
                historial_fitness.append(fitness)
                
                generaciones = gen
                mejor_fitness = fitness
                mejor_puntos = puntos
                mejor_distancia = distancia
    
    return {
        "poblacion": poblacion,
        "elitismo": elitismo,
        "fitness": mejor_fitness,
        "puntos": mejor_puntos,
        "distancia": mejor_distancia,
        "generaciones_ejecutadas": generaciones,
        "historial_fitness": historial_fitness,
        "historial_tiempos": historial_tiempos
    }

# Cargar todos los archivos JSON y LOG de la carpeta ejecuciones
datos_experimentos = []

for archivo in os.listdir(data_dir):
    ruta = os.path.join(data_dir, archivo)
    
    if archivo.endswith(".json"):
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
    
    elif archivo.endswith(".log"):
        # Procesar archivo log
        datos_log = extraer_datos_log(ruta)
        
        nombre = archivo.replace(".log", "").replace("ejecucion", "Ejecucion")
        
        experimento = {
            "nombre": nombre,
            "timestamp": "",
            "fecha": "",
            # Configuración
            "poblacion": datos_log["poblacion"],
            "elitismo": datos_log["elitismo"],
            "generaciones": None,
            "tiempo_limite_horas": 0,
            "modo": "tiempo",
            # Resultados
            "fitness": datos_log["fitness"],
            "puntos": datos_log["puntos"],
            "distancia": datos_log["distancia"],
            "tiempo_viaje": 0,
            "generaciones_ejecutadas": datos_log["generaciones_ejecutadas"],
            "tiempo_ejecucion_segundos": datos_log["historial_tiempos"][-1] if datos_log["historial_tiempos"] else 0,
            "tiempo_ejecucion_minutos": datos_log["historial_tiempos"][-1] / 60 if datos_log["historial_tiempos"] else 0,
            "fitness_por_segundo": datos_log["fitness"] / datos_log["historial_tiempos"][-1] if datos_log["historial_tiempos"] else 0,
            # Historial
            "historial_fitness": datos_log["historial_fitness"],
            "historial_tiempos": datos_log["historial_tiempos"],
            "archivo": archivo
        }
        
        datos_experimentos.append(experimento)

# Crear DataFrame con los resultados
df = pd.DataFrame(datos_experimentos)

# Ordenar por nombre
df = df.sort_values("nombre")

print("\n" + "="*120)
print("ANÁLISIS COMPARATIVO: DIFERENTES EJECUCIONES")
print("="*120)
print(f"\nTotal de ejecuciones analizadas: {len(df)}")

# ============================================================
# TABLA COMPARATIVA
# ============================================================
print("\n" + "="*120)
print("TABLA COMPARATIVA DE EJECUCIONES")
print("="*120)

tabla_comparativa = df[[
    "nombre", "poblacion", "elitismo", "fitness", "puntos", "distancia",
    "generaciones_ejecutadas", "tiempo_ejecucion_minutos", "fitness_por_segundo"
]].copy()

tabla_comparativa["elitismo_%"] = tabla_comparativa["elitismo"] * 100
tabla_comparativa["tiempo_ejecucion_minutos"] = tabla_comparativa["tiempo_ejecucion_minutos"].round(2)
tabla_comparativa["fitness"] = tabla_comparativa["fitness"].round(2)
tabla_comparativa["distancia"] = tabla_comparativa["distancia"].round(2)
tabla_comparativa["fitness_por_segundo"] = tabla_comparativa["fitness_por_segundo"].round(6)

# Reorganizar columnas
tabla_display = tabla_comparativa[[
    "nombre", "poblacion", "elitismo_%", "fitness", "puntos", "distancia",
    "generaciones_ejecutadas", "tiempo_ejecucion_minutos", "fitness_por_segundo"
]]

print(tabla_display.to_string(index=False))
print("\n" + "="*120)

# Guardar tabla en CSV
tabla_display.to_csv(os.path.join(output_dir, "tabla_comparativa_ejecuciones.csv"), index=False, encoding="utf-8")

# ============================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================
print("\n" + "="*120)
print("ANÁLISIS ESTADÍSTICO")
print("="*120)

mejor_idx = df['fitness'].idxmax()
peor_idx = df['fitness'].idxmin()

print(f"\n🏆 MEJOR EJECUCIÓN:")
print(f"   Nombre: {df.loc[mejor_idx, 'nombre']}")
print(f"   Fitness: {df.loc[mejor_idx, 'fitness']:.2f}")
print(f"   Configuración: Población={df.loc[mejor_idx, 'poblacion']}, Elitismo={df.loc[mejor_idx, 'elitismo']*100:.0f}%")
print(f"   Puntos: {df.loc[mejor_idx, 'puntos']}")
print(f"   Distancia: {df.loc[mejor_idx, 'distancia']:.2f} km")

print(f"\n❌ PEOR EJECUCIÓN:")
print(f"   Nombre: {df.loc[peor_idx, 'nombre']}")
print(f"   Fitness: {df.loc[peor_idx, 'fitness']:.2f}")
print(f"   Configuración: Población={df.loc[peor_idx, 'poblacion']}, Elitismo={df.loc[peor_idx, 'elitismo']*100:.0f}%")

print(f"\n📊 ESTADÍSTICAS GENERALES:")
print(f"   Fitness promedio: {df['fitness'].mean():.2f}")
print(f"   Desviación estándar fitness: {df['fitness'].std():.2f}")
print(f"   Diferencia mejor vs peor: {(df.loc[mejor_idx, 'fitness'] - df.loc[peor_idx, 'fitness']):.2f}")

# ============================================================
# GRÁFICA: Evolución del fitness para todas las ejecuciones
# ============================================================
print("\n" + "="*120)
print("GENERANDO GRÁFICA DE EVOLUCIÓN")
print("="*120)

plt.figure(figsize=(12, 7))

# Usar colores bien diferenciados
colores_distintos = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

for idx, (_, exp) in enumerate(df.iterrows()):
    if exp["historial_fitness"] and exp["historial_tiempos"]:
        tiempos_min = [t / 60 for t in exp["historial_tiempos"]]
        fitness = exp["historial_fitness"]
        
        # Asegurar que ambos arrays tengan la misma longitud
        min_len = min(len(tiempos_min), len(fitness))
        tiempos_min = tiempos_min[:min_len]
        fitness = fitness[:min_len]
        
        # Obtener el mejor fitness (último valor ya que es histórico)
        mejor_fitness = fitness[-1] if fitness else 0
        
        print(f"\n  {exp['nombre']:>12}: Fitness final = {mejor_fitness:.2f} | "
              f"Población={exp['poblacion']}, Elitismo={exp['elitismo']*100:.0f}%")
        
        color = colores_distintos[idx % len(colores_distintos)]
        plt.plot(tiempos_min, fitness, 
                label=f"{exp['nombre']} (Fitness: {mejor_fitness:.2f})", 
                linewidth=2.5, alpha=0.9, color=color)

plt.xlabel("Tiempo (minutos)", fontsize=12)
plt.ylabel("Mejor Fitness histórico", fontsize=12)
plt.title("Evolución del Fitness - Comparación entre Ejecuciones", fontsize=14, fontweight='bold')
plt.xlim(0, 120)  # Limitar el eje X a 120 minutos
plt.legend(loc="lower right", fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "ejecuciones_evolucion_fitness.png"), dpi=300, bbox_inches='tight')
plt.close()

print(f"\n✅ Gráfica generada: ejecuciones_evolucion_fitness.png")

# ============================================================
# RESUMEN FINAL
# ============================================================
print("\n" + "="*120)
print("ARCHIVOS GENERADOS")
print("="*120)
print(f"\nDirectorio: {output_dir}")
print("\nTablas:")
print("  - tabla_comparativa_ejecuciones.csv")
print("\nGráficas:")
print("  - ejecuciones_evolucion_fitness.png (Evolución temporal de todas las ejecuciones)")
print("\n" + "="*120 + "\n")
