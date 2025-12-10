(define (problem airport-baggage-problem-hard)
  (:domain airport-baggage)

  (:objects
    n0 n1 n2 - num
    p1 p2 p3 p4 p5 p6 p7 p8 inspeccion facturacion recogida - location
    e1 e2 e3 e4 e5 e6 e7 e8 e9 e10 - baggage
    v1 v2 - wagon
    m1 m2 - machine
  )
  
  (:init
    ; Adyacencias
    (adjacent facturacion recogida)
    (adjacent recogida facturacion)
    (adjacent facturacion inspeccion)
    (adjacent inspeccion facturacion)
    (adjacent recogida inspeccion)
    (adjacent inspeccion recogida)
    
    (adjacent facturacion p2)
    (adjacent p2 facturacion)
    (adjacent inspeccion p1)
    (adjacent p1 inspeccion)
    
    (adjacent p1 p3)
    (adjacent p3 p1)
    (adjacent p2 p4)
    (adjacent p4 p2)
    (adjacent p3 p4)
    (adjacent p4 p3)
    
    (adjacent inspeccion p5)
    (adjacent p5 inspeccion)
    (adjacent recogida p6)
    (adjacent p6 recogida)
    (adjacent p6 p8)
    (adjacent p8 p6)
    (adjacent p5 p7)
    (adjacent p7 p5)
    (adjacent p7 p8)
    (adjacent p8 p7)

    ; Relación de números
    (next_num n0 n1)
    (next_num n1 n2)
    
    ; Vagones en p2 (vacíos)
    (on-loc v1 p2)
    (quantity v1 n0)
    (on-loc v2 p2)
    (quantity v2 n0)
    
    ; Máquinas en p2
    (on-loc m1 p2)
    (free m1)
    (pulled-by m1 m1)
    (on-loc m2 p2)
    (free m2)
    (pulled-by m2 m2)
    
    ; Vagones libres
    (free v1)
    (free v2)
    
    ; Equipajes
    ; 1. Equipajes sospechosos
    (on-loc e1 p8)
    (suspect e1)
    (on-loc e3 p6)
    (suspect e3)
    (on-loc e4 p6)
    (suspect e4)
    (on-loc e7 p7)
    (suspect e7)
    (on-loc e10 p4)
    (suspect e10)
    
    ; 2. Equipajes normales
    (on-loc e2 p8)
    (safe e2)
    (on-loc e5 p6)
    (safe e5)
    (on-loc e6 facturacion)
    (safe e6)
    (on-loc e8 p5)
    (safe e8)
    (on-loc e9 p1)
    (safe e9)
  )
  
  (:goal (and
    ; 1. Equipajes sospechosos a recogida e inspeccionados
    (on-loc e1 recogida)
    (safe e1)
    (on-loc e3 recogida)
    (safe e3)
    (on-loc e4 recogida)
    (safe e4)
    (on-loc e7 recogida)
    (safe e7)
    (on-loc e10 recogida)
    (safe e10)
    
    ; 2. Traslados de equipajes normales
    (on-loc e2 p4)
    (on-loc e5 p1)
    (on-loc e6 p8)
    (on-loc e8 p3)
    (on-loc e9 p8)
  ))
)