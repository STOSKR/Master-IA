"""
Sistema de Análisis y Visualización para Resultados España
===========================================================
Genera gráficas y mapas interactivos a partir de resultados del algoritmo genético
"""

import json
import folium
from folium import plugins
from datetime import datetime
import os

# Importar utilidades
from utils_espana import get_lugar_por_id, distancia_haversine

# Try to import plotting libraries
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  Matplotlib no disponible - se omitirán algunas gráficas")

# Colores por ciudad para visualización
COLORES_CIUDADES = {
    "Madrid": "#FF0000",        # Rojo
    "Barcelona": "#0000FF",     # Azul
    "Sevilla": "#FFA500",       # Naranja
    "Valencia": "#800080",      # Púrpura
    "Granada": "#008000",       # Verde
    "Bilbao": "#FF69B4",        # Rosa
    "Toledo": "#8B4513",        # Marrón
    "Córdoba": "#00CED1",       # Turquesa
    "San Sebastián": "#FFD700", # Dorado
    "Santiago": "#4B0082"       # Índigo
}

# Iconos por tipo de lugar
ICONOS_TIPO = {
    "museo": "university",
    "palacio": "home",
    "catedral": "church",
    "parque": "tree",
    "playa": "umbrella",
    "restaurante": "cutlery",
    "bar": "glass",
    "tienda": "shopping-cart",
    "cafetería": "coffee",
    "plaza": "star",
    "mirador": "eye",
    "turistico": "camera"
}


def cargar_resultados(archivo_json):
    """Carga resultados del algoritmo genético"""
    with open(archivo_json, 'r', encoding='utf-8') as f:
        return json.load(f)


def analizar_evolucion_fitness(resultados):
    """Analiza la evolución del fitness a lo largo de las generaciones"""
    evolucion = resultados.get('evolucion_fitness', resultados.get('evolucion', []))
    
    if not evolucion:
        print("⚠️  No hay datos de evolución de fitness en el archivo JSON")
        print("💡 Para incluir evolución, modifica ejecutar_espana.py para guardar historial")
        return
    
    generaciones = [e['generacion'] for e in evolucion]
    fitness_mejor = [e['fitness_mejor'] for e in evolucion]
    fitness_promedio = [e['fitness_promedio'] for e in evolucion]
    fitness_peor = [e['fitness_peor'] for e in evolucion]
    
    plt.figure(figsize=(14, 8))
    
    # Gráfica principal
    plt.subplot(2, 2, 1)
    plt.plot(generaciones, fitness_mejor, 'g-', linewidth=2, label='Mejor')
    plt.plot(generaciones, fitness_promedio, 'b--', linewidth=1.5, label='Promedio')
    plt.plot(generaciones, fitness_peor, 'r:', linewidth=1, label='Peor')
    plt.xlabel('Generación', fontsize=11)
    plt.ylabel('Fitness', fontsize=11)
    plt.title('Evolución del Fitness', fontsize=13, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Mejora por generación
    plt.subplot(2, 2, 2)
    mejoras = [fitness_mejor[i] - fitness_mejor[i-1] if i > 0 else 0 
               for i in range(len(fitness_mejor))]
    plt.bar(generaciones, mejoras, color='green', alpha=0.6, edgecolor='darkgreen')
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.xlabel('Generación', fontsize=11)
    plt.ylabel('Mejora', fontsize=11)
    plt.title('Mejora por Generación', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Diversidad (diferencia mejor-peor)
    plt.subplot(2, 2, 3)
    diversidad = [fitness_mejor[i] - fitness_peor[i] for i in range(len(fitness_mejor))]
    plt.fill_between(generaciones, diversidad, alpha=0.4, color='purple')
    plt.plot(generaciones, diversidad, 'purple', linewidth=2)
    plt.xlabel('Generación', fontsize=11)
    plt.ylabel('Rango Fitness', fontsize=11)
    plt.title('Diversidad de Población (Mejor - Peor)', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Estadísticas finales
    plt.subplot(2, 2, 4)
    plt.axis('off')
    stats_text = f"""
    ESTADÍSTICAS DE EVOLUCIÓN
    {'='*35}
    
    Fitness Inicial:     {fitness_mejor[0]:.1f}
    Fitness Final:       {fitness_mejor[-1]:.1f}
    Mejora Total:        {fitness_mejor[-1] - fitness_mejor[0]:.1f}
    Mejora Porcentual:   {((fitness_mejor[-1] - fitness_mejor[0]) / abs(fitness_mejor[0]) * 100):.2f}%
    
    Promedio Inicial:    {fitness_promedio[0]:.1f}
    Promedio Final:      {fitness_promedio[-1]:.1f}
    
    Generaciones:        {len(generaciones)}
    Mejor Generación:    {generaciones[fitness_mejor.index(max(fitness_mejor))]}
    Mayor Mejora:        {max(mejoras):.1f} (gen {generaciones[mejoras.index(max(mejoras))]})
    """
    plt.text(0.1, 0.5, stats_text, fontsize=10, family='monospace',
             verticalalignment='center')
    
    plt.tight_layout()
    plt.savefig('evolucion_fitness_espana.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfica guardada: evolucion_fitness_espana.png")
    plt.close()


def analizar_distribucion_por_ciudades(resultados):
    """Analiza la distribución de días y lugares por ciudad"""
    # Adaptado para el formato actual del JSON
    itinerario = resultados.get('itinerario', [])
    
    if not itinerario:
        print("⚠️  No hay itinerario en los resultados")
        return
    
    # Extraer días y ciudades del itinerario
    dias = [dia_info['lugares_ids'] for dia_info in itinerario]
    ciudades = [dia_info['ciudad'] for dia_info in itinerario]
    
    # Contar días y lugares por ciudad
    dias_por_ciudad = {}
    lugares_por_ciudad = {}
    puntos_por_ciudad = {}
    
    for dia_idx, (dia_lugares, ciudad) in enumerate(zip(dias, ciudades)):
        if ciudad not in dias_por_ciudad:
            dias_por_ciudad[ciudad] = 0
            lugares_por_ciudad[ciudad] = 0
            puntos_por_ciudad[ciudad] = 0
        
        dias_por_ciudad[ciudad] += 1
        lugares_por_ciudad[ciudad] += len(dia_lugares)
        
        for lugar_id in dia_lugares:
            lugar = get_lugar_por_id(lugar_id)
            if lugar:
                puntos_por_ciudad[ciudad] += lugar['puntos']
    
    ciudades_visitadas = sorted(dias_por_ciudad.keys())
    
    plt.figure(figsize=(16, 10))
    
    # Días por ciudad
    plt.subplot(2, 3, 1)
    colores = [COLORES_CIUDADES.get(c, '#808080') for c in ciudades_visitadas]
    plt.bar(range(len(ciudades_visitadas)), 
            [dias_por_ciudad[c] for c in ciudades_visitadas],
            color=colores, edgecolor='black', linewidth=1.5)
    plt.xlabel('Ciudad', fontsize=11)
    plt.ylabel('Días', fontsize=11)
    plt.title('Días por Ciudad', fontsize=13, fontweight='bold')
    plt.xticks(range(len(ciudades_visitadas)), ciudades_visitadas, rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Lugares por ciudad
    plt.subplot(2, 3, 2)
    plt.bar(range(len(ciudades_visitadas)),
            [lugares_por_ciudad[c] for c in ciudades_visitadas],
            color=colores, edgecolor='black', linewidth=1.5)
    plt.xlabel('Ciudad', fontsize=11)
    plt.ylabel('Lugares visitados', fontsize=11)
    plt.title('Lugares Visitados por Ciudad', fontsize=13, fontweight='bold')
    plt.xticks(range(len(ciudades_visitadas)), ciudades_visitadas, rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Puntos por ciudad
    plt.subplot(2, 3, 3)
    plt.bar(range(len(ciudades_visitadas)),
            [puntos_por_ciudad[c] for c in ciudades_visitadas],
            color=colores, edgecolor='black', linewidth=1.5)
    plt.xlabel('Ciudad', fontsize=11)
    plt.ylabel('Puntos totales', fontsize=11)
    plt.title('Puntos Turísticos por Ciudad', fontsize=13, fontweight='bold')
    plt.xticks(range(len(ciudades_visitadas)), ciudades_visitadas, rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Distribución porcentual (pie chart)
    plt.subplot(2, 3, 4)
    plt.pie([dias_por_ciudad[c] for c in ciudades_visitadas],
            labels=ciudades_visitadas,
            colors=colores,
            autopct='%1.1f%%',
            startangle=90)
    plt.title('Distribución de Días (%)', fontsize=13, fontweight='bold')
    
    # Eficiencia (puntos por día)
    plt.subplot(2, 3, 5)
    eficiencia = [puntos_por_ciudad[c] / dias_por_ciudad[c] for c in ciudades_visitadas]
    plt.barh(range(len(ciudades_visitadas)), eficiencia, color=colores, 
             edgecolor='black', linewidth=1.5)
    plt.ylabel('Ciudad', fontsize=11)
    plt.xlabel('Puntos por día', fontsize=11)
    plt.title('Eficiencia por Ciudad (Puntos/Día)', fontsize=13, fontweight='bold')
    plt.yticks(range(len(ciudades_visitadas)), ciudades_visitadas)
    plt.grid(True, alpha=0.3, axis='x')
    
    # Tabla resumen
    plt.subplot(2, 3, 6)
    plt.axis('off')
    tabla_data = []
    for ciudad in ciudades_visitadas:
        tabla_data.append([
            ciudad,
            f"{dias_por_ciudad[ciudad]}",
            f"{lugares_por_ciudad[ciudad]}",
            f"{puntos_por_ciudad[ciudad]}",
            f"{puntos_por_ciudad[ciudad]/dias_por_ciudad[ciudad]:.1f}"
        ])
    
    tabla = plt.table(cellText=tabla_data,
                      colLabels=['Ciudad', 'Días', 'Lugares', 'Puntos', 'Pts/Día'],
                      cellLoc='center',
                      loc='center',
                      colWidths=[0.25, 0.12, 0.15, 0.15, 0.15])
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 2)
    
    # Colorear encabezados
    for i in range(5):
        tabla[(0, i)].set_facecolor('#4472C4')
        tabla[(0, i)].set_text_props(weight='bold', color='white')
    
    plt.title('Resumen por Ciudad', fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('distribucion_ciudades_espana.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfica guardada: distribucion_ciudades_espana.png")
    plt.close()


def analizar_metricas_diarias(resultados):
    """Analiza métricas día por día"""
    # Adaptado para el formato actual del JSON
    itinerario = resultados.get('itinerario', [])
    
    if not itinerario:
        print("⚠️  No hay itinerario en los resultados")
        return
    
    dias = [dia_info['lugares_ids'] for dia_info in itinerario]
    ciudades = [dia_info['ciudad'] for dia_info in itinerario]
    
    num_lugares = []
    puntos_dia = []
    distancias_dia = []
    tiempos_dia = []
    
    for dia_lugares in dias:
        num_lugares.append(len(dia_lugares))
        
        puntos = 0
        distancia = 0
        tiempo = 0
        
        lugares_objs = [get_lugar_por_id(lid) for lid in dia_lugares]
        
        for lugar in lugares_objs:
            if lugar:
                puntos += lugar['puntos']
                tiempo += lugar['tiempo_visita']
        
        for i in range(len(lugares_objs) - 1):
            if lugares_objs[i] and lugares_objs[i+1]:
                distancia += distancia_haversine(lugares_objs[i], lugares_objs[i+1])
        
        puntos_dia.append(puntos)
        distancias_dia.append(distancia)
        tiempos_dia.append(tiempo / 60)  # Convertir a horas
    
    dias_nums = list(range(1, len(dias) + 1))
    
    plt.figure(figsize=(16, 10))
    
    # Puntos por día
    plt.subplot(2, 2, 1)
    colores_dias = [COLORES_CIUDADES.get(c, '#808080') for c in ciudades]
    plt.bar(dias_nums, puntos_dia, color=colores_dias, edgecolor='black', linewidth=1)
    plt.axhline(y=np.mean(puntos_dia), color='red', linestyle='--', 
                linewidth=2, label=f'Media: {np.mean(puntos_dia):.1f}')
    plt.xlabel('Día', fontsize=11)
    plt.ylabel('Puntos', fontsize=11)
    plt.title('Puntos Turísticos por Día', fontsize=13, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    # Distancia por día
    plt.subplot(2, 2, 2)
    plt.bar(dias_nums, distancias_dia, color=colores_dias, edgecolor='black', linewidth=1)
    plt.axhline(y=np.mean(distancias_dia), color='red', linestyle='--',
                linewidth=2, label=f'Media: {np.mean(distancias_dia):.1f} km')
    plt.xlabel('Día', fontsize=11)
    plt.ylabel('Distancia (km)', fontsize=11)
    plt.title('Distancia Recorrida por Día', fontsize=13, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    # Tiempo por día
    plt.subplot(2, 2, 3)
    plt.bar(dias_nums, tiempos_dia, color=colores_dias, edgecolor='black', linewidth=1)
    plt.axhline(y=np.mean(tiempos_dia), color='red', linestyle='--',
                linewidth=2, label=f'Media: {np.mean(tiempos_dia):.1f} h')
    plt.xlabel('Día', fontsize=11)
    plt.ylabel('Tiempo (horas)', fontsize=11)
    plt.title('Tiempo de Visitas por Día', fontsize=13, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    # Número de lugares por día
    plt.subplot(2, 2, 4)
    plt.bar(dias_nums, num_lugares, color=colores_dias, edgecolor='black', linewidth=1)
    plt.axhline(y=np.mean(num_lugares), color='red', linestyle='--',
                linewidth=2, label=f'Media: {np.mean(num_lugares):.1f}')
    plt.xlabel('Día', fontsize=11)
    plt.ylabel('Número de lugares', fontsize=11)
    plt.title('Lugares Visitados por Día', fontsize=13, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    # Añadir leyenda de ciudades
    handles = [plt.Rectangle((0,0),1,1, color=COLORES_CIUDADES.get(c, '#808080')) 
               for c in set(ciudades)]
    labels = list(set(ciudades))
    plt.figlegend(handles, labels, loc='lower center', ncol=len(labels), 
                  bbox_to_anchor=(0.5, -0.05), fontsize=10)
    
    plt.tight_layout()
    plt.savefig('metricas_diarias_espana.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfica guardada: metricas_diarias_espana.png")
    plt.close()


def crear_mapa_interactivo(resultados, archivo_salida='mapa_ruta_espana.html'):
    """Crea un mapa interactivo con la ruta completa"""
    # Adaptado para el formato actual del JSON
    itinerario = resultados.get('itinerario', [])
    
    if not itinerario:
        print("⚠️  No hay itinerario en los resultados")
        return
    
    dias = [dia_info['lugares_ids'] for dia_info in itinerario]
    ciudades = [dia_info['ciudad'] for dia_info in itinerario]
    
    # Centro de España (aproximado)
    mapa = folium.Map(location=[40.0, -3.5], zoom_start=6, 
                      tiles='OpenStreetMap')
    
    # Añadir diferentes capas de mapas
    folium.TileLayer('CartoDB positron').add_to(mapa)
    folium.TileLayer('CartoDB dark_matter').add_to(mapa)
    
    # Crear grupos de capas por día
    feature_groups = {}
    
    for dia_idx, (dia_lugares, ciudad) in enumerate(zip(dias, ciudades)):
        dia_num = dia_idx + 1
        feature_group = folium.FeatureGroup(name=f'Día {dia_num} - {ciudad}')
        
        lugares_objs = [get_lugar_por_id(lid) for lid in dia_lugares if get_lugar_por_id(lid)]
        
        if not lugares_objs:
            continue
        
        # Añadir marcadores
        for idx, lugar in enumerate(lugares_objs):
            color = COLORES_CIUDADES.get(ciudad, 'gray')
            icono = ICONOS_TIPO.get(lugar.get('tipo', 'turistico'), 'info-sign')
            
            popup_html = f"""
            <div style="font-family: Arial; width: 250px;">
                <h4 style="color: {color}; margin: 5px 0;">
                    {idx + 1}. {lugar['nombre']}
                </h4>
                <hr style="margin: 5px 0;">
                <b>Tipo:</b> {lugar.get('tipo', 'N/A')}<br>
                <b>Ciudad:</b> {lugar.get('ciudad', 'N/A')}<br>
                <b>Puntos:</b> {lugar['puntos']}<br>
                <b>Tiempo visita:</b> {lugar['tiempo_visita']} min<br>
                <b>Día:</b> {dia_num}<br>
                <b>Orden:</b> {idx + 1} de {len(lugares_objs)}
            </div>
            """
            
            folium.Marker(
                location=[lugar['x'], lugar['y']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{idx+1}. {lugar['nombre']}",
                icon=folium.Icon(color='red' if idx == 0 else 'blue', 
                                icon=icono, prefix='fa')
            ).add_to(feature_group)
        
        # Añadir líneas conectando lugares del día
        coordenadas = [[l['x'], l['y']] for l in lugares_objs]
        folium.PolyLine(
            coordenadas,
            color=color,
            weight=3,
            opacity=0.7,
            popup=f'Día {dia_num} - {ciudad}'
        ).add_to(feature_group)
        
        feature_group.add_to(mapa)
    
    # Añadir control de capas
    folium.LayerControl(collapsed=False).add_to(mapa)
    
    # Añadir minimap
    minimap = plugins.MiniMap(toggle_display=True)
    mapa.add_child(minimap)
    
    # Añadir medidor de distancia
    plugins.MeasureControl(position='topright', 
                          primary_length_unit='kilometers').add_to(mapa)
    
    # Añadir botón de pantalla completa
    plugins.Fullscreen(position='topright').add_to(mapa)
    
    # Añadir leyenda
    leyenda_html = f"""
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 250px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; border-radius: 5px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
        <h4 style="margin-top:0; text-align:center;">Leyenda</h4>
        <p style="margin: 5px 0;"><b>Total días:</b> {len(dias)}</p>
        <p style="margin: 5px 0;"><b>Ciudades:</b> {len(set(ciudades))}</p>
        <p style="margin: 5px 0;"><b>Lugares:</b> {sum(len(d) for d in dias)}</p>
        <hr>
        <p style="margin: 5px 0; font-size: 12px;">
            <i class="fa fa-circle" style="color:red"></i> Primer lugar del día<br>
            <i class="fa fa-circle" style="color:blue"></i> Otros lugares<br>
        </p>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(leyenda_html))
    
    # Guardar mapa
    mapa.save(archivo_salida)
    print(f"✅ Mapa interactivo guardado: {archivo_salida}")


def generar_resumen_estadistico(resultados, archivo_salida='resumen_estadistico_espana.txt'):
    """Genera un resumen estadístico detallado en texto"""
    # Adaptado para el formato actual del JSON
    itinerario = resultados.get('itinerario', [])
    configuracion = resultados.get('configuracion', {})
    
    if not itinerario:
        print("⚠️  No hay itinerario en los resultados")
        return
    
    dias = [dia_info['lugares_ids'] for dia_info in itinerario]
    ciudades = [dia_info['ciudad'] for dia_info in itinerario]
    fitness = resultados.get('fitness', 0)
    
    # Calcular estadísticas
    total_lugares = sum(len(d) for d in dias)
    ciudades_visitadas = len(set(ciudades))
    
    # Estadísticas por ciudad
    stats_ciudades = {}
    for dia_lugares, ciudad in zip(dias, ciudades):
        if ciudad not in stats_ciudades:
            stats_ciudades[ciudad] = {'dias': 0, 'lugares': 0, 'puntos': 0}
        
        stats_ciudades[ciudad]['dias'] += 1
        stats_ciudades[ciudad]['lugares'] += len(dia_lugares)
        
        for lid in dia_lugares:
            lugar = get_lugar_por_id(lid)
            if lugar:
                stats_ciudades[ciudad]['puntos'] += lugar['puntos']
    
    # Generar texto
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RESUMEN ESTADÍSTICO - OPTIMIZACIÓN RUTA TURÍSTICA ESPAÑA\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("CONFIGURACIÓN DEL ALGORITMO\n")
        f.write("-"*80 + "\n")
        f.write(f"Población: {configuracion.get('poblacion', 'N/A')}\n")
        f.write(f"Generaciones: {configuracion.get('generaciones', 'N/A')}\n")
        f.write(f"Días de viaje: {configuracion.get('num_dias', 'N/A')}\n")
        f.write(f"Lugares por día: {configuracion.get('lugares_por_dia', 'N/A')}\n\n")
        
        f.write("RESULTADOS GLOBALES\n")
        f.write("-"*80 + "\n")
        f.write(f"Fitness total: {fitness:.2f}\n")
        f.write(f"Lugares visitados: {total_lugares}\n")
        f.write(f"Ciudades visitadas: {ciudades_visitadas} de 10\n")
        f.write(f"Promedio lugares/día: {total_lugares / len(dias):.1f}\n\n")
        
        f.write("DISTRIBUCIÓN POR CIUDAD\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Ciudad':<20} {'Días':>8} {'Lugares':>10} {'Puntos':>10} {'Pts/Día':>10}\n")
        f.write("-"*80 + "\n")
        
        for ciudad in sorted(stats_ciudades.keys()):
            stats = stats_ciudades[ciudad]
            pts_dia = stats['puntos'] / stats['dias']
            f.write(f"{ciudad:<20} {stats['dias']:>8} {stats['lugares']:>10} "
                   f"{stats['puntos']:>10} {pts_dia:>10.1f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write(f"Total días: {len(dias)}\n")
        f.write(f"Total lugares: {sum(s['lugares'] for s in stats_ciudades.values())}\n")
        f.write(f"Total puntos: {sum(s['puntos'] for s in stats_ciudades.values())}\n")
        f.write("="*80 + "\n")
    
    print(f"✅ Resumen estadístico guardado: {archivo_salida}")


def analizar_resultados_completo(archivo_json='resultados_espana_rapido.json'):
    """Ejecuta todos los análisis"""
    print("\n" + "="*80)
    print("🇪🇸 ANÁLISIS DE RESULTADOS - RUTA TURÍSTICA ESPAÑA")
    print("="*80 + "\n")
    
    # Cargar resultados
    print("📂 Cargando resultados...")
    resultados = cargar_resultados(archivo_json)
    print(f"✅ Archivo cargado: {archivo_json}\n")
    
    # Generar análisis
    print("📊 Generando gráficas de evolución...")
    analizar_evolucion_fitness(resultados)
    
    print("\n📊 Generando análisis por ciudades...")
    analizar_distribucion_por_ciudades(resultados)
    
    print("\n📊 Generando métricas diarias...")
    analizar_metricas_diarias(resultados)
    
    print("\n🗺️  Generando mapa interactivo...")
    crear_mapa_interactivo(resultados)
    
    print("\n📝 Generando resumen estadístico...")
    generar_resumen_estadistico(resultados)
    
    print("\n" + "="*80)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*80)
    print("\nArchivos generados:")
    print("  📊 evolucion_fitness_espana.png")
    print("  📊 distribucion_ciudades_espana.png")
    print("  📊 metricas_diarias_espana.png")
    print("  🗺️  mapa_ruta_espana.html")
    print("  📝 resumen_estadistico_espana.txt")
    print("\n💡 Abre mapa_ruta_espana.html en tu navegador para ver la ruta interactiva")
    print("="*80 + "\n")


if __name__ == "__main__":
    import sys
    
    # Permitir especificar archivo JSON como argumento
    archivo = sys.argv[1] if len(sys.argv) > 1 else 'resultados_espana_rapido.json'
    
    if not os.path.exists(archivo):
        print(f"❌ Error: No se encuentra el archivo '{archivo}'")
        print(f"💡 Primero ejecuta: python ejecutar_espana.py rapido")
    else:
        analizar_resultados_completo(archivo)
