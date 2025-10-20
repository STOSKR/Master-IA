# Guión de Presentación - "Long Long Way..." (5 minutos)

## 📍 RESPUESTA: Ubicación del sistema de FPS

**El sistema de FPS se encuentra en el archivo `src/main.js`:**

```javascript
// Líneas 18-19
import Stats from 'three/examples/jsm/libs/stats.module.js';

// Líneas 21-22 dentro de startGame()
const stats = new Stats();
document.body.appendChild(stats.dom);

// Línea 141 dentro de animate()
stats.update();
```

El contador de FPS utiliza la librería **Stats.js** de Three.js, que se inicializa al arrancar el juego y se actualiza en cada frame del bucle de animación.

---

## 🎮 GUIÓN DE PRESENTACIÓN DEL VIDEOJUEGO

### **[0:00 - 0:30] INTRODUCCIÓN Y CONCEPTO**

*"Hola, hoy voy a presentar mi proyecto de videojuego desarrollado con Three.js: **'Long Long Way...'** - un juego arcade inspirado en el clásico Crossy Road, donde controlamos a un vaquero del oeste que debe atravesar carreteras, ríos y bosques para avanzar lo máximo posible."*

**DEMOSTRACIÓN:** Mostrar pantalla inicial y primeros movimientos del personaje.

---

### **[0:30 - 1:15] MODELO DEL PERSONAJE Y TEXTURAS**

*"El personaje principal es un modelo 3D en formato GLB que he cargado usando **GLTFLoader** de Three.js. El modelo del vaquero está escalado 8 veces su tamaño original y tiene las rotaciones ajustadas para que mire en la dirección correcta."*

**CARACTERÍSTICAS TÉCNICAS:**
- Modelo cargado asincrónicamente desde `/models/vaquero.glb`
- Sistema de sombras activado: el personaje proyecta y recibe sombras (`castShadow` y `receiveShadow`)
- Altura ajustada para que no atraviese el suelo (posición Z = 5)

**DEMOSTRACIÓN:** Rotar cámara para mostrar el modelo desde diferentes ángulos.

*"El modelo está organizado en un contenedor padre que gestiona la posición, y un grupo visual hijo que gestiona las animaciones de movimiento y salto."*

---

### **[1:15 - 2:00] SISTEMA DE ILUMINACIÓN**

*"Para crear una atmósfera cálida y realista, he implementado un sistema de iluminación múltiple:"*

**1. Luz Ambiental** - Color cálido (0xfff8dc) con intensidad 0.6, proporciona iluminación base suave

**2. Luz Direccional** - Simula el sol, sigue al jugador y proyecta sombras dinámicas en tiempo real

**3. Luz Hemisférica** - Simula luz del cielo (color celeste arriba, verde abajo) con intensidad 0.4 para realismo atmosférico

*"Además, tenemos un skybox con gradiente de cielo celeste y niebla en el horizonte que se desvanece entre 600 y 1000 unidades de distancia."*

**DEMOSTRACIÓN:** Mostrar cómo las sombras siguen al jugador y el efecto de niebla a lo lejos.

---

### **[2:00 - 2:45] GENERACIÓN PROCEDURAL Y VEHÍCULOS**

*"El mapa se genera de forma procedural. A medida que avanzas, se van creando nuevas filas de carreteras, ríos y bosques de manera aleatoria."*

**TIPOS DE OBSTÁCULOS:**
- **Carreteras con coches** - Coches de colores aleatorios que se desplazan a diferentes velocidades
- **Carreteras con camiones** - Vehículos más grandes y lentos
- **Ríos con troncos** - Troncos flotantes que sirven de plataformas móviles
- **Bosques con árboles** - Árboles de alturas variables como obstáculos estáticos

*"Los vehículos tienen un sistema de fade-in/fade-out: aparecen y desaparecen gradualmente en los bordes del mapa para dar sensación de continuidad, ajustando su opacidad según la distancia."*

**CÓDIGO CLAVE:** `animateVehicles.js` - líneas 30-55

**DEMOSTRACIÓN:** Mostrar cómo los coches aparecen gradualmente y diferentes tipos de obstáculos.

---

### **[2:45 - 3:30] SISTEMA DE PARTÍCULAS Y EFECTOS**

*"He implementado dos sistemas de efectos visuales avanzados:"*

**1. SISTEMA DE PARTÍCULAS** (`particleSystem.js`)
   - **Polvo al aterrizar** - 8 partículas de color arena cuando el jugador cae al suelo
   - **Salpicaduras de agua** - 12 partículas azules cuando salta al río
   - **Humo de escape** - Partículas grises que salen de los vehículos (se expanden con el tiempo)
   
   *"Todas las partículas tienen física: gravedad, velocidad inicial, y se desvanecen gradualmente hasta desaparecer."*

**2. SISTEMA DE CLIMA** (`weatherSystem.js`)
   - **Lluvia dinámica** - Hasta 100 gotas de lluvia que siguen al jugador
   - **Transición suave** - La intensidad de la lluvia aumenta y disminuye gradualmente
   - **Reciclaje de gotas** - Las gotas se resetean cuando tocan el suelo

**DEMOSTRACIÓN:** Saltar varias veces para mostrar polvo, entrar al agua para ver salpicaduras.

---

### **[3:30 - 4:15] CONTROLES Y SISTEMA DE CÁMARAS**

*"El juego tiene dos sistemas de control:"*

**CONTROLES:**
- **Teclado:** Flechas direccionales (arriba, abajo, izquierda, derecha)
- **Táctil:** Botones en pantalla para dispositivos móviles
- **Tecla R:** Reiniciar juego cuando mueres

*"Sistema de cámara doble:"*

**CÁMARA PRINCIPAL** - Vista isométrica ortográfica que sigue al jugador desde atrás
   - Se ajusta automáticamente según el ratio de pantalla

**MINIMAPA** - Vista cenital en la esquina superior derecha
   - Cámara ortográfica con zoom 3x
   - Tamaño 200x200 píxeles con margen de 10px
   - Renderizado usando scissor test para no interferir con la vista principal

**DEMOSTRACIÓN:** Mover el personaje mostrando cómo ambas cámaras siguen la acción, redimensionar ventana.

---

### **[4:15 - 4:50] ANIMACIONES Y FÍSICA DEL JUGADOR**

*"El jugador tiene un sistema de animación suave con interpolación:"*

- **Movimientos suaves** - Transiciones fluidas entre casillas usando lerp (interpolación lineal)
- **Sistema de saltos** - Animación de arco parabólico cuando salta sobre un obstáculo inválido
- **Movimiento sobre troncos** - El jugador se mueve con los troncos en el río
- **Cola de movimientos** - Los comandos se encolan y ejecutan secuencialmente

*"También hay un sistema de detección de colisiones continuo que verifica si el jugador choca con coches o camiones, activando la animación de muerte."*

**DEMOSTRACIÓN:** Intentar saltar sobre un árbol, moverse sobre troncos, chocar con un coche.

---

### **[4:50 - 5:00] CONCLUSIÓN**

*"En resumen, este proyecto combina:**
- Carga de modelos 3D externos
- Sistema de iluminación multicapa
- Generación procedural de contenido
- Efectos de partículas avanzados
- Sistema de clima dinámico
- Física y animaciones suaves
- Interfaz responsive con doble cámara

**Todo implementado con Three.js y JavaScript vanilla. ¡Gracias!"**

---

## 📋 CHECKLIST DE DEMOSTRACIÓN

Durante el video, asegúrate de mostrar:

✅ Pantalla de inicio y controles  
✅ Modelo 3D del vaquero desde varios ángulos  
✅ Sombras dinámicas en movimiento  
✅ Diferentes tipos de vehículos (coches y camiones)  
✅ Efecto de fade-in/fade-out de vehículos  
✅ Partículas de polvo al saltar  
✅ Salpicaduras de agua al entrar al río  
✅ Sistema de lluvia activándose  
✅ Movimiento sobre troncos flotantes  
✅ Minimapa funcionando  
✅ Contador de puntuación  
✅ Colisión con vehículo y pantalla de Game Over  
✅ Botón de reinicio funcionando  

---

## 🎥 CONSEJOS PARA LA GRABACIÓN

1. **Activa el contador de FPS** (ya está activado automáticamente) para mostrar rendimiento
2. **Graba en 1080p** mínimo para que se vean bien los detalles
3. **Usa zoom en momentos clave** (partículas, sombras, efectos)
4. **Muestra el código brevemente** cuando menciones aspectos técnicos importantes
5. **Practica los movimientos antes** para hacer una demo fluida
6. **Mantén un ritmo constante** - no te detengas mucho en cada punto

¡Buena suerte con la presentación! 🎮✨
