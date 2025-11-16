# Procesar el log del algoritmo genético y comparar con el SA

import re
import pandas as pd
import matplotlib.pyplot as plt
import os

# Crear carpeta de salida si no existe
output_dir = ".\graficas_generadas"
os.makedirs(output_dir, exist_ok=True)

# Rutas de los archivos
log_ga_path = ".\data\log\elit10.log"
log_sa_path = ".\data\log\sa1.log"

# Función para extraer tiempo y fitness
def extraer_datos(log_path, label):
    pattern = re.compile(r"Tiempo:\s+([\d.]+)m.*Fitness:\s+([\d.]+)")
    tiempos, fitness = [], []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                tiempos.append(float(match.group(1)))
                fitness.append(float(match.group(2)))
    return pd.DataFrame({"Tiempo_min": tiempos, "Fitness": fitness, "Algoritmo": label})

# Extraer datos de ambos logs
df_ga = extraer_datos(log_ga_path, "Genético")
pattern_sa = re.compile(r"Tiempo:\s+([\d.]+)min.*Mejor\s*=\s*([\d.]+)")
tiempos_sa, mejores_sa = [], []
with open(log_sa_path, "r", encoding="utf-8") as f:
    for line in f:
        match = pattern_sa.search(line)
        if match:
            tiempos_sa.append(float(match.group(1)))
            mejores_sa.append(float(match.group(2)))
df_sa = pd.DataFrame({"Tiempo_min": tiempos_sa, "Fitness": mejores_sa, "Algoritmo": "Enfriamiento Simulado"})

df_ga.tail()

# Buscar los momentos de reinicio en el log GA
reinicio_pattern = re.compile(r"REINICIANDO POBLACIÓN.*Tiempo:\s+([\d.]+)m")
tiempos_reinicio = []

# Si el tiempo no aparece en esa línea, buscar la anterior que lo contenga
with open(log_ga_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if "REINICIANDO POBLACIÓN" in line:
            # Buscar hacia atrás la última línea con "Tiempo:"
            for j in range(i - 1, max(i - 10, 0), -1):
                match = re.search(r"Tiempo:\s+([\d.]+)m", lines[j])
                if match:
                    tiempos_reinicio.append(float(match.group(1)))
                    break

# --- Gráfico individual para el algoritmo genético con reinicios ---
plt.figure(figsize=(10, 6))
plt.plot(df_ga["Tiempo_min"], df_ga["Fitness"], color="blue", linewidth=2, label="Algoritmo Genético")
for i, t in enumerate(tiempos_reinicio):
    plt.axvline(x=t, color="red", linestyle="--", linewidth=1, label="Reinicio" if i == 0 else "")
plt.xlabel("Tiempo (minutos)")
plt.ylabel("Mejor Fitness histórico")
plt.title("Fitness vs Tiempo - Algoritmo Genético")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "GA_solo.png"), dpi=300, bbox_inches='tight')
plt.close()

# --- Gráfico comparativo con reinicios ---
plt.figure(figsize=(10, 6))
plt.plot(df_sa["Tiempo_min"], df_sa["Fitness"], color="green", label="Enfriamiento Simulado", linewidth=2)
plt.plot(df_ga["Tiempo_min"], df_ga["Fitness"], color="blue", label="Algoritmo Genético", linewidth=2)
for t in tiempos_reinicio:
    plt.axvline(x=t, color="red", linestyle="--", linewidth=1, label="Reinicio" if t == tiempos_reinicio[0] else "")
plt.xlabel("Tiempo (minutos)")
plt.ylabel("Mejor Fitness histórico")
plt.title("Comparación de Fitness - Enfriamiento Simulado vs Algoritmo Genético")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "GA_vs_SA.png"), dpi=300, bbox_inches='tight')
plt.close()

print(f"Gráficas guardadas en: {output_dir}")
print(f"- fitness_genetico.png")
print(f"- comparacion_fitness.png")
print(f"- fitness_genetico_reinicios.png")
print(f"- comparacion_fitness_reinicios.png")

tiempos_reinicio
