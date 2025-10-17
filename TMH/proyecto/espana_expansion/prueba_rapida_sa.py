"""
EJEMPLO RÁPIDO DE EJECUCIÓN - ENFRIAMIENTO SIMULADO
====================================================

Este script ejecuta una versión rápida (5 minutos) del enfriamiento simulado
para verificar que todo funciona correctamente y detectar saltos anormales.
"""

from enfriamiento_simulado import (
    enfriamiento_simulado,
    comparar_con_sin_2opt,
    crear_individuo_aleatorio,
    evaluar_individuo
)

print("\n" + "="*80)
print("🚀 PRUEBA RÁPIDA - ENFRIAMIENTO SIMULADO (5 minutos)")
print("⚠️  MODO DEBUG: Detectará y reportará saltos anormales en fitness")
print("="*80)

# Generar solución inicial
print("\n🎲 Generando solución inicial aleatoria...")
solucion_inicial = crear_individuo_aleatorio(num_dias=20, lugares_por_dia=12)
evaluar_individuo(solucion_inicial)

print(f"✅ Solución inicial creada:")
print(f"   • Fitness: {solucion_inicial.fitness:.1f}")
print(f"   • Puntos: {solucion_inicial.puntos_totales}")

# Ejecutar enfriamiento simulado (5 minutos) con debug activado
print("\n🔥 Ejecutando enfriamiento simulado con detección de saltos...")
print("📝 Todos los detalles se guardarán en el archivo de log")
resultados = enfriamiento_simulado(
    solucion_inicial=solucion_inicial,
    T_inicial=2000,
    T_minima=0.1,
    alpha=0.97,
    max_tiempo_segundos=300,  # 5 minutos
    iteraciones_sin_mejora_max=500,
    usar_2opt=True,
    verbose=True,
    debug_saltos=True  # ⚠️ ACTIVADO: Detecta saltos > 5000
)

# Mostrar resultados
print("\n" + "="*80)
print("📊 RESULTADOS FINALES")
print("="*80)

mejor = resultados["mejor_solucion"]
stats = resultados["estadisticas"]

print(f"\n🏆 Mejor solución encontrada:")
print(f"   • Fitness final: {mejor.fitness:.1f}")
print(f"   • Mejora: {stats['mejora_absoluta']:+.1f} ({stats['mejora_porcentual']:+.2f}%)")
print(f"   • Puntos totales: {mejor.puntos_totales}")
print(f"   • Tiempo total viaje: {mejor.tiempo_total/60:.1f} horas")
print(f"   • Distancia total: {mejor.distancia_total:.1f} km")

print(f"\n⚡ Estadísticas de ejecución:")
print(f"   • Iteraciones: {stats['iteraciones_realizadas']:,}")
print(f"   • Tiempo ejecución: {stats['tiempo_ejecucion_minutos']:.2f} minutos")
print(f"   • Mejoras encontradas: {stats['mejoras_encontradas']}")
print(f"   • Tasa aceptación: {stats['tasa_aceptacion']:.2f}%")

print(f"\n💾 Archivos generados:")
print(f"   • Gráfica de evolución guardada")
print(f"   • Log detallado con detección de saltos guardado")
print(f"   • Busca líneas con '⚠️ SALTO ANORMAL' en el archivo de log")

print("\n✅ Prueba completada exitosamente!")
print("="*80)
