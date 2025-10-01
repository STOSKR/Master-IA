import json
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from utils import lugares_turisticos, distancia_haversine # Importar los datos de los lugares y la función distancia_haversine

# Crear un diccionario para buscar coordenadas por nombre
coordenadas_lugares = {lugar["nombre"]: (lugar["y"], lugar["x"]) for lugar in lugares_turisticos}

# Cargar los resultados del archivo JSON
with open("resultados_ag.json", "r") as f:
    resultados = json.load(f)

historial_fitness = resultados["historial_fitness"]
historial_promedio = resultados["historial_promedio"]
soluciones_pareto = resultados["soluciones_pareto"]

# Gráfica de evolución del fitness
plt.figure(figsize=(10, 6))
plt.plot(historial_fitness, label="Mejor Fitness", color="blue")
plt.plot(historial_promedio, label="Fitness Promedio", color="orange")
plt.title("Evolución del Fitness a lo Largo de las Generaciones")
plt.xlabel("Generaciones")
plt.ylabel("Fitness")
plt.legend()
plt.grid()
plt.savefig("evolucion_fitness.png")

# Gráfica de la frontera de Pareto
puntos = [sol["puntos"] for sol in soluciones_pareto]
distancias = [sol["distancia"] for sol in soluciones_pareto]

# --- Lógica para encontrar la frontera de Pareto ---
# Un punto es de Pareto si no hay otro punto que lo domine
# (dominar = tener más puntos Y menos o igual distancia, o los mismos puntos Y menos distancia)
frontera_pareto_puntos = []
for i in range(len(soluciones_pareto)):
    es_dominado = False
    for j in range(len(soluciones_pareto)):
        if i == j:
            continue
        # ¿El punto j domina al punto i?
        if (soluciones_pareto[j]['puntos'] >= soluciones_pareto[i]['puntos'] and 
            soluciones_pareto[j]['distancia'] < soluciones_pareto[i]['distancia']) or \
           (soluciones_pareto[j]['puntos'] > soluciones_pareto[i]['puntos'] and 
            soluciones_pareto[j]['distancia'] <= soluciones_pareto[i]['distancia']):
            es_dominado = True
            break
    if not es_dominado:
        frontera_pareto_puntos.append(soluciones_pareto[i])

# Ordenar los puntos de la frontera para dibujar la línea
frontera_pareto_puntos = sorted(frontera_pareto_puntos, key=lambda x: x['distancia'])
puntos_frontera = [sol["puntos"] for sol in frontera_pareto_puntos]
distancias_frontera = [sol["distancia"] for sol in frontera_pareto_puntos]


plt.figure(figsize=(10, 6))
# Dibujar todas las soluciones en gris como fondo
plt.scatter(distancias, puntos, alpha=0.3, color="gray", label="Otras soluciones")
# Dibujar la frontera de Pareto resaltada en rojo y conectada por una línea
plt.plot(distancias_frontera, puntos_frontera, color='red', marker='o', linestyle='-', label="Frontera de Pareto")
plt.scatter(distancias_frontera, puntos_frontera, color='red')

plt.title("Frontera de Pareto: Puntos vs Distancia")
plt.xlabel("Distancia Total (km)")
plt.ylabel("Puntos Totales")
plt.legend()
plt.grid()
plt.savefig("frontera_pareto.png")

# --- Histograma de la distribución del Fitness Final ---
fitness_final = resultados["fitness_final"]

plt.figure(figsize=(10, 6))
plt.hist(fitness_final, bins=20, color='skyblue', edgecolor='black')
plt.title('Distribución del Fitness en la Última Generación')
plt.xlabel('Fitness')
plt.ylabel('Número de Individuos')
plt.grid(axis='y', alpha=0.75)
plt.savefig("histograma_fitness.png")


# --- Visualización de la Mejor Ruta con Plotly ---
mejor_ruta_indices = resultados["mejor_ruta"]

# Crear DataFrame con todos los lugares
df_lugares = pd.DataFrame(lugares_turisticos)
# Renombrar columnas para Plotly
df_lugares = df_lugares.rename(columns={'x': 'lat', 'y': 'lon', 'nombre': 'name'})

# DataFrame con la mejor ruta
df_ruta = df_lugares.iloc[mejor_ruta_indices].copy()
df_ruta['order'] = range(1, len(df_ruta) + 1)
df_ruta['text'] = df_ruta['order'].astype(str) + '. ' + df_ruta['name']

# Añadir los puntos de la ruta con tiempos de traslado y llegada
text_values = []
hora_actual = 9 * 60  # Empezamos a las 09:00 (en minutos)

for i in range(len(df_ruta)):
    row = df_ruta.iloc[i]
    llegada_str = f"{hora_actual // 60:02d}:{hora_actual % 60:02d}"
    
    if i == 0:
        traslado_min = 0
    else:
        # Accedemos a los índices correctos de la ruta original
        idx_anterior = mejor_ruta_indices[i-1]
        idx_actual = mejor_ruta_indices[i]
        dist = distancia_haversine(lugares_turisticos[idx_anterior], lugares_turisticos[idx_actual])
        traslado_min = ((int(dist * 25) + 4) // 5) * 5 # Velocidad media 25km/h, redondeo a 5 min

    # La hora de llegada para el siguiente punto es la actual + visita + traslado
    if i > 0:
        # El traslado se calcula desde el punto anterior (i-1)
        idx_anterior = mejor_ruta_indices[i-1]
        idx_actual = mejor_ruta_indices[i]
        dist_traslado = distancia_haversine(lugares_turisticos[idx_anterior], lugares_turisticos[idx_actual])
        tiempo_traslado = ((int(dist_traslado * 25) + 4) // 5) * 5
        
        # El tiempo de visita es del punto anterior
        tiempo_visita_anterior = df_ruta.iloc[i-1]['tiempo_visita']
        
        hora_actual += tiempo_visita_anterior + tiempo_traslado
        llegada_str = f"{hora_actual // 60:02d}:{hora_actual % 60:02d}"


    text = (f"{row['order']}. {row['name']}<br>"
            f"Llegada: {llegada_str} | Visita: {row['tiempo_visita']} min | Puntos: {row['puntos']}<br>"
            f"Traslado desde anterior: {traslado_min} min")
    text_values.append(text)

df_ruta['text'] = text_values

# Crear figura de Plotly
fig = go.Figure()

# Añadir todos los lugares como puntos grises
fig.add_trace(go.Scattergeo(
    lon = df_lugares["lon"],
    lat = df_lugares["lat"],
    hoverinfo = 'text',
    text = df_lugares["name"],
    mode = "markers",
    marker = dict(size=5, color='grey', opacity=0.7),
    name = 'Todos los lugares'
))

# Añadir la ruta como una línea
fig.add_trace(go.Scattergeo(
    lon = df_ruta["lon"],
    lat = df_ruta["lat"],
    mode = "lines",
    line = dict(width = 2, color = 'blue'),
    hoverinfo = 'none', # No mostrar info al pasar por la línea
    name = 'Mejor Ruta'
))

# Añadir los puntos de la ruta con texto en el hover
fig.add_trace(go.Scattergeo(
    lon = df_ruta["lon"],
    lat = df_ruta["lat"],
    hoverinfo = 'text',
    text = df_ruta["text"],
    mode = "markers", # Cambiado de "markers+text" a "markers"
    marker = dict(size=8, color='red'),
    name = 'Puntos de la Ruta'
))

# Configurar layout del mapa
fig.update_layout(
    title_text = 'Visualización Interactiva de la Mejor Ruta Turística con Tiempos de Traslado',
    showlegend = True,
    geo = dict(
        scope = 'world',
        projection_type = 'mercator',
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
        lataxis = {'range': [df_lugares.lat.min()-0.01, df_lugares.lat.max()+0.01]},
        lonaxis = {'range': [df_lugares.lon.min()-0.01, df_lugares.lon.max()+0.01]},
    ),
    height=700,
    margin={"r":0,"t":40,"l":0,"b":0}
)

fig.write_html("mapa_ruta_interactivo.html")


print("Gráficas generadas y guardadas como 'evolucion_fitness.png', 'frontera_pareto.png', 'histograma_fitness.png' y 'mapa_ruta_interactivo.html'.")

# Mostrar las gráficas de matplotlib
plt.show()