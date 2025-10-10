import math

lugares_turisticos = [
    # Palacios y Edificios Históricos
    {"nombre": "Palacio Real de Madrid", "x": 40.4179, "y": -3.7143, "puntos": 100, "tiempo_visita": 150, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Armeria Real", "x": 40.4178, "y": -3.7146, "puntos": 75, "tiempo_visita": 60, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Teatro Real", "x": 40.4187, "y": -3.7103, "puntos": 70, "tiempo_visita": 20, "apertura": "10:30", "cierre": "13:30", "tipo": "turistico"},
    {"nombre": "Congreso de los Diputados", "x": 40.4163, "y": -3.6961, "puntos": 60, "tiempo_visita": 20, "apertura": "09:00", "cierre": "14:00", "tipo": "turistico"},
    {"nombre": "Estación de Atocha", "x": 40.4069, "y": -3.6905, "puntos": 65, "tiempo_visita": 30, "apertura": "05:00", "cierre": "01:00", "tipo": "turistico"},
    {"nombre": "Catedral de Santa María la Real de la Almudena", "x": 40.4153, "y": -3.7145, "puntos": 75, "tiempo_visita": 45, "apertura": "09:00", "cierre": "20:30", "tipo": "turistico"},
    {"nombre": "Palacio de la Bolsa de Madrid", "x": 40.4110, "y": -3.6930, "puntos": 45, "tiempo_visita": 30, "apertura": "09:00", "cierre": "19:00", "tipo": "turistico"},

    # Museos
    {"nombre": "Museo Nacional del Prado", "x": 40.4138, "y": -3.6921, "puntos": 100, "tiempo_visita": 150, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Museo Nacional Centro de Arte Reina Sofía", "x": 40.4087, "y": -3.6947, "puntos": 90, "tiempo_visita": 120, "apertura": "10:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Museo Nacional Thyssen-Bornemisza", "x": 40.4167, "y": -3.6945, "puntos": 85, "tiempo_visita": 120, "apertura": "10:00", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "Museo geominero", "x": 40.4358, "y": -3.6916, "puntos": 55, "tiempo_visita": 75, "apertura": "09:00", "cierre": "14:00", "tipo": "turistico"},
    {"nombre": "Museo del Robot", "x": 40.4216, "y": -3.7094, "puntos": 60, "tiempo_visita": 60, "apertura": "11:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Museo Arqueológico Nacional de España", "x": 40.4253, "y": -3.6891, "puntos": 80, "tiempo_visita": 90, "apertura": "09:30", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Museo Sorolla", "x": 40.4380, "y": -3.6921, "puntos": 70, "tiempo_visita": 60, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Museo de San Isidro. Los Orígenes de Madrid", "x": 40.4118, "y": -3.7106, "puntos": 50, "tiempo_visita": 60, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Sweet Space", "x": 40.4239, "y": -3.6929, "puntos": 55, "tiempo_visita": 60, "apertura": "11:00", "cierre": "21:00", "tipo": "turistico"},

    # Plazas y Puertas (lugares emblemáticos)
    {"nombre": "Plaza Mayor de Madrid", "x": 40.4155, "y": -3.7074, "puntos": 95, "tiempo_visita": 30, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Puerta del Sol", "x": 40.4169, "y": -3.7038, "puntos": 100, "tiempo_visita": 20, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Plaza de Cibeles", "x": 40.4194, "y": -3.6934, "puntos": 90, "tiempo_visita": 20, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Plaza de España", "x": 40.4230, "y": -3.7110, "puntos": 75, "tiempo_visita": 30, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},

    # Parques y Jardines
    {"nombre": "Jardín del parque del Moro", "x": 40.4165, "y": -3.7171, "puntos": 70, "tiempo_visita": 90, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Parque de El Retiro", "x": 40.4153, "y": -3.6846, "puntos": 100, "tiempo_visita": 90, "apertura": "06:00", "cierre": "22:00", "tipo": "turistico"},
    {"nombre": "Templo de Debod", "x": 40.4240, "y": -3.7170, "puntos": 85, "tiempo_visita": 20, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Real Jardín Botánico de Madrid", "x": 40.4118, "y": -3.6882, "puntos": 75, "tiempo_visita": 90, "apertura": "10:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Casa de Campo", "x": 40.4140, "y": -3.7457, "puntos": 40, "tiempo_visita": 120, "apertura": "06:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Parque Cerro del Tío Pío (Parque de las Siete Tetas)", "x": 40.3886, "y": -3.6625, "puntos": 80, "tiempo_visita": 45, "apertura": "19:45", "cierre": "20:45", "tipo": "turistico"},

    # Monumentos y Miradores
    {"nombre": "Fuente del Neptuno", "x": 40.4151, "y": -3.6946, "puntos": 65, "tiempo_visita": 10, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Faro de Moncloa", "x": 40.4372708, "y": -3.7216827, "puntos": 70, "tiempo_visita": 45, "apertura": "09:30", "cierre": "20:00", "tipo": "turistico"},

    # Mercados, Tiendas y Barrios
    {"nombre": "WOW Concept", "x": 40.4203, "y": -3.7058, "puntos": 60, "tiempo_visita": 60, "apertura": "11:30", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Gran Vía", "x": 40.4203, "y": -3.7058, "puntos": 90, "tiempo_visita": 45, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Barrio de La Latina", "x": 40.4110, "y": -3.7095, "puntos": 80, "tiempo_visita": 120, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "El Rastro de Madrid", "x": 40.4094, "y": -3.7073, "puntos": 85, "tiempo_visita": 90, "apertura": "09:00", "cierre": "15:00", "tipo": "turistico"},

    # Estadios y Otros
    {"nombre": "Estadio Santiago Bernabéu", "x": 40.4531, "y": -3.6883, "puntos": 90, "tiempo_visita": 90, "apertura": "10:00", "cierre": "19:00", "tipo": "turistico"},
    
    # Restaurantes y Bares (ESCALA AJUSTADA)
    {"nombre": "Chocolateria San Gines", "x": 40.4160, "y": -3.7074, "puntos": 85, "tiempo_visita": 30, "apertura": "08:00", "cierre": "10:00", "tipo": "restaurante"},
    {"nombre": "Running sushi in Akihabara", "x": 40.4282, "y": -3.7041, "puntos": 65, "tiempo_visita": 90, "apertura": "13:00", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "Secretos de Lola", "x": 40.4146, "y": -3.7023, "puntos": 70, "tiempo_visita": 90, "apertura": "13:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "Filippo Pizza", "x": 40.4259, "y": -3.7053, "puntos": 55, "tiempo_visita": 90, "apertura": "13:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Inclán brutal bar", "x": 40.4151, "y": -3.7033, "puntos": 75, "tiempo_visita": 90, "apertura": "13:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "Le Petit Dinsum", "x": 40.4220, "y": -3.7000, "puntos": 60, "tiempo_visita": 60, "apertura": "13:30", "cierre": "23:30", "tipo": "restaurante"},
    {"nombre": "Mercado de San Miguel", "x": 40.4154, "y": -3.7089, "puntos": 95, "tiempo_visita": 90, "apertura": "10:00", "cierre": "00:00", "tipo": "restaurante"},

    # --- MÁS RESTAURANTES (ESCALA 0-100) ---
    # Comida Tradicional Española
    {"nombre": "Casa Botín", "x": 40.4147, "y": -3.7079, "puntos": 90, "tiempo_visita": 120, "apertura": "13:00", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "La Bola Taberna", "x": 40.4208, "y": -3.7104, "puntos": 80, "tiempo_visita": 90, "apertura": "13:30", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "Casa Lucio", "x": 40.4117, "y": -3.7100, "puntos": 85, "tiempo_visita": 120, "apertura": "13:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Malacatín", "x": 40.4102, "y": -3.7084, "puntos": 75, "tiempo_visita": 90, "apertura": "13:45", "cierre": "15:45", "tipo": "restaurante"},
    {"nombre": "Sobrino de Botín", "x": 40.4147, "y": -3.7079, "puntos": 90, "tiempo_visita": 120, "apertura": "13:00", "cierre": "23:00", "tipo": "restaurante"},

    # Tapas
    {"nombre": "El Tigre Sidrería", "x": 40.4215, "y": -3.6986, "puntos": 70, "tiempo_visita": 60, "apertura": "12:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "Juana La Loca", "x": 40.4115, "y": -3.7102, "puntos": 75, "tiempo_visita": 75, "apertura": "13:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Mercado de San Antón", "x": 40.4230, "y": -3.6988, "puntos": 80, "tiempo_visita": 90, "apertura": "10:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "StreetXO", "x": 40.4236, "y": -3.6911, "puntos": 95, "tiempo_visita": 90, "apertura": "13:30", "cierre": "22:30", "tipo": "restaurante"},
    {"nombre": "Sala de Despiece", "x": 40.4322, "y": -3.7011, "puntos": 85, "tiempo_visita": 75, "apertura": "13:00", "cierre": "23:00", "tipo": "restaurante"},

    # Comida Internacional
    {"nombre": "Yakitoro", "x": 40.4211, "y": -3.6968, "puntos": 80, "tiempo_visita": 90, "apertura": "13:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Ten con Ten", "x": 40.4278, "y": -3.6868, "puntos": 85, "tiempo_visita": 120, "apertura": "12:30", "cierre": "02:00", "tipo": "restaurante"},
    {"nombre": "Amazónico", "x": 40.4275, "y": -3.6871, "puntos": 90, "tiempo_visita": 150, "apertura": "13:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "DiverXO", "x": 40.4596, "y": -3.6838, "puntos": 100, "tiempo_visita": 180, "apertura": "14:00", "cierre": "22:00", "tipo": "restaurante"},

    # Grandes Almacenes y Centros Comerciales
    {"nombre": "El Corte Inglés (Preciados)", "x": 40.4181, "y": -3.7054, "puntos": 60, "tiempo_visita": 120, "apertura": "10:00", "cierre": "22:00", "tipo": "tienda"},
    {"nombre": "Fnac Callao", "x": 40.4193, "y": -3.7068, "puntos": 45, "tiempo_visita": 60, "apertura": "10:00", "cierre": "21:30", "tipo": "tienda"},
    {"nombre": "Primark Gran Vía", "x": 40.4203, "y": -3.7058, "puntos": 40, "tiempo_visita": 90, "apertura": "10:00", "cierre": "22:00", "tipo": "tienda"},
    {"nombre": "Zara (Plaza de España)", "x": 40.4230, "y": -3.7110, "puntos": 35, "tiempo_visita": 60, "apertura": "10:00", "cierre": "22:00", "tipo": "tienda"},

    # Calles Comerciales
    {"nombre": "Calle de Preciados", "x": 40.4185, "y": -3.7055, "puntos": 55, "tiempo_visita": 90, "apertura": "00:00", "cierre": "23:59", "tipo": "calle"},
    {"nombre": "Calle de Serrano", "x": 40.4290, "y": -3.6850, "puntos": 70, "tiempo_visita": 120, "apertura": "00:00", "cierre": "23:59", "tipo": "calle"},
    {"nombre": "Calle Fuencarral", "x": 40.4250, "y": -3.7010, "puntos": 65, "tiempo_visita": 90, "apertura": "00:00", "cierre": "23:59", "tipo": "calle"},

    # Tiendas de Regalos y Souvenirs
    {"nombre": "La Melguiza (azafrán)", "x": 40.4172, "y": -3.7091, "puntos": 45, "tiempo_visita": 20, "apertura": "10:30", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Casa de Diego (abanicos)", "x": 40.4165, "y": -3.7045, "puntos": 50, "tiempo_visita": 30, "apertura": "10:00", "cierre": "20:00", "tipo": "tienda"},
    {"nombre": "Turrones Vicens", "x": 40.4158, "y": -3.7070, "puntos": 40, "tiempo_visita": 15, "apertura": "10:00", "cierre": "22:00", "tipo": "tienda"},

    # --- MÁS LUGARES DE INTERÉS ---
    # Barrios
    {"nombre": "Barrio de las Letras", "x": 40.4140, "y": -3.6980, "puntos": 75, "tiempo_visita": 90, "apertura": "00:00", "cierre": "23:59", "tipo": "barrio"},
    {"nombre": "Barrio de Malasaña", "x": 40.4255, "y": -3.7045, "puntos": 85, "tiempo_visita": 120, "apertura": "00:00", "cierre": "23:59", "tipo": "barrio"},
    {"nombre": "Barrio de Chueca", "x": 40.4225, "y": -3.6980, "puntos": 80, "tiempo_visita": 90, "apertura": "00:00", "cierre": "23:59", "tipo": "barrio"},
    {"nombre": "Barrio de Salamanca", "x": 40.4280, "y": -3.6820, "puntos": 90, "tiempo_visita": 120, "apertura": "00:00", "cierre": "23:59", "tipo": "barrio"},

    # Otros Edificios y Monumentos
    {"nombre": "Puerta de Alcalá", "x": 40.4208, "y": -3.6887, "puntos": 95, "tiempo_visita": 15, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Banco de España", "x": 40.4188, "y": -3.6945, "puntos": 60, "tiempo_visita": 20, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Círculo de Bellas Artes (Azotea)", "x": 40.4198, "y": -3.6961, "puntos": 85, "tiempo_visita": 45, "apertura": "10:00", "cierre": "01:00", "tipo": "turistico"},
    {"nombre": "Palacio de Cristal", "x": 40.4135, "y": -3.6810, "puntos": 80, "tiempo_visita": 30, "apertura": "10:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Matadero Madrid", "x": 40.3919, "y": -3.7035, "puntos": 75, "tiempo_visita": 90, "apertura": "09:00", "cierre": "22:00", "tipo": "turistico"},
    {"nombre": "Estadio Cívitas Metropolitano", "x": 40.4363, "y": -3.5992, "puntos": 85, "tiempo_visita": 90, "apertura": "11:00", "cierre": "19:00", "tipo": "turistico"},

    # Ocio y Espectáculos
    {"nombre": "Teatro Lope de Vega (El Rey León)", "x": 40.4212, "y": -3.7086, "puntos": 95, "tiempo_visita": 180, "apertura": "19:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "WiZink Center", "x": 40.4232, "y": -3.6723, "puntos": 75, "tiempo_visita": 180, "apertura": "18:00", "cierre": "00:00", "tipo": "turistico"},
    {"nombre": "Cines Callao", "x": 40.4196, "y": -3.7069, "puntos": 50, "tiempo_visita": 150, "apertura": "15:00", "cierre": "01:00", "tipo": "turistico"},
    {"nombre": "Florida Park", "x": 40.4175, "y": -3.6855, "puntos": 75, "tiempo_visita": 120, "apertura": "20:00", "cierre": "05:00", "tipo": "restaurante"},
    {"nombre": "Corral de la Morería (Tablao Flamenco)", "x": 40.4129, "y": -3.7133, "puntos": 95, "tiempo_visita": 120, "apertura": "18:00", "cierre": "00:00", "tipo": "restaurante"},

    # --- MÁS RESTAURANTES (2ª TANDA) ---
    {"nombre": "Restaurante Sacha", "x": 40.4418, "y": -3.6848, "puntos": 90, "tiempo_visita": 120, "apertura": "13:30", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "La Tasquita de Enfrente", "x": 40.4245, "y": -3.7065, "puntos": 85, "tiempo_visita": 120, "apertura": "14:00", "cierre": "22:30", "tipo": "restaurante"},
    {"nombre": "DSTAgE", "x": 40.4251, "y": -3.6965, "puntos": 100, "tiempo_visita": 180, "apertura": "13:30", "cierre": "22:00", "tipo": "restaurante"},  # 2 Estrellas Michelin
    {"nombre": "Punto MX", "x": 40.4295, "y": -3.6855, "puntos": 95, "tiempo_visita": 150, "apertura": "13:30", "cierre": "23:00", "tipo": "restaurante"},  # 1 Estrella Michelin
    {"nombre": "Lhardy", "x": 40.4160, "y": -3.7020, "puntos": 80, "tiempo_visita": 120, "apertura": "13:00", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "Casa Benigna", "x": 40.4580, "y": -3.6620, "puntos": 75, "tiempo_visita": 90, "apertura": "14:00", "cierre": "23:00", "tipo": "restaurante"},

    # --- MÁS TIENDAS (2ª TANDA) ---
    {"nombre": "Mercado de la Paz", "x": 40.4300, "y": -3.6800, "puntos": 70, "tiempo_visita": 60, "apertura": "09:00", "cierre": "20:00", "tipo": "tienda"},
    {"nombre": "Real Fábrica Española", "x": 40.4145, "y": -3.6990, "puntos": 65, "tiempo_visita": 45, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Antigua Casa Talavera (cerámica)", "x": 40.4222, "y": -3.7123, "puntos": 55, "tiempo_visita": 30, "apertura": "10:00", "cierre": "20:00", "tipo": "tienda"},
    {"nombre": "Librería San Ginés", "x": 40.4161, "y": -3.7076, "puntos": 45, "tiempo_visita": 30, "apertura": "10:00", "cierre": "20:30", "tipo": "tienda"},

    # --- MÁS OCIO Y CULTURA (2ª TANDA) ---
    {"nombre": "CaixaForum Madrid", "x": 40.4095, "y": -3.6930, "puntos": 75, "tiempo_visita": 90, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Planetario de Madrid", "x": 40.3880, "y": -3.6950, "puntos": 65, "tiempo_visita": 75, "apertura": "10:00", "cierre": "19:30", "tipo": "turistico"},
    {"nombre": "Parque de Atracciones de Madrid", "x": 40.4110, "y": -3.7500, "puntos": 85, "tiempo_visita": 240, "apertura": "12:00", "cierre": "22:00", "tipo": "turistico"},
    {"nombre": "Zoo Aquarium de Madrid", "x": 40.4080, "y": -3.7600, "puntos": 80, "tiempo_visita": 210, "apertura": "10:30", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Teleférico de Madrid", "x": 40.4260, "y": -3.7260, "puntos": 60, "tiempo_visita": 25, "apertura": "11:00", "cierre": "19:30", "tipo": "turistico"},
    {"nombre": "Andén 0 - Estación de Chamberí", "x": 40.4333, "y": -3.7000, "puntos": 60, "tiempo_visita": 45, "apertura": "10:00", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "Hipódromo de la Zarzuela", "x": 40.4750, "y": -3.7800, "puntos": 70, "tiempo_visita": 180, "apertura": "11:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Mirador del Palacio de Cibeles", "x": 40.4194, "y": -3.6934, "puntos": 75, "tiempo_visita": 30, "apertura": "10:30", "cierre": "19:30", "tipo": "turistico"},
    {"nombre": "Parque Warner Madrid", "x": 40.2333, "y": -3.5950, "puntos": 90, "tiempo_visita": 360, "apertura": "11:30", "cierre": "22:00", "tipo": "turistico"},

    # --- RESTAURANTES (Alta Cocina - 2-3 Estrellas Michelin) ---
    {"nombre": "Coque", "x": 40.4360, "y": -3.6910, "puntos": 100, "tiempo_visita": 210, "apertura": "13:30", "cierre": "22:00", "tipo": "restaurante"},  # 2 Estrellas Michelin
    {"nombre": "Ramón Freixa Madrid", "x": 40.4285, "y": -3.6825, "puntos": 100, "tiempo_visita": 180, "apertura": "14:00", "cierre": "22:30", "tipo": "restaurante"},  # 2 Estrellas Michelin
    {"nombre": "Paco Roncero Restaurante", "x": 40.4170, "y": -3.7030, "puntos": 95, "tiempo_visita": 180, "apertura": "14:00", "cierre": "23:00", "tipo": "restaurante"},  # 1 Estrella Michelin
    {"nombre": "Kabuki Wellington", "x": 40.4220, "y": -3.6800, "puntos": 95, "tiempo_visita": 150, "apertura": "13:30", "cierre": "23:00", "tipo": "restaurante"},  # 1 Estrella Michelin
    {"nombre": "Gaytán", "x": 40.4450, "y": -3.6800, "puntos": 90, "tiempo_visita": 150, "apertura": "13:45", "cierre": "22:15", "tipo": "restaurante"},  # 1 Estrella Michelin
    {"nombre": "A'Barra", "x": 40.4380, "y": -3.6890, "puntos": 90, "tiempo_visita": 150, "apertura": "13:30", "cierre": "23:30", "tipo": "restaurante"},  # 1 Estrella Michelin
    {"nombre": "CEBO", "x": 40.4148, "y": -3.6965, "puntos": 90, "tiempo_visita": 150, "apertura": "13:30", "cierre": "22:30", "tipo": "restaurante"},  # 1 Estrella Michelin
    {"nombre": "Yugo The Bunker", "x": 40.4235, "y": -3.6975, "puntos": 85, "tiempo_visita": 120, "apertura": "14:00", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "La Terraza del Casino", "x": 40.4170, "y": -3.7030, "puntos": 95, "tiempo_visita": 180, "apertura": "14:00", "cierre": "23:00", "tipo": "restaurante"},  # 2 Estrellas Michelin
    {"nombre": "El Invernadero", "x": 40.4390, "y": -3.6930, "puntos": 95, "tiempo_visita": 180, "apertura": "14:00", "cierre": "22:00", "tipo": "restaurante"},  # 1 Estrella Michelin

    # --- RESTAURANTES (Informal/Tapas) ---
    {"nombre": "Taberna El Sur", "x": 40.4110, "y": -3.6980, "puntos": 70, "tiempo_visita": 75, "apertura": "12:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "Pez Tortilla", "x": 40.4230, "y": -3.7030, "puntos": 70, "tiempo_visita": 60, "apertura": "13:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Takos Al Pastor", "x": 40.4180, "y": -3.7080, "puntos": 75, "tiempo_visita": 45, "apertura": "13:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Federal Café", "x": 40.4220, "y": -3.7090, "puntos": 65, "tiempo_visita": 90, "apertura": "09:00", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "Ojalá", "x": 40.4265, "y": -3.7040, "puntos": 75, "tiempo_visita": 90, "apertura": "10:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "La Musa Latina", "x": 40.4120, "y": -3.7110, "puntos": 80, "tiempo_visita": 90, "apertura": "13:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "El Jardín Secreto", "x": 40.4215, "y": -3.7105, "puntos": 80, "tiempo_visita": 75, "apertura": "17:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Perrachica", "x": 40.4330, "y": -3.7000, "puntos": 85, "tiempo_visita": 120, "apertura": "09:00", "cierre": "01:00", "tipo": "restaurante"},
    {"nombre": "Habanera", "x": 40.4240, "y": -3.6910, "puntos": 85, "tiempo_visita": 120, "apertura": "12:00", "cierre": "02:00", "tipo": "restaurante"},
    {"nombre": "Rosi La Loca", "x": 40.4160, "y": -3.7020, "puntos": 80, "tiempo_visita": 75, "apertura": "12:00", "cierre": "01:00", "tipo": "restaurante"},

    # --- BARES Y COCTELERÍAS ---
    {"nombre": "Salmon Guru", "x": 40.4135, "y": -3.6995, "puntos": 90, "tiempo_visita": 90, "apertura": "17:00", "cierre": "02:00", "tipo": "restaurante"},
    {"nombre": "1862 Dry Bar", "x": 40.4260, "y": -3.7035, "puntos": 85, "tiempo_visita": 75, "apertura": "19:00", "cierre": "02:30", "tipo": "restaurante"},
    {"nombre": "Del Diego Cocktail Bar", "x": 40.4210, "y": -3.6990, "puntos": 80, "tiempo_visita": 75, "apertura": "19:00", "cierre": "03:00", "tipo": "restaurante"},
    {"nombre": "Angelita Madrid", "x": 40.4205, "y": -3.7015, "puntos": 85, "tiempo_visita": 90, "apertura": "13:00", "cierre": "02:00", "tipo": "restaurante"},
    {"nombre": "The Passenger", "x": 40.4250, "y": -3.7020, "puntos": 70, "tiempo_visita": 60, "apertura": "18:00", "cierre": "03:00", "tipo": "restaurante"},
    {"nombre": "Macera TallerBar", "x": 40.4255, "y": -3.7025, "puntos": 75, "tiempo_visita": 75, "apertura": "17:00", "cierre": "02:30", "tipo": "restaurante"},
    {"nombre": "La Vía Láctea", "x": 40.4265, "y": -3.7050, "puntos": 65, "tiempo_visita": 90, "apertura": "21:00", "cierre": "03:00", "tipo": "restaurante"},
    {"nombre": "TupperWare Club", "x": 40.4258, "y": -3.7038, "puntos": 60, "tiempo_visita": 90, "apertura": "22:00", "cierre": "03:30", "tipo": "restaurante"},
    {"nombre": "Harvey's Cocktail Bar", "x": 40.4248, "y": -3.7018, "puntos": 75, "tiempo_visita": 75, "apertura": "19:00", "cierre": "02:30", "tipo": "restaurante"},
    {"nombre": "Hemingway Bar (Casa Suecia)", "x": 40.4195, "y": -3.6960, "puntos": 85, "tiempo_visita": 90, "apertura": "19:00", "cierre": "02:00", "tipo": "restaurante"},

    # --- TIENDAS (Moda y Lujo) ---
    {"nombre": "Loewe (Serrano)", "x": 40.4280, "y": -3.6855, "puntos": 75, "tiempo_visita": 60, "apertura": "10:00", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Prada (Serrano)", "x": 40.4275, "y": -3.6850, "puntos": 70, "tiempo_visita": 60, "apertura": "10:00", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Gucci (Serrano)", "x": 40.4270, "y": -3.6845, "puntos": 70, "tiempo_visita": 60, "apertura": "10:00", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Louis Vuitton (Serrano)", "x": 40.4265, "y": -3.6840, "puntos": 95, "tiempo_visita": 60, "apertura": "10:00", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Chanel (Ortega y Gasset)", "x": 40.4290, "y": -3.6830, "puntos": 90, "tiempo_visita": 60, "apertura": "10:30", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Dior (Ortega y Gasset)", "x": 40.4288, "y": -3.6828, "puntos": 85, "tiempo_visita": 60, "apertura": "10:30", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Malababa", "x": 40.4272, "y": -3.6862, "puntos": 60, "tiempo_visita": 45, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Bimba y Lola (Serrano)", "x": 40.4268, "y": -3.6858, "puntos": 70, "tiempo_visita": 45, "apertura": "10:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Adolfo Dominguez (Serrano)", "x": 40.4260, "y": -3.6865, "puntos": 65, "tiempo_visita": 45, "apertura": "10:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Purificación García (Serrano)", "x": 40.4278, "y": -3.6852, "puntos": 65, "tiempo_visita": 45, "apertura": "10:00", "cierre": "21:00", "tipo": "tienda"},

    # --- TIENDAS (Concepto y Especializadas) ---
    {"nombre": "Do Design", "x": 40.4242, "y": -3.6952, "puntos": 50, "tiempo_visita": 45, "apertura": "11:00", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Sportivo", "x": 40.4258, "y": -3.7008, "puntos": 45, "tiempo_visita": 45, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "The Concrete", "x": 40.4238, "y": -3.6988, "puntos": 40, "tiempo_visita": 30, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "La Central de Callao (Librería)", "x": 40.4190, "y": -3.7075, "puntos": 60, "tiempo_visita": 60, "apertura": "10:00", "cierre": "22:00", "tipo": "tienda"},
    {"nombre": "Despacio (Arte)", "x": 40.4125, "y": -3.7005, "puntos": 35, "tiempo_visita": 30, "apertura": "11:00", "cierre": "20:00", "tipo": "tienda"},
    {"nombre": "Petra's Garden (Plantas)", "x": 40.4130, "y": -3.6985, "puntos": 30, "tiempo_visita": 30, "apertura": "10:30", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Swinton & Grant (Librería/Galería)", "x": 40.4080, "y": -3.7000, "puntos": 40, "tiempo_visita": 45, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "El Moderno Concept Store", "x": 40.4252, "y": -3.7042, "puntos": 45, "tiempo_visita": 45, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Kinda Kinks (Discos)", "x": 40.4240, "y": -3.7060, "puntos": 35, "tiempo_visita": 30, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "La Integral (Regalos)", "x": 40.4142, "y": -3.7012, "puntos": 40, "tiempo_visita": 30, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},

    # --- CULTURA Y MUSEOS (Alternativos) ---
    {"nombre": "Museo Lázaro Galdiano", "x": 40.4365, "y": -3.6850, "puntos": 65, "tiempo_visita": 75, "apertura": "10:00", "cierre": "16:30", "tipo": "turistico"},
    {"nombre": "Museo del Romanticismo", "x": 40.4248, "y": -3.6995, "puntos": 60, "tiempo_visita": 60, "apertura": "09:30", "cierre": "18:30", "tipo": "turistico"},
    {"nombre": "Museo de América", "x": 40.4395, "y": -3.7250, "puntos": 60, "tiempo_visita": 90, "apertura": "09:30", "cierre": "15:00", "tipo": "turistico"},
    {"nombre": "Museo del Traje", "x": 40.4410, "y": -3.7280, "puntos": 55, "tiempo_visita": 75, "apertura": "09:30", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "Museo de Historia de Madrid", "x": 40.4250, "y": -3.7000, "puntos": 50, "tiempo_visita": 60, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "La Casa Encendida", "x": 40.4075, "y": -3.6955, "puntos": 70, "tiempo_visita": 60, "apertura": "10:00", "cierre": "22:00", "tipo": "turistico"},
    {"nombre": "Fundación Telefónica", "x": 40.4200, "y": -3.7010, "puntos": 65, "tiempo_visita": 60, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Fundación Mapfre (Recoletos)", "x": 40.4230, "y": -3.6890, "puntos": 60, "tiempo_visita": 75, "apertura": "11:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Real Academia de Bellas Artes de San Fernando", "x": 40.4175, "y": -3.7015, "puntos": 70, "tiempo_visita": 90, "apertura": "10:00", "cierre": "15:00", "tipo": "turistico"},
    {"nombre": "Museo Nacional de Artes Decorativas", "x": 40.4170, "y": -3.6870, "puntos": 50, "tiempo_visita": 60, "apertura": "09:30", "cierre": "15:00", "tipo": "turistico"},

    # --- GALERÍAS DE ARTE ---
    {"nombre": "Galería Marlborough", "x": 40.4300, "y": -3.6880, "puntos": 40, "tiempo_visita": 30, "apertura": "11:00", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "Galería Elvira González", "x": 40.4240, "y": -3.6960, "puntos": 40, "tiempo_visita": 30, "apertura": "10:00", "cierre": "19:30", "tipo": "turistico"},
    {"nombre": "Galería Juana de Aizpuru", "x": 40.4245, "y": -3.6955, "puntos": 40, "tiempo_visita": 30, "apertura": "10:30", "cierre": "20:30", "tipo": "turistico"},
    {"nombre": "Galería Max Estrella", "x": 40.4100, "y": -3.6950, "puntos": 35, "tiempo_visita": 30, "apertura": "10:00", "cierre": "19:30", "tipo": "turistico"},
    {"nombre": "La Fresh Gallery", "x": 40.4128, "y": -3.7018, "puntos": 30, "tiempo_visita": 20, "apertura": "16:00", "cierre": "20:00", "tipo": "turistico"},

    # --- TEATROS Y ESPECTÁCULOS ---
    {"nombre": "Teatro Español", "x": 40.4145, "y": -3.7025, "puntos": 80, "tiempo_visita": 120, "apertura": "19:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Teatro de la Zarzuela", "x": 40.4160, "y": -3.6970, "puntos": 85, "tiempo_visita": 150, "apertura": "19:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Teatros del Canal", "x": 40.4380, "y": -3.7050, "puntos": 90, "tiempo_visita": 120, "apertura": "18:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Teatro Real Cinema", "x": 40.4185, "y": -3.7100, "puntos": 70, "tiempo_visita": 120, "apertura": "17:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Nuevo Teatro Alcalá", "x": 40.4240, "y": -3.6780, "puntos": 75, "tiempo_visita": 150, "apertura": "18:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Café Central (Jazz)", "x": 40.4140, "y": -3.7030, "puntos": 80, "tiempo_visita": 120, "apertura": "20:00", "cierre": "02:00", "tipo": "restaurante"},
    {"nombre": "Cardamomo Tablao Flamenco", "x": 40.4142, "y": -3.7002, "puntos": 90, "tiempo_visita": 90, "apertura": "18:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "La Riviera (Conciertos)", "x": 40.4060, "y": -3.7180, "puntos": 70, "tiempo_visita": 180, "apertura": "20:00", "cierre": "05:00", "tipo": "turistico"},
    {"nombre": "Teatro Circo Price", "x": 40.4065, "y": -3.6975, "puntos": 85, "tiempo_visita": 150, "apertura": "19:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Naves del Español en Matadero", "x": 40.3925, "y": -3.7040, "puntos": 80, "tiempo_visita": 120, "apertura": "18:00", "cierre": "22:00", "tipo": "turistico"},

    # --- PARQUES Y ZONAS VERDES ---
    {"nombre": "Parque del Oeste", "x": 40.4280, "y": -3.7230, "puntos": 70, "tiempo_visita": 90, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Madrid Río", "x": 40.4000, "y": -3.7100, "puntos": 80, "tiempo_visita": 120, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Quinta de los Molinos", "x": 40.4370, "y": -3.6300, "puntos": 65, "tiempo_visita": 75, "apertura": "06:30", "cierre": "22:00", "tipo": "turistico"},
    {"nombre": "Parque de Juan Carlos I", "x": 40.4600, "y": -3.6100, "puntos": 75, "tiempo_visita": 120, "apertura": "07:00", "cierre": "01:00", "tipo": "turistico"},
    {"nombre": "El Capricho", "x": 40.4550, "y": -3.5900, "puntos": 70, "tiempo_visita": 90, "apertura": "09:00", "cierre": "18:30", "tipo": "turistico"},
    {"nombre": "Invernadero del Palacio de Cristal de Arganzuela", "x": 40.3950, "y": -3.7050, "puntos": 60, "tiempo_visita": 45, "apertura": "09:00", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "Rosaleda del Parque del Oeste", "x": 40.4250, "y": -3.7220, "puntos": 50, "tiempo_visita": 30, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Jardines de Sabatini", "x": 40.4200, "y": -3.7140, "puntos": 75, "tiempo_visita": 45, "apertura": "09:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Dalieda de San Francisco", "x": 40.4120, "y": -3.7145, "puntos": 40, "tiempo_visita": 20, "apertura": "10:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Parque Forestal de Valdebebas", "x": 40.4800, "y": -3.6200, "puntos": 50, "tiempo_visita": 120, "apertura": "08:00", "cierre": "21:00", "tipo": "turistico"},

    # --- RESTAURANTES (Cocina Internacional) ---
    {"nombre": "Sacha", "x": 40.4400, "y": -3.6920, "puntos": 160, "tiempo_visita": 120, "apertura": "13:30", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "StreetXO", "x": 40.4280, "y": -3.6860, "puntos": 180, "tiempo_visita": 90, "apertura": "13:30", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "Nakeima Dumpling Bar", "x": 40.4310, "y": -3.7150, "puntos": 130, "tiempo_visita": 75, "apertura": "13:30", "cierre": "22:30", "tipo": "restaurante"},
    {"nombre": "Chuka Ramen Bar", "x": 40.4130, "y": -3.6980, "puntos": 110, "tiempo_visita": 60, "apertura": "13:30", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "Don Giovanni", "x": 40.4320, "y": -3.6820, "puntos": 140, "tiempo_visita": 120, "apertura": "13:30", "cierre": "23:30", "tipo": "restaurante"},
    {"nombre": "Tandoori Station", "x": 40.4350, "y": -3.7010, "puntos": 120, "tiempo_visita": 90, "apertura": "13:00", "cierre": "23:30", "tipo": "restaurante"},
    {"nombre": "Punto MX", "x": 40.4290, "y": -3.6830, "puntos": 190, "tiempo_visita": 150, "apertura": "14:00", "cierre": "22:00", "tipo": "restaurante"},
    {"nombre": "Sudestada", "x": 40.4310, "y": -3.6890, "puntos": 150, "tiempo_visita": 120, "apertura": "13:30", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "La Tasquita de Enfrente", "x": 40.4225, "y": -3.7085, "puntos": 170, "tiempo_visita": 120, "apertura": "13:30", "cierre": "23:00", "tipo": "restaurante"},
    {"nombre": "Bacira", "x": 40.4340, "y": -3.7020, "puntos": 130, "tiempo_visita": 90, "apertura": "13:30", "cierre": "23:30", "tipo": "restaurante"},

    # --- MERCADOS GASTRONÓMICOS ---
    {"nombre": "Mercado de San Ildefonso", "x": 40.4245, "y": -3.7015, "puntos": 90, "tiempo_visita": 75, "apertura": "12:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Mercado de la Paz", "x": 40.4295, "y": -3.6820, "puntos": 70, "tiempo_visita": 60, "apertura": "09:00", "cierre": "20:00", "tipo": "tienda"},
    {"nombre": "Mercado de Maravillas", "x": 40.4450, "y": -3.7050, "puntos": 60, "tiempo_visita": 60, "apertura": "09:00", "cierre": "20:00", "tipo": "tienda"},
    {"nombre": "Platea Madrid", "x": 40.4250, "y": -3.6880, "puntos": 120, "tiempo_visita": 90, "apertura": "12:00", "cierre": "02:00", "tipo": "restaurante"},
    {"nombre": "Mercado de Antón Martín", "x": 40.4115, "y": -3.6990, "puntos": 80, "tiempo_visita": 75, "apertura": "09:00", "cierre": "22:00", "tipo": "restaurante"},

    # --- MIRADORES ---
    {"nombre": "Mirador Madrid (Palacio de Cibeles)", "x": 40.4190, "y": -3.6920, "puntos": 70, "tiempo_visita": 30, "apertura": "10:30", "cierre": "19:30", "tipo": "turistico"},
    {"nombre": "Faro de Moncloa", "x": 40.4390, "y": -3.7240, "puntos": 60, "tiempo_visita": 30, "apertura": "09:30", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "The Hat Madrid (Rooftop Bar)", "x": 40.4150, "y": -3.7090, "puntos": 50, "tiempo_visita": 60, "apertura": "17:00", "cierre": "00:00", "tipo": "restaurante"},
    {"nombre": "Gourmet Experience (El Corte Inglés Callao)", "x": 40.4195, "y": -3.7065, "puntos": 80, "tiempo_visita": 60, "apertura": "10:00", "cierre": "22:00", "tipo": "restaurante"},
    {"nombre": "Azotea del Círculo de Bellas Artes", "x": 40.4190, "y": -3.6960, "puntos": 85, "tiempo_visita": 45, "apertura": "09:00", "cierre": "02:00", "tipo": "turistico"},

    # --- ESPACIOS CULTURALES Y OCIO ALTERNATIVO ---
    {"nombre": "CaixaForum Madrid", "x": 40.4090, "y": -3.6930, "puntos": 80, "tiempo_visita": 90, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Cineteca Madrid", "x": 40.3920, "y": -3.7030, "puntos": 60, "tiempo_visita": 120, "apertura": "17:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Ikono Madrid", "x": 40.4100, "y": -3.6980, "puntos": 50, "tiempo_visita": 60, "apertura": "11:00", "cierre": "22:00", "tipo": "turistico"},
    {"nombre": "Sweet Space Museum", "x": 40.4310, "y": -3.6900, "puntos": 45, "tiempo_visita": 75, "apertura": "11:00", "cierre": "21:00", "tipo": "turistico"},
    {"nombre": "Fox in a Box (Escape Room)", "x": 40.4130, "y": -3.6950, "puntos": 40, "tiempo_visita": 75, "apertura": "10:00", "cierre": "23:00", "tipo": "turistico"},
    {"nombre": "Fundación Juan March", "x": 40.4290, "y": -3.6840, "puntos": 65, "tiempo_visita": 60, "apertura": "11:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Ateneo de Madrid", "x": 40.4150, "y": -3.6990, "puntos": 55, "tiempo_visita": 45, "apertura": "09:00", "cierre": "22:00", "tipo": "turistico"},
    {"nombre": "Casa de México", "x": 40.4320, "y": -3.7180, "puntos": 50, "tiempo_visita": 60, "apertura": "10:00", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "CentroCentro", "x": 40.4190, "y": -3.6925, "puntos": 70, "tiempo_visita": 60, "apertura": "10:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Real Fábrica de Tapices", "x": 40.4040, "y": -3.6880, "puntos": 45, "tiempo_visita": 60, "apertura": "10:00", "cierre": "14:00", "tipo": "turistico"},

    # --- TIENDAS (Gourmet y Alimentación) ---
    {"nombre": "Cristina Oria (Ortega y Gasset)", "x": 40.4292, "y": -3.6810, "puntos": 50, "tiempo_visita": 30, "apertura": "10:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Poncelet Quesos", "x": 40.4325, "y": -3.6915, "puntos": 45, "tiempo_visita": 30, "apertura": "10:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "La Chinata (Oleoteca)", "x": 40.4185, "y": -3.7095, "puntos": 35, "tiempo_visita": 20, "apertura": "10:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Joselito's (Jamón)", "x": 40.4260, "y": -3.6830, "puntos": 60, "tiempo_visita": 30, "apertura": "10:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Chocolatería San Ginés (Tienda)", "x": 40.4170, "y": -3.7070, "puntos": 70, "tiempo_visita": 20, "apertura": "00:00", "cierre": "23:59", "tipo": "tienda"},
    {"nombre": "Turrones Vicens", "x": 40.4175, "y": -3.7055, "puntos": 40, "tiempo_visita": 15, "apertura": "10:00", "cierre": "22:00", "tipo": "tienda"},
    {"nombre": "Casa Mira (Turrones)", "x": 40.4165, "y": -3.6980, "puntos": 50, "tiempo_visita": 20, "apertura": "10:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "La Violeta (Caramelos)", "x": 40.4178, "y": -3.7038, "puntos": 45, "tiempo_visita": 15, "apertura": "10:00", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Mantequerías Bravo", "x": 40.4305, "y": -3.6875, "puntos": 55, "tiempo_visita": 30, "apertura": "09:30", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "El Riojano (Pastelería)", "x": 40.4155, "y": -3.7060, "puntos": 60, "tiempo_visita": 20, "apertura": "10:00", "cierre": "20:00", "tipo": "tienda"},

    # --- TIENDAS (Otras) ---
    {"nombre": "Generación X (Comics)", "x": 40.4205, "y": -3.7080, "puntos": 30, "tiempo_visita": 30, "apertura": "10:30", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Akira Comics", "x": 40.4400, "y": -3.6650, "puntos": 40, "tiempo_visita": 45, "apertura": "10:30", "cierre": "20:30", "tipo": "tienda"},
    {"nombre": "Curiosite (Regalos Originales)", "x": 40.4250, "y": -3.7030, "puntos": 35, "tiempo_visita": 30, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Lego Store (La Vaguada)", "x": 40.4780, "y": -3.7100, "puntos": 40, "tiempo_visita": 45, "apertura": "10:00", "cierre": "22:00", "tipo": "tienda"},
    {"nombre": "Magpie (Vintage)", "x": 40.4262, "y": -3.7048, "puntos": 30, "tiempo_visita": 45, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "Williamsburg (Decoración)", "x": 40.4270, "y": -3.7010, "puntos": 35, "tiempo_visita": 30, "apertura": "11:00", "cierre": "21:00", "tipo": "tienda"},
    {"nombre": "FNAC (Callao)", "x": 40.4198, "y": -3.7060, "puntos": 50, "tiempo_visita": 60, "apertura": "10:00", "cierre": "21:30", "tipo": "tienda"},
    {"nombre": "Casa del Libro (Gran Vía)", "x": 40.4208, "y": -3.7035, "puntos": 50, "tiempo_visita": 60, "apertura": "10:00", "cierre": "21:30", "tipo": "tienda"},
    {"nombre": "Pylones (Regalos)", "x": 40.4222, "y": -3.7022, "puntos": 30, "tiempo_visita": 20, "apertura": "10:30", "cierre": "21:30", "tipo": "tienda"},
    {"nombre": "Real Madrid Official Store (Gran Vía)", "x": 40.4200, "y": -3.7050, "puntos": 60, "tiempo_visita": 30, "apertura": "10:00", "cierre": "22:00", "tipo": "tienda"},

    # --- EDIFICIOS Y MONUMENTOS EMBLEMÁTICOS ---
    {"nombre": "Edificio Metrópolis", "x": 40.4195, "y": -3.6975, "puntos": 50, "tiempo_visita": 10, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Palacio de Longoria (SGAE)", "x": 40.4240, "y": -3.6980, "puntos": 40, "tiempo_visita": 10, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Puerta de San Vicente", "x": 40.4180, "y": -3.7200, "puntos": 30, "tiempo_visita": 10, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Viaducto de Segovia", "x": 40.4135, "y": -3.7130, "puntos": 35, "tiempo_visita": 15, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Cuatro Torres Business Area", "x": 40.4750, "y": -3.6880, "puntos": 45, "tiempo_visita": 30, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Torres KIO (Puerta de Europa)", "x": 40.4650, "y": -3.6880, "puntos": 40, "tiempo_visita": 15, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Banco de España", "x": 40.4185, "y": -3.6940, "puntos": 50, "tiempo_visita": 10, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Bolsa de Madrid", "x": 40.4150, "y": -3.6920, "puntos": 40, "tiempo_visita": 10, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Congreso de los Diputados", "x": 40.4160, "y": -3.6970, "puntos": 60, "tiempo_visita": 15, "apertura": "00:00", "cierre": "23:59", "tipo": "turistico"},
    {"nombre": "Estación de Atocha (Invernadero)", "x": 40.4070, "y": -3.6920, "puntos": 65, "tiempo_visita": 30, "apertura": "05:00", "cierre": "01:00", "tipo": "turistico"},

    # --- IGLESIAS Y TEMPLOS ---
    {"nombre": "Iglesia de San Ginés", "x": 40.4170, "y": -3.7075, "puntos": 40, "tiempo_visita": 20, "apertura": "08:30", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Iglesia de San Antonio de los Alemanes", "x": 40.4225, "y": -3.7030, "puntos": 50, "tiempo_visita": 20, "apertura": "10:30", "cierre": "14:00", "tipo": "turistico"},
    {"nombre": "Monasterio de la Encarnación", "x": 40.4195, "y": -3.7115, "puntos": 55, "tiempo_visita": 45, "apertura": "10:00", "cierre": "18:30", "tipo": "turistico"},
    {"nombre": "Panteón de Hombres Ilustres", "x": 40.4050, "y": -3.6860, "puntos": 45, "tiempo_visita": 30, "apertura": "10:00", "cierre": "18:00", "tipo": "turistico"},
    {"nombre": "Iglesia de San Jerónimo el Real", "x": 40.4130, "y": -3.6890, "puntos": 60, "tiempo_visita": 30, "apertura": "10:00", "cierre": "19:30", "tipo": "turistico"},
    {"nombre": "Catedral Anglicana de San Jorge", "x": 40.4300, "y": -3.6830, "puntos": 30, "tiempo_visita": 15, "apertura": "10:00", "cierre": "14:00", "tipo": "turistico"},
    {"nombre": "Oratorio del Caballero de Gracia", "x": 40.4200, "y": -3.7005, "puntos": 35, "tiempo_visita": 15, "apertura": "09:00", "cierre": "20:00", "tipo": "turistico"},
    {"nombre": "Iglesia de San Manuel y San Benito", "x": 40.4220, "y": -3.6815, "puntos": 40, "tiempo_visita": 20, "apertura": "09:00", "cierre": "19:00", "tipo": "turistico"},
    {"nombre": "Basílica de San Miguel", "x": 40.4140, "y": -3.7100, "puntos": 45, "tiempo_visita": 20, "apertura": "10:30", "cierre": "19:30", "tipo": "turistico"},
    {"nombre": "Ermita de San Antonio de la Florida", "x": 40.4230, "y": -3.7240, "puntos": 65, "tiempo_visita": 30, "apertura": "09:30", "cierre": "20:00", "tipo": "turistico"}
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
