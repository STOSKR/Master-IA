"""
Script de prueba para verificar que el algoritmo genético respeta las restricciones
con 30 días (la configuración de producción real)
"""

import random
from algoritmo_espana import (
    crear_individuo_aleatorio, validar_restricciones_ciudades, evaluar_individuo,
    reparar_individuo, crossover_dos_puntos, mutar, Individual
)
from config import MAX_DIAS_POR_CIUDAD, AGRUPAR

def analizar_secuencia_ciudades(individuo):
    """Analiza la secuencia de ciudades y detecta bloques consecutivos"""
    if not individuo.ciudades:
        return []
    
    bloques = []
    ciudad_actual = individuo.ciudades[0]
    dia_inicio = 0
    
    for dia_idx in range(1, len(individuo.ciudades)):
        if individuo.ciudades[dia_idx] != ciudad_actual:
            dias_bloque = dia_idx - dia_inicio
            bloques.append({
                'ciudad': ciudad_actual,
                'dia_inicio': dia_inicio + 1,
                'dia_fin': dia_idx,
                'dias': dias_bloque
            })
            ciudad_actual = individuo.ciudades[dia_idx]
            dia_inicio = dia_idx
    
    # Último bloque
    dias_bloque = len(individuo.ciudades) - dia_inicio
    bloques.append({
        'ciudad': ciudad_actual,
        'dia_inicio': dia_inicio + 1,
        'dia_fin': len(individuo.ciudades),
        'dias': dias_bloque
    })
    
    return bloques

def probar_30_dias():
    print("\n" + "="*80)
    print("🧪 PRUEBA: CREACIÓN DE INDIVIDUO CON 30 DÍAS")
    print("="*80)
    
    # Configuración
    num_dias = 30
    lugares_por_dia = 6
    
    print(f"\n⚙️ CONFIGURACIÓN:")
    print(f"  - Días totales: {num_dias}")
    print(f"  - Lugares por día: {lugares_por_dia}")
    print(f"  - MAX_DIAS_POR_CIUDAD: {MAX_DIAS_POR_CIUDAD}")
    print(f"  - AGRUPAR: {AGRUPAR}")
    
    # Crear individuo con seed fija para reproducibilidad
    random.seed(42)
    print(f"\n🎲 Creando individuo con seed=42...")
    individuo = crear_individuo_aleatorio(num_dias, lugares_por_dia)
    
    # Análisis
    print(f"\n✅ Individuo creado: {len(individuo.dias)} días, {len(individuo.ciudades)} ciudades asignadas")
    
    # Analizar secuencia de ciudades
    bloques = analizar_secuencia_ciudades(individuo)
    print(f"\n📊 SECUENCIA DE CIUDADES:")
    print(f"  Total de bloques: {len(bloques)}")
    
    violaciones = []
    for bloque in bloques:
        simbolo = "✅" if bloque['dias'] <= MAX_DIAS_POR_CIUDAD else "❌"
        print(f"  {simbolo} Días {bloque['dia_inicio']}-{bloque['dia_fin']}: {bloque['ciudad']} ({bloque['dias']} días)")
        if bloque['dias'] > MAX_DIAS_POR_CIUDAD:
            violaciones.append(bloque)
    
    # Validación
    es_valido = validar_restricciones_ciudades(individuo)
    print(f"\n🔍 VALIDACIÓN: {'✅ SÍ' if es_valido else '❌ NO'} (cumple restricciones)")
    
    # Evaluación
    print(f"\n💰 EVALUACIÓN:")
    fitness = evaluar_individuo(individuo)
    print(f"  🏆 FITNESS: {fitness:,.2f}")
    
    if fitness == -999999999:
        print(f"  ⚠️  FITNESS CATASTRÓFICO: El individuo viola restricciones críticas")
    
    # Resumen
    print(f"\n" + "="*80)
    print(f"RESUMEN:")
    if violaciones:
        print(f"  ❌ {len(violaciones)} violaciones detectadas:")
        for v in violaciones:
            print(f"     - {v['ciudad']}: {v['dias']} días (excede límite de {MAX_DIAS_POR_CIUDAD})")
    else:
        print(f"  ✅ TODOS los bloques respetan el límite de {MAX_DIAS_POR_CIUDAD} días")
    
    print(f"  Validación: {'✅ VÁLIDO' if es_valido else '❌ INVÁLIDO'}")
    print(f"  Fitness: {'✅ VIABLE' if fitness > -999999999 else '❌ CATASTRÓFICO'}")
    print("="*80)
    
    return individuo, violaciones

def probar_cruce():
    print("\n" + "="*80)
    print("🧬 PRUEBA: OPERADOR DE CRUCE (CROSSOVER)")
    print("="*80)
    
    # Crear dos padres válidos
    random.seed(100)
    print(f"\n🎲 Creando padres con seed=100...")
    padre1 = crear_individuo_aleatorio(30, 6)
    padre2 = crear_individuo_aleatorio(30, 6)
    
    print(f"\n👨 PADRE 1:")
    bloques1 = analizar_secuencia_ciudades(padre1)
    print(f"  Bloques: {len(bloques1)}")
    valido1 = validar_restricciones_ciudades(padre1)
    print(f"  Validación: {'✅' if valido1 else '❌'}")
    
    print(f"\n👩 PADRE 2:")
    bloques2 = analizar_secuencia_ciudades(padre2)
    print(f"  Bloques: {len(bloques2)}")
    valido2 = validar_restricciones_ciudades(padre2)
    print(f"  Validación: {'✅' if valido2 else '❌'}")
    
    # Realizar cruce
    print(f"\n🔀 Realizando cruce...")
    hijo1, hijo2 = crossover_dos_puntos(padre1, padre2)
    
    print(f"\n👶 HIJO 1:")
    bloques_h1 = analizar_secuencia_ciudades(hijo1)
    print(f"  Bloques: {len(bloques_h1)}")
    for bloque in bloques_h1:
        simbolo = "✅" if bloque['dias'] <= MAX_DIAS_POR_CIUDAD else "❌"
        print(f"    {simbolo} {bloque['ciudad']}: {bloque['dias']} días")
    valido_h1 = validar_restricciones_ciudades(hijo1)
    print(f"  Validación: {'✅ VÁLIDO' if valido_h1 else '❌ INVÁLIDO'}")
    
    print(f"\n👶 HIJO 2:")
    bloques_h2 = analizar_secuencia_ciudades(hijo2)
    print(f"  Bloques: {len(bloques_h2)}")
    for bloque in bloques_h2:
        simbolo = "✅" if bloque['dias'] <= MAX_DIAS_POR_CIUDAD else "❌"
        print(f"    {simbolo} {bloque['ciudad']}: {bloque['dias']} días")
    valido_h2 = validar_restricciones_ciudades(hijo2)
    print(f"  Validación: {'✅ VÁLIDO' if valido_h2 else '❌ INVÁLIDO'}")
    
    print(f"\n" + "="*80)
    print(f"RESUMEN CRUCE:")
    print(f"  Padre 1: {'✅' if valido1 else '❌'} → Hijo 1: {'✅' if valido_h1 else '❌'}")
    print(f"  Padre 2: {'✅' if valido2 else '❌'} → Hijo 2: {'✅' if valido_h2 else '❌'}")
    print(f"  {'✅ ÉXITO: Cruce preserva restricciones' if valido_h1 and valido_h2 else '❌ FALLO: Cruce rompe restricciones'}")
    print("="*80)

def probar_mutacion():
    print("\n" + "="*80)
    print("🧬 PRUEBA: OPERADOR DE MUTACIÓN")
    print("="*80)
    
    # Crear individuo válido
    random.seed(200)
    print(f"\n🎲 Creando individuo con seed=200...")
    individuo = crear_individuo_aleatorio(30, 6)
    
    print(f"\n🧬 ANTES DE MUTACIÓN:")
    bloques_antes = analizar_secuencia_ciudades(individuo)
    print(f"  Bloques: {len(bloques_antes)}")
    for bloque in bloques_antes:
        simbolo = "✅" if bloque['dias'] <= MAX_DIAS_POR_CIUDAD else "❌"
        print(f"    {simbolo} {bloque['ciudad']}: {bloque['dias']} días")
    valido_antes = validar_restricciones_ciudades(individuo)
    print(f"  Validación: {'✅ VÁLIDO' if valido_antes else '❌ INVÁLIDO'}")
    
    # Aplicar mutación
    print(f"\n🧬 Aplicando mutación...")
    mutar(individuo)
    
    print(f"\n🧬 DESPUÉS DE MUTACIÓN:")
    bloques_despues = analizar_secuencia_ciudades(individuo)
    print(f"  Bloques: {len(bloques_despues)}")
    for bloque in bloques_despues:
        simbolo = "✅" if bloque['dias'] <= MAX_DIAS_POR_CIUDAD else "❌"
        print(f"    {simbolo} {bloque['ciudad']}: {bloque['dias']} días")
    valido_despues = validar_restricciones_ciudades(individuo)
    print(f"  Validación: {'✅ VÁLIDO' if valido_despues else '❌ INVÁLIDO'}")
    
    print(f"\n" + "="*80)
    print(f"RESUMEN MUTACIÓN:")
    print(f"  Antes: {'✅ VÁLIDO' if valido_antes else '❌ INVÁLIDO'}")
    print(f"  Después: {'✅ VÁLIDO' if valido_despues else '❌ INVÁLIDO'}")
    print(f"  {'✅ ÉXITO: Mutación preserva restricciones' if valido_despues else '❌ FALLO: Mutación rompe restricciones'}")
    print("="*80)

if __name__ == "__main__":
    print("\n" + "🚀 "*40)
    print("BATERÍA DE PRUEBAS: ALGORITMO GENÉTICO 30 DÍAS")
    print("🚀 "*40)
    
    # Prueba 1: Creación individual
    individuo, violaciones = probar_30_dias()
    
    # Prueba 2: Operador de cruce
    probar_cruce()
    
    # Prueba 3: Operador de mutación
    probar_mutacion()
    
    print("\n" + "✅ "*40)
    print("PRUEBAS COMPLETADAS")
    print("✅ "*40 + "\n")
