import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

# --- Configuración de Estilo para Gráficos ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.titlesize': 16,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 11,
    'figure.titlesize': 22,
    'figure.facecolor': '#f4f4f4',
})

# --- Funciones de Carga y Procesamiento ---

def cargar_datos_experimento(filepath: str):
    """Carga y extrae los datos relevantes de un archivo JSON de resultados."""
    if not os.path.exists(filepath):
        print(f"⚠️  Advertencia: No se encontró el archivo '{filepath}'. Se omitirá.")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        config = data.get('configuracion', {})
        results = data.get('resultados', {})
        label = f"Pob={config.get('poblacion', 'N/A')}"
        
        # --- NUEVO: Calcular métricas de viabilidad ---
        historial_fitness = data.get('historial_fitness', [])
        historial_tiempos = data.get('historial_tiempos', [])
        
        gen_viabilidad = -1
        tiempo_viabilidad = -1
        
        if historial_fitness and historial_tiempos:
            for i, fitness in enumerate(historial_fitness):
                if fitness >= 0:
                    gen_viabilidad = i
                    # Asegurarse de que el índice no esté fuera de los límites de tiempo
                    if i < len(historial_tiempos):
                        tiempo_viabilidad = historial_tiempos[i]
                    else:
                        # Estimar si el array de tiempos es más corto
                        tiempo_viabilidad = historial_tiempos[-1]
                    break
        
        return {
            "label": label,
            "filepath": filepath,
            "config": config,
            "results": results,
            "historial_fitness": historial_fitness,
            "historial_tiempos": historial_tiempos,
            "gen_viabilidad": gen_viabilidad,
            "tiempo_viabilidad": tiempo_viabilidad
        }
    except Exception as e:
        print(f"❌ Error al procesar el archivo '{filepath}': {e}")
        return None

# --- Funciones de Visualización ---

def plot_comparativa_fitness_final(ax, data_experimentos, paleta_colores):
    """Genera un gráfico de barras comparando el fitness final."""
    labels = [exp['label'] for exp in data_experimentos]
    fitness_final = [exp['results'].get('fitness', 0) for exp in data_experimentos]
    
    bars = ax.bar(labels, fitness_final, color=paleta_colores, edgecolor='black', alpha=0.8)
    
    ax.set_title('Fitness Final Alcanzado', fontweight='bold')
    ax.set_ylabel('Mejor Fitness')
    ax.set_xlabel('Configuración')
    ax.bar_label(bars, fmt='{:,.0f}', padding=3)
    ax.tick_params(axis='x', rotation=15)

def plot_curvas_convergencia(ax, data_experimentos, paleta_colores):
    """Genera un gráfico de líneas comparando la evolución del fitness por generación."""
    ax.set_title('Curvas de Convergencia por Generación', fontweight='bold')
    ax.set_xlabel('Número de Generaciones')
    ax.set_ylabel('Mejor Fitness')

    max_generaciones = 0
    for i, exp in enumerate(data_experimentos):
        historial = exp.get('historial_fitness', [])
        if not historial: continue
        
        generaciones = np.arange(len(historial))
        ax.plot(generaciones, historial, label=exp['label'], color=paleta_colores[i], linewidth=2.5, alpha=0.9)
        max_generaciones = max(max_generaciones, len(generaciones))

    ax.legend(title="Experimentos")
    ax.set_xlim(0, max_generaciones)
    ax.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.7) # Línea de viabilidad

def plot_viabilidad(ax, data_experimentos, paleta_colores):
    """NUEVA FUNCIÓN: Genera un gráfico para comparar el tiempo y generaciones para alcanzar viabilidad (fitness >= 0)."""
    labels = [exp['label'] for exp in data_experimentos]
    tiempos_viabilidad = [exp.get('tiempo_viabilidad', 0) for exp in data_experimentos]
    
    bars = ax.bar(labels, tiempos_viabilidad, color=paleta_colores, edgecolor='black', alpha=0.8)
    
    ax.set_title('Tiempo para Superar la "Fase de Caos"', fontweight='bold')
    ax.set_ylabel('Tiempo (segundos)')
    ax.set_xlabel('Configuración')
    ax.tick_params(axis='x', rotation=15)
    
    # Añadir anotaciones con el número de generaciones
    for i, bar in enumerate(bars):
        gen = data_experimentos[i].get('gen_viabilidad', -1)
        if gen != -1:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    f'Gen: {gen}', ha='center', va='bottom', fontsize=10, fontweight='bold')

def plot_metricas_resultados(ax, data_experimentos, paleta_colores):
    """Genera un gráfico de barras agrupadas para Puntos y Distancia."""
    labels = [exp['label'] for exp in data_experimentos]
    puntos = [exp['results'].get('puntos', 0) for exp in data_experimentos]
    distancia = [exp['results'].get('distancia', 0) for exp in data_experimentos]
    
    x = np.arange(len(labels))
    width = 0.35
    
    ax.set_title('Puntos vs. Distancia de la Mejor Ruta', fontweight='bold')
    ax.set_ylabel('Puntos Totales Acumulados', color='tab:blue')
    bars1 = ax.bar(x - width/2, puntos, width, label='Puntos', color=[c for c in paleta_colores], edgecolor='black', alpha=0.8)
    ax.tick_params(axis='y', labelcolor='tab:blue')
    ax.bar_label(bars1, padding=3, fmt='{:,.0f}')
    
    ax2 = ax.twinx()
    ax2.set_ylabel('Distancia Total (km)', color='tab:red')
    bars2 = ax2.bar(x + width/2, distancia, width, label='Distancia', color=[c for c in paleta_colores], edgecolor='darkred', hatch='///', alpha=0.6)
    ax2.tick_params(axis='y', labelcolor='tab:red')
    ax2.bar_label(bars2, padding=3, fmt='{:.1f}')
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

# --- Función Principal ---

def comparar_experimentos(archivos_json: list, archivo_salida: str):
    """Función principal que orquesta la carga y la visualización."""
    print("Iniciando análisis comparativo...")
    
    data_experimentos = [exp for exp in (cargar_datos_experimento(f) for f in archivos_json) if exp]
    
    if len(data_experimentos) < 1:
        print("❌ Error: No se encontraron archivos de resultados válidos para comparar.")
        return

    data_experimentos.sort(key=lambda x: x['config'].get('poblacion', 0))
    paleta_colores = plt.cm.viridis(np.linspace(0.1, 0.9, len(data_experimentos)))

    fig, axes = plt.subplots(2, 2, figsize=(20, 15))
    fig.suptitle('Análisis Comparativo de Experimentos del Algoritmo Genético', fontweight='bold')

    # Generar cada uno de los gráficos
    plot_comparativa_fitness_final(axes[0, 0], data_experimentos, paleta_colores)
    plot_curvas_convergencia(axes[0, 1], data_experimentos, paleta_colores)
    plot_viabilidad(axes[1, 0], data_experimentos, paleta_colores) # Nueva gráfica
    plot_metricas_resultados(axes[1, 1], data_experimentos, paleta_colores)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    try:
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"\n✅ ¡Análisis completado! Gráfica guardada como '{archivo_salida}'")
    except Exception as e:
        print(f"\n❌ Error al guardar la gráfica: {e}")
    
    plt.close()


if __name__ == '__main__':
    archivos_a_comparar = [
        "Pob_1000_17_03_18.json",
        "Pob_3000_17_03_18.json",
        "Pob_5000_17_03_18.json"
    ]
    
    nombre_grafica_salida = "comparativa_experimentos.png"
    
    comparar_experimentos(archivos_a_comparar, nombre_grafica_salida)
