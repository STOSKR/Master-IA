"""
Script para generar gráficas del algoritmo genético
Uso: python generar_graficas.py resultados_espana_modo1.json
"""

import json
import matplotlib.pyplot as plt
import sys

def cargar_resultados(archivo):
    """Carga los resultados desde el JSON"""
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def graficar_evolucion_fitness(resultados, output='evolucion_fitness.png'):
    """Gráfica de evolución del fitness a través de las generaciones"""
    historial_global = resultados['historial_fitness']
    historial_gen = resultados.get('historial_mejor_gen', historial_global)
    generaciones = range(len(historial_global))
    
    plt.figure(figsize=(14, 7))
    
    # Línea del mejor de cada generación (puede variar)
    plt.plot(generaciones, historial_gen, linewidth=1.5, color='#A23B72', 
             alpha=0.6, label='Mejor de cada generación')
    plt.fill_between(generaciones, historial_gen, alpha=0.2, color='#A23B72')
    
    # Línea del mejor global (siempre crece)
    plt.plot(generaciones, historial_global, linewidth=2.5, color='#2E86AB', 
             label='Mejor global (acumulado)', zorder=10)
    
    plt.title('Evolución del Fitness - Algoritmo Genético', fontsize=16, fontweight='bold')
    plt.xlabel('Generación', fontsize=12)
    plt.ylabel('Fitness', fontsize=12)
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    print(f"✅ Gráfica guardada: {output}")
    plt.close()

def graficar_metricas(resultados, output='metricas_globales.png'):
    """Gráfica de barras con las métricas globales"""
    metricas = {
        'Fitness': resultados['fitness'],
        'Puntos': resultados['puntos_totales'],
        'Tiempo (h)': resultados['tiempo_total_min'] / 60,
        'Distancia (km)': resultados['distancia_total_km']
    }
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    
    bars = ax.bar(metricas.keys(), metricas.values(), color=colores, alpha=0.8)
    
    # Añadir valores encima de las barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.title('Métricas Globales de la Mejor Solución', fontsize=16, fontweight='bold')
    plt.ylabel('Valor', fontsize=12)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    print(f"✅ Gráfica guardada: {output}")
    plt.close()

def graficar_ciudades_visitadas(resultados, output='ciudades_visitadas.png'):
    """Gráfica de pastel con las ciudades visitadas"""
    # Contar días por ciudad
    ciudades_dias = {}
    for item in resultados['itinerario']:
        ciudad = item['ciudad']
        ciudades_dias[ciudad] = ciudades_dias.get(ciudad, 0) + 1
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colores = plt.cm.Set3(range(len(ciudades_dias)))
    
    wedges, texts, autotexts = ax.pie(
        ciudades_dias.values(),
        labels=ciudades_dias.keys(),
        autopct='%1.1f%%',
        startangle=90,
        colors=colores,
        textprops={'fontsize': 11}
    )
    
    # Mejorar apariencia
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    plt.title(f'Distribución de Días por Ciudad ({resultados["num_dias"]} días totales)',
              fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    print(f"✅ Gráfica guardada: {output}")
    plt.close()

def graficar_lugares_por_dia(resultados, output='lugares_por_dia.png'):
    """Gráfica de barras con el número de lugares visitados por día"""
    dias = [item['dia'] for item in resultados['itinerario']]
    num_lugares = [item['num_lugares'] for item in resultados['itinerario']]
    
    plt.figure(figsize=(14, 6))
    plt.bar(dias, num_lugares, color='#2E86AB', alpha=0.8)
    plt.axhline(y=sum(num_lugares)/len(num_lugares), color='red', linestyle='--',
                label=f'Promedio: {sum(num_lugares)/len(num_lugares):.1f}')
    
    plt.title('Número de Lugares Visitados por Día', fontsize=16, fontweight='bold')
    plt.xlabel('Día', fontsize=12)
    plt.ylabel('Número de Lugares', fontsize=12)
    plt.legend()
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    print(f"✅ Gráfica guardada: {output}")
    plt.close()

def graficar_comparacion_generaciones(resultados, output='comparacion_generaciones.png'):
    """Gráfica comparando Gen 1, Gen 50, Gen 100, Gen final"""
    historial = resultados['historial_fitness']
    
    puntos_clave = [
        (1, historial[0], 'Gen 1'),
        (50, historial[49] if len(historial) > 49 else historial[-1], 'Gen 50'),
        (100, historial[99] if len(historial) > 99 else historial[-1], 'Gen 100'),
        (len(historial), historial[-1], f'Gen {len(historial)}')
    ]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    generaciones = [p[0] for p in puntos_clave]
    fitness_vals = [p[1] for p in puntos_clave]
    labels = [p[2] for p in puntos_clave]
    
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#06A77D']
    bars = ax.bar(range(len(puntos_clave)), fitness_vals, color=colors, alpha=0.8)
    ax.set_xticks(range(len(puntos_clave)))
    ax.set_xticklabels(labels)
    
    # Añadir valores
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.title('Comparación de Fitness en Generaciones Clave', fontsize=16, fontweight='bold')
    plt.ylabel('Fitness', fontsize=12)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    print(f"✅ Gráfica guardada: {output}")
    plt.close()

def generar_todas_graficas(archivo_resultados):
    """Genera todas las gráficas"""
    print(f"\n{'='*80}")
    print(f"📊 GENERANDO GRÁFICAS")
    print(f"{'='*80}\n")
    
    resultados = cargar_resultados(archivo_resultados)
    
    graficar_evolucion_fitness(resultados)
    graficar_metricas(resultados)
    graficar_ciudades_visitadas(resultados)
    graficar_lugares_por_dia(resultados)
    graficar_comparacion_generaciones(resultados)
    
    print(f"\n{'='*80}")
    print(f"✅ GRÁFICAS GENERADAS EXITOSAMENTE")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
    else:
        archivo = "resultados_espana_modo1.json"
    
    try:
        generar_todas_graficas(archivo)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{archivo}'")
        print(f"💡 Uso: python generar_graficas.py <archivo_resultados.json>")
    except Exception as e:
        print(f"❌ Error: {e}")
