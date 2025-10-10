from utils_espana import lugares_turisticos_espana, get_lugares_ciudad

print(f"Total de lugares: {len(lugares_turisticos_espana)}")
print("\nLugares por ciudad:")
for ciudad in ['Madrid', 'Barcelona', 'Sevilla', 'Valencia', 'Granada', 'Bilbao', 'Toledo', 'Córdoba', 'San Sebastián', 'Santiago']:
    cantidad = len(get_lugares_ciudad(ciudad))
    print(f"  {ciudad:15s}: {cantidad:3d} lugares")
