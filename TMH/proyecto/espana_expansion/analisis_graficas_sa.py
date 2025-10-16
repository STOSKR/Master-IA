"""
Análisis y Generación de Gráficas para Enfriamiento Simulado
Genera visualizaciones detalladas de los resultados del algoritmo SA
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11


def crear_carpeta_resultados(base_nombre: str) -> Path:
    """
    Crea una carpeta con timestamp para guardar los resultados.
    
    Args:
        base_nombre: Nombre base del archivo de resultados
    
    Returns:
        Path de la carpeta creada
    """
    timestamp = datetime.now().strftime("%d_%H_%M")
    carpeta = Path(f"es_{base_nombre}_{timestamp}")
    carpeta.mkdir(exist_ok=True)
    return carpeta


def cargar_resultados(archivo_json: str) -> dict:
    """
    Carga los resultados del enfriamiento simulado desde un archivo JSON.
    
    Args:
        archivo_json: Ruta al archivo JSON con los resultados
    
    Returns:
        Diccionario con los resultados
    """
    with open(archivo_json, 'r', encoding='utf-8') as f:
        return json.load(f)


def grafica_evolucion_fitness(resultados: dict, carpeta: Path):
    """
    Genera gráfica de la evolución del fitness durante el enfriamiento simulado.
    Muestra tanto el fitness actual como el mejor fitness.
    """
    historial = resultados['historial']
    fitness_actual = historial['fitness_actual']
    mejor_fitness = historial['mejor_fitness']
    stats = resultados['estadisticas']
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    iteraciones = range(len(fitness_actual))
    
    # Línea del fitness actual (puede subir y bajar)
    ax.plot(iteraciones, fitness_actual, 
            color='steelblue', alpha=0.6, linewidth=1, 
            label='Fitness actual')
    
    # Línea del mejor fitness (siempre crece o se mantiene)
    ax.plot(iteraciones, mejor_fitness, 
            color='darkgreen', linewidth=2, 
            label='Mejor fitness global')
    
    # Marcar fitness inicial y final
    ax.axhline(y=stats['fitness_inicial'], 
              color='red', linestyle='--', alpha=0.5, 
              label=f'Fitness inicial: {stats["fitness_inicial"]:.1f}')
    
    ax.axhline(y=stats['fitness_final'], 
              color='green', linestyle='--', alpha=0.5, 
              label=f'Fitness final: {stats["fitness_final"]:.1f}')
    
    ax.set_xlabel('Iteración')
    ax.set_ylabel('Fitness')
    ax.set_title('Evolución del Fitness - Enfriamiento Simulado')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    # Añadir texto con estadísticas
    textstr = f'Iteraciones: {stats["iteraciones_realizadas"]}\n'
    textstr += f'Mejora: {stats["mejora_absoluta"]:+.1f} ({stats["mejora_porcentual"]:+.2f}%)\n'
    textstr += f'Mejoras encontradas: {stats["mejoras_encontradas"]}\n'
    textstr += f'Tasa aceptación: {stats["tasa_aceptacion"]:.1f}%'
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.savefig(carpeta / 'evolucion_fitness.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gráfica guardada: evolucion_fitness.png")


def grafica_temperatura(resultados: dict, carpeta: Path):
    """
    Genera gráfica de la evolución de la temperatura durante el enfriamiento.
    """
    historial = resultados['historial']
    temperatura = historial['temperatura']
    stats = resultados['estadisticas']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    iteraciones = range(len(temperatura))
    
    # Gráfica 1: Temperatura en escala lineal
    ax1.plot(iteraciones, temperatura, color='orangered', linewidth=2)
    ax1.set_xlabel('Iteración')
    ax1.set_ylabel('Temperatura')
    ax1.set_title('Evolución de la Temperatura (Escala Lineal)')
    ax1.grid(True, alpha=0.3)
    
    # Marcar temperatura final
    ax1.axhline(y=stats['temperatura_final'], 
               color='blue', linestyle='--', alpha=0.5,
               label=f'T final: {stats["temperatura_final"]:.4f}')
    ax1.legend()
    
    # Gráfica 2: Temperatura en escala logarítmica
    ax2.plot(iteraciones, temperatura, color='orangered', linewidth=2)
    ax2.set_xlabel('Iteración')
    ax2.set_ylabel('Temperatura (log)')
    ax2.set_title('Evolución de la Temperatura (Escala Logarítmica)')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig(carpeta / 'evolucion_temperatura.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gráfica guardada: evolucion_temperatura.png")


def grafica_fitness_vs_temperatura(resultados: dict, carpeta: Path):
    """
    Genera gráfica de correlación entre fitness y temperatura.
    """
    historial = resultados['historial']
    fitness_actual = historial['fitness_actual']
    temperatura = historial['temperatura']
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Scatter plot con degradado de color según iteración
    scatter = ax.scatter(temperatura, fitness_actual, 
                        c=range(len(fitness_actual)), 
                        cmap='viridis', alpha=0.6, s=20)
    
    ax.set_xlabel('Temperatura')
    ax.set_ylabel('Fitness')
    ax.set_title('Relación Fitness vs Temperatura')
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3)
    
    # Barra de color para mostrar progreso temporal
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Iteración')
    
    plt.tight_layout()
    plt.savefig(carpeta / 'fitness_vs_temperatura.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gráfica guardada: fitness_vs_temperatura.png")


def grafica_aceptaciones(resultados: dict, carpeta: Path):
    """
    Genera gráfica de aceptaciones y rechazos.
    """
    stats = resultados['estadisticas']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfica 1: Pie chart de aceptaciones vs rechazos
    labels = ['Aceptaciones', 'Rechazos']
    sizes = [stats['total_aceptaciones'], stats['total_rechazos']]
    colors = ['lightgreen', 'lightcoral']
    explode = (0.05, 0)
    
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.set_title('Distribución de Aceptaciones vs Rechazos')
    
    # Gráfica 2: Barras con estadísticas
    categorias = ['Total\nIteraciones', 'Aceptaciones', 'Rechazos', 'Mejoras\nEncontradas']
    valores = [
        stats['iteraciones_realizadas'],
        stats['total_aceptaciones'],
        stats['total_rechazos'],
        stats['mejoras_encontradas']
    ]
    colores_barras = ['steelblue', 'lightgreen', 'lightcoral', 'gold']
    
    bars = ax2.bar(categorias, valores, color=colores_barras, alpha=0.7)
    ax2.set_ylabel('Cantidad')
    ax2.set_title('Estadísticas de Ejecución')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores sobre las barras
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(carpeta / 'estadisticas_aceptaciones.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gráfica guardada: estadisticas_aceptaciones.png")


def grafica_distribucion_ciudades(resultados: dict, carpeta: Path):
    """
    Genera gráfica de la distribución de ciudades visitadas.
    """
    mejor_solucion = resultados['mejor_solucion']
    itinerario = mejor_solucion['itinerario']
    
    # Contar días por ciudad
    ciudades_contador = {}
    for dia in itinerario:
        ciudad = dia['ciudad']
        ciudades_contador[ciudad] = ciudades_contador.get(ciudad, 0) + 1
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfica 1: Barras horizontales
    ciudades = list(ciudades_contador.keys())
    dias_por_ciudad = list(ciudades_contador.values())
    
    y_pos = np.arange(len(ciudades))
    colors = plt.cm.Set3(np.linspace(0, 1, len(ciudades)))
    
    bars = ax1.barh(y_pos, dias_por_ciudad, color=colors, alpha=0.8)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(ciudades)
    ax1.set_xlabel('Número de días')
    ax1.set_title('Días por Ciudad')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Añadir valores
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width)} días',
                ha='left', va='center', fontweight='bold')
    
    # Gráfica 2: Pie chart
    ax2.pie(dias_por_ciudad, labels=ciudades, autopct='%1.1f%%',
            colors=colors, shadow=True, startangle=90)
    ax2.set_title('Distribución Porcentual de Días')
    
    plt.tight_layout()
    plt.savefig(carpeta / 'distribucion_ciudades.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gráfica guardada: distribucion_ciudades.png")


def grafica_metricas_solucion(resultados: dict, carpeta: Path):
    """
    Genera gráfica con las métricas principales de la solución.
    """
    mejor_solucion = resultados['mejor_solucion']
    inicial = resultados['solucion_inicial']
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Gráfica 1: Comparación Inicial vs Final - Fitness
    categorias = ['Solución\nInicial', 'Solución\nFinal']
    fitness_vals = [inicial['fitness'], mejor_solucion['fitness']]
    colors = ['lightcoral', 'lightgreen']
    
    bars = ax1.bar(categorias, fitness_vals, color=colors, alpha=0.7)
    ax1.set_ylabel('Fitness')
    ax1.set_title('Comparación de Fitness')
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom' if height > 0 else 'top', 
                fontweight='bold')
    
    # Gráfica 2: Comparación Inicial vs Final - Puntos
    puntos_vals = [inicial['puntos_totales'], mejor_solucion['puntos_totales']]
    
    bars = ax2.bar(categorias, puntos_vals, color=colors, alpha=0.7)
    ax2.set_ylabel('Puntos Totales')
    ax2.set_title('Comparación de Puntos')
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    # Gráfica 3: Métricas de la mejor solución
    metricas = ['Tiempo\nTotal (h)', 'Distancia\nTotal (km)', 'Ciudades\nVisitadas', 'Días\nTotales']
    valores = [
        mejor_solucion['tiempo_total_min'] / 60,
        mejor_solucion['distancia_total_km'],
        len(mejor_solucion['ciudades_visitadas']),
        mejor_solucion['num_dias']
    ]
    colors_metricas = ['skyblue', 'orange', 'lightgreen', 'plum']
    
    bars = ax3.bar(metricas, valores, color=colors_metricas, alpha=0.7)
    ax3.set_ylabel('Valor')
    ax3.set_title('Métricas de la Mejor Solución')
    ax3.grid(True, alpha=0.3, axis='y')
    
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontweight='bold')
    
    # Gráfica 4: Lugares por día
    itinerario = mejor_solucion['itinerario']
    dias = [f"D{dia['dia']}" for dia in itinerario]
    lugares_por_dia = [dia['num_lugares'] for dia in itinerario]
    
    ax4.bar(range(len(dias)), lugares_por_dia, color='steelblue', alpha=0.7)
    ax4.set_xlabel('Día')
    ax4.set_ylabel('Número de Lugares')
    ax4.set_title('Lugares Visitados por Día')
    ax4.set_xticks(range(len(dias)))
    ax4.set_xticklabels(dias, rotation=45)
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.axhline(y=np.mean(lugares_por_dia), color='red', linestyle='--', 
                alpha=0.5, label=f'Promedio: {np.mean(lugares_por_dia):.1f}')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig(carpeta / 'metricas_solucion.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gráfica guardada: metricas_solucion.png")


def grafica_convergencia(resultados: dict, carpeta: Path):
    """
    Genera gráfica de análisis de convergencia del algoritmo.
    """
    historial = resultados['historial']
    mejor_fitness = historial['mejor_fitness']
    stats = resultados['estadisticas']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    iteraciones = range(len(mejor_fitness))
    
    # Gráfica 1: Mejor fitness con zonas de mejora
    ax1.plot(iteraciones, mejor_fitness, color='darkgreen', linewidth=2)
    ax1.fill_between(iteraciones, mejor_fitness, alpha=0.3, color='green')
    ax1.set_xlabel('Iteración')
    ax1.set_ylabel('Mejor Fitness')
    ax1.set_title('Convergencia del Algoritmo')
    ax1.grid(True, alpha=0.3)
    
    # Marcar mejoras
    mejoras = []
    for i in range(1, len(mejor_fitness)):
        if mejor_fitness[i] > mejor_fitness[i-1]:
            mejoras.append(i)
    
    if mejoras:
        ax1.scatter(mejoras, [mejor_fitness[i] for i in mejoras],
                   color='red', s=50, zorder=5, label='Mejoras encontradas')
        ax1.legend()
    
    # Gráfica 2: Diferencia entre iteraciones (velocidad de mejora)
    diferencias = [mejor_fitness[i] - mejor_fitness[i-1] for i in range(1, len(mejor_fitness))]
    
    ax2.plot(range(1, len(mejor_fitness)), diferencias, 
            color='purple', linewidth=1, alpha=0.7)
    ax2.fill_between(range(1, len(mejor_fitness)), diferencias, 
                     alpha=0.3, color='purple')
    ax2.set_xlabel('Iteración')
    ax2.set_ylabel('Δ Fitness')
    ax2.set_title('Velocidad de Mejora (Diferencia entre iteraciones)')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig(carpeta / 'analisis_convergencia.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gráfica guardada: analisis_convergencia.png")


def generar_reporte_texto(resultados: dict, carpeta: Path):
    """
    Genera un reporte en texto plano con las estadísticas principales.
    """
    stats = resultados['estadisticas']
    mejor_solucion = resultados['mejor_solucion']
    inicial = resultados['solucion_inicial']
    
    reporte = []
    reporte.append("="*80)
    reporte.append("REPORTE DE ENFRIAMIENTO SIMULADO")
    reporte.append("="*80)
    reporte.append("")
    
    reporte.append("CONFIGURACIÓN Y EJECUCIÓN:")
    reporte.append("-" * 80)
    reporte.append(f"Iteraciones realizadas:       {stats['iteraciones_realizadas']:,}")
    reporte.append(f"Temperatura inicial:          {resultados['historial']['temperatura'][0]:.2f}")
    reporte.append(f"Temperatura final:            {stats['temperatura_final']:.6f}")
    reporte.append(f"Total de aceptaciones:        {stats['total_aceptaciones']:,} ({stats['tasa_aceptacion']:.2f}%)")
    reporte.append(f"Total de rechazos:            {stats['total_rechazos']:,}")
    reporte.append(f"Mejoras encontradas:          {stats['mejoras_encontradas']}")
    reporte.append("")
    
    reporte.append("RESULTADOS DE FITNESS:")
    reporte.append("-" * 80)
    reporte.append(f"Fitness inicial:              {stats['fitness_inicial']:.2f}")
    reporte.append(f"Fitness final:                {stats['fitness_final']:.2f}")
    reporte.append(f"Mejora absoluta:              {stats['mejora_absoluta']:+.2f}")
    reporte.append(f"Mejora porcentual:            {stats['mejora_porcentual']:+.2f}%")
    reporte.append("")
    
    reporte.append("MÉTRICAS DE LA SOLUCIÓN:")
    reporte.append("-" * 80)
    reporte.append(f"Puntos iniciales:             {inicial['puntos_totales']:,}")
    reporte.append(f"Puntos finales:               {mejor_solucion['puntos_totales']:,}")
    reporte.append(f"Diferencia de puntos:         {mejor_solucion['puntos_totales'] - inicial['puntos_totales']:+,}")
    reporte.append(f"Tiempo total:                 {mejor_solucion['tiempo_total_min']/60:.2f} horas")
    reporte.append(f"Distancia total:              {mejor_solucion['distancia_total_km']:.2f} km")
    reporte.append(f"Días totales:                 {mejor_solucion['num_dias']}")
    reporte.append(f"Ciudades visitadas:           {len(mejor_solucion['ciudades_visitadas'])}")
    reporte.append("")
    
    reporte.append("CIUDADES VISITADAS:")
    reporte.append("-" * 80)
    for ciudad in mejor_solucion['ciudades_visitadas']:
        reporte.append(f"  • {ciudad}")
    reporte.append("")
    
    reporte.append("DISTRIBUCIÓN POR CIUDAD:")
    reporte.append("-" * 80)
    ciudades_contador = {}
    for dia in mejor_solucion['itinerario']:
        ciudad = dia['ciudad']
        ciudades_contador[ciudad] = ciudades_contador.get(ciudad, 0) + 1
    
    for ciudad, dias in sorted(ciudades_contador.items(), key=lambda x: x[1], reverse=True):
        porcentaje = (dias / mejor_solucion['num_dias']) * 100
        reporte.append(f"  {ciudad:20s} : {dias:2d} días ({porcentaje:5.1f}%)")
    reporte.append("")
    
    reporte.append("="*80)
    reporte.append(f"Reporte generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    reporte.append("="*80)
    
    # Guardar reporte
    with open(carpeta / 'reporte_estadisticas.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(reporte))
    
    print(f"✓ Reporte guardado: reporte_estadisticas.txt")
    
    # También imprimir en consola
    print("\n" + '\n'.join(reporte))


def generar_todas_graficas(archivo_json: str):
    """
    Genera todas las gráficas y reportes del enfriamiento simulado.
    
    Args:
        archivo_json: Ruta al archivo JSON con los resultados
    """
    print(f"\n{'='*80}")
    print(f"GENERACIÓN DE GRÁFICAS - ENFRIAMIENTO SIMULADO")
    print(f"{'='*80}\n")
    
    # Cargar resultados
    print(f"📂 Cargando resultados desde: {archivo_json}")
    resultados = cargar_resultados(archivo_json)
    
    # Crear carpeta para guardar resultados
    base_nombre = Path(archivo_json).stem
    carpeta = crear_carpeta_resultados(base_nombre)
    print(f"📁 Carpeta de salida: {carpeta}\n")
    
    print(f"🎨 Generando gráficas...\n")
    
    # Generar todas las gráficas
    try:
        grafica_evolucion_fitness(resultados, carpeta)
        grafica_temperatura(resultados, carpeta)
        grafica_fitness_vs_temperatura(resultados, carpeta)
        grafica_aceptaciones(resultados, carpeta)
        grafica_distribucion_ciudades(resultados, carpeta)
        grafica_metricas_solucion(resultados, carpeta)
        grafica_convergencia(resultados, carpeta)
        
        print(f"\n📊 Generando reporte de texto...\n")
        generar_reporte_texto(resultados, carpeta)
        
        print(f"\n{'='*80}")
        print(f"✅ GENERACIÓN COMPLETADA EXITOSAMENTE")
        print(f"{'='*80}")
        print(f"\n📁 Todos los archivos guardados en: {carpeta.absolute()}")
        print(f"📈 Total de gráficas generadas: 7")
        print(f"📄 Reporte de estadísticas: reporte_estadisticas.txt\n")
        
    except Exception as e:
        print(f"\n❌ ERROR al generar gráficas: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"\n{'='*80}")
        print(f"USO: python analisis_graficas_sa.py <archivo_resultados.json>")
        print(f"{'='*80}\n")
        print(f"Ejemplos:")
        print(f"  python analisis_graficas_sa.py resultados_sa_standalone.json")
        print(f"  python analisis_graficas_sa.py resultados_sa_hybrid.json")
        print(f"  python analisis_graficas_sa.py resultados_sa_custom.json\n")
        sys.exit(1)
    
    archivo_json = sys.argv[1]
    
    if not Path(archivo_json).exists():
        print(f"\n❌ ERROR: El archivo '{archivo_json}' no existe.\n")
        sys.exit(1)
    
    exito = generar_todas_graficas(archivo_json)
    sys.exit(0 if exito else 1)
