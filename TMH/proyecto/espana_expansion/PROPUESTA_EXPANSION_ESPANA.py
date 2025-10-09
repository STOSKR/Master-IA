"""
PROPUESTA: EXPANSIÓN A RUTA TURÍSTICA POR ESPAÑA
================================================

OBJETIVO: Aumentar la complejidad manteniendo la lógica simple

CAMBIOS PROPUESTOS:
==================

1. DATASET EXPANDIDO
-------------------
   ANTES: 253 lugares en Madrid
   AHORA: ~1500 lugares en 10 ciudades españolas
   
   Ciudades incluidas:
   - Madrid (253 lugares) ✓ Ya existe
   - Barcelona (200 lugares)
   - Sevilla (150 lugares)
   - Valencia (150 lugares)
   - Granada (100 lugares)
   - Bilbao (100 lugares)
   - Toledo (100 lugares)
   - Córdoba (80 lugares)
   - San Sebastián (80 lugares)
   - Santiago de Compostela (80 lugares)
   
   TOTAL: ~1,293 lugares

2. RESTRICCIÓN NUEVA: LÍMITE POR CIUDAD
---------------------------------------
   - Máximo 4 días consecutivos en la misma ciudad
   - Obliga a cambiar de ciudad periódicamente
   - Añade costo de transporte entre ciudades

3. CÁLCULO DE COMPLEJIDAD
-------------------------
   Con 1,293 lugares y límite de 4 días/ciudad:
   
   Viaje de 20 días (5 ciudades × 4 días):
   - Combinaciones de ciudades: C(10, 5) × 5! = 252 × 120 = 30,240
   - Lugares por día: C(1293, 12)
   - Días totales: 20
   - Espacio de búsqueda: [C(1293,12) × 12!]^20 × 30,240 × factores
   
   RESULTADO: ~10^400+ (mucho mayor que 10^251.5)

4. TRANSPORTE ENTRE CIUDADES
----------------------------
   - Avión: rápido (1-2h), caro (50-200€)
   - Tren AVE: medio (2-4h), medio (30-100€)
   - Bus: lento (4-8h), barato (20-50€)
   
   Añade tiempo y costo al cambiar de ciudad

5. LÓGICA SIMPLIFICADA
----------------------
   El algoritmo NO cambia, solo:
   - Añadimos campo "ciudad" a cada lugar
   - Validamos que no se excedan 4 días/ciudad
   - Calculamos transporte entre ciudades
   
   LA COMPLEJIDAD AUMENTA NATURALMENTE por:
   ✓ Más lugares (253 → 1,293)
   ✓ Más días (7 → 20)
   ✓ Restricción de cambio de ciudad
   ✓ Optimización de transporte intercity

IMPLEMENTACIÓN
=============

Opción 1: DATASET MANUAL (MÁS TRABAJO, MÁS REALISTA)
----------------------------------------------------
Crear manualmente listas de lugares para cada ciudad
Ventajas: Datos reales, más credibilidad
Desventajas: Mucho trabajo manual

Opción 2: DATASET GENERADO (RÁPIDO, SUFICIENTE)
-----------------------------------------------
Generar lugares sintéticos para cada ciudad
Ventajas: Rápido, suficiente para demostrar NP-Hard
Desventajas: Datos ficticios

Opción 3: DATASET HÍBRIDO (RECOMENDADO)
---------------------------------------
- Mantener Madrid real (253 lugares) ✓
- Generar ~100-200 lugares por ciudad basados en tipos
- Ajustar nombres, coordenadas y características
Ventajas: Balance entre realismo y eficiencia

CÓDIGO LIMPIO
=============

Simplificaciones propuestas:
1. Eliminar comentarios redundantes
2. Combinar funciones pequeñas
3. Usar comprehensions en vez de loops
4. Reducir prints de debug
5. Extraer constantes a archivo de configuración

ESTRUCTURA PROPUESTA:
====================

utils_espana.py (NUEVO)
├── lugares_turisticos_madrid (253 lugares) ✓
├── lugares_turisticos_barcelona (200 lugares)
├── lugares_turisticos_sevilla (150 lugares)
├── ... (otras ciudades)
└── DISTANCIAS_CIUDADES = {
        ("Madrid", "Barcelona"): {"avion": 1h, "tren": 2.5h, "bus": 6h},
        ...
    }

restricciones_espana.py (ACTUALIZADO)
├── validar_limite_ciudad(ruta, max_dias_ciudad=4)
├── calcular_transporte_intercity(ciudad_origen, ciudad_destino)
└── calcular_complejidad_espana(num_lugares, num_ciudades, dias)

algoritmo_genetico.py (LIMPIADO)
└── [Código simplificado sin comentarios innecesarios]

COMPLEJIDAD FINAL
================

Con la configuración propuesta:
- Lugares: 1,293
- Ciudades: 10
- Días: 20 (5 ciudades × 4 días máx.)
- Lugares/día: 12

Complejidad ≈ 10^420

ESTO ES 168 ÓRDENES DE MAGNITUD MAYOR QUE LA CONFIGURACIÓN ACTUAL (10^251.5)

¿PROCEDER?
=========

Opción A: Implementar expansión a España (Dataset híbrido)
Opción B: Solo limpiar código actual (mantener Madrid)
Opción C: Ambas (limpiar + expandir)

¿Qué prefieres?
"""

print(__doc__)
