"""
Script para analizar y comparar resultados de diferentes configuraciones
Genera gráficas comparativas de fitness, convergencia y métricas
"""

import json
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def cargar_resultados(directorio):
    """Carga todos los archivos JSON de un directorio"""
    resultados = []
    archivos = glob.glob(f"{directorio}/*.json")
    
    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                datos['archivo'] = os.path.basename(archivo)
                resultados.append(datos)
        except Exception as e:
            print(f"⚠️  Error al cargar {archivo}: {e}")
    
    return resultados


def grafica_comparacion_convergencia(resultados, titulo, output_file):
    """Genera gráfica comparando la convergencia de diferentes configuraciones"""
    plt.figure(figsize=(14, 8))
    
    for res in resultados:
        nombre = res.get('nombre', res.get('archivo', 'Unknown'))
        historial = res.get('historial_fitness', [])
        
        if historial:
            plt.plot(historial, linewidth=2, label=nombre, alpha=0.8)
    
    plt.xlabel('Generación', fontsize=13)
    plt.ylabel('Fitness', fontsize=13)
    plt.title(titulo, fontsize=15, fontweight='bold')
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfica guardada: {output_file}")
    plt.close()


def grafica_comparacion_metricas(resultados, titulo, output_file):
    """Genera gráfica de barras comparando métricas finales"""
    nombres = [res.get('nombre', res.get('archivo', 'Unknown')) for res in resultados]
    fitness_valores = [res.get('resultados', {}).get('fitness', 0) for res in resultados]
    puntos_valores = [res.get('resultados', {}).get('puntos', 0) for res in resultados]
    distancia_valores = [res.get('resultados', {}).get('distancia', 0) for res in resultados]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Fitness
    axes[0, 0].bar(range(len(nombres)), fitness_valores, color='steelblue', alpha=0.8)
    axes[0, 0].set_xticks(range(len(nombres)))
    axes[0, 0].set_xticklabels(nombres, rotation=45, ha='right', fontsize=9)
    axes[0, 0].set_ylabel('Fitness', fontsize=12)
    axes[0, 0].set_title('Fitness Final', fontsize=13, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # Añadir valores sobre las barras
    for i, v in enumerate(fitness_valores):
        axes[0, 0].text(i, v, f'{v:.0f}', ha='center', va='bottom', fontsize=9)
    
    # Puntos
    axes[0, 1].bar(range(len(nombres)), puntos_valores, color='green', alpha=0.8)
    axes[0, 1].set_xticks(range(len(nombres)))
    axes[0, 1].set_xticklabels(nombres, rotation=45, ha='right', fontsize=9)
    axes[0, 1].set_ylabel('Puntos', fontsize=12)
    axes[0, 1].set_title('Puntos Totales', fontsize=13, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    for i, v in enumerate(puntos_valores):
        axes[0, 1].text(i, v, f'{v:.0f}', ha='center', va='bottom', fontsize=9)
    
    # Distancia
    axes[1, 0].bar(range(len(nombres)), distancia_valores, color='orange', alpha=0.8)
    axes[1, 0].set_xticks(range(len(nombres)))
    axes[1, 0].set_xticklabels(nombres, rotation=45, ha='right', fontsize=9)
    axes[1, 0].set_ylabel('Distancia (km)', fontsize=12)
    axes[1, 0].set_title('Distancia Total', fontsize=13, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    for i, v in enumerate(distancia_valores):
        axes[1, 0].text(i, v, f'{v:.0f}', ha='center', va='bottom', fontsize=9)
    
    # Fitness por segundo
    fitness_por_segundo = [res.get('resultados', {}).get('fitness_por_segundo', 0) for res in resultados]
    axes[1, 1].bar(range(len(nombres)), fitness_por_segundo, color='purple', alpha=0.8)
    axes[1, 1].set_xticks(range(len(nombres)))
    axes[1, 1].set_xticklabels(nombres, rotation=45, ha='right', fontsize=9)
    axes[1, 1].set_ylabel('Fitness/segundo', fontsize=12)
    axes[1, 1].set_title('Eficiencia (Fitness por segundo)', fontsize=13, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    for i, v in enumerate(fitness_por_segundo):
        axes[1, 1].text(i, v, f'{v:.2f}', ha='center', va='bottom', fontsize=9)
    
    plt.suptitle(titulo, fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfica guardada: {output_file}")
    plt.close()


def tabla_comparativa(resultados):
    """Imprime tabla comparativa de resultados"""
    print("\n" + "="*120)
    print("TABLA COMPARATIVA DE RESULTADOS")
    print("="*120)
    
    # Encabezados
    print(f"{'Configuración':<25} {'Fitness':>10} {'Puntos':>10} {'Distancia':>12} "
          f"{'Tiempo(m)':>10} {'Gens':>8} {'Fit/s':>10}")
    print("-"*120)
    
    for res in resultados:
        nombre = res.get('nombre', res.get('archivo', 'Unknown'))[:24]
        fitness = res.get('resultados', {}).get('fitness', 0)
        puntos = res.get('resultados', {}).get('puntos', 0)
        distancia = res.get('resultados', {}).get('distancia', 0)
        tiempo = res.get('resultados', {}).get('tiempo_ejecucion', 0) / 60
        gens = res.get('resultados', {}).get('generaciones_ejecutadas', 0)
        fit_s = res.get('resultados', {}).get('fitness_por_segundo', 0)
        
        print(f"{nombre:<25} {fitness:>10.1f} {puntos:>10.0f} {distancia:>12.1f} "
              f"{tiempo:>10.2f} {gens:>8} {fit_s:>10.2f}")
    
    print("="*120 + "\n")


def analizar_parametros_mutacion_cruce(resultados):
    """Análisis específico para configuraciones de mutación y cruce"""
    print("\n" + "="*100)
    print("ANÁLISIS DE PARÁMETROS (MUTACIÓN Y CRUCE)")
    print("="*100)
    
    for res in resultados:
        nombre = res.get('nombre', 'Unknown')
        config = res.get('configuracion', {})
        resultado = res.get('resultados', {})
        
        prob_mut = config.get('prob_mutacion', 'N/A')
        prob_cruce = config.get('prob_cruce', 'N/A')
        fitness = resultado.get('fitness', 0)
        
        print(f"\n{nombre}:")
        print(f"  Mutación: {prob_mut*100 if isinstance(prob_mut, float) else 'N/A'}%")
        print(f"  Cruce: {prob_cruce*100 if isinstance(prob_cruce, float) else 'N/A'}%")
        print(f"  Fitness: {fitness:.1f}")
        print(f"  Generaciones: {resultado.get('generaciones_ejecutadas', 'N/A')}")
    
    print("\n" + "="*100 + "\n")


def generar_informe_completo(directorio, nombre_analisis, output_dir="analisis_comparativos"):
    """Genera informe completo con todas las gráficas y análisis"""
    
    print(f"\n{'='*100}")
    print(f"GENERANDO INFORME: {nombre_analisis}")
    print(f"{'='*100}\n")
    
    # Cargar resultados
    resultados = cargar_resultados(directorio)
    
    if not resultados:
        print(f"❌ No se encontraron resultados en {directorio}")
        return
    
    print(f"✅ Cargados {len(resultados)} resultados\n")
    
    # Crear directorio de salida
    os.makedirs(output_dir, exist_ok=True)
    
    # Ordenar por fitness
    resultados.sort(key=lambda x: x.get('resultados', {}).get('fitness', 0), reverse=True)
    
    # Generar gráficas
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    grafica_comparacion_convergencia(
        resultados,
        f"Comparación de Convergencia - {nombre_analisis}",
        f"{output_dir}/{timestamp}_convergencia_{nombre_analisis}.png"
    )
    
    grafica_comparacion_metricas(
        resultados,
        f"Comparación de Métricas - {nombre_analisis}",
        f"{output_dir}/{timestamp}_metricas_{nombre_analisis}.png"
    )
    
    # Tabla comparativa
    tabla_comparativa(resultados)
    
    # Análisis de parámetros (si aplica)
    if any('prob_mutacion' in res.get('configuracion', {}) for res in resultados):
        analizar_parametros_mutacion_cruce(resultados)
    
    # Guardar ranking en JSON
    ranking_file = f"{output_dir}/{timestamp}_ranking_{nombre_analisis}.json"
    ranking = [
        {
            'posicion': i+1,
            'nombre': res.get('nombre', 'Unknown'),
            'fitness': res.get('resultados', {}).get('fitness', 0),
            'puntos': res.get('resultados', {}).get('puntos', 0),
            'distancia': res.get('resultados', {}).get('distancia', 0),
            'configuracion': res.get('configuracion', {})
        }
        for i, res in enumerate(resultados)
    ]
    
    with open(ranking_file, 'w', encoding='utf-8') as f:
        json.dump(ranking, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Ranking guardado: {ranking_file}")
    
    print(f"\n{'='*100}")
    print(f"INFORME COMPLETADO: {nombre_analisis}")
    print(f"Archivos generados en: {output_dir}/")
    print(f"{'='*100}\n")


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analizar y comparar resultados de configuraciones')
    parser.add_argument('--directorio', type=str, required=True,
                       help='Directorio con archivos JSON de resultados')
    parser.add_argument('--nombre', type=str, required=True,
                       help='Nombre del análisis')
    parser.add_argument('--output-dir', type=str, default='analisis_comparativos',
                       help='Directorio para guardar análisis (default: analisis_comparativos)')
    
    args = parser.parse_args()
    
    generar_informe_completo(args.directorio, args.nombre, args.output_dir)


if __name__ == "__main__":
    main()
