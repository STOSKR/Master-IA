# 🗺️ Algoritmo Genético - Rutas Turísticas

Proyecto de optimización de rutas turísticas usando algoritmos genéticos.

## 📁 Estructura del Proyecto

```
proyecto/
├── madrid_original/          ← Implementación original (Madrid, 7 días)
│   ├── algoritmo_genetico.py
│   ├── utils.py (253 lugares)
│   └── README.md
│
├── espana_expansion/         ← Nueva implementación (España, 20 días)
│   ├── algoritmo_espana.py (CÓDIGO LIMPIO)
│   ├── config.py
│   ├── utils_espana.py (1,293 lugares)
│   ├── restricciones_espana.py
│   ├── ejecutar_espana.py
│   ├── utils.py (copia para importaciones)
│   ├── ALGORITMO_ESPANA_COMPLETADO.md
│   └── README.md
│
└── [archivos auxiliares]
```

## 🎯 Dos Versiones Disponibles

### 1. Madrid Original (Simple)
- **Carpeta:** `madrid_original/`
- **Lugares:** 253 (solo Madrid)
- **Días:** 7
- **Complejidad:** 10^251.5
- **Restricciones:** Completas y complejas
- **Uso:** Pruebas rápidas, proyecto original

### 2. España Expansión (Avanzado) ⭐
- **Carpeta:** `espana_expansion/`
- **Lugares:** 1,293 (10 ciudades españolas)
- **Días:** 20
- **Complejidad:** 10^753.3
- **Restricciones:** Simplificadas + límite 4 días/ciudad
- **Código:** Limpio, profesional, optimizado
- **Uso:** Proyecto completo, mejores resultados

## 🚀 Inicio Rápido

### Madrid Original
```bash
cd madrid_original
python ejecutar_algoritmo.py
```

### España (Recomendado)
```bash
cd espana_expansion
python ejecutar_espana.py completo
```

## 📊 Comparación

| Característica | Madrid Original | España Expansión |
|----------------|-----------------|------------------|
| **Lugares** | 253 | 1,293 |
| **Ciudades** | 1 | 10 |
| **Días** | 7 | 20 |
| **Complejidad** | 10^251.5 | **10^753.3** |
| **Código** | Original | **Limpio** |
| **Restricciones** | Complejas | Simplificadas |
| **Optimización** | O(n²) | **O(1)** |
| **Reproducible** | No | **Sí (semilla)** |

## 📖 Documentación

- **Madrid:** Ver `madrid_original/README.md`
- **España:** Ver `espana_expansion/README.md`
- **Detalles completos:** Ver `espana_expansion/ALGORITMO_ESPANA_COMPLETADO.md`

## 🎓 Características Técnicas

### Algoritmo Genético
- Población: 3,000-10,000 individuos
- Generaciones: 200-600
- Elitismo: 20%
- Mutaciones: 4 tipos (swap, insert, reverse, replace)
- Selección: Torneo (k=3)
- Cruce: Dos puntos por día

### Optimizaciones (España)
- ✅ Búsqueda O(1) por ID con diccionarios
- ✅ Semilla fija para reproducibilidad
- ✅ Código modular y limpio
- ✅ Type hints completos
- ✅ Sin comentarios redundantes

## 🏆 Mejores Prácticas

1. **Para pruebas rápidas:** Usa `madrid_original/`
2. **Para proyecto completo:** Usa `espana_expansion/`
3. **Para comparar fitness:** Usa semilla fija (ya configurada)
4. **Para máxima calidad:** Ejecuta modo `intenso`

## 📝 Notas

- La semilla aleatoria está fija en `SEMILLA_LUGARES = 42` (España)
- Los lugares de Madrid son REALES en ambas versiones
- Los lugares de otras ciudades son generados (reproducibles)
- Todas las comparaciones de fitness son válidas con la semilla fija

---

**Versión:** 2.0  
**Última actualización:** Octubre 2025  
**Estado:** ✅ Ambas versiones funcionando
