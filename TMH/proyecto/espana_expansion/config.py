"""
Configuración centralizada del algoritmo genético de rutas turísticas
"""

# Parámetros de tiempo
TIEMPO_DIA = 16 * 60  # 960 minutos (16 horas)
TIEMPO_VISITA_PROMEDIO = 75  # minutos
HORA_INICIO = 9 * 60  # 9:00 AM
TIEMPO_COMIDA_MIN = 90  # Tiempo de comida (minutos)
TIEMPO_CENA_MIN = 90  # Tiempo de cena (minutos)
VELOCIDAD_MEDIA_KMH = 30  # Velocidad promedio en ciudad (km/h)

# Parámetros del algoritmo genético
POBLACION_DEFAULT = 10000
GENERACIONES_DEFAULT = 400
PROB_CRUCE = 0.8
PROB_MUTACION = 0.2
PROBABILIDAD_CRUCE = 0.8  # Alias
PROBABILIDAD_MUTACION = 0.2  # Alias
ELITISMO_PORCENTAJE = 0.2
SELECCION_PORCENTAJE = 0.2

# Parámetros de reset por estancamiento
UMBRAL_ESTANCAMIENTO = 30  # generaciones sin mejora

# Pesos de fitness
PESO_PUNTOS_INICIAL = 0.9
PESO_DISTANCIA_INICIAL = 1.0
AJUSTE_PESO_POR_DIA = 0.025  # Reducir a la mitad el ajuste original

# Penalizaciones
PENALIZACION_COMIDA_FALTA = 100
PENALIZACION_COMIDA_BONUS = -100
PENALIZACION_COMIDA_MAL_HORARIO = 50
PENALIZACION_FUERA_HORARIO = 200
PENALIZACION_EXCESO_TIEMPO = 5  # Por minuto de exceso
PENALIZACION_LIMITE_CIUDAD = 1000  # Si excede 4 días en misma ciudad
FACTOR_PENALIZACION_TIEMPO = 3

# Horarios de comidas
HORA_ALMUERZO_MIN = 13.5 * 60
HORA_ALMUERZO_MAX = 14.5 * 60
HORA_CENA_MIN = 20.5 * 60
HORA_CENA_MAX = 22 * 60

# Mutaciones
TIPOS_MUTACION = ['intercambio', 'inversion', 'agregar', 'quitar']
PESOS_MUTACION = [0.4, 0.3, 0.15, 0.15]

# Restricciones
RESTRICCIONES_ACTIVAS = True
PRESUPUESTO_DIARIO = 150  # euros
MAX_DIAS_POR_CIUDAD = 4  # Máximo días consecutivos en una ciudad

# Lugares mínimos por ruta
LUGARES_MIN = 4
