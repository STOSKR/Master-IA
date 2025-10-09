# 🇪🇸 España - Expansión Multi-Ciudad

Esta carpeta contiene la implementación **nueva y limpia** del algoritmo genético para rutas turísticas por toda España.

## 📋 Archivos Principales

### Código Limpio
- **`algoritmo_espana.py`** - Algoritmo genético limpio desde cero (código profesional)
- **`config.py`** - Configuración centralizada (todas las constantes)
- **`utils_espana.py`** - Dataset de 1,293 lugares en 10 ciudades españolas
- **`restricciones_espana.py`** - Restricciones simplificadas + límite 4 días/ciudad
- **`ejecutar_espana.py`** - Script de ejecución con 4 modos

### Soporte
- **`utils.py`** - Dataset original de Madrid (usado para generar lugares)

### Documentación
- **`ALGORITMO_ESPANA_COMPLETADO.md`** - Documentación completa del sistema
- **`RESUMEN_EXPANSION_ESPANA.md`** - Resumen ejecutivo
- **`PROPUESTA_EXPANSION_ESPANA.py`** - Propuesta inicial

## 📊 Características

- **Lugares:** 1,293 lugares turísticos en 10 ciudades
  - Madrid: 253 lugares REALES
  - Barcelona: 200 lugares
  - Sevilla, Valencia: 150 cada una
  - Granada, Bilbao, Toledo: 100 cada una
  - Córdoba, San Sebastián, Santiago: 80 cada una

- **Días:** 20 días de viaje
- **Complejidad:** 10^753.3 (501 órdenes de magnitud mayor que Madrid)
- **Restricción clave:** Máximo 4 días consecutivos por ciudad
- **Transporte:** Avión, Tren AVE, Bus entre ciudades

## 🎯 Ventajas vs. Madrid Original

✅ **Complejidad brutal:** 10^753.3 vs 10^251.5  
✅ **Código limpio:** Sin comentarios redundantes, funciones cortas  
✅ **Lógica simple:** Solo límite de ciudad + fatiga básica  
✅ **Optimizado:** Búsqueda O(1) con diccionarios  
✅ **Reproducible:** Semilla fija (SEMILLA_LUGARES = 42)  
✅ **Multi-ciudad:** 10 ciudades españolas  

## 🚀 Cómo ejecutar

### Modo rápido (prueba)
```bash
cd espana_expansion
python ejecutar_espana.py rapido
```

### Modo completo (recomendado)
```bash
python ejecutar_espana.py completo
```

### Modos disponibles
- **`rapido`** - 3,000 población, 200 generaciones (~5 min)
- **`medio`** - 5,000 población, 400 generaciones (~15 min)
- **`completo`** - 8,000 población, 500 generaciones (~30 min)
- **`intenso`** - 10,000 población, 600 generaciones (~60 min)

## 📈 Resultados esperados

- **Fitness:** 15,000-18,000
- **Puntos:** 17,000-19,000
- **Tiempo:** 350-450 horas
- **Distancia:** 900-1,200 km
- **Ciudades visitadas:** 5-8 ciudades

## 🔧 Configuración

### Semilla aleatoria (reproducibilidad)
En `utils_espana.py`:
```python
SEMILLA_LUGARES = 42  # Genera siempre los mismos lugares
```

### Parámetros principales
En `config.py`:
```python
TIEMPO_DIA = 960  # 16 horas por día
MAX_DIAS_POR_CIUDAD = 4  # Máximo 4 días consecutivos
PROBABILIDAD_CRUCE = 0.8
PROBABILIDAD_MUTACION = 0.2
```

## 📄 Salida

El algoritmo genera:
- **JSON:** `resultados_espana_{modo}.json` con toda la información
- **Consola:** Análisis detallado día por día
- **Métricas:** Fitness, puntos, tiempo, distancia, ciudades visitadas

## 🎓 Complejidad Demostrada

```
Configuración:
- Lugares: 1,293
- Ciudades: 10
- Días: 20
- Lugares/día: 12
- Max días/ciudad: 4

Cálculo:
Combinaciones/día: C(1293,12) = 4.33×10^28
Permutaciones/día: 4.33×10^28 × 12! = 2.07×10^37
Espacio total: (2.07×10^37)^20 × combinaciones_ciudades

RESULTADO: 10^753.3
```

### Contexto
- Átomos en universo: 10^80
- TSP 100 ciudades: 10^157
- Madrid: 10^251.5
- **España: 10^753.3** ⭐

---

**Versión:** 1.0 - Código Limpio  
**Fecha:** Octubre 2025  
**Complejidad:** 10^753.3  
**Estado:** ✅ Funcionando perfectamente
