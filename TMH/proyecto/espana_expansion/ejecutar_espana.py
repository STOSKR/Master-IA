"""
Script de ejecución del Algoritmo Genético para España
Permite ejecutar con diferentes configuraciones
"""

from algoritmo_espana import algoritmo_genetico_espana, analizar_solucion, exportar_resultados
import sys

def main():
    print("\n" + "="*80)
    print("🇪🇸 OPTIMIZACIÓN DE RUTA TURÍSTICA POR ESPAÑA")
    print("="*80)
    print("\nDataset: 1,293 lugares en 10 ciudades españolas")
    print("Complejidad del problema: 10^753.3")
    print("="*80 + "\n")
    
    # Configuraciones predefinidas
    configs = {
        "rapido": {
            "num_dias": 20,
            "lugares_por_dia": 12,
            "tam_poblacion": 3000,
            "num_generaciones": 200,
            "tasa_elitismo": 0.20,
            "descripcion": "Ejecución rápida (prueba)"
        },
        "medio": {
            "num_dias": 20,
            "lugares_por_dia": 12,
            "tam_poblacion": 5000,
            "num_generaciones": 400,
            "tasa_elitismo": 0.20,
            "descripcion": "Ejecución media (equilibrio)"
        },
        "completo": {
            "num_dias": 20,
            "lugares_por_dia": 12,
            "tam_poblacion": 8000,
            "num_generaciones": 500,
            "tasa_elitismo": 0.20,
            "descripcion": "Ejecución completa (mejor calidad)"
        },
        "intenso": {
            "num_dias": 20,
            "lugares_por_dia": 12,
            "tam_poblacion": 10000,
            "num_generaciones": 600,
            "tasa_elitismo": 0.20,
            "descripcion": "Ejecución intensa (máxima calidad)"
        }
    }
    
    # Seleccionar configuración
    if len(sys.argv) > 1:
        modo = sys.argv[1].lower()
    else:
        print("Modos disponibles:")
        for nombre, cfg in configs.items():
            print(f"  • {nombre:10s}: {cfg['descripcion']}")
            print(f"    Población: {cfg['tam_poblacion']:,}, Generaciones: {cfg['num_generaciones']}")
        
        print("\nUso: python ejecutar_espana.py [modo]")
        print("Ejemplo: python ejecutar_espana.py medio")
        print("\nUsando modo 'rapido' por defecto...\n")
        modo = "rapido"
    
    if modo not in configs:
        print(f"❌ Modo '{modo}' no reconocido. Opciones: {', '.join(configs.keys())}")
        return
    
    config = configs[modo]
    print(f"✅ Modo seleccionado: {modo.upper()}")
    print(f"   {config['descripcion']}")
    print(f"   Población: {config['tam_poblacion']:,} | Generaciones: {config['num_generaciones']}\n")
    
    # Ejecutar algoritmo
    resultados = algoritmo_genetico_espana(
        num_dias=config["num_dias"],
        lugares_por_dia=config["lugares_por_dia"],
        tam_poblacion=config["tam_poblacion"],
        num_generaciones=config["num_generaciones"],
        tasa_elitismo=config["tasa_elitismo"]
    )
    
    # Analizar resultados
    analizar_solucion(resultados["mejor_individuo"])
    
    # Exportar
    nombre_archivo = f"resultados_espana_{modo}.json"
    exportar_resultados(resultados, nombre_archivo)
    
    print(f"\n{'='*80}")
    print(f"✅ PROCESO COMPLETADO")
    print(f"{'='*80}")
    print(f"📄 Resultados guardados en: {nombre_archivo}")
    print(f"🎯 Fitness final: {resultados['mejor_individuo'].fitness:.1f}")
    print(f"⭐ Puntos totales: {resultados['mejor_individuo'].puntos_totales}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
