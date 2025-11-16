"""
Script para monitorear el progreso de las ejecuciones en tiempo real
Muestra una tabla actualizada con el estado de cada configuración
"""

import os
import json
import glob
import time
from datetime import datetime
import sys


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def cargar_ultimo_resultado(directorio):
    """Carga el resultado más reciente de un directorio"""
    archivos = glob.glob(f"{directorio}/*.json")
    if not archivos:
        return None
    
    # Ordenar por fecha de modificación
    archivo_reciente = max(archivos, key=os.path.getmtime)
    
    try:
        with open(archivo_reciente, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            datos['archivo'] = os.path.basename(archivo_reciente)
            datos['modificacion'] = datetime.fromtimestamp(os.path.getmtime(archivo_reciente))
            return datos
    except:
        return None


def contar_archivos(directorio):
    """Cuenta archivos JSON en un directorio"""
    if not os.path.exists(directorio):
        return 0
    return len(glob.glob(f"{directorio}/*.json"))


def mostrar_progreso():
    """Muestra tabla de progreso de todas las ejecuciones"""
    
    directorios = {
        'Mutación': 'resultados_mutacion',
        'Cruce': 'resultados_cruce',
        'Combinaciones': 'resultados_combinaciones',
        'Comparativa': 'resultados_comparativa',
        'Elitismo': 'resultados_elitismo',
        'Población': 'resultados_poblacion'
    }
    
    limpiar_pantalla()
    
    print("="*120)
    print(" "*40 + "MONITOR DE PROGRESO - EXPERIMENTOS AG")
    print("="*120)
    print(f"Actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*120)
    print()
    
    # Tabla de estado
    print(f"{'Categoría':<20} {'Resultados':>12} {'Último Fitness':>15} {'Última Actualización':>25}")
    print("-"*120)
    
    total_resultados = 0
    
    for categoria, directorio in directorios.items():
        num_archivos = contar_archivos(directorio)
        total_resultados += num_archivos
        
        ultimo = cargar_ultimo_resultado(directorio)
        
        if ultimo:
            fitness = ultimo.get('resultados', {}).get('fitness', 0)
            hora = ultimo['modificacion'].strftime('%H:%M:%S')
            
            print(f"{categoria:<20} {num_archivos:>12} {fitness:>15.1f} {hora:>25}")
        else:
            print(f"{categoria:<20} {num_archivos:>12} {'N/A':>15} {'N/A':>25}")
    
    print("-"*120)
    print(f"{'TOTAL':<20} {total_resultados:>12}")
    print("="*120)
    print()
    
    # Mejores resultados por categoría
    print("MEJORES RESULTADOS POR CATEGORÍA:")
    print("-"*120)
    
    for categoria, directorio in directorios.items():
        archivos = glob.glob(f"{directorio}/*.json")
        if not archivos:
            continue
        
        mejores = []
        for archivo in archivos:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    mejores.append({
                        'nombre': datos.get('nombre', 'Unknown'),
                        'fitness': datos.get('resultados', {}).get('fitness', 0),
                        'puntos': datos.get('resultados', {}).get('puntos', 0)
                    })
            except:
                continue
        
        if mejores:
            mejor = max(mejores, key=lambda x: x['fitness'])
            print(f"{categoria:<20} → {mejor['nombre']:<25} "
                  f"Fitness: {mejor['fitness']:>10.1f}  Puntos: {mejor['puntos']:>5}")
    
    print("="*120)
    print()
    print("💡 Presiona CTRL+C para salir")
    print("🔄 Actualizando cada 30 segundos...")


def monitorear(intervalo=30):
    """Monitorea continuamente el progreso"""
    try:
        while True:
            mostrar_progreso()
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("\n\n✅ Monitoreo finalizado")
        sys.exit(0)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitorear progreso de experimentos')
    parser.add_argument('--intervalo', type=int, default=30,
                       help='Intervalo de actualización en segundos (default: 30)')
    
    args = parser.parse_args()
    
    print("\n🚀 Iniciando monitor de progreso...")
    print(f"📊 Actualizando cada {args.intervalo} segundos\n")
    
    time.sleep(2)
    monitorear(args.intervalo)
