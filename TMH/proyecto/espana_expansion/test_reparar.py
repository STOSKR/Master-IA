"""
Test específico para verificar si la función reparar_individuo() funciona
"""

import random
from algoritmo_espana import (
    reparar_individuo, validar_restricciones_ciudades, Individual
)
from config import MAX_DIAS_POR_CIUDAD

def test_reparar_barcelona_8_dias():
    """
    Test con el caso específico: Barcelona 8 días consecutivos
    """
    print("\n" + "="*80)
    print("🔧 TEST: REPARAR INDIVIDUO CON BARCELONA 8 DÍAS")
    print("="*80)
    
    # Crear individuo con Barcelona 8 días al final (el caso problemático)
    ciudades = [
        'Madrid', 'Madrid',  # días 1-2
        'Sevilla', 'Sevilla', 'Sevilla', 'Sevilla',  # días 3-6
        'Toledo',  # día 7
        'Córdoba', 'Córdoba', 'Córdoba', 'Córdoba',  # días 8-11
        'Bilbao', 'Bilbao', 'Bilbao', 'Bilbao',  # días 12-15
        'San Sebastián', 'San Sebastián',  # días 16-17
        'Santiago', 'Santiago',  # días 18-19
        'Granada', 'Granada',  # días 20-21
        'Valencia',  # día 22
        'Barcelona', 'Barcelona', 'Barcelona', 'Barcelona', 'Barcelona', 'Barcelona', 'Barcelona', 'Barcelona'  # días 23-30 (8 días)
    ]
    
    # Crear días vacíos (no importan los lugares para este test)
    dias = [[] for _ in range(30)]
    
    individuo = Individual(dias, ciudades)
    
    print(f"\n📊 ANTES DE REPARAR:")
    print(f"  Total días: {len(individuo.ciudades)}")
    
    # Contar días de Barcelona
    dias_barcelona = sum(1 for c in individuo.ciudades if c == 'Barcelona')
    print(f"  Barcelona: {dias_barcelona} días")
    
    # Encontrar bloque consecutivo más largo de Barcelona
    max_consecutivos = 0
    consecutivos_actual = 0
    for ciudad in individuo.ciudades:
        if ciudad == 'Barcelona':
            consecutivos_actual += 1
            max_consecutivos = max(max_consecutivos, consecutivos_actual)
        else:
            consecutivos_actual = 0
    
    print(f"  Barcelona consecutivos máximos: {max_consecutivos} días")
    print(f"  Límite permitido: {MAX_DIAS_POR_CIUDAD} días")
    print(f"  Validación: {'❌ INVÁLIDO' if not validar_restricciones_ciudades(individuo) else '✅ VÁLIDO'}")
    
    # REPARAR
    print(f"\n🔧 Reparando individuo...")
    random.seed(999)  # Seed fija para reproducibilidad
    individuo_reparado = reparar_individuo(individuo)
    
    print(f"\n📊 DESPUÉS DE REPARAR:")
    print(f"  Total días: {len(individuo_reparado.ciudades)}")
    
    # Contar días de Barcelona
    dias_barcelona_rep = sum(1 for c in individuo_reparado.ciudades if c == 'Barcelona')
    print(f"  Barcelona: {dias_barcelona_rep} días")
    
    # Encontrar bloque consecutivo más largo de Barcelona
    max_consecutivos_rep = 0
    consecutivos_actual_rep = 0
    for ciudad in individuo_reparado.ciudades:
        if ciudad == 'Barcelona':
            consecutivos_actual_rep += 1
            max_consecutivos_rep = max(max_consecutivos_rep, consecutivos_actual_rep)
        else:
            consecutivos_actual_rep = 0
    
    print(f"  Barcelona consecutivos máximos: {max_consecutivos_rep} días")
    print(f"  Validación: {'✅ VÁLIDO' if validar_restricciones_ciudades(individuo_reparado) else '❌ INVÁLIDO'}")
    
    # Mostrar secuencia completa
    print(f"\n📋 SECUENCIA COMPLETA DESPUÉS DE REPARAR:")
    ciudad_anterior = None
    contador = 0
    for dia_idx, ciudad in enumerate(individuo_reparado.ciudades, 1):
        if ciudad != ciudad_anterior:
            if ciudad_anterior is not None:
                simbolo = "✅" if contador <= MAX_DIAS_POR_CIUDAD else "❌"
                print(f"  {simbolo} Días {dia_idx-contador}-{dia_idx-1}: {ciudad_anterior} ({contador} días)")
            ciudad_anterior = ciudad
            contador = 1
        else:
            contador += 1
    # Último bloque
    simbolo = "✅" if contador <= MAX_DIAS_POR_CIUDAD else "❌"
    print(f"  {simbolo} Días {len(individuo_reparado.ciudades)-contador+1}-{len(individuo_reparado.ciudades)}: {ciudad_anterior} ({contador} días)")
    
    print("\n" + "="*80)
    return individuo_reparado, validar_restricciones_ciudades(individuo_reparado)

if __name__ == "__main__":
    individuo_reparado, es_valido = test_reparar_barcelona_8_dias()
    
    if es_valido:
        print("\n✅✅✅ ÉXITO: La función reparar_individuo() FUNCIONA correctamente")
    else:
        print("\n❌❌❌ FALLO: La función reparar_individuo() NO repara correctamente")
