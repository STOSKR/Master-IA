#!/usr/bin/env python3
"""
Script para analizar y comparar por pares los resultados de diferentes 
temperaturas iniciales en el algoritmo de Enfriamiento Simulado.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import re


def cargar_json(ruta):
    """Carga un archivo JSON y extrae información relevante."""
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extraer configuración
    config = data.get("configuracion", {})
    temp_inicial = config.get("T_inicial", config.get("temperatura_inicial", None))
    
    # Extraer estadísticas
    stats = data.get("estadisticas", data.get("resultados", {}))
    
    # Extraer historial
    historial = data.get("historial", {})
    mejor_fitness = historial.get("mejor_fitness", [])
    
    # Generar timestamps sintéticos si no existen
    tiempo_total = stats.get("tiempo_ejecucion_minutos", 240.0)
    if historial.get("tiempo_minutos"):
        tiempos = historial["tiempo_minutos"]
    else:
        # Generar tiempos lineales
        num_puntos = len(mejor_fitness)
        tiempos = [i * tiempo_total / max(num_puntos - 1, 1) for i in range(num_puntos)]
    
    return {
        "temperatura": temp_inicial,
        "fitness_final": stats.get("fitness_final", 0),
        "fitness_inicial": stats.get("fitness_inicial", 0),
        "mejora_porcentual": stats.get("mejora_porcentual", 0),
        "iteraciones": stats.get("iteraciones_realizadas", 0),
        "tiempo_minutos": tiempo_total,
        "mejoras_encontradas": stats.get("mejoras_encontradas", 0),
        "tasa_aceptacion": stats.get("tasa_aceptacion", stats.get("tasa_aceptacion_pct", 0)),
        "historial_fitness": mejor_fitness,
        "historial_tiempo": tiempos,
        "archivo": ruta.name
    }


def generar_grafica_comparativa(datos_a, datos_b, output_dir="./graficas_generadas"):
    """
    Genera una gráfica comparativa entre dos configuraciones de temperatura.
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    temp_a = datos_a["temperatura"]
    temp_b = datos_b["temperatura"]
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Sincronizar longitudes
    tiempos_a = datos_a["historial_tiempo"]
    fitness_a = datos_a["historial_fitness"]
    min_len_a = min(len(tiempos_a), len(fitness_a))
    tiempos_a = tiempos_a[:min_len_a]
    fitness_a = fitness_a[:min_len_a]
    
    tiempos_b = datos_b["historial_tiempo"]
    fitness_b = datos_b["historial_fitness"]
    min_len_b = min(len(tiempos_b), len(fitness_b))
    tiempos_b = tiempos_b[:min_len_b]
    fitness_b = fitness_b[:min_len_b]
    
    # Graficar ambas evoluciones
    ax.plot(tiempos_a, fitness_a, 
            label=f'T={temp_a} (Fitness: {datos_a["fitness_final"]:.2f})',
            linewidth=2.5, color='#2E86AB', alpha=0.9)
    
    ax.plot(tiempos_b, fitness_b,
            label=f'T={temp_b} (Fitness: {datos_b["fitness_final"]:.2f})',
            linewidth=2.5, color='#A23B72', alpha=0.9)
    
    # Configuración
    ax.set_xlabel('Tiempo (minutos)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Fitness', fontsize=14, fontweight='bold')
    ax.set_title(f'Comparación: Temperatura {temp_a} vs {temp_b}\nEnfriamiento Simulado', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=12, loc='lower right', framealpha=0.95)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, 240)  # Limitar a 240 minutos (4 horas)
    
    plt.tight_layout()
    
    # Guardar
    nombre_archivo = f"comparacion_T{temp_a}_vs_T{temp_b}.png"
    output_path = Path(output_dir) / nombre_archivo
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Gráfica guardada: {nombre_archivo}")


def generar_tabla_comparativa(todos_datos, output_dir="./graficas_generadas"):
    """Genera una tabla comparativa con todas las configuraciones."""
    Path(output_dir).mkdir(exist_ok=True)
    
    # Ordenar por temperatura
    todos_datos_sorted = sorted(todos_datos, key=lambda x: x["temperatura"])
    
    fig, ax = plt.subplots(figsize=(16, len(todos_datos_sorted) * 0.8 + 2))
    ax.axis('tight')
    ax.axis('off')
    
    # Crear tabla
    headers = ['Temp.', 'Fitness\nFinal', 'Fitness\nInicial', 'Mejora\n%', 
               'Iteraciones', 'Mejoras', 'Tasa\nAcept. %']
    
    tabla_data = []
    for datos in todos_datos_sorted:
        fila = [
            f"{datos['temperatura']:.1f}",
            f"{datos['fitness_final']:.2f}",
            f"{datos['fitness_inicial']:.2f}",
            f"{datos['mejora_porcentual']:.2f}%",
            f"{datos['iteraciones']:,}",
            f"{datos['mejoras_encontradas']}",
            f"{datos['tasa_aceptacion']:.2f}%"
        ]
        tabla_data.append(fila)
    
    # Crear la tabla
    table = ax.table(cellText=tabla_data, colLabels=headers,
                     cellLoc='center', loc='center',
                     colWidths=[0.08, 0.12, 0.12, 0.10, 0.15, 0.10, 0.12])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    # Estilo de encabezados
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor('#2E86AB')
        cell.set_text_props(weight='bold', color='white', fontsize=12)
    
    # Estilo de filas (alternar colores)
    for i in range(1, len(tabla_data) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#F0F0F0')
            else:
                cell.set_facecolor('#FFFFFF')
    
    # Resaltar mejor fitness
    mejor_idx = max(range(len(todos_datos_sorted)), 
                    key=lambda i: todos_datos_sorted[i]["fitness_final"])
    
    for j in range(len(headers)):
        cell = table[(mejor_idx + 1, j)]
        cell.set_facecolor('#90EE90')
        cell.set_text_props(weight='bold')
    
    plt.title('Comparación de Temperaturas Iniciales - Enfriamiento Simulado',
              fontsize=16, fontweight='bold', pad=20)
    
    # Guardar
    output_path = Path(output_dir) / "tabla_comparativa_temperaturas.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Tabla comparativa guardada: tabla_comparativa_temperaturas.png")


def generar_grafica_todas(todos_datos, output_dir="./graficas_generadas"):
    """Genera una gráfica con todas las evoluciones juntas."""
    Path(output_dir).mkdir(exist_ok=True)
    
    # Ordenar por temperatura
    todos_datos_sorted = sorted(todos_datos, key=lambda x: x["temperatura"])
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Colores para cada temperatura
    colores = ['#E63946', '#F77F00', '#06D6A0', '#118AB2', '#073B4C', '#A23B72']
    
    for i, datos in enumerate(todos_datos_sorted):
        tiempos = datos["historial_tiempo"]
        fitness = datos["historial_fitness"]
        min_len = min(len(tiempos), len(fitness))
        tiempos = tiempos[:min_len]
        fitness = fitness[:min_len]
        
        temp = datos["temperatura"]
        fitness_final = datos["fitness_final"]
        
        ax.plot(tiempos, fitness,
                label=f'T={temp} (Fitness: {fitness_final:.2f})',
                linewidth=2.5, color=colores[i % len(colores)], alpha=0.85)
    
    ax.set_xlabel('Tiempo (minutos)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Fitness', fontsize=14, fontweight='bold')
    ax.set_title('Comparación Global: Todas las Temperaturas\nEnfriamiento Simulado',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='lower right', framealpha=0.95)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, 240)
    
    plt.tight_layout()
    
    output_path = Path(output_dir) / "comparacion_todas_temperaturas.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Gráfica global guardada: comparacion_todas_temperaturas.png")


def main():
    """Función principal."""
    data_dir = Path("./data/temperatura")
    
    # Buscar archivos JSON (excluir el generado por log_to_json.py)
    archivos = sorted([f for f in data_dir.glob("*.json") 
                      if f.name.startswith("resultados_")])
    
    if len(archivos) < 2:
        print(f"❌ Error: Se necesitan al menos 2 archivos JSON para comparar.")
        print(f"   Encontrados: {len(archivos)} en {data_dir}")
        return
    
    print(f"\n{'='*80}")
    print(f"📊 ANÁLISIS COMPARATIVO DE TEMPERATURAS")
    print(f"{'='*80}")
    print(f"Directorio: {data_dir}")
    print(f"Archivos encontrados: {len(archivos)}")
    print(f"{'='*80}\n")
    
    # Cargar todos los datos
    todos_datos = []
    for archivo in archivos:
        print(f"📖 Cargando: {archivo.name}")
        datos = cargar_json(archivo)
        todos_datos.append(datos)
        print(f"   T_inicial = {datos['temperatura']}, Fitness = {datos['fitness_final']:.2f}")
    
    print(f"\n{'='*80}")
    print(f"📈 GENERANDO GRÁFICAS COMPARATIVAS POR PARES")
    print(f"{'='*80}\n")
    
    # Generar comparaciones por pares
    comparaciones = 0
    for i in range(len(todos_datos)):
        for j in range(i + 1, len(todos_datos)):
            print(f"Comparando T={todos_datos[i]['temperatura']} vs T={todos_datos[j]['temperatura']}")
            generar_grafica_comparativa(todos_datos[i], todos_datos[j])
            comparaciones += 1
    
    print(f"\n  Total de comparaciones por pares: {comparaciones}")
    
    print(f"\n{'='*80}")
    print(f"📊 GENERANDO GRÁFICA GLOBAL")
    print(f"{'='*80}\n")
    
    # Generar gráfica con todas las temperaturas
    generar_grafica_todas(todos_datos)
    
    print(f"\n{'='*80}")
    print(f"📋 GENERANDO TABLA COMPARATIVA")
    print(f"{'='*80}\n")
    
    # Generar tabla comparativa
    generar_tabla_comparativa(todos_datos)
    
    # Resumen final
    print(f"\n{'='*80}")
    print(f"✅ ANÁLISIS COMPLETADO")
    print(f"{'='*80}")
    print(f"Configuraciones analizadas: {len(todos_datos)}")
    print(f"Comparaciones por pares: {comparaciones}")
    print(f"Gráficas generadas: {comparaciones + 2}")  # pares + global + tabla
    
    # Mostrar mejor configuración
    mejor = max(todos_datos, key=lambda x: x["fitness_final"])
    print(f"\n🏆 MEJOR CONFIGURACIÓN:")
    print(f"   Temperatura inicial: {mejor['temperatura']}")
    print(f"   Fitness final: {mejor['fitness_final']:.2f}")
    print(f"   Mejora: {mejor['mejora_porcentual']:.2f}%")
    print(f"   Iteraciones: {mejor['iteraciones']:,}")
    print(f"   Tasa aceptación: {mejor['tasa_aceptacion']:.2f}%")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
