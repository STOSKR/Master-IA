"""
Test con DEBUG activado para ver qué pasa en reparar_individuo
"""

import random
from algoritmo_espana import Individual

# HACK: Activar DEBUG en la función
import algoritmo_espana
# Modificar temporalmente el código para activar debug
codigo_original = algoritmo_espana.reparar_individuo.__code__

def test_con_debug():
    print("\n" + "="*80)
    print("🐛 TEST CON DEBUG ACTIVADO")
    print("="*80)
    
    # Crear individuo problemático
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
        'Barcelona', 'Barcelona', 'Barcelona', 'Barcelona', 'Barcelona', 'Barcelona', 'Barcelona', 'Barcelona'
    ]
    
    dias = [[] for _ in range(30)]
    individuo = Individual(dias, ciudades)
    
    print(f"\n📊 ANTES:")
    print(f"   Barcelona días 23-30: 8 días consecutivos ❌")
    
    # Modificar directamente el código para activar DEBUG
    import types
    
    # Leer el código fuente de la función
    with open('algoritmo_espana.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Reemplazar DEBUG_REPARAR = False por True temporalmente
    contenido_modificado = contenido.replace(
        'DEBUG_REPARAR = False  # Cambiar a True para ver debug',
        'DEBUG_REPARAR = True  # DEBUG ACTIVADO'
    )
    
    # Guardar temporalmente
    with open('_temp_debug.py', 'w', encoding='utf-8') as f:
        f.write(contenido_modificado)
    
    # Importar la versión con debug
    import importlib.util
    spec = importlib.util.spec_from_file_location("temp_module", "_temp_debug.py")
    temp_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(temp_module)
    
    # Ejecutar la reparación con debug
    random.seed(999)
    individuo_reparado = temp_module.reparar_individuo(individuo)
    
    print(f"\n📊 DESPUÉS:")
    i = 0
    while i < len(individuo_reparado.ciudades):
        ciudad_actual = individuo_reparado.ciudades[i]
        inicio = i
        
        while i < len(individuo_reparado.ciudades) and individuo_reparado.ciudades[i] == ciudad_actual:
            i += 1
        
        dias_bloque = i - inicio
        simbolo = "✅" if dias_bloque <= 4 else "❌"
        print(f"   {simbolo} Días {inicio+1}-{i}: {ciudad_actual} ({dias_bloque} días)")
    
    # Limpiar archivo temporal
    import os
    if os.path.exists('_temp_debug.py'):
        os.remove('_temp_debug.py')
    if os.path.exists('__pycache__'):
        import shutil
        shutil.rmtree('__pycache__', ignore_errors=True)

if __name__ == "__main__":
    test_con_debug()
