# Análisis comparativo: Con 2-opt vs Sin 2-opt

import json
import os
import matplotlib.pyplot as plt

# Crear carpeta de salida si no existe
output_dir = "./graficas_generadas"
os.makedirs(output_dir, exist_ok=True)

# Directorio con los archivos JSON
data_dir = "./data/2opt"

# Cargar los archivos JSON
datos_experimentos = []

archivos = [
    "sin_2opt.json",
    "2opt.json"
]

for archivo in archivos:
    ruta = os.path.join(data_dir, archivo)
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
            
            config = datos.get("configuracion", {})
            mejor_sol = datos.get("mejor_solucion", {})
            
            # Determinar nombre según si usa 2-opt o no
            usar_2opt = config.get("usar_2opt", False)
            nombre = "Con 2-opt" if usar_2opt else "Sin 2-opt"
            
            # Extraer historial (puede estar en diferentes estructuras)
            historial = datos.get("historial", {})
            historial_fitness = historial.get("mejor_fitness", historial.get("fitness_actual", []))
            historial_tiempos = historial.get("tiempos", historial.get("tiempos_segundos", []))
            
            # Si no hay tiempos, generar sintéticamente basado en el tiempo total
            if not historial_tiempos and historial_fitness:
                estadisticas = datos.get("estadisticas", {})
                tiempo_total = estadisticas.get("tiempo_ejecucion_segundos", 7200)
                num_puntos = len(historial_fitness)
                # Generar tiempos lineales
                historial_tiempos = [(i * tiempo_total / num_puntos) for i in range(num_puntos)]
            
            experimento = {
                "nombre": nombre,
                "usar_2opt": usar_2opt,
                "fitness": mejor_sol.get("fitness", 0),
                "puntos": mejor_sol.get("puntos_totales", 0),
                "distancia": mejor_sol.get("distancia_total_km", 0),
                "historial_fitness": historial_fitness,
                "historial_tiempos": historial_tiempos,
                "archivo": archivo
            }
            
            datos_experimentos.append(experimento)
            print(f"✅ Cargado: {archivo}")
            print(f"   - Nombre: {nombre}")
            print(f"   - Mejor fitness: {experimento['fitness']:.2f}")
            print(f"   - Puntos: {experimento['puntos']}")
            print(f"   - Distancia: {experimento['distancia']:.2f} km")
            print(f"   - Datos en historial: {len(experimento['historial_fitness'])}")
    else:
        print(f"❌ No encontrado: {archivo}")

print("\n" + "="*120)
print("ANÁLISIS COMPARATIVO: IMPACTO DE LA OPTIMIZACIÓN 2-OPT")
print("="*120)
print(f"\nTotal de experimentos analizados: {len(datos_experimentos)}")

# ============================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================
if len(datos_experimentos) >= 2:
    print("\n" + "="*120)
    print("ANÁLISIS ESTADÍSTICO")
    print("="*120)
    
    exp_sin = next((e for e in datos_experimentos if not e['usar_2opt']), None)
    exp_con = next((e for e in datos_experimentos if e['usar_2opt']), None)
    
    if exp_sin and exp_con:
        print(f"\n📊 SIN 2-OPT:")
        print(f"   Fitness: {exp_sin['fitness']:.2f}")
        print(f"   Puntos: {exp_sin['puntos']}")
        print(f"   Distancia: {exp_sin['distancia']:.2f} km")
        
        print(f"\n📊 CON 2-OPT:")
        print(f"   Fitness: {exp_con['fitness']:.2f}")
        print(f"   Puntos: {exp_con['puntos']}")
        print(f"   Distancia: {exp_con['distancia']:.2f} km")
        
        print(f"\n💡 COMPARACIÓN:")
        diff_fitness = exp_con['fitness'] - exp_sin['fitness']
        diff_puntos = exp_con['puntos'] - exp_sin['puntos']
        diff_distancia = exp_con['distancia'] - exp_sin['distancia']
        
        print(f"   Diferencia Fitness: {diff_fitness:+.2f} ({(diff_fitness/exp_sin['fitness']*100):+.2f}%)")
        print(f"   Diferencia Puntos: {diff_puntos:+d} ({(diff_puntos/exp_sin['puntos']*100):+.2f}%)")
        print(f"   Diferencia Distancia: {diff_distancia:+.2f} km ({(diff_distancia/exp_sin['distancia']*100):+.2f}%)")
        
        if diff_fitness > 0:
            print(f"\n✅ La versión CON 2-opt obtuvo MEJOR fitness")
        elif diff_fitness < 0:
            print(f"\n⚠️  La versión SIN 2-opt obtuvo MEJOR fitness")
        else:
            print(f"\n➖ Ambas versiones obtuvieron el MISMO fitness")

# ============================================================
# GRÁFICA: Evolución del fitness comparativa
# ============================================================
if datos_experimentos:
    plt.figure(figsize=(12, 7))
    
    # Colores distintos
    colores = ['#d62728', '#2ca02c']  # Rojo para sin 2-opt, verde para con 2-opt
    
    for idx, exp in enumerate(datos_experimentos):
        if exp["historial_fitness"] and exp["historial_tiempos"]:
            # Convertir tiempos a minutos
            tiempos_min = [t / 60 for t in exp["historial_tiempos"]]
            
            # Asegurar que las listas tengan la misma longitud
            min_len = min(len(tiempos_min), len(exp["historial_fitness"]))
            tiempos_min = tiempos_min[:min_len]
            fitness = exp["historial_fitness"][:min_len]
            
            mejor_fitness = exp['fitness']
            
            plt.plot(tiempos_min, fitness, 
                    label=f"{exp['nombre']} (Fitness: {mejor_fitness:.2f})", 
                    linewidth=2, alpha=0.8, 
                    color=colores[idx % len(colores)])
            
            # Imprimir en consola
            print(f"\n{exp['nombre']}:")
            print(f"  Mejor Fitness: {mejor_fitness:.2f}")
    
    plt.xlabel("Tiempo (minutos)", fontsize=12)
    plt.ylabel("Mejor Fitness histórico", fontsize=12)
    plt.title("Evolución del Fitness - Comparación Con/Sin optimización 2-opt", fontsize=14, fontweight='bold')
    plt.xlim(0, 120)  # Limitar a 120 minutos
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "comparacion_2opt.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n" + "="*120)
    print("ARCHIVO GENERADO")
    print("="*120)
    print(f"✅ comparacion_2opt.png")
    print(f"\n📁 Ubicación: {os.path.abspath(output_dir)}")
else:
    print("\n⚠️ No se encontraron archivos JSON válidos para procesar")
