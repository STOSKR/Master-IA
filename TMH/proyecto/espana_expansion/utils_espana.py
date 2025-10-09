"""
Dataset de lugares turísticos para toda España
Expansión del dataset de Madrid a 10 ciudades españolas
Total: ~1,293 lugares
"""

import random
from utils import lugares_turisticos as madrid_lugares
from math import radians, sin, cos, sqrt, atan2

# SEMILLA FIJA para reproducibilidad de lugares generados
SEMILLA_LUGARES = 42
random.seed(SEMILLA_LUGARES)

# Reutilizar la función de distancia
def distancia_haversine(lugar1, lugar2):
    R = 6371
    # Soporte para ambos formatos: x/y (Madrid original) y latitud/longitud (generado)
    lat1 = radians(lugar1.get("latitud", lugar1.get("x", 0)))
    lon1 = radians(lugar1.get("longitud", lugar1.get("y", 0)))
    lat2 = radians(lugar2.get("latitud", lugar2.get("x", 0)))
    lon2 = radians(lugar2.get("longitud", lugar2.get("y", 0)))
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

def generar_lugares_ciudad(ciudad, num_lugares, offset_id):
    """
    Genera lugares turísticos sintéticos para una ciudad basándose en tipos comunes
    """
    coord = COORDENADAS_CIUDADES[ciudad]
    tipos_lugar = ["museo", "restaurante", "parque", "plaza", "tienda", "bar", "palacio", "catedral", "mirador"]
    lugares = []
    
    nombres_base = {
        "museo": ["Museo de Arte", "Museo Histórico", "Museo Contemporáneo", "Centro Cultural"],
        "restaurante": ["Casa", "El Rincón de", "Taberna", "Mesón", "Gastrobar"],
        "parque": ["Parque", "Jardines", "Paseo", "Alameda"],
        "plaza": ["Plaza Mayor", "Plaza", "Plaza del", "Plazuela"],
        "tienda": ["Boutique", "Tienda", "Galería", "Centro Comercial"],
        "bar": ["Bar", "Cafetería", "Cervecería", "Bodega"],
        "palacio": ["Palacio", "Casa", "Edificio Histórico"],
        "catedral": ["Catedral", "Basílica", "Iglesia", "Ermita"],
        "mirador": ["Mirador", "Torre", "Azotea"],
    }
    
    for i in range(num_lugares):
        tipo = random.choice(tipos_lugar)
        nombre_base = random.choice(nombres_base.get(tipo, ["Lugar"]))
        
        lugar = {
            "id": offset_id + i,
            "nombre": f"{nombre_base} {ciudad} {i+1}",
            "x": coord["lat"] + random.uniform(-0.05, 0.05),
            "y": coord["lon"] + random.uniform(-0.05, 0.05),
            "puntos": random.randint(40, 100),
            "tiempo_visita": random.choice([30, 45, 60, 90, 120]),
            "apertura": "09:00",
            "cierre": random.choice(["20:00", "21:00", "22:00", "23:00"]),
            "tipo": tipo,
            "ciudad": ciudad
        }
        lugares.append(lugar)
    
    return lugares

def crear_dataset_espana():
    lugares_totales = []
    offset = 0
    
    for lugar in madrid_lugares:
        lugar_copia = lugar.copy()
        lugar_copia["ciudad"] = "Madrid"
        lugar_copia["id"] = offset
        lugares_totales.append(lugar_copia)
        offset += 1
    
    print(f"✅ Madrid: {len(madrid_lugares)} lugares (reales)")
    
    distribucion = {
        "Barcelona": 200,
        "Sevilla": 150,
        "Valencia": 150,
        "Granada": 100,
        "Bilbao": 100,
        "Toledo": 100,
        "Córdoba": 80,
        "San Sebastián": 80,
        "Santiago": 80,
    }
    
    for ciudad, num_lugares in distribucion.items():
        lugares_ciudad = generar_lugares_ciudad(ciudad, num_lugares, offset)
        lugares_totales.extend(lugares_ciudad)
        offset += num_lugares
        print(f"✅ {ciudad}: {num_lugares} lugares")
    
    print(f"\n🎯 TOTAL: {len(lugares_totales)} lugares en España")
    return lugares_totales

lugares_turisticos_espana = crear_dataset_espana()

# Diccionario para búsqueda rápida por ID
lugares_por_id = {lugar["id"]: lugar for lugar in lugares_turisticos_espana}

def get_lugar_por_id(lugar_id: int):
    """Obtiene un lugar por su ID (búsqueda O(1))"""
    return lugares_por_id.get(lugar_id)

def get_lugares_por_ids(ids: list):
    """Obtiene múltiples lugares por sus IDs (optimizado)"""
    return [lugares_por_id[lid] for lid in ids if lid in lugares_por_id]

def get_lugares_ciudad(ciudad):
    """Retorna solo los lugares de una ciudad específica"""
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
    print("📊 DATASET DE ESPAÑA - RESUMEN")
    print("="*70)
    
    por_ciudad = {}
    for lugar in lugares_turisticos_espana:
        ciudad = lugar["ciudad"]
        por_ciudad[ciudad] = por_ciudad.get(ciudad, 0) + 1
    
    for ciudad, count in sorted(por_ciudad.items()):
        print(f"  {ciudad:20s}: {count:4d} lugares")
    
    print(f"\n  {'TOTAL':20s}: {len(lugares_turisticos_espana):4d} lugares")
    print("="*70)
    
    # Ejemplo de transporte
    print("\n🚄 EJEMPLO DE TRANSPORTE INTERCITY:")
    print("="*70)
    tiempo, costo = calcular_transporte_intercity("Madrid", "Barcelona", "tren")
    print(f"Madrid → Barcelona (Tren): {tiempo} min, {costo}€")
    
    tiempo, costo = calcular_transporte_intercity("Madrid", "Barcelona", "avion")
    print(f"Madrid → Barcelona (Avión): {tiempo} min, {costo}€")
    
    tiempo, costo = calcular_transporte_intercity("Sevilla", "Granada", "bus")
    print(f"Sevilla → Granada (Bus): {tiempo} min, {costo}€")
    print("="*70)
