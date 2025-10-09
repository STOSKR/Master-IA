import random
from math import radians, sin, cos, sqrt, atan2

# SEMILLA FIJA para reproducibilidad de lugares generados
SEMILLA_LUGARES = 777
random.seed(SEMILLA_LUGARES)

# Función de distancia Haversine
def distancia_haversine(lugar1, lugar2):
    R = 6371
    lat1, lon1 = radians(lugar1["x"]), radians(lugar1["y"])
    lat2, lon2 = radians(lugar2["x"]), radians(lugar2["y"])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

# Coordenadas centrales de cada ciudad
COORDENADAS_CIUDADES = {
    "Madrid": {"lat": 40.4168, "lon": -3.7038},
    "Barcelona": {"lat": 41.3851, "lon": 2.1734},
    "Sevilla": {"lat": 37.3891, "lon": -5.9845},
    "Valencia": {"lat": 39.4699, "lon": -0.3763},
    "Granada": {"lat": 37.1773, "lon": -3.5986},
    "Bilbao": {"lat": 43.2630, "lon": -2.9350},
    "Toledo": {"lat": 39.8628, "lon": -4.0273},
    "Córdoba": {"lat": 37.8882, "lon": -4.7794},
    "San Sebastián": {"lat": 43.3183, "lon": -1.9812},
    "Santiago": {"lat": 42.8805, "lon": -8.5457},
}

# Transporte intercity
TRANSPORTE_INTERCITY = {
    ("Madrid", "Barcelona"): {"avion": 65, "tren": 150, "bus": 360, "coste_avion": 80, "coste_tren": 50, "coste_bus": 25},
    ("Madrid", "Sevilla"): {"avion": 60, "tren": 165, "bus": 300, "coste_avion": 70, "coste_tren": 45, "coste_bus": 20},
    ("Madrid", "Valencia"): {"avion": 55, "tren": 100, "bus": 240, "coste_avion": 65, "coste_tren": 35, "coste_bus": 18},
    ("Madrid", "Bilbao"): {"avion": 60, "tren": 270, "bus": 300, "coste_avion": 75, "coste_tren": 40, "coste_bus": 22},
    ("Madrid", "Granada"): {"avion": 65, "tren": 270, "bus": 300, "coste_avion": 70, "coste_tren": 45, "coste_bus": 20},
    ("Madrid", "Toledo"): {"tren": 33, "bus": 60, "coste_tren": 15, "coste_bus": 8},
    ("Madrid", "Córdoba"): {"avion": 55, "tren": 105, "bus": 240, "coste_avion": 65, "coste_tren": 35, "coste_bus": 18},
    ("Madrid", "San Sebastián"): {"avion": 65, "tren": 315, "bus": 330, "coste_avion": 80, "coste_tren": 45, "coste_bus": 25},
    ("Madrid", "Santiago"): {"avion": 65, "tren": 330, "bus": 390, "coste_avion": 85, "coste_tren": 50, "coste_bus": 28},
    ("Barcelona", "Valencia"): {"avion": 45, "tren": 180, "bus": 210, "coste_avion": 60, "coste_tren": 30, "coste_bus": 15},
    ("Barcelona", "Sevilla"): {"avion": 80, "tren": 330, "bus": 600, "coste_avion": 90, "coste_tren": 60, "coste_bus": 35},
    ("Barcelona", "Bilbao"): {"avion": 60, "tren": 390, "bus": 360, "coste_avion": 75, "coste_tren": 45, "coste_bus": 25},
    ("Sevilla", "Granada"): {"tren": 165, "bus": 180, "coste_tren": 30, "coste_bus": 18},
    ("Sevilla", "Córdoba"): {"tren": 45, "bus": 120, "coste_tren": 20, "coste_bus": 12},
    ("Granada", "Córdoba"): {"bus": 150, "coste_bus": 15},
    ("Bilbao", "San Sebastián"): {"tren": 150, "bus": 90, "coste_tren": 18, "coste_bus": 10},
}

TRANSPORTE_COMPLETO = {}
for (origen, destino), info in TRANSPORTE_INTERCITY.items():
    TRANSPORTE_COMPLETO[(origen, destino)] = info
    TRANSPORTE_COMPLETO[(destino, origen)] = info

# ============================================================================
# MADRID - 253 LUGARES REALES (del utils.py original)
# ============================================================================
from utils import lugares_turisticos as madrid_lugares_originales

lugares_madrid = []
for idx, lugar in enumerate(madrid_lugares_originales):
    lugar_copia = lugar.copy()
    lugar_copia["id"] = idx
    lugar_copia["ciudad"] = "Madrid"
    lugares_madrid.append(lugar_copia)

# ============================================================================
# BARCELONA - 60 REALES + 140 GENERADOS = 200
# ============================================================================
lugares_barcelona_reales = [
    # Top 60 lugares REALES de Barcelona
    {"nombre": "Sagrada Familia", "x": 41.4036, "y": 2.1744, "puntos": 100, "tiempo_visita": 120, "tipo": "catedral"},
    {"nombre": "Park Güell", "x": 41.4145, "y": 2.1527, "puntos": 95, "tiempo_visita": 90, "tipo": "parque"},
    {"nombre": "Casa Batlló", "x": 41.3916, "y": 2.1649, "puntos": 90, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "La Pedrera (Casa Milà)", "x": 41.3954, "y": 2.1619, "puntos": 90, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "Barrio Gótico", "x": 41.3825, "y": 2.1769, "puntos": 95, "tiempo_visita": 120, "tipo": "turistico"},
    {"nombre": "La Rambla", "x": 41.3811, "y": 2.1739, "puntos": 90, "tiempo_visita": 60, "tipo": "turistico"},
    {"nombre": "Catedral de Barcelona", "x": 41.3840, "y": 2.1760, "puntos": 90, "tiempo_visita": 60, "tipo": "catedral"},
    {"nombre": "Mercado de La Boquería", "x": 41.3816, "y": 2.1717, "puntos": 85, "tiempo_visita": 60, "tipo": "tienda"},
    {"nombre": "Museo Picasso", "x": 41.3851, "y": 2.1805, "puntos": 90, "tiempo_visita": 90, "tipo": "museo"},
    {"nombre": "Palau de la Música Catalana", "x": 41.3875, "y": 2.1752, "puntos": 85, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "Camp Nou", "x": 41.3809, "y": 2.1228, "puntos": 85, "tiempo_visita": 120, "tipo": "museo"},
    {"nombre": "Montjuïc", "x": 41.3640, "y": 2.1656, "puntos": 90, "tiempo_visita": 180, "tipo": "parque"},
    {"nombre": "Museo Nacional de Arte de Cataluña", "x": 41.3681, "y": 2.1535, "puntos": 90, "tiempo_visita": 120, "tipo": "museo"},
    {"nombre": "Basílica Santa María del Mar", "x": 41.3832, "y": 2.1818, "puntos": 85, "tiempo_visita": 45, "tipo": "catedral"},
    {"nombre": "Parc de la Ciutadella", "x": 41.3874, "y": 2.1864, "puntos": 85, "tiempo_visita": 120, "tipo": "parque"},
    {"nombre": "Barceloneta (Playa)", "x": 41.3755, "y": 2.1904, "puntos": 85, "tiempo_visita": 120, "tipo": "playa"},
    {"nombre": "Port Vell", "x": 41.3752, "y": 2.1835, "puntos": 80, "tiempo_visita": 60, "tipo": "turistico"},
    {"nombre": "Hospital de Sant Pau", "x": 41.4136, "y": 2.1747, "puntos": 80, "tiempo_visita": 60, "tipo": "turistico"},
    {"nombre": "Fundación Joan Miró", "x": 41.3688, "y": 2.1599, "puntos": 85, "tiempo_visita": 90, "tipo": "museo"},
    {"nombre": "Tibidabo", "x": 41.4231, "y": 2.1185, "puntos": 80, "tiempo_visita": 180, "tipo": "parque"},
    {"nombre": "CosmoCaixa", "x": 41.4129, "y": 2.1304, "puntos": 80, "tiempo_visita": 120, "tipo": "museo"},
    {"nombre": "Casa Vicens", "x": 41.4034, "y": 2.1506, "puntos": 75, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Palau Güell", "x": 41.3791, "y": 2.1743, "puntos": 80, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "Castillo de Montjuïc", "x": 41.3638, "y": 2.1658, "puntos": 80, "tiempo_visita": 90, "tipo": "palacio"},
    {"nombre": "MACBA (Arte Contemporáneo)", "x": 41.3830, "y": 2.1673, "puntos": 75, "tiempo_visita": 90, "tipo": "museo"},
    {"nombre": "Aquàrium Barcelona", "x": 41.3760, "y": 2.1844, "puntos": 75, "tiempo_visita": 120, "tipo": "museo"},
    {"nombre": "Plaça Reial", "x": 41.3801, "y": 2.1749, "puntos": 75, "tiempo_visita": 30, "tipo": "plaza"},
    {"nombre": "Pueblo Español", "x": 41.3685, "y": 2.1491, "puntos": 70, "tiempo_visita": 90, "tipo": "turistico"},
    {"nombre": "Museo Marítimo", "x": 41.3761, "y": 2.1755, "puntos": 70, "tiempo_visita": 90, "tipo": "museo"},
    {"nombre": "Gran Teatre del Liceu", "x": 41.3797, "y": 2.1735, "puntos": 75, "tiempo_visita": 60, "tipo": "turistico"},
    {"nombre": "Fundación Antoni Tàpies", "x": 41.3918, "y": 2.1627, "puntos": 70, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "Passeig de Gràcia", "x": 41.3935, "y": 2.1649, "puntos": 85, "tiempo_visita": 90, "tipo": "turistico"},
    {"nombre": "Port Olímpic", "x": 41.3869, "y": 2.1963, "puntos": 70, "tiempo_visita": 60, "tipo": "turistico"},
    {"nombre": "Torre Bellesguard", "x": 41.4174, "y": 2.1213, "puntos": 70, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Jardines del Laberinto de Horta", "x": 41.4378, "y": 2.1480, "puntos": 75, "tiempo_visita": 90, "tipo": "parque"},
    {"nombre": "Casa Amatller", "x": 41.3917, "y": 2.1651, "puntos": 70, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Palau Reial Major", "x": 41.3838, "y": 2.1768, "puntos": 70, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Museo Historia Barcelona", "x": 41.3842, "y": 2.1770, "puntos": 75, "tiempo_visita": 90, "tipo": "museo"},
    {"nombre": "Casa Lleó Morera", "x": 41.3911, "y": 2.1656, "puntos": 65, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Anillo Olímpico", "x": 41.3661, "y": 2.1538, "puntos": 65, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Jardines de Montjuïc", "x": 41.3665, "y": 2.1611, "puntos": 75, "tiempo_visita": 60, "tipo": "parque"},
    {"nombre": "Parc de Collserola", "x": 41.4217, "y": 2.1047, "puntos": 70, "tiempo_visita": 120, "tipo": "parque"},
    {"nombre": "Iglesia de Santa María del Pi", "x": 41.3823, "y": 2.1738, "puntos": 65, "tiempo_visita": 30, "tipo": "catedral"},
    {"nombre": "Palau de la Virreina", "x": 41.3819, "y": 2.1723, "puntos": 65, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Mercado de Santa Caterina", "x": 41.3851, "y": 2.1784, "puntos": 70, "tiempo_visita": 60, "tipo": "tienda"},
    {"nombre": "Basílica de la Mercè", "x": 41.3799, "y": 2.1810, "puntos": 70, "tiempo_visita": 30, "tipo": "catedral"},
    {"nombre": "Monumento a Colón", "x": 41.3758, "y": 2.1775, "puntos": 65, "tiempo_visita": 20, "tipo": "turistico"},
    {"nombre": "Arco de Triunfo Barcelona", "x": 41.3912, "y": 2.1806, "puntos": 65, "tiempo_visita": 20, "tipo": "turistico"},
    {"nombre": "Recinto Modernista Sant Pau", "x": 41.4138, "y": 2.1751, "puntos": 75, "tiempo_visita": 75, "tipo": "turistico"},
    {"nombre": "Bunkers del Carmel", "x": 41.4166, "y": 2.1621, "puntos": 80, "tiempo_visita": 60, "tipo": "mirador"},
    {"nombre": "Plaça de Catalunya", "x": 41.3874, "y": 2.1700, "puntos": 75, "tiempo_visita": 30, "tipo": "plaza"},
    {"nombre": "Barrio del Born", "x": 41.3849, "y": 2.1829, "puntos": 80, "tiempo_visita": 90, "tipo": "turistico"},
    {"nombre": "El Raval", "x": 41.3815, "y": 2.1690, "puntos": 70, "tiempo_visita": 90, "tipo": "turistico"},
    {"nombre": "Plaça d'Espanya", "x": 41.3750, "y": 2.1491, "puntos": 70, "tiempo_visita": 30, "tipo": "plaza"},
    {"nombre": "Torre Agbar", "x": 41.4036, "y": 2.1894, "puntos": 65, "tiempo_visita": 30, "tipo": "turistico"},
    {"nombre": "Monasterio de Pedralbes", "x": 41.3939, "y": 2.1098, "puntos": 75, "tiempo_visita": 75, "tipo": "catedral"},
    {"nombre": "Palau Sant Jordi", "x": 41.3648, "y": 2.1530, "puntos": 65, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Museo del Chocolate", "x": 41.3862, "y": 2.1826, "puntos": 60, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "Jardín Botánico Barcelona", "x": 41.3650, "y": 2.1583, "puntos": 70, "tiempo_visita": 75, "tipo": "parque"},
    {"nombre": "Plaça del Rei", "x": 41.3839, "y": 2.1765, "puntos": 70, "tiempo_visita": 30, "tipo": "plaza"},
]

# ============================================================================
# SEVILLA - 40 REALES + 110 GENERADOS = 150
# ============================================================================
lugares_sevilla_reales = [
    {"nombre": "Catedral de Sevilla y Giralda", "x": 37.3858, "y": -5.9928, "puntos": 100, "tiempo_visita": 120, "tipo": "catedral"},
    {"nombre": "Real Alcázar de Sevilla", "x": 37.3830, "y": -5.9920, "puntos": 100, "tiempo_visita": 120, "tipo": "palacio"},
    {"nombre": "Plaza de España", "x": 37.3768, "y": -5.9866, "puntos": 95, "tiempo_visita": 60, "tipo": "plaza"},
    {"nombre": "Barrio de Santa Cruz", "x": 37.3842, "y": -5.9886, "puntos": 90, "tiempo_visita": 120, "tipo": "turistico"},
    {"nombre": "Torre del Oro", "x": 37.3823, "y": -5.9962, "puntos": 80, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Parque de María Luisa", "x": 37.3773, "y": -5.9871, "puntos": 85, "tiempo_visita": 90, "tipo": "parque"},
    {"nombre": "Metropol Parasol (Setas)", "x": 37.3929, "y": -5.9918, "puntos": 80, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Archivo de Indias", "x": 37.3849, "y": -5.9933, "puntos": 75, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "Hospital de los Venerables", "x": 37.3837, "y": -5.9900, "puntos": 75, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "Basílica de la Macarena", "x": 37.3987, "y": -5.9905, "puntos": 80, "tiempo_visita": 45, "tipo": "catedral"},
    {"nombre": "Palacio de las Dueñas", "x": 37.3948, "y": -5.9894, "puntos": 75, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "Casa de Pilatos", "x": 37.3895, "y": -5.9857, "puntos": 80, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "Museo de Bellas Artes", "x": 37.3922, "y": -5.9966, "puntos": 80, "tiempo_visita": 90, "tipo": "museo"},
    {"nombre": "Isla de la Cartuja", "x": 37.4059, "y": -6.0047, "puntos": 70, "tiempo_visita": 120, "tipo": "parque"},
    {"nombre": "Puente de Triana", "x": 37.3880, "y": -6.0020, "puntos": 70, "tiempo_visita": 30, "tipo": "turistico"},
    {"nombre": "Triana (Barrio)", "x": 37.3872, "y": -6.0050, "puntos": 85, "tiempo_visita": 90, "tipo": "turistico"},
    {"nombre": "Palacio de San Telmo", "x": 37.3809, "y": -5.9917, "puntos": 70, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Ayuntamiento de Sevilla", "x": 37.3893, "y": -5.9932, "puntos": 65, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Iglesia del Salvador", "x": 37.3903, "y": -5.9907, "puntos": 70, "tiempo_visita": 30, "tipo": "catedral"},
    {"nombre": "Palacio de Lebrija", "x": 37.3907, "y": -5.9918, "puntos": 70, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "Monasterio de la Cartuja", "x": 37.4063, "y": -6.0052, "puntos": 75, "tiempo_visita": 75, "tipo": "catedral"},
    {"nombre": "Plaza de Toros Maestranza", "x": 37.3861, "y": -5.9983, "puntos": 75, "tiempo_visita": 60, "tipo": "turistico"},
    {"nombre": "Cámara Oscura (Torre Venerables)", "x": 37.3835, "y": -5.9898, "puntos": 65, "tiempo_visita": 45, "tipo": "museo"},
    {"nombre": "Palacio de la Condesa de Lebrija", "x": 37.3908, "y": -5.9919, "puntos": 70, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "Acuario de Sevilla", "x": 37.4050, "y": -6.0040, "puntos": 65, "tiempo_visita": 90, "tipo": "museo"},
    {"nombre": "Museo del Baile Flamenco", "x": 37.3885, "y": -5.9916, "puntos": 70, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "Teatro de la Maestranza", "x": 37.3858, "y": -5.9975, "puntos": 65, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Alameda de Hércules", "x": 37.3980, "y": -5.9953, "puntos": 65, "tiempo_visita": 45, "tipo": "plaza"},
    {"nombre": "Calle Betis", "x": 37.3867, "y": -6.0063, "puntos": 70, "tiempo_visita": 60, "tipo": "turistico"},
    {"nombre": "Murallas de Sevilla", "x": 37.3957, "y": -5.9894, "puntos": 65, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Palacio Arzobispal", "x": 37.3862, "y": -5.9920, "puntos": 65, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Pabellón de la Navegación", "x": 37.4052, "y": -6.0048, "puntos": 65, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "Antiquarium", "x": 37.3930, "y": -5.9919, "puntos": 70, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "Jardines del Alcázar", "x": 37.3833, "y": -5.9905, "puntos": 80, "tiempo_visita": 75, "tipo": "parque"},
    {"nombre": "Capilla de San José", "x": 37.3891, "y": -5.9910, "puntos": 60, "tiempo_visita": 30, "tipo": "catedral"},
    {"nombre": "Plaza del Triunfo", "x": 37.3847, "y": -5.9928, "puntos": 70, "tiempo_visita": 20, "tipo": "plaza"},
    {"nombre": "Hospital de la Caridad", "x": 37.3846, "y": -5.9967, "puntos": 65, "tiempo_visita": 45, "tipo": "museo"},
    {"nombre": "Castillo de San Jorge", "x": 37.3885, "y": -6.0030, "puntos": 60, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Centro Cerámico Triana", "x": 37.3876, "y": -6.0042, "puntos": 60, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "Torre de Don Fadrique", "x": 37.3943, "y": -5.9852, "puntos": 60, "tiempo_visita": 30, "tipo": "turistico"},
]

# ============================================================================
# OTRAS CIUDADES - LUGARES REALES PRINCIPALES
# ============================================================================

# VALENCIA - 40 reales + 110 generados = 150
lugares_valencia_reales = [
    {"nombre": "Ciudad de las Artes y las Ciencias", "x": 39.4568, "y": -0.3514, "puntos": 100, "tiempo_visita": 180, "tipo": "museo"},
    {"nombre": "Oceanográfico Valencia", "x": 39.4518, "y": -0.3487, "puntos": 95, "tiempo_visita": 180, "tipo": "museo"},
    {"nombre": "Catedral de Valencia", "x": 39.4756, "y": -0.3750, "puntos": 90, "tiempo_visita": 60, "tipo": "catedral"},
    {"nombre": "Lonja de la Seda", "x": 39.4750, "y": -0.3792, "puntos": 90, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "Mercado Central", "x": 39.4740, "y": -0.3795, "puntos": 85, "tiempo_visita": 60, "tipo": "tienda"},
    {"nombre": "Bioparc Valencia", "x": 39.4800, "y": -0.4103, "puntos": 85, "tiempo_visita": 180, "tipo": "parque"},
    {"nombre": "Jardín del Turia", "x": 39.4748, "y": -0.3595, "puntos": 85, "tiempo_visita": 120, "tipo": "parque"},
    {"nombre": "Playa de la Malvarrosa", "x": 39.4806, "y": -0.3234, "puntos": 80, "tiempo_visita": 180, "tipo": "playa"},
    {"nombre": "Torres de Serranos", "x": 39.4804, "y": -0.3752, "puntos": 75, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Plaza de la Virgen", "x": 39.4755, "y": -0.3747, "puntos": 80, "tiempo_visita": 30, "tipo": "plaza"},
    {"nombre": "IVAM (Museo Arte Moderno)", "x": 39.4782, "y": -0.3786, "puntos": 75, "tiempo_visita": 90, "tipo": "museo"},
    {"nombre": "Museo de Bellas Artes Valencia", "x": 39.4795, "y": -0.3727, "puntos": 80, "tiempo_visita": 90, "tipo": "museo"},
    {"nombre": "Palacio del Marqués de Dos Aguas", "x": 39.4750, "y": -0.3763, "puntos": 75, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "Albufera de Valencia", "x": 39.3328, "y": -0.3445, "puntos": 85, "tiempo_visita": 180, "tipo": "parque"},
    {"nombre": "Estación del Norte", "x": 39.4665, "y": -0.3775, "puntos": 70, "tiempo_visita": 30, "tipo": "turistico"},
    {"nombre": "Plaza del Ayuntamiento", "x": 39.4697, "y": -0.3773, "puntos": 75, "tiempo_visita": 30, "tipo": "plaza"},
    {"nombre": "Torres de Quart", "x": 39.4775, "y": -0.3825, "puntos": 70, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Barrio del Carmen", "x": 39.4784, "y": -0.3778, "puntos": 80, "tiempo_visita": 90, "tipo": "turistico"},
    {"nombre": "Museo Fallero", "x": 39.4632, "y": -0.3592, "puntos": 70, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "Palau de la Música", "x": 39.4756, "y": -0.3550, "puntos": 70, "tiempo_visita": 60, "tipo": "turistico"},
    {"nombre": "Iglesia de San Nicolás", "x": 39.4761, "y": -0.3770, "puntos": 75, "tiempo_visita": 45, "tipo": "catedral"},
    {"nombre": "Jardines de Monforte", "x": 39.4674, "y": -0.3577, "puntos": 65, "tiempo_visita": 60, "tipo": "parque"},
    {"nombre": "Museo de Ciencias Naturales", "x": 39.4686, "y": -0.3669, "puntos": 65, "tiempo_visita": 75, "tipo": "museo"},
    {"nombre": "Plaza de Toros Valencia", "x": 39.4676, "y": -0.3735, "puntos": 70, "tiempo_visita": 60, "tipo": "turistico"},
    {"nombre": "Puerto de Valencia", "x": 39.4538, "y": -0.3155, "puntos": 70, "tiempo_visita": 90, "tipo": "turistico"},
    {"nombre": "Hemisfèric", "x": 39.4553, "y": -0.3523, "puntos": 80, "tiempo_visita": 90, "tipo": "museo"},
    {"nombre": "Palau de les Arts", "x": 39.4580, "y": -0.3541, "puntos": 75, "tiempo_visita": 60, "tipo": "turistico"},
    {"nombre": "Jardines del Real (Viveros)", "x": 39.4817, "y": -0.3666, "puntos": 70, "tiempo_visita": 90, "tipo": "parque"},
    {"nombre": "Colegio del Patriarca", "x": 39.4747, "y": -0.3759, "puntos": 65, "tiempo_visita": 45, "tipo": "catedral"},
    {"nombre": "Puente de las Flores", "x": 39.4757, "y": -0.3638, "puntos": 65, "tiempo_visita": 20, "tipo": "turistico"},
    {"nombre": "Mercado de Colón", "x": 39.4734, "y": -0.3704, "puntos": 70, "tiempo_visita": 45, "tipo": "tienda"},
    {"nombre": "Iglesia de Santa Catalina", "x": 39.4762, "y": -0.3759, "puntos": 65, "tiempo_visita": 30, "tipo": "catedral"},
    {"nombre": "Museo de la Historia de Valencia", "x": 39.4591, "y": -0.3297, "puntos": 65, "tiempo_visita": 75, "tipo": "museo"},
    {"nombre": "Lonja del Pescado", "x": 39.4724, "y": -0.3748, "puntos": 60, "tiempo_visita": 30, "tipo": "turistico"},
    {"nombre": "Palacio de Benicarló", "x": 39.4757, "y": -0.3732, "puntos": 60, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Instituto Valenciano Arte Moderno", "x": 39.4782, "y": -0.3787, "puntos": 70, "tiempo_visita": 75, "tipo": "museo"},
    {"nombre": "Museo de la Seda", "x": 39.4748, "y": -0.3774, "puntos": 60, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "La Marina de Valencia", "x": 39.4588, "y": -0.3205, "puntos": 65, "tiempo_visita": 90, "tipo": "turistico"},
    {"nombre": "Basílica de la Virgen", "x": 39.4754, "y": -0.3745, "puntos": 70, "tiempo_visita": 30, "tipo": "catedral"},
    {"nombre": "Palacio de Justicia", "x": 39.4678, "y": -0.3750, "puntos": 60, "tiempo_visita": 30, "tipo": "palacio"},
]

# GRANADA - 30 reales + 70 generados = 100
lugares_granada_reales = [
    {"nombre": "La Alhambra", "x": 37.1760, "y": -3.5881, "puntos": 100, "tiempo_visita": 180, "tipo": "palacio"},
    {"nombre": "Generalife", "x": 37.1778, "y": -3.5856, "puntos": 95, "tiempo_visita": 90, "tipo": "parque"},
    {"nombre": "Albaicín", "x": 37.1810, "y": -3.5935, "puntos": 95, "tiempo_visita": 120, "tipo": "turistico"},
    {"nombre": "Mirador de San Nicolás", "x": 37.1811, "y": -3.5932, "puntos": 90, "tiempo_visita": 45, "tipo": "mirador"},
    {"nombre": "Catedral de Granada", "x": 37.1759, "y": -3.5989, "puntos": 90, "tiempo_visita": 60, "tipo": "catedral"},
    {"nombre": "Capilla Real", "x": 37.1761, "y": -3.5988, "puntos": 90, "tiempo_visita": 60, "tipo": "catedral"},
    {"nombre": "Sacromonte (Abadía)", "x": 37.1834, "y": -3.5840, "puntos": 85, "tiempo_visita": 90, "tipo": "turistico"},
    {"nombre": "Monasterio de la Cartuja", "x": 37.1932, "y": -3.6063, "puntos": 80, "tiempo_visita": 60, "tipo": "catedral"},
    {"nombre": "Parque de las Ciencias", "x": 37.1660, "y": -3.6075, "puntos": 80, "tiempo_visita": 120, "tipo": "museo"},
    {"nombre": "Basílica San Juan de Dios", "x": 37.1774, "y": -3.6018, "puntos": 75, "tiempo_visita": 45, "tipo": "catedral"},
    {"nombre": "Palacio de Carlos V", "x": 37.1765, "y": -3.5893, "puntos": 85, "tiempo_visita": 60, "tipo": "palacio"},
    {"nombre": "Alcaicería", "x": 37.1763, "y": -3.5982, "puntos": 70, "tiempo_visita": 60, "tipo": "tienda"},
    {"nombre": "Corral del Carbón", "x": 37.1768, "y": -3.5977, "puntos": 65, "tiempo_visita": 30, "tipo": "turistico"},
    {"nombre": "Monasterio San Jerónimo", "x": 37.1810, "y": -3.6039, "puntos": 75, "tiempo_visita": 60, "tipo": "catedral"},
    {"nombre": "Carmen de los Mártires", "x": 37.1736, "y": -3.5916, "puntos": 75, "tiempo_visita": 60, "tipo": "parque"},
    {"nombre": "Palacio de Dar al-Horra", "x": 37.1819, "y": -3.5946, "puntos": 70, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Bañuelo (Baños Árabes)", "x": 37.1788, "y": -3.5918, "puntos": 70, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Casa de Zafra", "x": 37.1783, "y": -3.5927, "puntos": 65, "tiempo_visita": 45, "tipo": "museo"},
    {"nombre": "Museo Arqueológico Granada", "x": 37.1784, "y": -3.5929, "puntos": 70, "tiempo_visita": 75, "tipo": "museo"},
    {"nombre": "Plaza Nueva", "x": 37.1775, "y": -3.5964, "puntos": 75, "tiempo_visita": 30, "tipo": "plaza"},
    {"nombre": "Paseo de los Tristes", "x": 37.1771, "y": -3.5910, "puntos": 75, "tiempo_visita": 45, "tipo": "turistico"},
    {"nombre": "Torres Bermejas", "x": 37.1738, "y": -3.5943, "puntos": 65, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Casa del Chapiz", "x": 37.1823, "y": -3.5874, "puntos": 65, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Museo de la Alhambra", "x": 37.1765, "y": -3.5893, "puntos": 70, "tiempo_visita": 75, "tipo": "museo"},
    {"nombre": "Colegiata del Salvador", "x": 37.1816, "y": -3.5916, "puntos": 65, "tiempo_visita": 30, "tipo": "catedral"},
    {"nombre": "Palacio de los Córdova", "x": 37.1779, "y": -3.5960, "puntos": 60, "tiempo_visita": 45, "tipo": "palacio"},
    {"nombre": "Puerta de Elvira", "x": 37.1805, "y": -3.6013, "puntos": 60, "tiempo_visita": 20, "tipo": "turistico"},
    {"nombre": "Huerto del Carlos", "x": 37.1742, "y": -3.5881, "puntos": 65, "tiempo_visita": 45, "tipo": "parque"},
    {"nombre": "Museo Cuevas Sacromonte", "x": 37.1851, "y": -3.5813, "puntos": 70, "tiempo_visita": 60, "tipo": "museo"},
    {"nombre": "Mirador de la Lona", "x": 37.1819, "y": -3.5828, "puntos": 65, "tiempo_visita": 30, "tipo": "mirador"},
]

# Función para generar lugares complementarios
def generar_lugares_complementarios(ciudad, num_lugares, offset_id, coord):
    """Genera restaurantes, bares y tiendas con semilla fija"""
    tipos = ["restaurante", "bar", "tienda", "cafetería"]
    nombres_base = {
        "restaurante": ["Restaurante", "Tasca", "Mesón", "Taberna"],
        "bar": ["Bar", "Cervecería", "Bodega", "Tapería"],
        "tienda": ["Boutique", "Tienda", "Mercado", "Centro Comercial"],
        "cafetería": ["Café", "Cafetería", "Pastelería", "Heladería"]
    }
    
    lugares = []
    for i in range(num_lugares):
        tipo = random.choice(tipos)
        nombre = f"{random.choice(nombres_base[tipo])} {ciudad} {i+1}"
        lugares.append({
            "id": offset_id + i,
            "nombre": nombre,
            "x": coord["lat"] + random.uniform(-0.05, 0.05),
            "y": coord["lon"] + random.uniform(-0.05, 0.05),
            "puntos": random.randint(40, 70),
            "tiempo_visita": random.choice([45, 60, 90]),
            "apertura": "09:00",
            "cierre": random.choice(["21:00", "22:00", "23:00"]),
            "tipo": tipo,
            "ciudad": ciudad
        })
    return lugares

# ============================================================================
# CREAR DATASET COMPLETO
# ============================================================================
def crear_dataset_espana():
    lugares_totales = []
    offset = 0
    
    # MADRID - 253 reales
    lugares_totales.extend(lugares_madrid)
    offset += len(lugares_madrid)
    print(f"✅ Madrid: {len(lugares_madrid)} lugares (100% reales)")
    
    # BARCELONA - 60 reales + 140 generados
    for lugar in lugares_barcelona_reales:
        lugar["id"] = offset
        lugar["apertura"] = "09:00"
        lugar["cierre"] = "21:00"
        lugar["ciudad"] = "Barcelona"
        offset += 1
    lugares_totales.extend(lugares_barcelona_reales)
    complementarios = generar_lugares_complementarios("Barcelona", 140, offset, COORDENADAS_CIUDADES["Barcelona"])
    lugares_totales.extend(complementarios)
    offset += 140
    print(f"✅ Barcelona: {len(lugares_barcelona_reales)} reales + 140 generados = 200 lugares")
    
    # SEVILLA - 40 reales + 110 generados
    for lugar in lugares_sevilla_reales:
        lugar["id"] = offset
        lugar["apertura"] = "09:00"
        lugar["cierre"] = "21:00"
        lugar["ciudad"] = "Sevilla"
        offset += 1
    lugares_totales.extend(lugares_sevilla_reales)
    complementarios = generar_lugares_complementarios("Sevilla", 110, offset, COORDENADAS_CIUDADES["Sevilla"])
    lugares_totales.extend(complementarios)
    offset += 110
    print(f"✅ Sevilla: {len(lugares_sevilla_reales)} reales + 110 generados = 150 lugares")
    
    # VALENCIA - 40 reales + 110 generados
    for lugar in lugares_valencia_reales:
        lugar["id"] = offset
        lugar["apertura"] = "09:00"
        lugar["cierre"] = "21:00"
        lugar["ciudad"] = "Valencia"
        offset += 1
    lugares_totales.extend(lugares_valencia_reales)
    complementarios = generar_lugares_complementarios("Valencia", 110, offset, COORDENADAS_CIUDADES["Valencia"])
    lugares_totales.extend(complementarios)
    offset += 110
    print(f"✅ Valencia: {len(lugares_valencia_reales)} reales + 110 generados = 150 lugares")
    
    # GRANADA - 30 reales + 70 generados
    for lugar in lugares_granada_reales:
        lugar["id"] = offset
        lugar["apertura"] = "09:00"
        lugar["cierre"] = "21:00"
        lugar["ciudad"] = "Granada"
        offset += 1
    lugares_totales.extend(lugares_granada_reales)
    complementarios = generar_lugares_complementarios("Granada", 70, offset, COORDENADAS_CIUDADES["Granada"])
    lugares_totales.extend(complementarios)
    offset += 70
    print(f"✅ Granada: {len(lugares_granada_reales)} reales + 70 generados = 100 lugares")
    
    # RESTO DE CIUDADES - Solo generados por ahora (100, 100, 80, 80, 80)
    for ciudad, num_lugares in [("Bilbao", 100), ("Toledo", 100), ("Córdoba", 80), ("San Sebastián", 80), ("Santiago", 80)]:
        complementarios = generar_lugares_complementarios(ciudad, num_lugares, offset, COORDENADAS_CIUDADES[ciudad])
        lugares_totales.extend(complementarios)
        offset += num_lugares
        print(f"✅ {ciudad}: {num_lugares} lugares (generados)")
    
    print(f"\n🎯 TOTAL: {len(lugares_totales)} lugares")
    print(f"   📍 Lugares REALES: {len(lugares_madrid) + len(lugares_barcelona_reales) + len(lugares_sevilla_reales) + len(lugares_valencia_reales) + len(lugares_granada_reales)}")
    print(f"   🔄 Lugares generados: {len(lugares_totales) - (len(lugares_madrid) + len(lugares_barcelona_reales) + len(lugares_sevilla_reales) + len(lugares_valencia_reales) + len(lugares_granada_reales))}")
    
    return lugares_totales

lugares_turisticos_espana = crear_dataset_espana()

# Diccionario para búsqueda O(1)
lugares_por_id = {lugar["id"]: lugar for lugar in lugares_turisticos_espana}

def get_lugar_por_id(lugar_id: int):
    return lugares_por_id.get(lugar_id)

def get_lugares_por_ids(ids: list):
    return [lugares_por_id[lid] for lid in ids if lid in lugares_por_id]

def get_lugares_ciudad(ciudad):
    return [l for l in lugares_turisticos_espana if l["ciudad"] == ciudad]

def calcular_transporte_intercity(ciudad_origen, ciudad_destino, tipo_transporte="tren"):
    if ciudad_origen == ciudad_destino:
        return 0, 0
    
    clave = (ciudad_origen, ciudad_destino)
    if clave not in TRANSPORTE_COMPLETO:
        clave = (ciudad_destino, ciudad_origen)
    
    if clave not in TRANSPORTE_COMPLETO:
        return None, None
    
    info = TRANSPORTE_COMPLETO[clave]
    
    if tipo_transporte in info:
        tiempo = info[tipo_transporte]
        costo = info.get(f"coste_{tipo_transporte}", 0)
        return tiempo, costo
    
    if "bus" in info:
        return info["bus"], info.get("coste_bus", 0)
    elif "tren" in info:
        return info["tren"], info.get("coste_tren", 0)
    elif "avion" in info:
        return info["avion"], info.get("coste_avion", 0)
    
    return None, None

if __name__ == "__main__":
    print("\n" + "="*70)
    print("📊 DATASET HÍBRIDO DE ESPAÑA - RESUMEN")
    print("="*70)
    
    por_ciudad = {}
    reales_por_ciudad = {}
    
    for lugar in lugares_turisticos_espana:
        ciudad = lugar["ciudad"]
        por_ciudad[ciudad] = por_ciudad.get(ciudad, 0) + 1
        
        # Contar reales (los que no tienen nombre tipo "Restaurante X 1")
        if not any(x in lugar["nombre"] for x in ["Restaurante", "Bar", "Tienda", "Café", "Tasca", "Mesón"]):
            reales_por_ciudad[ciudad] = reales_por_ciudad.get(ciudad, 0) + 1
    
    for ciudad in sorted(por_ciudad.keys()):
        reales = reales_por_ciudad.get(ciudad, 0)
        total = por_ciudad[ciudad]
        print(f"  {ciudad:20s}: {total:4d} lugares ({reales} reales)")
    
    total_reales = sum(reales_por_ciudad.values())
    total_lugares = len(lugares_turisticos_espana)
    print(f"\n  {'TOTAL':20s}: {total_lugares:4d} lugares ({total_reales} reales, {total_lugares - total_reales} generados)")
    print("="*70)
    
    print("\n🚄 EJEMPLO DE TRANSPORTE INTERCITY:")
    print("="*70)
    tiempo, costo = calcular_transporte_intercity("Madrid", "Barcelona", "tren")
    print(f"Madrid → Barcelona (Tren): {tiempo} min, {costo}€")
    
    tiempo, costo = calcular_transporte_intercity("Madrid", "Barcelona", "avion")
    print(f"Madrid → Barcelona (Avión): {tiempo} min, {costo}€")
    print("="*70)
