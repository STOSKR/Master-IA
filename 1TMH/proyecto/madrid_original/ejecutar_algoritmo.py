"""
Script de ejemplo para ejecutar el algoritmo genético de rutas turísticas
Puede ejecutar tanto el modo de un día como el modo multidías
"""

from algoritmo_genetico import algoritmo_genetico_reemplazo_mixto, algoritmo_genetico_multidias, imprimir_mejor_ruta

def ejecutar_un_dia():
    """Ejecuta el algoritmo para optimizar un solo día"""
    print("\n" + "="*70)
    print("📅 OPTIMIZACIÓN DE RUTA TURÍSTICA - UN DÍA")
    print("="*70)
    
    resultado = algoritmo_genetico_reemplazo_mixto(
        generaciones=600,
        tamaño_poblacion=10000,
        prob_cruce=0.8,
        prob_mutacion=0.2,
        tiempo_disponible=14 * 60,  # 14 horas en minutos
        w_puntos=1.0,
        w_distancia=1.0
    )
    
    print(f"\n🏆 MEJOR RUTA ENCONTRADA")
    imprimir_mejor_ruta(resultado["mejor_ruta"], resultado["evaluacion"])
    
    return resultado

def ejecutar_multidias(num_dias=5, usar_restricciones=True):
    """Ejecuta el algoritmo para optimizar múltiples días"""
    print("\n" + "="*70)
    print(f"🗓️  OPTIMIZACIÓN DE RUTA TURÍSTICA - {num_dias} DÍAS")
    if usar_restricciones:
        print("🔒 MODO: CON RESTRICCIONES COMPLEJAS")
    else:
        print("📍 MODO: BÁSICO (SIN RESTRICCIONES COMPLEJAS)")
    print("="*70)
    
    resultado = algoritmo_genetico_multidias(
        generaciones=400,       # Menos generaciones por día
        tamaño_poblacion=10000,  # Población reducida para eficiencia
        prob_cruce=0.8,
        prob_mutacion=0.2,
        dias=num_dias,
        tiempo_disponible=14 * 60,  # 14 horas por día en minutos
        perfil_usuario="balanceado",  # Opciones: cultural, gastronomico, naturaleza, shopping, balanceado
        usar_restricciones=usar_restricciones
    )
    
    print("\n" + "="*70)
    print(f"✅ PLANIFICACIÓN DE {num_dias} DÍAS COMPLETADA")
    print("="*70)
    print(f"📊 Fitness total: {resultado['historial_completo']['mejor_fitness_total']:.2f}")
    print(f"🎯 Puntos totales: {resultado['historial_completo']['puntos_totales']:.2f}")
    print(f"🚗 Distancia total: {resultado['historial_completo']['distancia_total']:.2f} km")
    print(f"⏱️  Tiempo total: {resultado['historial_completo']['tiempo_total']/60:.2f} horas")
    if usar_restricciones:
        print(f"💰 Costo total: {resultado['historial_completo'].get('costo_total', 0):.2f} €")
    print(f"📍 Lugares únicos visitados: {sum(len(r['mejor_ruta']) for r in resultado['resultados_dias'])}")
    
    return resultado

def ejecutar_comparativa():
    """Ejecuta una comparativa rápida entre diferentes configuraciones"""
    print("\n" + "="*70)
    print("🔬 COMPARATIVA DE CONFIGURACIONES")
    print("="*70)
    
    configs = [
        {"nombre": "3 días", "dias": 3, "gen": 200, "pob": 3000},
        {"nombre": "5 días", "dias": 5, "gen": 300, "pob": 5000},
        {"nombre": "7 días", "dias": 7, "gen": 250, "pob": 4000},
    ]
    
    resultados = []
    
    for config in configs:
        print(f"\n{'='*70}")
        print(f"Ejecutando: {config['nombre']}")
        print(f"{'='*70}")
        
        resultado = algoritmo_genetico_multidias(
            generaciones=config['gen'],
            tamaño_poblacion=config['pob'],
            prob_cruce=0.8,
            prob_mutacion=0.2,
            dias=config['dias']
        )
        
        resultados.append({
            "config": config['nombre'],
            "fitness": resultado['historial_completo']['mejor_fitness_total'],
            "puntos": resultado['historial_completo']['puntos_totales'],
            "distancia": resultado['historial_completo']['distancia_total'],
            "lugares": sum(len(r['mejor_ruta']) for r in resultado['resultados_dias'])
        })
    
    # Imprimir tabla comparativa
    print("\n" + "="*70)
    print("📊 TABLA COMPARATIVA")
    print("="*70)
    print(f"{'Config':<15} {'Fitness':<12} {'Puntos':<10} {'Distancia':<12} {'Lugares':<10}")
    print("-"*70)
    
    for r in resultados:
        print(f"{r['config']:<15} {r['fitness']:<12.2f} {r['puntos']:<10} {r['distancia']:<12.2f} {r['lugares']:<10}")
    
    return resultados

if __name__ == "__main__":
    import sys
    
    print("\n🧬 ALGORITMO GENÉTICO - OPTIMIZACIÓN DE RUTAS TURÍSTICAS")
    print("="*70)
    print("Opciones disponibles:")
    print("  1. Un día (optimización intensiva)")
    print("  2. Múltiples días - 3 días (CON restricciones complejas)")
    print("  3. Múltiples días - 5 días (CON restricciones complejas)")
    print("  4. Múltiples días - 7 días (CON restricciones complejas)")
    print("  5. Comparativa: 5 días CON vs SIN restricciones")
    print("  6. Mostrar análisis de complejidad")
    print("="*70)
    
    if len(sys.argv) > 1:
        opcion = sys.argv[1]
    else:
        opcion = input("\nSeleccione una opción (1-6) [por defecto: 3]: ").strip() or "3"
    
    if opcion == "1":
        ejecutar_un_dia()
    elif opcion == "2":
        ejecutar_multidias(3, usar_restricciones=True)
    elif opcion == "3":
        ejecutar_multidias(5, usar_restricciones=True)
    elif opcion == "4":
        ejecutar_multidias(7, usar_restricciones=True)
    elif opcion == "5":
        print("\n🔬 COMPARATIVA: CON vs SIN RESTRICCIONES COMPLEJAS")
        print("="*70)
        print("\n1️⃣  Ejecutando SIN restricciones complejas...")
        resultado_basico = ejecutar_multidias(5, usar_restricciones=False)
        
        print("\n\n2️⃣  Ejecutando CON restricciones complejas...")
        resultado_complejo = ejecutar_multidias(5, usar_restricciones=True)
        
        print("\n" + "="*70)
        print("📊 TABLA COMPARATIVA")
        print("="*70)
        print(f"{'Métrica':<30} {'Sin Restricciones':<20} {'Con Restricciones':<20}")
        print("-"*70)
        print(f"{'Fitness Total':<30} {resultado_basico['historial_completo']['mejor_fitness_total']:<20.2f} {resultado_complejo['historial_completo']['mejor_fitness_total']:<20.2f}")
        print(f"{'Puntos Totales':<30} {resultado_basico['historial_completo']['puntos_totales']:<20.2f} {resultado_complejo['historial_completo']['puntos_totales']:<20.2f}")
        print(f"{'Distancia Total (km)':<30} {resultado_basico['historial_completo']['distancia_total']:<20.2f} {resultado_complejo['historial_completo']['distancia_total']:<20.2f}")
        print(f"{'Costo Total (€)':<30} {resultado_basico['historial_completo'].get('costo_total', 0):<20.2f} {resultado_complejo['historial_completo'].get('costo_total', 0):<20.2f}")
        print(f"{'Lugares Visitados':<30} {sum(len(r['mejor_ruta']) for r in resultado_basico['resultados_dias']):<20} {sum(len(r['mejor_ruta']) for r in resultado_complejo['resultados_dias']):<20}")
        print("="*70)
        
    elif opcion == "6":
        print("\n📊 ANÁLISIS DE COMPLEJIDAD DEL PROBLEMA")
        print("="*70)
        try:
            from TMH.proyecto.madrid_original.restricciones_complejas import calcular_complejidad
            from utils import lugares_turisticos
            
            for dias in [3, 5, 7, 10]:
                comp = calcular_complejidad(len(lugares_turisticos), dias)
                print(f"\n🗓️  {dias} DÍAS:")
                print(f"   Espacio de búsqueda total: {comp['espacio_busqueda_total']:.2e}")
                print(f"   Espacio válido (con restricciones): {comp['espacio_busqueda_valido']:.2e}")
                print(f"   Factor de reducción: {(1 - comp['espacio_busqueda_valido']/comp['espacio_busqueda_total'])*100:.1f}%")
        except ImportError:
            print("❌ Módulo 'restricciones_complejas' no disponible")
    else:
        print(f"❌ Opción no válida: {opcion}")
        print("Ejecutando opción por defecto (5 días CON restricciones)...")
        ejecutar_multidias(5, usar_restricciones=True)
    
    print("\n✅ Ejecución completada!")
    print("📁 Resultados guardados en archivos JSON")
