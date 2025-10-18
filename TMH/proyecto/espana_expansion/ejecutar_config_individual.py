import argparse
import json
import time
import os
from datetime import datetime
import matplotlib.pyplot as plt

from algoritmo_espana import algoritmo_genetico_espana, analizar_solucion, configurar_logging

def parsear_argumentos():
    
    parser = argparse.ArgumentParser(
        description='Ejecutar algoritmo genético con configuración específica'
    )
    
    parser.add_argument('--nombre', type=str, required=True,
                        help='Nombre identificador de la configuración')
    
    parser.add_argument('--dias', type=int, default=20,
                        help='Número de días del viaje (default: 20)')
    parser.add_argument('--lugares-por-dia', type=int, default=12,
                        help='Lugares por día (default: 12)')

    parser.add_argument('--poblacion', type=int, default=750,
                        help='Tamaño de la población (default: 750)')
    parser.add_argument('--elitismo', type=float, default=0.15,
                        help='Tasa de elitismo 0.05-0.35 (default: 0.15)')
    
    parser.add_argument('--generaciones', type=int, default=None,
                        help='Número de generaciones a ejecutar')
    parser.add_argument('--horas', type=float, default=None,
                        help='Tiempo límite en HORAS (puede ser decimal: 0.5 = 30min, 8 = 8 horas) (default: 1.0)')
    
    parser.add_argument('--guardar-json', action='store_true',
                        help='Guardar resultados en JSON')
    parser.add_argument('--guardar-grafica', action='store_true',
                        help='Guardar gráfica de convergencia')
    parser.add_argument('--mostrar-analisis', action='store_true',
                        help='Mostrar análisis detallado del itinerario')
    parser.add_argument('--output-dir', type=str, default='.',
                        help='Directorio para guardar archivos (default: .)')
    
    return parser.parse_args()


def ejecutar_con_config(args):
    if args.generaciones is None and args.horas is None:
        args.horas = 2
        print("⚠️  No se especificó --generaciones ni --horas, usando --horas 2.0 por defecto\n")
    
    timestamp = datetime.now().strftime("%d_%H_%M")
    nombre_archivo = args.nombre.replace(' ', '_').replace('/', '-')
    
    print("\n" + "="*100)
    print(f"EJECUCIÓN: {args.nombre}")
    print("="*100)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nCONFIGURACIÓN:")
    print(f"  - Días: {args.dias}")
    print(f"  - Lugares/día: {args.lugares_por_dia}")
    print(f"  - Población: {args.poblacion}")
    print(f"  - Elitismo: {args.elitismo*100:.0f}%")
    
    if args.generaciones:
        print(f"  - Generaciones: {args.generaciones}")
        modo = "generaciones"
    else:
        horas = int(args.horas)
        minutos = int((args.horas - horas) * 60)
        print(f"  - Tiempo límite: {horas}h {minutos}m ({args.horas:.2f}h)")
        modo = "tiempo"
    
    print("="*100 + "\n")
    
    # Ejecutar algoritmo
    tiempo_inicio = time.time()
    
    resultado = algoritmo_genetico_espana(
        num_dias=args.dias,
        lugares_por_dia=args.lugares_por_dia,
        tam_poblacion=args.poblacion,
        num_generaciones=args.generaciones,
        tasa_elitismo=args.elitismo,
        tiempo_limite_horas=args.horas
    )
    
    tiempo_total = time.time() - tiempo_inicio
    mejor = resultado['mejor_individuo']
    
    # Mostrar resultados
    print("\n" + "="*100)
    print("RESULTADOS FINALES")
    print("="*100)
    print(f"🏆 Fitness: {mejor.fitness:.1f}")
    print(f"⭐ Puntos: {mejor.puntos_totales}")
    print(f"🚗 Distancia: {mejor.distancia_total:.1f} km")
    print(f"⏰ Tiempo viaje: {mejor.tiempo_total/60:.1f} horas")
    print(f"📊 Generaciones: {resultado['generaciones_ejecutadas']}")
    print(f"⏱️  Tiempo ejecución: {tiempo_total:.2f}s ({tiempo_total/60:.2f}m)")
    print(f"🎯 Fitness/segundo: {mejor.fitness/tiempo_total:.2f}")
    print("="*100 + "\n")
    
    # Guardar JSON
    if args.guardar_json:
        archivo_json = f"{args.output_dir}/{timestamp}_{nombre_archivo}.json"
        
        datos = {
            'nombre': args.nombre,
            'timestamp': timestamp,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'configuracion': {
                'dias': args.dias,
                'lugares_por_dia': args.lugares_por_dia,
                'poblacion': args.poblacion,
                'elitismo': args.elitismo,
                'generaciones': args.generaciones,
                'tiempo_limite_horas': args.horas,
                'modo': modo
            },
            'resultados': {
                'fitness': mejor.fitness,
                'puntos': mejor.puntos_totales,
                'distancia': mejor.distancia_total,
                'tiempo_viaje': mejor.tiempo_total,
                'generaciones_ejecutadas': resultado['generaciones_ejecutadas'],
                'tiempo_ejecucion': tiempo_total,
                'fitness_por_segundo': mejor.fitness / tiempo_total
            },
            'historial_fitness': resultado['historial_fitness'],
            'historial_tiempos': resultado['historial_tiempos']
        }
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(archivo_json), exist_ok=True)
        
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON guardado: {archivo_json}")
    
    # Guardar gráfica
    if args.guardar_grafica:
        archivo_png = f"{args.output_dir}/{timestamp}_{nombre_archivo}.png"
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Gráfica vs generaciones
        axes[0].plot(resultado['historial_fitness'], linewidth=2, color='steelblue')
        axes[0].set_xlabel('Generación', fontsize=12)
        axes[0].set_ylabel('Fitness', fontsize=12)
        axes[0].set_title(f'Convergencia - {args.nombre}', fontsize=13, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        # Gráfica vs tiempo
        axes[1].plot(resultado['historial_tiempos'], resultado['historial_fitness'], 
                    linewidth=2, color='green')
        axes[1].set_xlabel('Tiempo', fontsize=12)
        axes[1].set_ylabel('Fitness', fontsize=12)
        axes[1].set_title(f'Fitness vs Tiempo - {args.nombre}', fontsize=13, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(archivo_png, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfica guardada: {archivo_png}")
    
    # Mostrar análisis detallado
    if args.mostrar_analisis:
        print("\n" + "="*100)
        print("ANÁLISIS DETALLADO DEL ITINERARIO")
        print("="*100 + "\n")
        analizar_solucion(mejor)
    
    print("\n✅ Ejecución completada!")
    print(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100 + "\n")
    
    return resultado


def main():
    """Función principal"""
    args = parsear_argumentos()
    
    timestamp = datetime.now().strftime("%d_%H_%M")
    nombre_archivo = args.nombre.replace(' ', '_').replace('/', '-')
    log_file = configurar_logging(
        output_dir="logs", 
        prefijo=f"{nombre_archivo}"
    )
    
    print(f"\n📝 Log guardado en: {log_file}\n")
    
    ejecutar_con_config(args)


if __name__ == "__main__":
    main()
