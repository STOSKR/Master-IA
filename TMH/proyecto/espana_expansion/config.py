TIEMPO_DIA = 16 * 60
TIEMPO_VISITA_PROMEDIO = 75
HORA_INICIO = 9 * 60
TIEMPO_COMIDA_MIN = 90
TIEMPO_CENA_MIN = 90
VELOCIDAD_MEDIA = 15

POBLACION_DEFAULT = 10000
GENERACIONES_DEFAULT = 400
PROB_CRUCE = 0.8
PROB_MUTACION = 0.35 
PROBABILIDAD_CRUCE = 0.8  
PROBABILIDAD_MUTACION = 0.35
ELITISMO_PORCENTAJE = 0.15 
SELECCION_PORCENTAJE = 0.2

UMBRAL_ESTANCAMIENTO = 50

PESO_PUNTOS_INICIAL = 0.9
PESO_DISTANCIA_INICIAL = 1.0
AJUSTE_PESO_POR_DIA = 0.01

# Penalizaciones
PENALIZACION_COMIDA_FALTA = 100  # Reducido de 200 → 100
PENALIZACION_CENA_FALTA = 100    # Reducido de 200 → 100
PENALIZACION_COMIDA_MAL_HORARIO = 100  # Reducido de 200 → 100
PENALIZACION_FUERA_HORARIO = 500  # CRÍTICA: Visitas fuera de horario no son aceptables
PENALIZACION_EXCESO_TIEMPO = 50   # Reducido de 100 → 50 (más gradual)
PENALIZACION_LIMITE_CIUDAD = 100
PENALIZACION_RESTAURANTES_CONSECUTIVOS = 200  # Reducido de 300 → 200
FACTOR_PENALIZACION_TIEMPO = 3
PENALIZACION_FUERA_HORARIO_APERTURA = 800  # CRÍTICA: Imposible visitar fuera de apertura
PENALIZACION_EXCESO_PRESUPUESTO = 10
PENALIZACION_CAMBIO_CIUDAD_INNECESARIO = 300  # Reducido de 1000 → 300 (MÁS RAZONABLE)
PENALIZACION_DISTANCIA_POR_KM = 0.3  # Reducido de 0.5 → 0.3 (más gradual)

# Horarios de comidas
HORA_DESAYUNO_MIN = 8 * 60  
HORA_DESAYUNO_MAX = 10 * 60
HORA_ALMUERZO_MIN = 13 * 60
HORA_ALMUERZO_MAX = 15 * 60
HORA_CENA_MIN = 20 * 60
HORA_CENA_MAX = 22 * 60

# Mutaciones
TIPOS_MUTACION = ['intercambio', 'inversion', 'agregar', 'quitar']
PESOS_MUTACION = [0.4, 0.3, 0.15, 0.15]

# Restricciones
RESTRICCIONES_ACTIVAS = True
PRESUPUESTO_DIARIO = 200
MAX_DIAS_POR_CIUDAD = 4  
AGRUPAR = True
LUGARES_MIN = 4

# Horarios predeterminados por tipo de lugar
HORARIOS_TIPO = {
    "museo": {"apertura": 10 * 60, "cierre": 19 * 60},  # 10:00 - 19:00
    "catedral": {"apertura": 9 * 60, "cierre": 20 * 60},  # 9:00 - 20:00
    "palacio": {"apertura": 10 * 60, "cierre": 18 * 60},  # 10:00 - 18:00
    "parque": {"apertura": 8 * 60, "cierre": 22 * 60},  # 8:00 - 22:00
    "playa": {"apertura": 7 * 60, "cierre": 23 * 60},  # 7:00 - 23:00
    "restaurante": {"apertura": 12 * 60, "cierre": 23 * 60},  # 12:00 - 23:00
    "bar": {"apertura": 10 * 60, "cierre": 2 * 60},  # 10:00 - 02:00 (siguiente día)
    "cafetería": {"apertura": 8 * 60, "cierre": 22 * 60},  # 8:00 - 22:00
    "tienda": {"apertura": 10 * 60, "cierre": 21 * 60},  # 10:00 - 21:00
    "plaza": {"apertura": 0, "cierre": 24 * 60},  # Siempre abierto
    "mirador": {"apertura": 8 * 60, "cierre": 21 * 60},  # 8:00 - 21:00
    "turistico": {"apertura": 9 * 60, "cierre": 20 * 60}  # 9:00 - 20:00
}

# Precios estimados por tipo de lugar (euros)
PRECIOS_TIPO = {
    "museo": 15,
    "catedral": 8,
    "palacio": 12,
    "parque": 0,
    "playa": 0,
    "restaurante": 25,
    "bar": 8,
    "cafetería": 5,
    "tienda": 10,
    "plaza": 0,
    "mirador": 5,
    "turistico": 10
}