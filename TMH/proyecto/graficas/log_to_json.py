#!/usr/bin/env python3
"""
Script para convertir logs de Simulated Annealing a formato JSON estructurado.
Extrae toda la información relevante del log y la estructura en un JSON similar 
al generado por el algoritmo.
"""

import re
import json
from datetime import datetime
from pathlib import Path


def parse_sa_log_to_json(log_path):
    """
    Parsea un archivo de log de Simulated Annealing y genera un diccionario JSON.
    
    Args:
        log_path: Ruta al archivo .log
        
    Returns:
        dict: Diccionario con toda la información estructurada
    """
    
    with open(log_path, 'r', encoding='utf-8') as f:
        log_content = f.read()
    
    # Estructura base del JSON
    resultado = {
        "modo": None,
        "timestamp_inicio": None,
        "timestamp_fin": None,
        "configuracion": {
            "temperatura_inicial": None,
            "temperatura_minima": None,
            "tipo_enfriamiento": None,
            "max_tiempo_minutos": None,
            "max_iter_sin_mejora": None,
            "usar_2opt": None
        },
        "solucion_inicial": {
            "fitness": None,
            "puntos": None
        },
        "resultados": {
            "fitness_inicial": None,
            "fitness_final": None,
            "mejora_absoluta": None,
            "mejora_porcentual": None,
            "puntos_totales": None,
            "tiempo_total_horas": None,
            "distancia_total_km": None,
            "iteraciones_realizadas": None,
            "tiempo_ejecucion_minutos": None,
            "temperatura_final": None,
            "total_aceptaciones": None,
            "total_rechazos": None,
            "tasa_aceptacion": None,
            "mejoras_encontradas": None
        },
        "historial": {
            "mejor_fitness": [],
            "fitness_actual": [],
            "temperatura": [],
            "tiempo_minutos": [],
            "tasa_aceptacion": [],
            "iteraciones": []
        },
        "mejoras": [],
        "fases": []
    }
    
    # ==================== EXTRACCIÓN DE DATOS ====================
    
    # Timestamps
    match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', log_content)
    if match:
        resultado["timestamp_inicio"] = match.group(1)
    
    # Buscar último timestamp
    timestamps = re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', log_content)
    if timestamps:
        resultado["timestamp_fin"] = timestamps[-1]
    
    # Modo
    match = re.search(r'Modo (\d+):', log_content)
    if match:
        resultado["modo"] = int(match.group(1))
    
    # Configuración
    match = re.search(r'Temperatura inicial:\s*([\d.]+)', log_content)
    if match:
        resultado["configuracion"]["temperatura_inicial"] = float(match.group(1))
    
    match = re.search(r'Temperatura mínima:\s*([\d.]+)', log_content)
    if match:
        resultado["configuracion"]["temperatura_minima"] = float(match.group(1))
    
    match = re.search(r'Tipo de enfriamiento:\s*[^\n]*\s*(\w+)', log_content)
    if match:
        resultado["configuracion"]["tipo_enfriamiento"] = match.group(1)
    
    match = re.search(r'Máx\. tiempo:\s*([\d.]+)\s*minutos', log_content)
    if match:
        resultado["configuracion"]["max_tiempo_minutos"] = float(match.group(1))
    
    match = re.search(r'Máx\. iter\. sin mejora:\s*([\d,]+)', log_content)
    if match:
        resultado["configuracion"]["max_iter_sin_mejora"] = int(match.group(1).replace(',', ''))
    
    match = re.search(r'Usar optimización 2-opt:\s*[^\n]*\s*(SÍ|NO)', log_content)
    if match:
        resultado["configuracion"]["usar_2opt"] = (match.group(1) == "SÍ")
    
    # Solución inicial
    match = re.search(r'Solución inicial creada - Fitness:\s*([\d.]+),\s*Puntos:\s*(\d+)', log_content)
    if match:
        resultado["solucion_inicial"]["fitness"] = float(match.group(1))
        resultado["solucion_inicial"]["puntos"] = int(match.group(2))
    
    # Resultados finales
    match = re.search(r'Iteraciones realizadas:\s*([\d,]+)', log_content)
    if match:
        resultado["resultados"]["iteraciones_realizadas"] = int(match.group(1).replace(',', ''))
    
    match = re.search(r'Tiempo de ejecución:\s*([\d.]+)\s*minutos', log_content)
    if match:
        resultado["resultados"]["tiempo_ejecucion_minutos"] = float(match.group(1))
    
    match = re.search(r'Fitness inicial:\s*([\d.]+)', log_content, re.MULTILINE)
    if match:
        resultado["resultados"]["fitness_inicial"] = float(match.group(1))
    
    match = re.search(r'Fitness final:\s*([\d.]+)', log_content)
    if match:
        resultado["resultados"]["fitness_final"] = float(match.group(1))
    
    match = re.search(r'Mejora absoluta:\s*\+([\d.]+)', log_content)
    if match:
        resultado["resultados"]["mejora_absoluta"] = float(match.group(1))
    
    match = re.search(r'Mejora porcentual:\s*\+([\d.]+)%', log_content)
    if match:
        resultado["resultados"]["mejora_porcentual"] = float(match.group(1))
    
    match = re.search(r'Puntos totales:\s*(\d+)', log_content)
    if match:
        resultado["resultados"]["puntos_totales"] = int(match.group(1))
    
    match = re.search(r'Tiempo total:\s*([\d.]+)h', log_content)
    if match:
        resultado["resultados"]["tiempo_total_horas"] = float(match.group(1))
    
    match = re.search(r'Distancia total:\s*([\d.]+)km', log_content)
    if match:
        resultado["resultados"]["distancia_total_km"] = float(match.group(1))
    
    match = re.search(r'Temperatura final:\s*([\d.]+)', log_content)
    if match:
        resultado["resultados"]["temperatura_final"] = float(match.group(1))
    
    match = re.search(r'Total aceptaciones:\s*([\d,]+)\s*\(([\d.]+)%\)', log_content)
    if match:
        resultado["resultados"]["total_aceptaciones"] = int(match.group(1).replace(',', ''))
        resultado["resultados"]["tasa_aceptacion"] = float(match.group(2))
    
    match = re.search(r'Total rechazos:\s*([\d,]+)', log_content)
    if match:
        resultado["resultados"]["total_rechazos"] = int(match.group(1).replace(',', ''))
    
    match = re.search(r'Mejoras encontradas:\s*(\d+)', log_content)
    if match:
        resultado["resultados"]["mejoras_encontradas"] = int(match.group(1))
    
    # ==================== EXTRACCIÓN DE HISTORIAL ====================
    
    # Extraer líneas de progreso (cada 500 iteraciones)
    patron_progreso = r'Iter\s+(\d+)\s*\|\s*Tiempo:\s*([\d.]+)min.*?\|\s*T\s*=\s*([\d.]+)\s*\|\s*Fitness\s*=\s*([\d.]+)\s*\|\s*Mejor\s*=\s*([\d.]+)\s*\|\s*Aceptación\s*=\s*([\d.]+)%'
    
    for match in re.finditer(patron_progreso, log_content):
        iteracion = int(match.group(1))
        tiempo = float(match.group(2))
        temperatura = float(match.group(3))
        fitness_actual = float(match.group(4))
        mejor_fitness = float(match.group(5))
        tasa_acept = float(match.group(6))
        
        resultado["historial"]["iteraciones"].append(iteracion)
        resultado["historial"]["tiempo_minutos"].append(tiempo)
        resultado["historial"]["temperatura"].append(temperatura)
        resultado["historial"]["fitness_actual"].append(fitness_actual)
        resultado["historial"]["mejor_fitness"].append(mejor_fitness)
        resultado["historial"]["tasa_aceptacion"].append(tasa_acept)
    
    # ==================== EXTRACCIÓN DE MEJORAS ====================
    
    patron_mejora = r'🌟 MEJORA #(\d+) en iter (\d+): Fitness=([\d.]+) \(\+([\d.]+)\), Puntos=(\d+)'
    
    for match in re.finditer(patron_mejora, log_content):
        mejora_num = int(match.group(1))
        iteracion = int(match.group(2))
        fitness = float(match.group(3))
        incremento = float(match.group(4))
        puntos = int(match.group(5))
        
        resultado["mejoras"].append({
            "numero": mejora_num,
            "iteracion": iteracion,
            "fitness": fitness,
            "incremento": incremento,
            "puntos": puntos
        })
    
    # ==================== EXTRACCIÓN DE FASES ====================
    
    patron_fase = r'--- Cambiando a Fase:\s*([^\(]+)\s*\(([^\)]+)\)\s*\(Progreso:\s*([\d.]+)%\) ---'
    
    for match in re.finditer(patron_fase, log_content):
        fase_nombre = match.group(1).strip()
        fase_tipo = match.group(2).strip()
        progreso = float(match.group(3))
        
        resultado["fases"].append({
            "nombre": fase_nombre,
            "tipo": fase_tipo,
            "progreso": progreso
        })
    
    return resultado


def save_json(data, output_path):
    """Guarda el diccionario como JSON con formato legible."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON guardado en: {output_path}")


def main():
    """Función principal."""
    import sys
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        log_path = Path(sys.argv[1])
    else:
        # Ruta por defecto
        log_path = Path("../espana_expansion/logs/23_03_24_sa.log")
    
    if not log_path.exists():
        print(f"❌ Error: No se encontró el archivo {log_path}")
        print(f"\n💡 Uso: python log_to_json.py [ruta_al_log.log]")
        return
    
    print(f"📖 Leyendo log: {log_path}")
    
    # Parsear log
    resultado = parse_sa_log_to_json(log_path)
    
    # Generar nombre de salida
    log_name = log_path.stem  # 23_03_24_sa
    output_path = Path(f"./json_generados/{log_name}.json")
    output_path.parent.mkdir(exist_ok=True)
    
    # Guardar JSON
    save_json(resultado, output_path)
    
    # Mostrar resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN DEL LOG PROCESADO")
    print("=" * 80)
    print(f"Modo: {resultado['modo']}")
    print(f"Tiempo de ejecución: {resultado['resultados']['tiempo_ejecucion_minutos']:.2f} minutos")
    print(f"Iteraciones: {resultado['resultados']['iteraciones_realizadas']:,}")
    print(f"Fitness inicial: {resultado['resultados']['fitness_inicial']:.2f}")
    print(f"Fitness final: {resultado['resultados']['fitness_final']:.2f}")
    print(f"Mejora: +{resultado['resultados']['mejora_absoluta']:.2f} ({resultado['resultados']['mejora_porcentual']:.2f}%)")
    print(f"Mejoras encontradas: {resultado['resultados']['mejoras_encontradas']}")
    print(f"Puntos en historial: {len(resultado['historial']['mejor_fitness'])}")
    print(f"Fases detectadas: {len(resultado['fases'])}")
    print("=" * 80)


if __name__ == "__main__":
    main()
