# Análisis comparativo de resultados de algoritmos genéticos

import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Crear carpeta de salida si no existe
output_dir = ".\graficas_generadas"
os.makedirs(output_dir, exist_ok=True)

# Directorio con los archivos JSON
data_dir = ".\data"

# Cargar todos los archivos JSON
datos_experimentos = []

for archivo in os.listdir(data_dir):
    if archivo.endswith(".json"):
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
                "tiempo_ejecucion_minutos": resultados.get("tiempo_ejecucion", 0) / 60,  # Convertir a minutos
                "fitness_por_segundo": resultados.get("fitness_por_segundo", 0),
                # Historial
                "historial_fitness": datos.get("historial_fitness", []),
                "historial_tiempos": datos.get("historial_tiempos", []),
                "archivo": archivo
            }
            
            datos_experimentos.append(experimento)

# Crear DataFrame con los resultados
df = pd.DataFrame(datos_experimentos)

# Ordenar por elitismo
df = df.sort_values("elitismo")

# ============================================================
# TABLA 1: Resumen de configuraciones y resultados finales
# ============================================================
print("\n" + "="*80)
print("TABLA 1: Resumen de Experimentos")
print("="*80)

tabla_resumen = df[[
    "nombre", "elitismo", "poblacion", "tiempo_limite_horas",
    "fitness", "puntos", "distancia", "generaciones_ejecutadas",
    "tiempo_ejecucion_minutos"
]].copy()

tabla_resumen["tiempo_ejecucion_minutos"] = tabla_resumen["tiempo_ejecucion_minutos"].round(2)
tabla_resumen["fitness"] = tabla_resumen["fitness"].round(2)
tabla_resumen["distancia"] = tabla_resumen["distancia"].round(2)

print(tabla_resumen.to_string(index=False))

# Guardar tabla en CSV
tabla_resumen.to_csv(os.path.join(output_dir, "tabla_resumen.csv"), index=False, encoding="utf-8")

# ============================================================
# TABLA 2: Comparación de rendimiento
# ============================================================
print("\n" + "="*80)
print("TABLA 2: Comparación de Rendimiento")
print("="*80)

tabla_rendimiento = df[[
    "nombre", "elitismo", "fitness", "fitness_por_segundo",
    "generaciones_ejecutadas", "tiempo_ejecucion_minutos"
]].copy()

tabla_rendimiento["fitness_por_segundo"] = tabla_rendimiento["fitness_por_segundo"].round(6)
tabla_rendimiento["tiempo_ejecucion_minutos"] = tabla_rendimiento["tiempo_ejecucion_minutos"].round(2)

print(tabla_rendimiento.to_string(index=False))

# Guardar tabla en CSV
tabla_rendimiento.to_csv(os.path.join(output_dir, "tabla_rendimiento.csv"), index=False, encoding="utf-8")

# ============================================================
# GRÁFICA 1: Fitness final por nivel de elitismo
# ============================================================
plt.figure(figsize=(10, 6))
plt.bar(df["nombre"], df["fitness"], color="steelblue", alpha=0.8)
plt.xlabel("Experimento")
plt.ylabel("Fitness Final")
plt.title("Fitness Final por Experimento")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "comparacion_fitness_final.png"), dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# GRÁFICA 2: Evolución del fitness a lo largo del tiempo
# ============================================================
plt.figure(figsize=(12, 7))

for _, exp in df.iterrows():
    if exp["historial_fitness"] and exp["historial_tiempos"]:
        # Convertir tiempos de segundos a minutos
        tiempos_min = [t / 60 for t in exp["historial_tiempos"]]
        plt.plot(tiempos_min, exp["historial_fitness"], 
                label=f"{exp['nombre']} (E={exp['elitismo']})", 
                linewidth=2, alpha=0.8)

plt.xlabel("Tiempo (minutos)")
plt.ylabel("Mejor Fitness histórico")
plt.title("Evolución del Fitness - Comparación entre Niveles de Elitismo")
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "comparacion_elit.png"), dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# GRÁFICA 3: Relación Elitismo vs Fitness Final
# ============================================================
plt.figure(figsize=(10, 6))
plt.scatter(df["elitismo"] * 100, df["fitness"], s=200, color="coral", alpha=0.7, edgecolors="black")
for _, row in df.iterrows():
    plt.annotate(row["nombre"].replace("Elit_", ""), 
                (row["elitismo"] * 100, row["fitness"]),
                xytext=(5, 5), textcoords='offset points', fontsize=9)
plt.xlabel("Elitismo (%)")
plt.ylabel("Fitness Final")
plt.title("Relación entre Nivel de Elitismo y Fitness Final")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "elitismo_vs_fitness.png"), dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# GRÁFICA 4: Generaciones ejecutadas vs Fitness
# ============================================================
plt.figure(figsize=(10, 6))
plt.scatter(df["generaciones_ejecutadas"], df["fitness"], s=200, color="seagreen", alpha=0.7, edgecolors="black")
for _, row in df.iterrows():
    plt.annotate(row["nombre"].replace("Elit_", ""), 
                (row["generaciones_ejecutadas"], row["fitness"]),
                xytext=(5, 5), textcoords='offset points', fontsize=9)
plt.xlabel("Generaciones Ejecutadas")
plt.ylabel("Fitness Final")
plt.title("Relación entre Generaciones Ejecutadas y Fitness Final")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "generaciones_vs_fitness.png"), dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# GRÁFICA 5: Velocidad de convergencia (Fitness por segundo)
# ============================================================
plt.figure(figsize=(10, 6))
plt.bar(df["nombre"], df["fitness_por_segundo"], color="purple", alpha=0.7)
plt.xlabel("Experimento")
plt.ylabel("Fitness por Segundo")
plt.title("Velocidad de Convergencia (Fitness por Segundo)")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "velocidad_convergencia.png"), dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# GRÁFICA 6: Componentes del Fitness (Puntos y Distancia)
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Puntos obtenidos
ax1.bar(df["nombre"], df["puntos"], color="gold", alpha=0.7)
ax1.set_xlabel("Experimento")
ax1.set_ylabel("Puntos")
ax1.set_title("Puntos Obtenidos por Experimento")
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis="y", alpha=0.3)

# Distancia recorrida
ax2.bar(df["nombre"], df["distancia"], color="crimson", alpha=0.7)
ax2.set_xlabel("Experimento")
ax2.set_ylabel("Distancia")
ax2.set_title("Distancia Recorrida por Experimento")
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "componentes_fitness.png"), dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# ESTADÍSTICAS ADICIONALES
# ============================================================
print("\n" + "="*80)
print("ESTADÍSTICAS ADICIONALES")
print("="*80)

print(f"\nMejor Fitness: {df.loc[df['fitness'].idxmax(), 'nombre']} = {df['fitness'].max():.2f}")
print(f"Peor Fitness: {df.loc[df['fitness'].idxmin(), 'nombre']} = {df['fitness'].min():.2f}")
print(f"Fitness Promedio: {df['fitness'].mean():.2f}")
print(f"Desviación Estándar: {df['fitness'].std():.2f}")

print(f"\nMayor velocidad de convergencia: {df.loc[df['fitness_por_segundo'].idxmax(), 'nombre']}")
print(f"Menor velocidad de convergencia: {df.loc[df['fitness_por_segundo'].idxmin(), 'nombre']}")

print(f"\nMás generaciones ejecutadas: {df.loc[df['generaciones_ejecutadas'].idxmax(), 'nombre']} = {df['generaciones_ejecutadas'].max()}")
print(f"Menos generaciones ejecutadas: {df.loc[df['generaciones_ejecutadas'].idxmin(), 'nombre']} = {df['generaciones_ejecutadas'].min()}")

# ============================================================
# RESUMEN FINAL
# ============================================================
print("\n" + "="*80)
print("RESUMEN GUARDADO")
print("="*80)
print(f"\nArchivos generados en: {output_dir}")
print("- tabla_resumen.csv")
print("- tabla_rendimiento.csv")
print("- comparacion_fitness_final.png")
print("- evolucion_fitness_comparativa.png")
print("- elitismo_vs_fitness.png")
print("- generaciones_vs_fitness.png")
print("- velocidad_convergencia.png")
print("- componentes_fitness.png")
