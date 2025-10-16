# ⚠️ Guía de Ejecución en Paralelo - Carga del Sistema

## ¿Se Me Reventará el Ordenador?

### Respuesta Corta: **NO, pero hay límites** 🔧

Tu ordenador **NO se romperá**, pero puede volverse **MUY LENTO** si ejecutas demasiados procesos a la vez.

---

## 📊 Consumo de Recursos por Proceso

### CPU (Procesador)
- **1 proceso**: ~15-25% de 1 núcleo = **1-2 núcleos ocupados**
- **3 procesos**: ~50-75% CPU total (en máquina de 4-8 núcleos)
- **5 procesos**: ~80-100% CPU total
- **8+ procesos**: CPU al 100%, sistema muy lento

### RAM (Memoria)
- **1 proceso**: ~300-500 MB
- **3 procesos**: ~1-1.5 GB
- **5 procesos**: ~2-2.5 GB
- **10 procesos**: ~5 GB

### Disco
- Mínimo impacto (solo al guardar resultados al final)

---

## 💻 ¿Cuántos Procesos Puedo Ejecutar?

### Recomendaciones por Tipo de PC:

#### 🟢 PC Básica (4 núcleos, 8 GB RAM)
- **Máximo recomendado**: 2-3 procesos en paralelo
- **Óptimo**: 2 procesos
- **Ejemplo**: 
  ```
  - Config 1: Población 500
  - Config 2: Población 1000
  ```

#### 🟡 PC Media (6-8 núcleos, 16 GB RAM)
- **Máximo recomendado**: 4-5 procesos en paralelo
- **Óptimo**: 3-4 procesos
- **Ejemplo**:
  ```
  - Config 1: Población 500
  - Config 2: Población 1500
  - Config 3: Población 3000
  - Config 4: Elitismo diferente
  ```

#### 🟢 PC Potente (12+ núcleos, 32 GB RAM)
- **Máximo recomendado**: 8-10 procesos en paralelo
- **Óptimo**: 6-8 procesos
- **Puedes lanzar**: Comparativa completa de elitismo (5 configs) + poblaciones (3 configs)

---

## 🔍 Cómo Saber las Especificaciones de Tu PC

### En Windows:

```powershell
# Ver número de núcleos
wmic cpu get NumberOfCores,NumberOfLogicalProcessors

# Ver RAM total
wmic computersystem get TotalPhysicalMemory

# O más simple: Abrir Task Manager (Ctrl+Shift+Esc)
# Pestaña "Rendimiento" -> Ver CPU y RAM
```

**Ejemplo de salida:**
```
NumberOfCores  NumberOfLogicalProcessors
8              16
```
- **8 núcleos físicos** = Puedes ejecutar 4-6 procesos cómodamente
- **16 hilos lógicos** = Con HyperThreading/SMT

---

## 🚦 Señales de Sobrecarga

### ⚠️ Tu PC está sobrecargado si:
- ❌ El mouse se mueve con lag
- ❌ Las ventanas tardan en abrirse
- ❌ El ventilador suena muy fuerte constantemente
- ❌ Task Manager muestra CPU al 100% todo el tiempo
- ❌ Otras aplicaciones se congelan

### ✅ Tu PC está bien si:
- ✅ El mouse se mueve fluidamente
- ✅ Puedes navegar por internet normalmente
- ✅ Task Manager muestra CPU 70-90% (es normal)
- ✅ El ventilador suena más pero no excesivamente

---

## 🎯 Estrategias Recomendadas

### Estrategia 1: Secuencial (Más Seguro)
```
Día 1: Ejecutar Config 1 (8h overnight)
Día 2: Ejecutar Config 2 (8h overnight)
Día 3: Ejecutar Config 3 (8h overnight)
```
✅ **Ventaja**: Sin riesgo de sobrecarga  
❌ **Desventaja**: 3 días para 3 configuraciones

### Estrategia 2: Paralelo Moderado (Recomendado)
```
Overnight: Ejecutar 2-3 configs simultáneas (8h)
```
✅ **Ventaja**: 3x más rápido que secuencial  
✅ **Seguro para la mayoría de PCs**

### Estrategia 3: Paralelo Intensivo (Solo PCs Potentes)
```
Overnight: Ejecutar 5-8 configs simultáneas
```
✅ **Ventaja**: Máxima eficiencia  
⚠️ **Requiere**: PC potente (8+ núcleos, 16+ GB RAM)

### Estrategia 4: Mixta (Más Inteligente)
```
Configuraciones pesadas (población grande): 1-2 en paralelo
Configuraciones ligeras (población pequeña): 3-4 en paralelo
```
**Ejemplo**:
```powershell
# Lanzar 2 configs pesadas
lanzar_config3.bat  # Población 3000
lanzar_intensivo_12h.bat  # Población 2000

# O lanzar 4 configs ligeras
lanzar_config1.bat  # Población 500
lanzar_elitismo_05.bat  # Población 1000
lanzar_elitismo_15.bat  # Población 1000
lanzar_quick_2h.bat  # Población 500
```

---

## 📋 Guía Práctica de Ejecución

### Antes de Lanzar en Paralelo:

1. **Cierra programas innecesarios**
   - Navegador con muchas pestañas
   - Juegos
   - Editores de video
   - Otros programas pesados

2. **Verifica recursos disponibles**
   ```
   Abre Task Manager (Ctrl+Shift+Esc)
   Pestaña "Rendimiento"
   - CPU debe estar < 30% en reposo
   - RAM debe tener al menos 4 GB libres
   ```

3. **Planifica cuántos procesos lanzar**
   ```
   Núcleos de CPU ÷ 2 = Procesos recomendados
   
   Ejemplos:
   - 4 núcleos → 2 procesos
   - 6 núcleos → 3 procesos
   - 8 núcleos → 4 procesos
   - 12 núcleos → 6 procesos
   ```

### Durante la Ejecución:

1. **Monitorea el Task Manager**
   - CPU: OK si está 70-95%
   - RAM: OK si no llega al 90%

2. **Si el PC se pone muy lento**:
   ```
   - Abre una terminal que esté ejecutando
   - Presiona Ctrl+C para detener
   - Espera que termine
   - El sistema volverá a la normalidad
   ```

3. **Puedes seguir usando el PC** para:
   ✅ Navegar internet (ligero)
   ✅ Editar documentos
   ✅ Ver videos (puede ir un poco lento)
   ✅ Programar en editor de texto
   
   ❌ NO recomendado durante ejecución:
   - Juegos
   - Edición de video
   - Compilar código grande
   - Otros entrenamientos de IA

---

## 🔧 Configuraciones por Tipo de Experimento

### Experimento Overnight (8 horas)

#### PC Básica (4 núcleos):
```powershell
# Lanzar SOLO 2 configuraciones
lanzar_config1.bat  # Población 500
lanzar_config2.bat  # Población 1500
```

#### PC Media (6-8 núcleos):
```powershell
# Usar el script maestro (3 configs)
lanzar_todas_paralelo.bat
```

#### PC Potente (12+ núcleos):
```powershell
# Lanzar comparativa completa de elitismo
lanzar_comparativa_elitismo.bat  # 5 configs
```

### Experimento Rápido (2-4 horas)

Cualquier PC puede ejecutar 2-3 configuraciones:

```powershell
# Terminal 1
lanzar_quick_2h.bat

# Terminal 2
lanzar_elitismo_15.bat

# Terminal 3 (opcional, solo si PC > 4 núcleos)
lanzar_elitismo_25.bat
```

---

## 🆘 Solución de Problemas

### Problema: "Mi PC va muy lento"

**Solución**:
1. Abre Task Manager (Ctrl+Shift+Esc)
2. Pestaña "Detalles" o "Procesos"
3. Busca `python.exe`
4. Clic derecho → "Finalizar tarea" en UNO de ellos
5. Espera 10 segundos
6. El PC debería mejorar

### Problema: "No puedo detener un proceso"

**Solución**:
```powershell
# En PowerShell
taskkill /F /IM python.exe

# Esto mata TODOS los procesos Python
# Solo úsalo si no tienes otros scripts Python importantes corriendo
```

### Problema: "El PC se congeló completamente"

**Solución**:
1. Espera 30 segundos (puede estar solo muy lento)
2. Si no responde: Ctrl+Alt+Del → Task Manager
3. Si ni eso funciona: Mantén presionado el botón de encendido 5 segundos (apagado forzado)
4. **Nota**: Los resultados parciales NO se guardarán

---

## 💾 Guardar Trabajo Antes de Ejecutar

### ⚠️ IMPORTANTE:

Antes de lanzar ejecuciones largas (4+ horas):

1. **Guarda todo tu trabajo abierto**
   - Documentos
   - Código
   - Navegador (guarda pestañas importantes)

2. **Deshabilita suspensión**
   ```
   Panel de Control → Opciones de Energía
   → "Nunca" en "Suspender equipo"
   ```

3. **Deshabilita actualizaciones automáticas**
   ```
   Windows Update → Pausar actualizaciones por 1 semana
   ```

4. **Conecta el portátil a corriente** (no usar batería)

---

## 📊 Tabla de Referencia Rápida

| Núcleos CPU | RAM   | Procesos Seguros | Procesos Máximo | Ejemplo de Uso          |
|-------------|-------|------------------|-----------------|-------------------------|
| 2-4         | 4-8GB | 1-2              | 2-3             | 2 configs overnight     |
| 4-6         | 8-16GB| 2-3              | 4-5             | 3 configs overnight     |
| 6-8         | 16GB  | 3-4              | 5-6             | Comparativa elitismo    |
| 8-12        | 16-32GB| 4-6             | 8-10            | Múltiples comparativas  |
| 12+         | 32GB+ | 6-8              | 12+             | Experimentos masivos    |

---

## 🎓 Resumen de Mejores Prácticas

### ✅ HACER:
- Empezar con 1-2 procesos para probar
- Monitorear Task Manager la primera vez
- Cerrar programas innecesarios
- Ejecutar overnight cuando no uses el PC
- Guardar todo antes de lanzar
- Usar `--output-dir` diferente para cada experimento

### ❌ NO HACER:
- Lanzar más procesos que núcleos de CPU
- Dejar el PC sin supervisión en la primera ejecución larga
- Ejecutar mientras juegas o editas video
- Llenar la RAM al 100%
- Olvidar deshabilitar suspensión en ejecuciones largas

---

## 🚀 Recomendación Final

**Para empezar (Primera vez)**:
```powershell
# Prueba de 30 minutos con 1 solo proceso
lanzar_test_30min.bat

# Si todo va bien, lanza 2 procesos de 2 horas
lanzar_quick_2h.bat
# Y en otra terminal:
lanzar_elitismo_15.bat
```

**Una vez probado (Overnight)**:
```powershell
# PC Básica/Media: 2-3 procesos
lanzar_todas_paralelo.bat

# PC Potente: 5 procesos
lanzar_comparativa_elitismo.bat
```

---

**Tu PC estará bien. Solo respeta los límites de tus recursos y no tendrás problemas. 💪**
