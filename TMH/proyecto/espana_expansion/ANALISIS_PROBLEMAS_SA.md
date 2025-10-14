# Análisis de Problemas en Enfriamiento Simulado

## Fecha: 2025-10-14

## Problema Identificado
El algoritmo de enfriamiento simulado (SA) no está mejorando los resultados del algoritmo genético (GA) en el modo híbrido.

## Análisis del Código Actual

### 1. Generación de Vecinos (`generar_vecino`)

**Problemas encontrados:**

#### a) Vecindad muy limitada
```python
tipo_perturbacion = random.choices(
    ["swap", "reemplazar", "cambiar_ciudad"],
    weights=[0.70, 0.20, 0.10]
)[0]
```

- **70% swap**: Solo intercambia dos lugares dentro del mismo día
  - Impacto limitado en el fitness
  - No cambia significativamente la estructura
  
- **20% reemplazar**: Cambia un lugar por otro de la misma ciudad
  - Puede mejorar, pero es muy local
  
- **10% cambiar ciudad**: Es la única operación que cambia estructura
  - Muy poco frecuente (solo 1 de cada 10 vecinos)
  - Además tiene muchas restricciones que pueden impedir el cambio

#### b) Restricciones demasiado estrictas
```python
# No regresar a ciudades ya visitadas
ciudades_visitadas = set(vecino.ciudades[:dia_idx])

# Filtrar ciudades candidatas
candidatas = []
for c in ciudades_disponibles:
    if c == ciudad_actual:
        continue
    if c in ciudades_visitadas:  # <- Muy restrictivo
        continue
    candidatas.append(c)
```

Esto hace que casi nunca se pueda cambiar de ciudad, limitando severamente la exploración.

#### c) Duplicados reducen calidad
La función `eliminar_duplicados_dia` se llama al final, pero el proceso de generación puede introducir lugares duplicados que luego son reemplazados por lugares aleatorios, reduciendo la calidad del vecino.

### 2. Temperatura Inicial

**En modo híbrido:**
```python
resultados_sa = enfriamiento_desde_genetico(
    resultados_genetico=resultados_ga,
    usar_mejor=True,
    T_inicial=1000,  # <- MUY BAJA
    alpha=0.98,
    max_iteraciones=5000
)
```

**Problema**: 
- T_inicial = 1000 es muy baja cuando se parte de una solución de alta calidad (el mejor del GA)
- Con temperatura baja, la probabilidad de aceptar soluciones peores es casi nula
- Esto convierte al SA en una búsqueda voraz (greedy), sin capacidad de escapar de óptimos locales

### 3. Probabilidad de Aceptación

Con temperatura T=1000 y una solución que empeora en ΔE=-100:

```
P = exp(-100 / 1000) = exp(-0.1) ≈ 0.90  (90% de aceptación)
```

Pero después de 100 iteraciones con α=0.98:
```
T = 1000 * 0.98^100 ≈ 132
P = exp(-100 / 132) ≈ 0.46  (46% de aceptación)
```

Y después de 500 iteraciones:
```
T = 1000 * 0.98^500 ≈ 0.0165
P = exp(-100 / 0.0165) ≈ 0  (prácticamente 0%)
```

**Conclusión**: El algoritmo pierde rápidamente su capacidad de exploración.

### 4. Función de Fitness

La función de fitness del GA penaliza fuertemente:
- Cambios de ciudad (transporte intercity)
- Distancias dentro de días
- Tiempo de visitas

Esto hace que cualquier cambio significativo (como cambiar ciudades) tienda a empeorar el fitness inicialmente, y con temperatura baja, estos cambios nunca son aceptados.

## Soluciones Propuestas

### Solución 1: Mejorar la Generación de Vecinos

```python
# Aumentar probabilidad de cambios estructurales
tipo_perturbacion = random.choices(
    ["swap", "reemplazar", "cambiar_ciudad", "swap_intercity", "ruta_2opt"],
    weights=[0.40, 0.20, 0.20, 0.10, 0.10]
)[0]
```

**Nuevas operaciones:**

#### a) `swap_intercity`: Intercambiar días completos
```python
elif tipo_perturbacion == "swap_intercity":
    # Intercambiar dos días completos (incluida la ciudad)
    if len(vecino.dias) >= 2:
        i, j = random.sample(range(len(vecino.dias)), 2)
        vecino.dias[i], vecino.dias[j] = vecino.dias[j], vecino.dias[i]
        vecino.ciudades[i], vecino.ciudades[j] = vecino.ciudades[j], vecino.ciudades[i]
```

#### b) `ruta_2opt`: Optimización 2-opt dentro de un día
```python
elif tipo_perturbacion == "ruta_2opt":
    # Mejorar orden de visita dentro de un día (minimizar distancia)
    dia_idx = random.randint(0, len(vecino.dias) - 1)
    dia = vecino.dias[dia_idx]
    if len(dia) >= 4:
        i = random.randint(0, len(dia) - 3)
        j = random.randint(i + 2, len(dia))
        # Invertir segmento [i+1:j]
        vecino.dias[dia_idx] = dia[:i+1] + dia[i+1:j][::-1] + dia[j:]
```

#### c) Relajar restricciones de cambio de ciudad
```python
# Permitir volver a ciudades visitadas si mejora el fitness
# Solo aplicar restricción en generación inicial
```

### Solución 2: Ajustar Temperatura Inicial

**Para modo híbrido (desde GA):**
```python
# Opción A: Temperatura adaptativa basada en fitness
T_inicial = abs(solucion_inicial.fitness) * 0.1  # 10% del fitness inicial

# Opción B: Temperatura alta para permitir exploración
T_inicial = 5000  # En lugar de 1000
```

**Para modo standalone (desde cero):**
```python
T_inicial = 2000  # Mantener actual
```

### Solución 3: Esquema de Enfriamiento Adaptativo

En lugar de enfriamiento geométrico fijo, usar enfriamiento adaptativo:

```python
# Si encuentra mejoras, enfriar más lento
if mejoras_recientes > 0:
    alpha_actual = 0.99  # Enfriar más lento
else:
    alpha_actual = 0.95  # Enfriar más rápido

temperatura = temperatura * alpha_actual
```

O usar enfriamiento de Lundy-Mees:
```python
temperatura = temperatura / (1 + beta * temperatura)
```

### Solución 4: Multi-Start con Perturbación

En lugar de partir del mejor del GA, partir de diferentes soluciones del top 10 y ejecutar SA en cada una:

```python
def enfriamiento_multistart(resultados_ga, num_starts=5):
    top_10 = sorted(poblacion_final, key=lambda x: x.fitness, reverse=True)[:10]
    
    mejores_sa = []
    for i in range(num_starts):
        inicio = random.choice(top_10)
        resultado_sa = enfriamiento_simulado(inicio, T_inicial=3000)
        mejores_sa.append(resultado_sa)
    
    return max(mejores_sa, key=lambda r: r['mejor_solucion'].fitness)
```

### Solución 5: SA como Perturbación Fuerte

Implementar operador de perturbación fuerte cada N iteraciones:

```python
if iteracion % 500 == 0 and iteraciones_sin_mejora > 100:
    # Perturbación fuerte: cambiar múltiples ciudades
    for _ in range(5):
        dia_aleatorio = random.randint(0, len(solucion_actual.dias) - 1)
        # Cambiar ciudad y regenerar día
```

## Recomendación Final

**Implementar en orden:**

1. ✅ **Prioridad Alta**: Solución 1 - Mejorar vecindad (agregar swap_intercity y 2-opt)
2. ✅ **Prioridad Alta**: Solución 2 - Aumentar temperatura inicial a 5000 en modo híbrido
3. ✅ **Prioridad Media**: Solución 3 - Enfriamiento adaptativo
4. ⚠️ **Prioridad Baja**: Solución 4 - Multi-start (costoso computacionalmente)
5. ⚠️ **Opcional**: Solución 5 - Perturbación fuerte (puede ser contraproducente)

## Métricas para Validar Mejoras

Después de implementar las soluciones, medir:

1. **Tasa de mejora**: ¿SA mejora el fitness del GA?
2. **Tasa de aceptación**: Debe estar entre 30-60% al inicio, 5-15% al final
3. **Número de mejoras encontradas**: Debe ser > 10 en 5000 iteraciones
4. **Mejora porcentual**: Objetivo > 1% de mejora sobre el mejor del GA

## Conclusión

El problema principal es que el SA está configurado para refinamiento muy local, cuando en realidad necesita hacer exploración significativa para escapar del óptimo local donde está el GA. Las soluciones propuestas aumentan la capacidad de exploración sin sacrificar convergencia.
