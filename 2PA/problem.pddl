(define (problem airport-baggage-problem)
  (:domain airport-baggage)
  
  (:objects
    n0 n1 n2 - number
    p1 p2 p3 p4 p5 p6 p7 p8 inspeccion facturacion recogida - location
    e1 e2 e3 e4 e5 e6 - baggage
    v1 v2 v3 v4 v5 - wagon
    m1 m2 - machine
  )
  
  (:init
    ; Adyacencias
    (adjacent facturacion recogida)
    (adjacent recogida facturacion)
    (adjacent facturacion inspeccion)
    (adjacent inspeccion facturacion)
    (adjacent facturacion p2)
    (adjacent p2 facturacion)
    
    (adjacent recogida inspeccion)
    (adjacent inspeccion recogida)
    (adjacent recogida p6)
    (adjacent p6 recogida)
    
    (adjacent inspeccion p1)
    (adjacent p1 inspeccion)
    (adjacent inspeccion p5)
    (adjacent p5 inspeccion)
    
    (adjacent p1 p3)
    (adjacent p3 p1)
    (adjacent p2 p4)
    (adjacent p4 p2)
    (adjacent p3 p4)
    (adjacent p4 p3)
    
    (adjacent p5 p7)
    (adjacent p7 p5)
    (adjacent p6 p8)
    (adjacent p8 p6)
    (adjacent p7 p8)
    (adjacent p8 p7)
    
    ; Relación de números
    (next_num n0 n1)
    (next_num n1 n2)
    
    ; Vagones en p1 (vacíos)
    (on-loc v1 p1)
    (quantity v1 n0)
    (on-loc v2 p1)
    (quantity v2 n0)
    (on-loc v3 p1)
    (quantity v3 n0)
    
    ; Vagones en p5 (vacíos)
    (on-loc v4 p5)
    (quantity v4 n0)
    (on-loc v5 p5)
    (quantity v5 n0)
    
    ; Máquinas en recogida
    (on-loc m1 recogida)
    (on-loc m2 recogida)
    
    ; Equipajes
    ; 1. Un equipaje no sospechoso facturado debe ir a la puerta 4
    (on-loc e1 facturacion)
    
    ; 2. Un equipaje no sospechoso facturado debe ir a la puerta 8
    (on-loc e2 facturacion)
    
    ; 3. Un equipaje sospechoso llega a la puerta 6 y debe ir a recogida
    (on-loc e3 p6)
    (suspect e3)
    
    ; 4. Un equipaje no sospechoso llega a la puerta 6 y debe ir a recogida
    (on-loc e4 p6)
    
    ; 5. Un equipaje no sospechoso llega a la puerta 2 y debe ir a recogida
    (on-loc e5 p2)
    
    ; 6. Un equipaje sospechoso llega a la puerta 2 y debe ir a recogida
    (on-loc e6 p2)
    (suspect e6)
  )
  
  (:goal (and
    ; 1. Equipaje e1 en puerta 4
    (on-loc e1 p4)
    
    ; 2. Equipaje e2 en puerta 8
    (on-loc e2 p8)
    
    ; 3. Equipaje e3 en recogida y no sospechoso
    (on-loc e3 recogida)
    (not (suspect e3))
    
    ; 4. Equipaje e4 en recogida
    (on-loc e4 recogida)
    
    ; 5. Equipaje e5 en recogida
    (on-loc e5 recogida)
    
    ; 6. Equipaje e6 en recogida y no sospechoso
    (on-loc e6 recogida)
    (not (suspect e6))
  ))
)
