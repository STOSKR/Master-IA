# Objetos
- Máquina (sin equipajes)
- Vagón (máx. 2 equipajes)
- Equipaje
- Ubicación

# Relaciones
- Los vagones tienen que estar encadenados a una máquina para moverse.
- Se puede encadenar nº infinito de vagones.
- Un vagón se puede encadenar/desencadenar del tren en cualquier momento, pero para hacerlo, el vagón debe de estar vacío.
- Los equipajes sospechosos deben pasar previamente por la oficina de inspección.

# Literals

Relaciones principales:
- on-loc(máquina | vagón | equipaje, ubicación)
- attached(vagón, máquina) # encadenado
- in-wagon(equipaje, vagón)

Propiedades/estados: 
- suspect(equipaje)
- quantity(vagón, número)

Abstracciones (no dinámicos):
- adjacent(ubicación, ubicación)
- next_num(número, número)

# Objetos
- número: {n0, n1, n2} (abstracciones para representar los números 0, 1 y 2)
- ubicación: {p1, p2, p3, p4, p5, p6, p7, p8, inspeccion, facturacion, recogida}
- equipaje: {e1, e2, e3, e4, e5, e6} 
- vagón: {v1, v2, v3, v4, v5}
- máquina: {m1, m2}

# Literals inicializados
## Adyacencia
facturacion <-> recogida
    - adjacent(facturacion, recogida)
    - adjacent(recogida, facturacion)
facturacion <-> inspeccion
    - adjacent(facturacion, inspeccion)
    - adjacent(inspeccion, facturacion)
facturacion <-> p2
    - adjacent(facturacion, p2)
    - adjacent(p2, facturacion)

recogida <-> inspeccion
    - adjacent(recogida, inspeccion)
    - adjacent(inspeccion, recogida)
recogida <-> p6
    - adjacent(recogida, p6)
    - adjacent(p6, recogida)

inspeccion <-> p1
    - adjacent(inspeccion, p1)
    - adjacent(p1, inspeccion)
inspeccion <-> p5
    - adjacent(inspeccion, p5)
    - adjacent(p5, inspeccion)

p1 <-> p3
    - adjacent(p1, p3)
    - adjacent(p3, p1)
p2 <-> p4
    - adjacent(p2, p4)
    - adjacent(p4, p2)
p3 <-> p4
    - adjacent(p3, p4)
    - adjacent(p4, p3)

p5 <-> p7
    - adjacent(p5, p7)
    - adjacent(p7, p5)
p6 <-> p8
    - adjacent(p6, p8)
    - adjacent(p8, p6)
p7 <-> p8
    - adjacent(p7, p8)
    - adjacent(p8, p7)

## Relación de números
next_num(n0, n1)
next_num(n1, n2)


## Literals de estado inicial
Tres vagones sueltos en la puerta1:
- on-loc(v1, p1), quantity(v1, n0)
- on-loc(v2, p1), quantity(v2, n0)
- on-loc(v3, p1), quantity(v3, n0)
Dos vagones sueltos en la puerta5:
- on-loc(v4, p5), quantity(v4, n0)
- on-loc(v5, p5), quantity(v5, n0)
Dos máquinas en recogida de equipajes:
- on-loc(m1, recogida), on-loc(m2, recogida)

6 equipajes (situaciones iniciales y finales):

- 1. Un equipaje no sospechoso facturado debe ir a la puerta 4.
    on-loc(e1, facturacion)
- 2. Un equipaje no sospechoso facturado debe ir a la puerta 8.
    on-loc(e2, facturacion)
- 3. Un equipaje sospechoso llega a la puerta 6 y debe ir a la zona de recogida de equipajes.
    on-loc(e3, p6), suspect(e3)
- 4. Un equipaje no sospechoso llega a la puerta 6 y debe ir a la zona de recogida de equipajes.
    on-loc(e4, p6)
- 5. Un equipaje no sospechoso llega a la puerta 2 y debe ir a la zona de recogida de equipajes.
    on-loc(e5, p2)
- 6. Un equipaje sospechoso llega a la puerta 2 y debe ir a la zona de recogida de equipajes.
    on-loc(e6, p2), suspect(e6)

# Literals de estado final/objetivo

6 equipajes (situaciones iniciales y finales):

- 1. Un equipaje no sospechoso facturado debe ir a la puerta 4.
    on-loc(e1, p4)
- 2. Un equipaje no sospechoso facturado debe ir a la puerta 8.
    on-loc(e2, p8)
- 3. Un equipaje sospechoso llega a la puerta 6 y debe ir a la zona de recogida de equipajes.
    on-loc(e3, recogida), ~suspect(e3)
- 4. Un equipaje no sospechoso llega a la puerta 6 y debe ir a la zona de recogida de equipajes.
    on-loc(e4, recogida)
- 5. Un equipaje no sospechoso llega a la puerta 2 y debe ir a la zona de recogida de equipajes.
    on-loc(e5, recogida)
- 6. Un equipaje sospechoso llega a la puerta 2 y debe ir a la zona de recogida de equipajes.
    on-loc(e6, recogida), ~suspect(e6)

# Operadores
Vamos a suponer que los vagones no se enganchan en cadena uno detrás de otro sino que la relación siempre es vagón-máquina tanto para enganchar como desenganchar.

move(m, u, l):
    ;; máquina `m` se mueve desde ubicación `u` hasta ubicación `l`
    precond: adjacent(u, l), on-loc(m, u), 
    effects: on-loc(m, l), ~on-loc(m, u)

attach(v, m, u):
    ;; vagón `v` se engancha a máquina `m` en ubicación `u`
    precond: on-loc(m, u), on-loc(v, u), quantity(v, n0) # está vacío 
    effects: attached(v, m), ~on-loc(v, u)

detach(v, m, u):
    ;; vagón `v` se desengancha de máquina `m` en ubicación `u`
    precond: on-loc(m, u), attached(v, m), quantity(v, n0) # está vacío 
    effects: ~attached(v, m), on-loc(v, u)

## Gestión del nº de equipajes
load(s, v, m, u, n_now, n_next):
    ;; equipaje `s` se carga en vagón `v` (con `n_now` equipajes cargados) de la máquina `m` en ubicación `u`
    precond: on-loc(s, u), on-loc(m, u), attached(v, m), quantity(v, n_now), next_num(n_now, n_next) # next_num nos sirve para controlar los incrementos
    effects: in-wagon(s, v), ~on-loc(s, u), quantity(v, n_next), ~quantity(v, n_now)

unload(s, v, m, u, n_now, n_next):
    ;; equipaje `s` se descarga del vagón `v` (con `n_now` equipajes cargados) de la máquina `m` en ubicación `u`
    precond: on-loc(m, u), attached(v, m), in-wagon(s, v), quantity(v, n_now), next_num(n_next, n_now) # invertimos next_num para controlar el decremento
    effects: ~in-wagon(s, v), on-loc(s, u), quantity(v, n_next), ~quantity(v, n_now)

inspect(s, v, m):
    ;; equipaje `s` (sospechoso) del vagón `v` de la máquina `m` se inspecciona en `inspeccion` (la oficina de inspección) 
    precond: on-loc(m, inspeccion), attached(v, m), in-wagon(s, v), suspect(s)
    effects: ~suspect(s)