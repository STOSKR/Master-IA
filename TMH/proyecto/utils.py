import math

lugares_turisticos = [
    # Palacios y Edificios Históricos
    {"nombre": "Palacio Real de Madrid", "x": 40.4179, "y": -3.7143, "puntos": 95, "tiempo_visita": 120, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Armeria Real", "x": 40.4178, "y": -3.7146, "puntos": 80, "tiempo_visita": 60, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Teatro Real", "x": 40.4187, "y": -3.7103, "puntos": 85, "tiempo_visita": 60, "apertura": "10:30", "cierre": "13:30", "tipo": "turistico"},
    {"nombre": "Congreso de los Diputados", "x": 40.4163, "y": -3.6961, "puntos": 70, "tiempo_visita": 45, "apertura": "09:00", "cierre": "14:00", "tipo": "turistico"},
    {"nombre": "Estación de Atocha", "x": 40.4069, "y": -3.6905, "puntos": 75, "tiempo_visita": 30, "apertura": "05:00", "cierre": "01:00", "tipo": "turistico"},
    {"nombre": "Catedral de Santa María la Real de la Almudena", "x": 40.4153, "y": -3.7145, "puntos": 80, "tiempo_visita": 45, "apertura": "09:00", "cierre": "20:30", "tipo": "turistico"},
    {"nombre": "Palacio de Liria", "x": 40.4277, "y": -3.7124, "puntos": 70, "tiempo_visita": 65, "apertura": "10:15", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Palacio de la Bolsa de Madrid", "x": 40.4110, "y": -3.6930, "puntos": 50, "tiempo_visita": 30, "apertura": "09:00", "cierre": "19:00", "tipo": "turistico"},

    # Museos
    {"nombre": "Museo Nacional del Prado", "x": 40.4138, "y": -3.6921, "puntos": 100, "tiempo_visita": 150, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Museo Nacional Centro de Arte Reina Sofía", "x": 40.4087, "y": -3.6947, "puntos": 95, "tiempo_visita": 120, "apertura": "10:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Museo Nacional Thyssen-Bornemisza", "x": 40.4167, "y": -3.6945, "puntos": 90, "tiempo_visita": 120, "apertura": "10:00", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "Museo geominero", "x": 40.4358, "y": -3.6916, "puntos": 65, "tiempo_visita": 75, "apertura": "09:00", "cierre": "14:00", "tipo": "turistico"},
    {"nombre": "Museo del Robot", "x": 40.4216, "y": -3.7094, "puntos": 60, "tiempo_visita": 60, "apertura": "11:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Museo Arqueológico Nacional de España", "x": 40.4253, "y": -3.6891, "puntos": 80, "tiempo_visita": 90, "apertura": "09:30", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Museo Sorolla", "x": 40.4380, "y": -3.6921, "puntos": 70, "tiempo_visita": 60, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Museo de San Isidro. Los Orígenes de Madrid", "x": 40.4118, "y": -3.7106, "puntos": 60, "tiempo_visita": 60, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Sweet Space", "x": 40.4239, "y": -3.6929, "puntos": 50, "tiempo_visita": 60, "apertura": "11:00", "cierre": "21:00", "tipo": "turistico"},

    # Plazas y Puertas
    {"nombre": "Plaza Mayor de Madrid", "x": 40.4155, "y": -3.7074, "puntos": 95, "tiempo_visita": 30, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Puerta del Sol", "x": 40.4169, "y": -3.7038, "puntos": 95, "tiempo_visita": 20, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Plaza de Cibeles", "x": 40.4194, "y": -3.6934, "puntos": 90, "tiempo_visita": 20, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Puerta de Alcalá", "x": 40.4203, "y": -3.6885, "puntos": 85, "tiempo_visita": 15, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Plaza de España", "x": 40.4230, "y": -3.7110, "puntos": 75, "tiempo_visita": 30, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Puerta de Toledo", "x": 40.4067, "y": -3.7139, "puntos": 50, "tiempo_visita": 20, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},

    # Parques y Jardines
    {"nombre": "Jardín del parque del Moro", "x": 40.4165, "y": -3.7171, "puntos": 75, "tiempo_visita": 60, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Parque de El Retiro", "x": 40.4153, "y": -3.6846, "puntos": 100, "tiempo_visita": 90, "apertura": "06:00", "cierre": "22:00", "tipo": "turistico"},
    {"nombre": "Templo de Debod", "x": 40.4240, "y": -3.7170, "puntos": 85, "tiempo_visita": 40, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Real Jardín Botánico de Madrid", "x": 40.4118, "y": -3.6882, "puntos": 65, "tiempo_visita": 45, "apertura": "10:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Casa de Campo", "x": 40.4140, "y": -3.7457, "puntos": 70, "tiempo_visita": 120, "apertura": "06:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Parque de El Capricho", "x": 40.4450, "y": -3.6179, "puntos": 75, "tiempo_visita": 60, "apertura": "09:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Parque Cerro del Tío Pío (Parque de las Siete Tetas)", "x": 40.3886, "y": -3.6625, "puntos": 65, "tiempo_visita": 45, "apertura": "06:00", "cierre": "22:00", "tipo": "turistico"},

    # Monumentos y Miradores
    {"nombre": "Fuente del Neptuno", "x": 40.4151, "y": -3.6946, "puntos": 70, "tiempo_visita": 10, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Faro de Moncloa", "x": 40.4372708, "y": -3.7216827, "puntos": 60, "tiempo_visita": 45, "apertura": "09:30", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Azotea del Círculo de Bellas Artes", "x": 40.4188, "y": -3.6983, "puntos": 80, "tiempo_visita": 30, "apertura": "12:00", "cierre": "01:00", "tipo": "turistico"},
    {"nombre": "Mirador Madrid (Palacio de Cibeles)", "x": 40.4194, "y": -3.6920, "puntos": 70, "tiempo_visita": 30, "apertura": "10:00", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "Monumento a Alfonso XII (Parque de El Retiro)", "x": 40.4153, "y": -3.6835, "puntos": 85, "tiempo_visita": 30, "apertura": "06:00", "cierre": "22:00", "tipo": "turistico"},

    # Mercados, Tiendas y Barrios
    {"nombre": "Mercado de San Miguel", "x": 40.4154, "y": -3.7089, "puntos": 75, "tiempo_visita": 40, "apertura": "10:00", "cierre": "00:00", "tipo": "turistico"},
    {"nombre": "WOW Concept", "x": 40.4203, "y": -3.7058, "puntos": 60, "tiempo_visita": 60, "apertura": "11:30", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Gran Vía", "x": 40.4203, "y": -3.7058, "puntos": 95, "tiempo_visita": 45, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Mercado de San Antón", "x": 40.4233, "y": -3.6995, "puntos": 55, "tiempo_visita": 40, "apertura": "10:00", "cierre": "00:00", "tipo": "turistico"},
    {"nombre": "Barrio de Malasaña", "x": 40.4272, "y": -3.7063, "puntos": 80, "tiempo_visita": 120, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Barrio de La Latina", "x": 40.4110, "y": -3.7095, "puntos": 85, "tiempo_visita": 120, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "El Rastro de Madrid", "x": 40.4094, "y": -3.7073, "puntos": 70, "tiempo_visita": 90, "apertura": "09:00", "cierre": "15:00", "tipo": "turistico"},
    {"nombre": "La Tabacalera de Lavapiés", "x": 40.4071, "y": -3.6986, "puntos": 45, "tiempo_visita": 60, "apertura": "11:00", "cierre": "22:00", "tipo": "turistico"},

    # Estadios y Otros
    {"nombre": "Estadio Santiago Bernabéu", "x": 40.4531, "y": -3.6883, "puntos": 85, "tiempo_visita": 90, "apertura": "10:00", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "Plaza de Toros de Las Ventas", "x": 40.4322, "y": -3.6637, "puntos": 65, "tiempo_visita": 60, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Ciudad Universitaria de Madrid", "x": 40.4490, "y": -3.7130, "puntos": 20, "tiempo_visita": 60, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},

    # Restaurantes y Bares
    {"nombre": "Chocolateria San Gines", "x": 40.4160, "y": -3.7074, "puntos": 80, "tiempo_visita": 30, "apertura": "08:00", "cierre": "23:30", "tipo": "restaurante"},
    {"nombre": "Running sushi in Akihabara", "x": 40.4282, "y": -3.7041, "puntos": 65, "tiempo_visita": 60, "apertura": "13:00", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "Secretos de Lola", "x": 40.4146, "y": -3.7023, "puntos": 70, "tiempo_visita": 90, "apertura": "13:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "Filippo Pizza", "x": 40.4259, "y": -3.7053, "puntos": 60, "tiempo_visita": 75, "apertura": "13:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Inclán brutal bar", "x": 40.4151, "y": -3.7033, "puntos": 75, "tiempo_visita": 90, "apertura": "13:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "Le Petit Dinsum", "x": 40.4220, "y": -3.7000, "puntos": 65, "tiempo_visita": 80, "apertura": "13:30", "cierre": "23:30", "tipo": "restaurante"},
    {"nombre": "Gourmet Experience El Corte Inglés Callao", "x": 40.4200, "y": -3.7059, "puntos": 70, "tiempo_visita": 60, "apertura": "10:00", "cierre": "23:00", "tipo": "restaurante"},
]


def distancia_haversine(lugar1: dict, lugar2: dict) -> float:
    
    R = 6371.0
    lat1, lon1 = math.radians(lugar1["x"]), math.radians(lugar1["y"])
    lat2, lon2 = math.radians(lugar2["x"]), math.radians(lugar2["y"])
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c

    return distancia

"""

def redondear_a_franja_15(tiempo: float) -> int:
    return math.ceil(tiempo / 15) * 15
    
def crear_ruta_aleatoria(max_lugares: int = len(lugares_turisticos)) -> List[int]:
    num_lugares = random.randint(2, max_lugares)
    return random.sample(range(len(lugares_turisticos)), num_lugares)

def evaluar_ruta(ruta: List[int], tiempo_max: int = tiempo_maximo_dia) -> dict:
    if len(ruta) == 0:
        return {"puntos": 0, "distancia": 0, "tiempo": 0, "fitness": 0, "valida": False}
    
    puntos_total = 0
    distancia_total = 0
    tiempo_total = 0
    
    # Calcular puntos y tiempo de visita
    for i in ruta:
        lugar = lugares_turisticos[i]
        puntos_total += lugar["puntos"]
        tiempo_total += lugar["tiempo_visita"]
    
    # Calcular distancia total del recorrido
    for i in range(len(ruta) - 1):
        lugar_actual = lugares_turisticos[ruta[i]]
        lugar_siguiente = lugares_turisticos[ruta[i + 1]]
        distancia_total += distancia_entre_puntos(lugar_actual, lugar_siguiente)
    
    # Agregar tiempo de viaje (asumiendo velocidad constante)
    tiempo_viaje = distancia_total * 20  # 20 minutos por unidad de distancia
    tiempo_total += tiempo_viaje
    
    # Verificar si la ruta es válida (dentro del tiempo máximo)
    valida = tiempo_total <= tiempo_max
    
    # Calcular fitness: maximizar puntos, minimizar distancia
    if valida:
        fitness = puntos_total - (distancia_total * 10)  # Penalizar distancia
    else:
        fitness = 0  # Ruta inválida
    
    return {
        "puntos": puntos_total,
        "distancia": round(distancia_total, 2),
        "tiempo": round(tiempo_total, 2),
        "fitness": round(fitness, 2),
        "valida": valida
    }
    
    
def cruce_simple(padre1: List[int], padre2: List[int]) -> Tuple[List[int], List[int]]:
    # Tomar lugares únicos de ambos padres
    lugares_combinados = list(set(padre1 + padre2))
    
    # Crear dos hijos con longitudes aleatorias
    max_len = min(len(lugares_combinados), 4)  # máximo 4 lugares
    len_hijo1 = random.randint(2, max_len)
    len_hijo2 = random.randint(2, max_len)
    
    # Mezclar y seleccionar
    random.shuffle(lugares_combinados)
    hijo1 = lugares_combinados[:len_hijo1]
    hijo2 = lugares_combinados[:len_hijo2]
    
    return hijo1, hijo2

"""
