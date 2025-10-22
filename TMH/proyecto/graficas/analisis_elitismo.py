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
data_dir = ".\data\json"

# Cargar todos los archivos JSON
datos_experimentos = []

for archivo in os.listdir(data_dir):
    if archivo.endswith(".json") and archivo.startswith("Elit_"):
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

print("\n" + "="*80)
print("RESUMEN GUARDADO")
