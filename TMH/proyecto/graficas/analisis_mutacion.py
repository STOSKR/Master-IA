# Análisis comparativo de diferentes configuraciones de MUTACIÓN

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

# Cargar solo los archivos JSON que empiezan con "Mut"
datos_experimentos = []

for archivo in os.listdir(data_dir):
    if archivo.startswith("Mut") and archivo.endswith(".json"):
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
                "prob_mutacion": config.get("prob_mutacion", 0),
                "prob_cruce": config.get("prob_cruce", 0),
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

# Ordenar por probabilidad de mutación
df = df.sort_values("prob_mutacion")

print("\n" + "="*120)
print("ANÁLISIS COMPARATIVO: IMPACTO DE LA PROBABILIDAD DE MUTACIÓN")
print("="*120)
print(f"\nTotal de experimentos analizados: {len(df)}")
print(f"Rango de mutación: {df['prob_mutacion'].min()*100:.0f}% - {df['prob_mutacion'].max()*100:.0f}%")
print(f"Configuración común: Cruce={df['prob_cruce'].iloc[0]*100:.0f}%, Elitismo={df['elitismo'].iloc[0]*100:.0f}%")

# ============================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================
print("\n" + "="*120)
print("ANÁLISIS ESTADÍSTICO")
print("="*120)

mejor_idx = df['fitness'].idxmax()
peor_idx = df['fitness'].idxmin()

print(f"\n🏆 MEJOR RESULTADO:")
print(f"   Configuración: {df.loc[mejor_idx, 'nombre']} (Mutación {df.loc[mejor_idx, 'prob_mutacion']*100:.0f}%)")
print(f"   Fitness: {df.loc[mejor_idx, 'fitness']:.2f}")
print(f"   Puntos: {df.loc[mejor_idx, 'puntos']}")
print(f"   Distancia: {df.loc[mejor_idx, 'distancia']:.2f} km")
print(f"   Generaciones: {df.loc[mejor_idx, 'generaciones_ejecutadas']}")

print(f"\n❌ PEOR RESULTADO:")
print(f"   Configuración: {df.loc[peor_idx, 'nombre']} (Mutación {df.loc[peor_idx, 'prob_mutacion']*100:.0f}%)")
print(f"   Fitness: {df.loc[peor_idx, 'fitness']:.2f}")
print(f"   Puntos: {df.loc[peor_idx, 'puntos']}")
print(f"   Distancia: {df.loc[peor_idx, 'distancia']:.2f} km")

print(f"\n📊 ESTADÍSTICAS GENERALES:")
print(f"   Fitness promedio: {df['fitness'].mean():.2f}")
print(f"   Desviación estándar fitness: {df['fitness'].std():.2f}")
print(f"   Mejora del mejor vs peor: {((df.loc[mejor_idx, 'fitness'] - df.loc[peor_idx, 'fitness']) / df.loc[peor_idx, 'fitness'] * 100):.2f}%")

# Velocidad de convergencia
mejor_velocidad_idx = df['fitness_por_segundo'].idxmax()
print(f"\n⚡ MAYOR VELOCIDAD DE CONVERGENCIA:")
print(f"   Configuración: {df.loc[mejor_velocidad_idx, 'nombre']} (Mutación {df.loc[mejor_velocidad_idx, 'prob_mutacion']*100:.0f}%)")
print(f"   Fitness/segundo: {df.loc[mejor_velocidad_idx, 'fitness_por_segundo']:.6f}")

# ============================================================
# GRÁFICA 1: Evolución del fitness comparativa
# ============================================================
plt.figure(figsize=(12, 7))

colores = plt.cm.coolwarm(np.linspace(0, 1, len(df)))

for idx, (_, exp) in enumerate(df.iterrows()):
    if exp["historial_fitness"] and exp["historial_tiempos"]:
        tiempos_min = [t / 60 for t in exp["historial_tiempos"]]
        plt.plot(tiempos_min, exp["historial_fitness"], 
                label=f"{exp['nombre']} ({exp['prob_mutacion']*100:.0f}%)", 
                linewidth=2, alpha=0.8, color=colores[idx])

plt.xlabel("Tiempo (minutos)", fontsize=12)
plt.ylabel("Mejor Fitness histórico", fontsize=12)
plt.title("Evolución del Fitness - Comparación entre Niveles de Mutación", fontsize=14, fontweight='bold')
plt.legend(loc="lower right", fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "comparacion_mut.png"), dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# ANÁLISIS DE CORRELACIÓN
# ============================================================
print("\n" + "="*120)
print("ANÁLISIS DE CORRELACIÓN")
print("="*120)

correlacion_mut_fitness = df['prob_mutacion'].corr(df['fitness'])
correlacion_mut_puntos = df['prob_mutacion'].corr(df['puntos'])
correlacion_mut_distancia = df['prob_mutacion'].corr(df['distancia'])
correlacion_mut_gen = df['prob_mutacion'].corr(df['generaciones_ejecutadas'])

print(f"\nCorrelación Mutación vs:")
print(f"  - Fitness: {correlacion_mut_fitness:+.4f}")
print(f"  - Puntos: {correlacion_mut_puntos:+.4f}")
print(f"  - Distancia: {correlacion_mut_distancia:+.4f}")
print(f"  - Generaciones: {correlacion_mut_gen:+.4f}")

if abs(correlacion_mut_fitness) > 0.5:
    tendencia = "FUERTE" if abs(correlacion_mut_fitness) > 0.7 else "MODERADA"
    direccion = "POSITIVA" if correlacion_mut_fitness > 0 else "NEGATIVA"
    print(f"\n💡 CONCLUSIÓN: Existe una correlación {tendencia} {direccion} entre mutación y fitness")
else:
    print(f"\n💡 CONCLUSIÓN: La correlación entre mutación y fitness es DÉBIL")

# ============================================================
# RESUMEN FINAL
# ============================================================
print("\n" + "="*120)
print("ARCHIVOS GENERADOS")
