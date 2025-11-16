(define (domain airport-baggage)
  (:requirements :strips :typing)
  
  (:types
    location number machine wagon baggage - object
  )
  
  (:predicates
    (on-loc ?obj - object ?loc - location)
    (attached ?w - wagon ?obj - object)
    (in-wagon ?b - baggage ?w - wagon)
    (suspect ?b - baggage)
    (quantity ?w - wagon ?n - number)
    (adjacent ?l1 - location ?l2 - location)
    (next_num ?n1 - number ?n2 - number)
  )
  
  (:action move
    :parameters (?m - machine ?u - location ?l - location)
    :precondition (and
      (adjacent ?u ?l)
      (on-loc ?m ?u)
    )
    :effect (and
      (on-loc ?m ?l)
      (not (on-loc ?m ?u))
    )
  )
  
  (:action attach
    :parameters (?v - wagon ?obj - object ?u - location)
    :precondition (and
      (on-loc ?v ?u)
      (on-loc ?obj ?u)
      (quantity ?v n0)
    )
    :effect (and
      (attached ?v ?obj)
      (not (on-loc ?v ?u))
    )
  )
  
  (:action detach
    :parameters (?v - wagon ?obj - object ?u - location)
    :precondition (and
      (on-loc ?obj ?u)
      (attached ?v ?obj)
      (quantity ?v n0)
    )
    :effect (and
      (not (attached ?v ?obj))
      (on-loc ?v ?u)
    )
  )
  
  (:action load
    :parameters (?s - baggage ?v - wagon ?m - machine ?u - location ?n_now - number ?n_next - number)
    :precondition (and
      (on-loc ?s ?u)
      (on-loc ?m ?u)
      (attached ?v ?m)
      (quantity ?v ?n_now)
      (next_num ?n_now ?n_next)
    )
    :effect (and
      (in-wagon ?s ?v)
      (not (on-loc ?s ?u))
      (quantity ?v ?n_next)
      (not (quantity ?v ?n_now))
    )
  )
  
  (:action unload
    :parameters (?s - baggage ?v - wagon ?m - machine ?u - location ?n_now - number ?n_next - number)
    :precondition (and
      (on-loc ?m ?u)
      (attached ?v ?m)
      (in-wagon ?s ?v)
      (quantity ?v ?n_now)
      (next_num ?n_next ?n_now)
    )
    :effect (and
      (not (in-wagon ?s ?v))
      (on-loc ?s ?u)
      (quantity ?v ?n_next)
      (not (quantity ?v ?n_now))
    )
  )
  
  (:action inspect
    :parameters (?s - baggage ?v - wagon ?m - machine)
    :precondition (and
      (on-loc ?m inspeccion)
      (attached ?v ?m)
      (in-wagon ?s ?v)
      (suspect ?s)
    )
    :effect (and
      (not (suspect ?s))
    )
  )
)
