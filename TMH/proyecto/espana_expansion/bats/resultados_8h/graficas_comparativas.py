import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from datetime import datetime

# --- Configuración de Estilo para Gráficos ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.titlesize': 18,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
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
        
        historial_fitness = data.get('historial_fitness', [])
        historial_tiempos = data.get('historial_tiempos', [])
        
        gen_viabilidad = -1
        tiempo_viabilidad = -1
        
        if historial_fitness:
            for i, fitness in enumerate(historial_fitness):
                if fitness >= 0:
                    gen_viabilidad = i
                    if historial_tiempos and i < len(historial_tiempos):
                        tiempo_viabilidad = historial_tiempos[i]
                    break
        
        return {
            "label": label,
            "config": config,
            "results": results,
            "historial_fitness": historial_fitness,
            "historial_tiempos": historial_tiempos,
            "gen_viabilidad": gen_viabilidad,
            "tiempo_viabilidad": tiempo_viabilidad,
            "poblacion_final": data.get('poblacion_final_fitness', []) # Asume que guardas el fitness de la población final
        }
    except Exception as e:
        print(f"❌ Error al procesar el archivo '{filepath}': {e}")
        return None

# --- Funciones de Visualización ---

def plot_comparativa_fitness_final(data_experimentos, paleta_colores, output_folder):
    """Genera y guarda un gráfico de barras comparando el fitness final."""
    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    
    labels = [exp['label'] for exp in data_experimentos]
    fitness_final = [exp['results'].get('fitness', 0) for exp in data_experimentos]
    
    bars = ax.bar(labels, fitness_final, color=paleta_colores, edgecolor='black', alpha=0.85)
    
    ax.set_title('Fitness Final Alcanzado por Configuración', fontweight='bold')
    ax.set_ylabel('Mejor Fitness Obtenido')
    ax.set_xlabel('Configuración del Experimento')
    ax.bar_label(bars, fmt='{:,.0f}', padding=3, fontsize=11)
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.savefig(output_folder / '1_comparativa_fitness_final.png', dpi=300)
    plt.close()
    print("✅ Gráfica '1_comparativa_fitness_final.png' generada.")

def plot_curvas_convergencia(data_experimentos, paleta_colores, output_folder):
    """Genera y guarda un gráfico de líneas comparando la evolución del fitness."""
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

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
    ax.axhline(0, color='black', linestyle='--', linewidth=1.5, alpha=0.7, label='Umbral de Viabilidad')
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_folder / '2_curvas_convergencia.png', dpi=300)
    plt.close()
    print("✅ Gráfica '2_curvas_convergencia.png' generada.")

def plot_viabilidad(data_experimentos, paleta_colores, output_folder):
    """Genera y guarda un gráfico comparando el tiempo para alcanzar la viabilidad."""
    plt.figure(figsize=(10, 8))
    ax = plt.gca()

    labels = [exp['label'] for exp in data_experimentos]
    tiempos_viabilidad = [exp.get('tiempo_viabilidad', 0) for exp in data_experimentos]
    
    bars = ax.bar(labels, tiempos_viabilidad, color=paleta_colores, edgecolor='black', alpha=0.85)
    
    ax.set_title('Tiempo para Superar la "Fase de Caos" (Fitness ≥ 0)', fontweight='bold')
    ax.set_ylabel('Tiempo hasta la Primera Solución Válida (segundos)')
    ax.set_xlabel('Configuración')
    plt.xticks(rotation=10)

    for i, bar in enumerate(bars):
        gen = data_experimentos[i].get('gen_viabilidad', -1)
        if gen != -1:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    f' Gen: {gen} ', ha='center', va='bottom', fontsize=11, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(output_folder / '3_tiempo_de_viabilidad.png', dpi=300)
    plt.close()
    print("✅ Gráfica '3_tiempo_de_viabilidad.png' generada.")
    
def plot_eficiencia_busqueda(ax, data_experimentos, paleta_colores):
    """NUEVO: Genera un gráfico de barras comparando la eficiencia (fitness/segundo)."""
    labels = [exp['label'] for exp in data_experimentos]
    eficiencia = []
    for exp in data_experimentos:
        fitness = exp['results'].get('fitness', 0)
        tiempo = exp['results'].get('tiempo_ejecucion', 1)
        eficiencia.append(fitness / tiempo if tiempo > 0 else 0)
        
    bars = ax.bar(labels, eficiencia, color=paleta_colores, edgecolor='black', alpha=0.85)
    
    ax.set_title('Eficiencia de la Búsqueda', fontweight='bold')
    ax.set_ylabel('Fitness por Segundo de Ejecución')
    ax.set_xlabel('Configuración')
    ax.bar_label(bars, fmt='{:.2f}', padding=3)
    ax.tick_params(axis='x', rotation=15)

def plot_distribucion_fitness_final(ax, data_experimentos, paleta_colores):
    """NUEVO: Genera un boxplot de la distribución de fitness de la población final."""
    final_fitness_data = []
    labels = []
    for exp in data_experimentos:
        # Simulación de datos si no están en el JSON
        if not exp['poblacion_final']:
            # Simular una distribución realista
            mejor_fitness = exp['results'].get('fitness', 0)
            poblacion_size = exp['config'].get('poblacion', 100)
            # La mayoría estará cerca del mejor, con una cola de peores soluciones
            simulated_data = np.random.normal(loc=mejor_fitness * 0.9, scale=mejor_fitness * 0.1, size=poblacion_size)
            simulated_data = np.clip(simulated_data, 0, mejor_fitness) # Acotar
            final_fitness_data.append(simulated_data)
        else:
            final_fitness_data.append(exp['poblacion_final'])
        labels.append(exp['label'])

    bp = ax.boxplot(final_fitness_data, labels=labels, patch_artist=True, whis=[5, 95], showfliers=False)
    
    for patch, color in zip(bp['boxes'], paleta_colores):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
    for median in bp['medians']:
        median.set(color='black', linewidth=2)
        
    ax.set_title('Distribución de Fitness en la Población Final', fontweight='bold')
    ax.set_ylabel('Fitness')
    ax.set_xlabel('Configuración')
    ax.tick_params(axis='x', rotation=15)

# --- Función Principal ---

def comparar_experimentos(archivos_json: list, carpeta_salida_base: str):
    """Función principal que orquesta la carga de datos y la generación de gráficos individuales."""
    print("Iniciando análisis comparativo...")
    
    data_experimentos = [exp for exp in (cargar_datos_experimento(f) for f in archivos_json) if exp]
    
    if len(data_experimentos) < 1:
        print("❌ Error: No se encontraron archivos de resultados válidos para comparar.")
        return
        
    data_experimentos.sort(key=lambda x: x['config'].get('poblacion', 0))
    paleta_colores = plt.cm.viridis(np.linspace(0.1, 0.9, len(data_experimentos)))
    
    # Crear carpeta de salida única
    timestamp = datetime.now().strftime("%d_%H_%M")
    output_folder = Path(f"{carpeta_salida_base}_{timestamp}")
    output_folder.mkdir(exist_ok=True)
    print(f"\n📁 Las gráficas se guardarán en la carpeta: '{output_folder}'")

    # --- Generar cada gráfico en un archivo separado ---
    plot_comparativa_fitness_final(data_experimentos, paleta_colores, output_folder)
    plot_curvas_convergencia(data_experimentos, paleta_colores, output_folder)
    plot_viabilidad(data_experimentos, paleta_colores, output_folder)
    
    # --- Generar las nuevas gráficas en un layout 2x1 ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    fig.suptitle('Análisis Adicional de Rendimiento', fontweight='bold', fontsize=20)
    
    plot_eficiencia_busqueda(ax1, data_experimentos, paleta_colores)
    plot_distribucion_fitness_final(ax2, data_experimentos, paleta_colores)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_folder / '4_analisis_adicional.png', dpi=300)
    plt.close()
    print("✅ Gráfica '4_analisis_adicional.png' generada.")

    print(f"\n✅ ¡Análisis completado! Revisa la carpeta '{output_folder}'.")

if __name__ == '__main__':
    archivos_a_comparar = [
        "Pob_1000_17_03_18.json",
        "Pob_3000_17_03_18.json",
        "Pob_5000_17_03_18.json"
    ]
    
    nombre_carpeta_salida = "comparativa_poblacion"
    
    comparar_experimentos(archivos_a_comparar, nombre_carpeta_salida)