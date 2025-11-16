"""
Script de prueba para verificar la funcionalidad de reparación de horarios.
"""

from algoritmo_espana import (
    Individual,
    verificar_lugar_en_horario,
    intentar_intercambio_horarios,
    buscar_lugar_alternativo_horario,
    reparar_horarios_individuo,
    evaluar_individuo
)
from utils_espana import get_lugares_por_ids, get_lugares_ciudad
from config import HORARIOS_TIPO, HORA_INICIO

def test_verificar_lugar_en_horario():
    """Prueba la función de verificación de horarios."""
    print("=" * 80)
    print("TEST 1: Verificar lugar en horario")
    print("=" * 80)
    
    # Lugar tipo museo (abre 10:00 - 19:00)
    lugar_museo = {"tipo": "museo", "nombre": "Museo del Prado"}
    
    # Caso 1: Visitar a las 11:00 (debería estar abierto)
    hora_inicio_1 = 11 * 60  # 11:00
    hora_fin_1 = hora_inicio_1 + 90  # 12:30
    resultado_1 = verificar_lugar_en_horario(lugar_museo, hora_inicio_1, hora_fin_1)
    print(f"\n1. Museo a las 11:00 (abre 10:00): {resultado_1} ✓" if resultado_1 else f"\n1. Museo a las 11:00: {resultado_1} ✗")
    
    # Caso 2: Visitar a las 8:00 (cerrado, abre a las 10:00)
    hora_inicio_2 = 8 * 60  # 8:00
    hora_fin_2 = hora_inicio_2 + 90  # 9:30
    resultado_2 = verificar_lugar_en_horario(lugar_museo, hora_inicio_2, hora_fin_2)
    print(f"2. Museo a las 8:00 (abre 10:00): {resultado_2} ✗" if not resultado_2 else f"2. Museo a las 8:00: {resultado_2} ✓")
    
    # Caso 3: Parque (abre 8:00 - 22:00)
    lugar_parque = {"tipo": "parque", "nombre": "Retiro"}
    hora_inicio_3 = 9 * 60  # 9:00
    hora_fin_3 = hora_inicio_3 + 120  # 11:00
    resultado_3 = verificar_lugar_en_horario(lugar_parque, hora_inicio_3, hora_fin_3)
    print(f"3. Parque a las 9:00 (abre 8:00): {resultado_3} ✓" if resultado_3 else f"3. Parque a las 9:00: {resultado_3} ✗")
    
    print("\n✅ Test 1 completado\n")

def test_individuo_simple():
    """Prueba la creación y evaluación de un individuo simple."""
    print("=" * 80)
    print("TEST 2: Crear y evaluar individuo con problemas de horario")
    print("=" * 80)
    
    # Obtener lugares de Madrid
    lugares_madrid = get_lugares_ciudad("Madrid")
    if not lugares_madrid:
        print("⚠️  No se encontraron lugares de Madrid")
        return
    
    # Seleccionar algunos lugares para el test
    # Buscar un museo y un parque
    museo = next((l for l in lugares_madrid if l.get("tipo") == "museo"), None)
    parque = next((l for l in lugares_madrid if l.get("tipo") == "parque"), None)
    restaurante = next((l for l in lugares_madrid if l.get("tipo") == "restaurante"), None)
    
    if not all([museo, parque, restaurante]):
        print("⚠️  No se encontraron todos los tipos de lugares necesarios")
        print(f"   Museo: {museo is not None}")
        print(f"   Parque: {parque is not None}")
        print(f"   Restaurante: {restaurante is not None}")
        return
    
    print(f"\nLugares seleccionados:")
    print(f"  - Museo: {museo['nombre']} (abre {HORARIOS_TIPO['museo']['apertura']//60}:00)")
    print(f"  - Parque: {parque['nombre']} (abre {HORARIOS_TIPO['parque']['apertura']//60}:00)")
    print(f"  - Restaurante: {restaurante['nombre']} (abre {HORARIOS_TIPO['restaurante']['apertura']//60}:00)")
    
    # Crear un día problemático: museo primero (cerrado a las 9:00)
    dia_problematico = [museo["id"], parque["id"], restaurante["id"]]
    ciudades = ["Madrid"]
    
    print(f"\nOrden original (problemático):")
    print(f"  9:00 - {museo['nombre']} (CERRADO hasta 10:00) ❌")
    print(f"  ↓")
    print(f"  ~11:00 - {parque['nombre']} (abierto) ✓")
    print(f"  ↓")
    print(f"  ~13:00 - {restaurante['nombre']} (abierto) ✓")
    
    individuo = Individual([dia_problematico], ciudades)
    
    print(f"\nEvaluando individuo antes de reparar...")
    fitness_antes = evaluar_individuo(individuo)
    print(f"  Fitness antes: {fitness_antes:.2f}")
    
    print(f"\nIntentando reparar horarios...")
    individuo_reparado = reparar_horarios_individuo(individuo, max_intentos=3)
    
    print(f"Evaluando individuo después de reparar...")
    fitness_despues = evaluar_individuo(individuo_reparado)
    print(f"  Fitness después: {fitness_despues:.2f}")
    
    # Mostrar el orden después de reparar
    lugares_reparados = get_lugares_por_ids(individuo_reparado.dias[0])
    print(f"\nOrden después de reparar:")
    for lugar in lugares_reparados:
        tipo = lugar.get('tipo', 'desconocido')
        horario = HORARIOS_TIPO.get(tipo, {"apertura": 0, "cierre": 24*60})
        print(f"  - {lugar['nombre']} ({tipo}, abre {horario['apertura']//60}:00)")
    
    mejora = fitness_despues - fitness_antes
    print(f"\nMejora de fitness: {mejora:+.2f}")
    print(f"{'✅' if mejora >= 0 else '⚠️'} Test 2 completado\n")

def main():
    """Ejecuta todos los tests."""
    print("\n" + "🔧" * 40)
    print("TESTS DE REPARACIÓN DE HORARIOS")
    print("🔧" * 40 + "\n")
    
    try:
        test_verificar_lugar_en_horario()
        test_individuo_simple()
        
        print("=" * 80)
        print("✅ TODOS LOS TESTS COMPLETADOS")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR durante los tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
