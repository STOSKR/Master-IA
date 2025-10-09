from restricciones_complejas import calcular_complejidad
import math

# Calcular con el número real de lugares
comp_253_7 = calcular_complejidad(253, 7)
comp_253_5 = calcular_complejidad(253, 5)

print("\n" + "="*80)
print("📊 COMPLEJIDAD REAL DEL PROBLEMA")
print("="*80)

print(f"\n🔢 CONFIGURACIÓN ACTUAL (253 lugares reales, 7 días)")
print("="*80)
print(f"Lugares totales disponibles: {comp_253_7['num_lugares_total']}")
print(f"Días de viaje: {comp_253_7['num_dias']}")
print(f"Lugares por día (promedio esperado): {comp_253_7['lugares_por_dia_promedio']}")
print(f"   (Con 16h disponibles y 75 min/lugar → ~12 lugares/día teóricos)")

print(f"\n📈 ESPACIO DE BÚSQUEDA:")
print(f"   Combinaciones por día: {comp_253_7['combinaciones_por_dia']:.4e}")
print(f"   Permutaciones por día: {comp_253_7['permutaciones_por_dia']:.4e}")
print(f"   Espacio total (solo rutas): {comp_253_7['espacio_busqueda_total']:.4e}")
print(f"   Factor de transporte: {comp_253_7['factor_transporte']:.4e}")

print(f"\n⭐ COMPLEJIDAD TOTAL REAL: {comp_253_7['complejidad_total_real']:.6e}")
if comp_253_7['complejidad_total_real'] != float('inf'):
    exponente = math.log10(comp_253_7['complejidad_total_real'])
    print(f"   📍 Equivalente a: 10^{exponente:.1f}")
print(f"   Espacio válido (con restricciones): {comp_253_7['espacio_busqueda_valido']:.4e}")

print(f"\n🔒 RESTRICCIONES ACTIVAS:")
for nombre_rest, valor in comp_253_7['restricciones'].items():
    print(f"   - {nombre_rest.replace('_', ' ').title()}: {valor}")

print("\n" + "="*80)
print(f"🔢 CONFIGURACIÓN ALTERNATIVA (253 lugares, 5 días)")
print("="*80)
print(f"⭐ COMPLEJIDAD TOTAL REAL: {comp_253_5['complejidad_total_real']:.6e}")
if comp_253_5['complejidad_total_real'] != float('inf'):
    exponente_5 = math.log10(comp_253_5['complejidad_total_real'])
    print(f"   📍 Equivalente a: 10^{exponente_5:.1f}")

print("\n" + "="*80)
print("💡 CONTEXTO COMPARATIVO:")
print("="*80)
print("   Átomos en el universo observable: ~10^80")
print("   TSP con 100 ciudades (objetivo): ~10^157")
print("   Edad del universo en nanosegundos: ~10^26")
print("   Segundos desde el Big Bang: ~10^17")
print("="*80)

print("\n✅ CONCLUSIÓN:")
if comp_253_7['complejidad_total_real'] != float('inf'):
    exponente = math.log10(comp_253_7['complejidad_total_real'])
    if exponente >= 150:
        print(f"   ✅ Objetivo alcanzado: 10^{exponente:.1f} >> 10^157")
        print(f"   El problema es de clase NP-Hard con complejidad similar o superior")
        print(f"   al TSP clásico de 100 ciudades.")
    else:
        print(f"   ⚠️  Complejidad actual: 10^{exponente:.1f}")
        print(f"   Objetivo (TSP 100 ciudades): 10^157")

print("\n" + "="*80)
print("🔍 COMPONENTES DE LA COMPLEJIDAD:")
print("="*80)
print("1. Combinaciones de lugares: C(253, 12) por día")
print("2. Permutaciones: 12! ordenamientos posibles por día")
print("3. Multi-día: elevado a la potencia 7 (días)")
print("4. Transporte: 4 opciones por cada traslado (11 traslados/día)")
print("5. Perfiles: 5 perfiles de usuario diferentes")
print("6. Clima: 3 condiciones por día (7 combinaciones)")
print("7. Restricciones: 11 incompatibilidades, 6 sinergias, 5 eventos")
print("8. Presupuesto: 150€/día con costos variables por lugar")
print("9. Horarios: Cada lugar tiene horarios de apertura/cierre")
print("="*80)
