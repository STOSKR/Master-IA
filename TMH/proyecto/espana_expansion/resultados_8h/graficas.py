import json
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos del JSON
with open('Pob_5000_17_03_18.json', 'r') as f:
    data = json.load(f)

historial_fitness = data['historial_fitness']
generaciones = range(len(historial_fitness))

# --- Creación del Gráfico Multi-Panel ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 7))
fig.suptitle('Análisis de la Evolución del Fitness (Pob_5000)', fontsize=16, fontweight='bold')

# --- Panel 1: Vista Completa ---
ax1.plot(generaciones, historial_fitness, color='steelblue', linewidth=2)
ax1.set_title('1. Convergencia Global', fontsize=14)
ax1.set_xlabel('Generación')
ax1.set_ylabel('Fitness')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.text(0.05, 0.1, 'Muestra el gran salto inicial\nal eliminar penalizaciones.', 
         transform=ax1.transAxes, fontsize=10, style='italic')


# --- Panel 2: Vista "Zoom" en Fitness Positivo ---
# Filtrar datos para que solo se muestren los positivos
fitness_positivos = [f for f in historial_fitness if f >= 0]
primera_gen_positiva = len(historial_fitness) - len(fitness_positivos)
generaciones_positivas = range(primera_gen_positiva, len(historial_fitness))

ax2.plot(generaciones_positivas, fitness_positivos, color='green', linewidth=2)
ax2.set_title('2. Fase de Optimización Fina (Fitness > 0)', fontsize=14)
ax2.set_xlabel('Generación')
ax2.set_ylabel('Fitness')
ax2.set_ylim(0, max(historial_fitness) * 1.1) # Empezar eje Y en 0
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.text(0.05, 0.1, 'Muestra la mejora gradual\nuna vez la ruta es válida.', 
         transform=ax2.transAxes, fontsize=10, style='italic')


# --- Panel 3: Tasa de Mejora ---
# Calcular la diferencia entre generaciones consecutivas
mejoras = np.diff(historial_fitness, prepend=historial_fitness[0])
mejoras[mejoras < 0] = 0 # Solo mostrar mejoras positivas

ax3.bar(generaciones, mejoras, color='purple', alpha=0.7)
ax3.set_title('3. Tasa de Mejora por Generación', fontsize=14)
ax3.set_xlabel('Generación')
ax3.set_ylabel('Incremento de Fitness')
ax3.grid(True, axis='y', linestyle='--', alpha=0.6)
# Usar escala logarítmica para ver tanto las mejoras grandes como las pequeñas
ax3.set_yscale('log')
ax3.text(0.05, 0.1, 'Picos altos al inicio, mejoras\npequeñas al final (convergencia).', 
         transform=ax3.transAxes, fontsize=10, style='italic')


# --- Guardar la figura ---
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('analisis_convergencia_mejorado.png', dpi=300)

print("Gráfico multi-panel guardado como 'analisis_convergencia_mejorado.png'")