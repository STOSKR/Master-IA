import math

lugares_turisticos = [
    # Palacios y Edificios Históricos
    {"nombre": "Palacio Real de Madrid", "x": 40.4179, "y": -3.7143, "puntos": 200, "tiempo_visita": 150, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Armeria Real", "x": 40.4178, "y": -3.7146, "puntos": 80, "tiempo_visita": 60, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Teatro Real", "x": 40.4187, "y": -3.7103, "puntos": 85, "tiempo_visita": 20, "apertura": "10:30", "cierre": "13:30", "tipo": "turistico"},
    {"nombre": "Congreso de los Diputados", "x": 40.4163, "y": -3.6961, "puntos": 80, "tiempo_visita": 20, "apertura": "09:00", "cierre": "14:00", "tipo": "turistico"},
    {"nombre": "Estación de Atocha", "x": 40.4069, "y": -3.6905, "puntos": 75, "tiempo_visita": 30, "apertura": "05:00", "cierre": "01:00", "tipo": "turistico"},
    {"nombre": "Catedral de Santa María la Real de la Almudena", "x": 40.4153, "y": -3.7145, "puntos": 50, "tiempo_visita": 45, "apertura": "09:00", "cierre": "20:30", "tipo": "turistico"},
    {"nombre": "Palacio de la Bolsa de Madrid", "x": 40.4110, "y": -3.6930, "puntos": 50, "tiempo_visita": 30, "apertura": "09:00", "cierre": "19:00", "tipo": "turistico"},

    # Museos
    {"nombre": "Museo Nacional del Prado", "x": 40.4138, "y": -3.6921, "puntos": 200, "tiempo_visita": 150, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Museo Nacional Centro de Arte Reina Sofía", "x": 40.4087, "y": -3.6947, "puntos": 70, "tiempo_visita": 120, "apertura": "10:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Museo Nacional Thyssen-Bornemisza", "x": 40.4167, "y": -3.6945, "puntos": 70, "tiempo_visita": 120, "apertura": "10:00", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "Museo geominero", "x": 40.4358, "y": -3.6916, "puntos": 70, "tiempo_visita": 75, "apertura": "09:00", "cierre": "14:00", "tipo": "turistico"},
    {"nombre": "Museo del Robot", "x": 40.4216, "y": -3.7094, "puntos": 80, "tiempo_visita": 60, "apertura": "11:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Museo Arqueológico Nacional de España", "x": 40.4253, "y": -3.6891, "puntos": 70, "tiempo_visita": 90, "apertura": "09:30", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Museo Sorolla", "x": 40.4380, "y": -3.6921, "puntos": 40, "tiempo_visita": 60, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Museo de San Isidro. Los Orígenes de Madrid", "x": 40.4118, "y": -3.7106, "puntos": 40, "tiempo_visita": 60, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Sweet Space", "x": 40.4239, "y": -3.6929, "puntos": 50, "tiempo_visita": 60, "apertura": "11:00", "cierre": "21:00", "tipo": "turistico"},

    # Plazas y Puertas
    {"nombre": "Plaza Mayor de Madrid", "x": 40.4155, "y": -3.7074, "puntos": 100, "tiempo_visita": 30, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Puerta del Sol", "x": 40.4169, "y": -3.7038, "puntos": 100, "tiempo_visita": 20, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Plaza de Cibeles", "x": 40.4194, "y": -3.6934, "puntos": 90, "tiempo_visita": 20, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Plaza de España", "x": 40.4230, "y": -3.7110, "puntos": 75, "tiempo_visita": 30, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},

    # Parques y Jardines
    {"nombre": "Jardín del parque del Moro", "x": 40.4165, "y": -3.7171, "puntos": 75, "tiempo_visita": 90, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Parque de El Retiro", "x": 40.4153, "y": -3.6846, "puntos": 100, "tiempo_visita": 90, "apertura": "06:00", "cierre": "22:00", "tipo": "turistico"},
    {"nombre": "Templo de Debod", "x": 40.4240, "y": -3.7170, "puntos": 85, "tiempo_visita": 20, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Real Jardín Botánico de Madrid", "x": 40.4118, "y": -3.6882, "puntos": 70, "tiempo_visita": 90, "apertura": "10:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Casa de Campo", "x": 40.4140, "y": -3.7457, "puntos": 30, "tiempo_visita": 120, "apertura": "06:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Parque Cerro del Tío Pío (Parque de las Siete Tetas)", "x": 40.3886, "y": -3.6625, "puntos": 70, "tiempo_visita": 45, "apertura": "19:45", "cierre": "20:45", "tipo": "turistico"},

    # Monumentos y Miradores
    {"nombre": "Fuente del Neptuno", "x": 40.4151, "y": -3.6946, "puntos": 70, "tiempo_visita": 10, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Faro de Moncloa", "x": 40.4372708, "y": -3.7216827, "puntos": 70, "tiempo_visita": 45, "apertura": "09:30", "cierre": "20:00", "tipo": "turistico"},

    # Mercados, Tiendas y Barrios
    {"nombre": "WOW Concept", "x": 40.4203, "y": -3.7058, "puntos": 80, "tiempo_visita": 60, "apertura": "11:30", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Gran Vía", "x": 40.4203, "y": -3.7058, "puntos": 90, "tiempo_visita": 45, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Barrio de La Latina", "x": 40.4110, "y": -3.7095, "puntos": 60, "tiempo_visita": 120, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "El Rastro de Madrid", "x": 40.4094, "y": -3.7073, "puntos": 60, "tiempo_visita": 90, "apertura": "09:00", "cierre": "15:00", "tipo": "turistico"},

    # Estadios y Otros
    {"nombre": "Estadio Santiago Bernabéu", "x": 40.4531, "y": -3.6883, "puntos": 90, "tiempo_visita": 90, "apertura": "10:00", "cierre": "19:00", "tipo": "turistico"},
    
    # Restaurantes y Bares
    {"nombre": "Chocolateria San Gines", "x": 40.4160, "y": -3.7074, "puntos": 90, "tiempo_visita": 30, "apertura": "08:00", "cierre": "10:00", "tipo": "restaurante"},
    {"nombre": "Running sushi in Akihabara", "x": 40.4282, "y": -3.7041, "puntos": 70, "tiempo_visita": 90, "apertura": "13:00", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "Secretos de Lola", "x": 40.4146, "y": -3.7023, "puntos": 90, "tiempo_visita": 90, "apertura": "13:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "Filippo Pizza", "x": 40.4259, "y": -3.7053, "puntos": 60, "tiempo_visita": 90, "apertura": "13:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Inclán brutal bar", "x": 40.4151, "y": -3.7033, "puntos": 85, "tiempo_visita": 90, "apertura": "13:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "Le Petit Dinsum", "x": 40.4220, "y": -3.7000, "puntos": 60, "tiempo_visita": 60, "apertura": "13:30", "cierre": "23:30", "tipo": "restaurante"},
    {"nombre": "Mercado de San Miguel", "x": 40.4154, "y": -3.7089, "puntos": 100, "tiempo_visita": 90, "apertura": "10:00", "cierre": "00:00", "tipo": "restaurante"},
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
def optimizar_parametros():
    generaciones_list = [400, 600, 800, 1000]
    tamaño_poblacion_list = [300, 500, 700, 1000, 2000, 5000]
    prob_cruce_list = [round(x, 2) for x in [i * 0.05 for i in range(2, 20)]]  # 0.1 to 0.95
    prob_mutacion_list = [round(x, 2) for x in [i * 0.05 for i in range(1, 20)]]  # 0.05 to 0.95
    iteraciones_por_combinacion = 3

    mejor_fitness_global = -1
    mejores_parametros = {}

    for generaciones in generaciones_list:
        for tamaño_poblacion in tamaño_poblacion_list:
            for prob_cruce in prob_cruce_list:
                for prob_mutacion in prob_mutacion_list:
                    fitness_promedio = 0
                    for iteracion in range(iteraciones_por_combinacion):
                        print(f"\nIteración {iteracion + 1}/{iteraciones_por_combinacion} para parámetros: Generaciones={generaciones}, Tamaño Población={tamaño_poblacion}, Prob. Cruce={prob_cruce}, Prob. Mutación={prob_mutacion}")
                        resultado = algoritmo_genetico_reemplazo_mixto(
                            generaciones, tamaño_poblacion, prob_cruce, prob_mutacion
                        )
                        fitness_promedio += resultado["evaluacion"]["fitness"]

                    fitness_promedio /= iteraciones_por_combinacion

                    if fitness_promedio > mejor_fitness_global:
                        mejor_fitness_global = fitness_promedio
                        mejores_parametros = {
                            "generaciones": generaciones,
                            "tamaño_poblacion": tamaño_poblacion,
                            "prob_cruce": prob_cruce,
                            "prob_mutacion": prob_mutacion,
                            "mejor_fitness_promedio": mejor_fitness_global
                        }

    print("\n================ RESULTADOS =================")
    print("Mejores parámetros encontrados:")
    for clave, valor in mejores_parametros.items():
        print(f"{clave}: {valor}")

    return mejores_parametros

def algoritmo_genetico_simple(generaciones: int = 100, tamaño_poblacion: int = 1000, 
                             prob_cruce: float = 0.8, prob_mutacion: float = 0.3, tiempo_disponible: int = t_dia) -> dict:
    print(f"\n🧬 ALGORITMO GENÉTICO")
    print(f"Generaciones: {generaciones}, Población: {tamaño_poblacion}")
    print(f"Prob. cruce: {prob_cruce}, Prob. mutación: {prob_mutacion}")
    print("="*50)
    
    # 1. Crear población inicial
    poblacion, fitness_scores = inicializar_poblacion_y_evaluar(tamaño_poblacion, tiempo_disponible)
    mejor_fitness_historico, mejor_ruta_historica = -1, []
    historial_fitness = []
    
    for generacion in range(generaciones):
        # 2. Evaluar población
        fitness_scores = []
        for ruta in poblacion:
            evaluacion = evaluar_ruta(ruta)
            fitness_scores.append(evaluacion["fitness"])
        
        # 3. Encontrar el mejor de esta generación
        mejor_idx = fitness_scores.index(max(fitness_scores))
        mejor_ruta_gen = poblacion[mejor_idx]
        mejor_fitness_gen = fitness_scores[mejor_idx]
        
        # 4. Actualizar el mejor histórico
        if mejor_fitness_gen > mejor_fitness_historico:
            mejor_fitness_historico = mejor_fitness_gen
            mejor_ruta_historica = mejor_ruta_gen.copy()
        
        # 5. Guardar para histórico
        historial_fitness.append(mejor_fitness_gen)
        
        # 6. Mostrar progreso cada 20 generaciones
        if generacion % 20 == 0 or generacion == generaciones - 1:
            print(f"| Gen {generacion:3d} | Mejor Fitness: {mejor_fitness_gen:8.2f} | Fitness Promedio: {sum(fitness_scores)/len(fitness_scores):8.2f} | Mejor Histórico: {mejor_fitness_historico:8.2f} |")
        
        # 7. Crear nueva población
        poblacion = evolucionar_poblacion(poblacion, fitness_scores, tamaño_poblacion, prob_cruce, prob_mutacion)

    # Resultado final
    evaluacion_final = evaluar_ruta(mejor_ruta_historica)
    imprimir_mejor_ruta(mejor_ruta_historica, evaluacion_final)
    
    return {
        "mejor_ruta": mejor_ruta_historica,
        "evaluacion": evaluacion_final,
        "historial_fitness": historial_fitness,
        "algoritmo": "Genético"
    }

def algoritmo_genetico_estado_estacionario(generaciones: int = 100, tamaño_poblacion: int = 1000, 
                                           prob_cruce: float = 0.8, prob_mutacion: float = 0.3, 
                                           tiempo_disponible: int = t_dia) -> dict:
    print(f"\n🧬 ALGORITMO GENÉTICO (ESTADO ESTACIONARIO)")
    print(f"Generaciones: {generaciones}, Población: {tamaño_poblacion}")
    print(f"Prob. cruce: {prob_cruce}, Prob. mutación: {prob_mutacion}")
    print("="*50)

    # 1. Crear población inicial
    poblacion, fitness_scores = inicializar_poblacion_y_evaluar(tamaño_poblacion, tiempo_disponible)
    mejor_fitness_historico = -1
    mejor_ruta_historica = []
    historial_fitness = []

    for generacion in range(generaciones):
        # 2. Evaluar población
        fitness_scores = [evaluar_ruta(ruta)["fitness"] for ruta in poblacion]

        # 3. Ordenar población por fitness (de mejor a peor)
        poblacion_ordenada = [ruta for _, ruta in sorted(zip(fitness_scores, poblacion), key=lambda x: x[0], reverse=True)]
        fitness_ordenado = sorted(fitness_scores, reverse=True)

        # 4. Mantener el 90% de los mejores individuos
        num_mejores = int(0.9 * tamaño_poblacion)
        nueva_poblacion = poblacion_ordenada[:num_mejores]

        # 5. Generar hijos para reemplazar el 10% de los peores
        num_hijos = tamaño_poblacion - num_mejores
        hijos = []
        while len(hijos) < num_hijos:
            padre1, padre2 = seleccion_ranking(poblacion, fitness_scores, 2)
            if random.random() < prob_cruce:
                hijo1, hijo2 = cruce_ordenado(padre1, padre2)
            else:
                hijo1, hijo2 = padre1.copy(), padre2.copy()

            hijo1 = mutacion(hijo1, prob_mutacion)
            hijo2 = mutacion(hijo2, prob_mutacion)
            hijos.extend([hijo1, hijo2])

        # 6. Evaluar hijos y reemplazar a los peores si son mejores
        hijos = hijos[:num_hijos]  # Asegurar que no haya más hijos de los necesarios
        for i, hijo in enumerate(hijos):
            evaluacion_hijo = evaluar_ruta(hijo)["fitness"]
            if evaluacion_hijo > fitness_ordenado[-(i + 1)]:  # Comparar con los peores
                nueva_poblacion.append(hijo)
            else:
                nueva_poblacion.append(poblacion_ordenada[-(i + 1)])

        # 7. Actualizar población
        poblacion = nueva_poblacion[:tamaño_poblacion]

        # 8. Actualizar el mejor histórico
        mejor_fitness_gen = max(fitness_scores)
        mejor_ruta_gen = poblacion_ordenada[0]
        if mejor_fitness_gen > mejor_fitness_historico:
            mejor_fitness_historico = mejor_fitness_gen
            mejor_ruta_historica = mejor_ruta_gen.copy()

        # 9. Guardar para histórico
        historial_fitness.append(mejor_fitness_gen)

        # 10. Mostrar progreso cada 20 generaciones
        if generacion % 20 == 0 or generacion == generaciones - 1:
            print(f"Gen {generacion:2d}: Mejor fitness = {mejor_fitness_gen:7.2f}, Promedio = {sum(fitness_scores)/len(fitness_scores):7.2f}")

    # Resultado final
    evaluacion_final = evaluar_ruta(mejor_ruta_historica)
    imprimir_mejor_ruta(mejor_ruta_historica, evaluacion_final)
    return {
        "mejor_ruta": mejor_ruta_historica,
        "evaluacion": evaluacion_final,
        "historial_fitness": historial_fitness,
        "algoritmo": "Genético Estado Estacionario"
    }


def imprimir_ruta(ruta: List[int], evaluacion: dict, tiempo_disponible: int):
    print("\n" + "="*50)
    print("RUTA:")
    for i, lugar_idx in enumerate(ruta):
        lugar = lugares_turisticos[lugar_idx]
        print(f"{i+1}. {lugar['nombre']} (Puntos: {lugar['puntos']}, Tiempo: {lugar['tiempo_visita']}min)")
    
    print(f"\nRESULTADOS:")
    print(f"Puntos totales: {evaluacion['puntos']}")
    print(f"Distancia total: {evaluacion['distancia']}")
    print(f"Tiempo total: {evaluacion['tiempo']} minutos (de {tiempo_disponible} disponibles)")
    print(f"Válida: {'Sí' if evaluacion['valida'] else 'No'}")
    print(f"Fitness: {evaluacion['fitness']}")

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
