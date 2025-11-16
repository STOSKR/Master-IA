import * as THREE from "three";
import { tileSize } from "../constants";
import { Wheel } from "./Wheel";

export function Truck(initialTileIndex, direction, color) {
    const truck = new THREE.Group();
    truck.position.x = initialTileIndex * tileSize;
    if (!direction) truck.rotation.z = Math.PI;

    // Base del chasis
    const chassis = new THREE.Mesh(
        new THREE.BoxGeometry(100, 32, 8),
        new THREE.MeshLambertMaterial({
            color: 0x2a2a2a,
            flatShading: true,
        })
    );
    chassis.position.z = 10;
    chassis.castShadow = true;
    chassis.receiveShadow = true;
    truck.add(chassis);

    // Carga/remolque principal
    const cargoBase = new THREE.Mesh(
        new THREE.BoxGeometry(70, 35, 25),
        new THREE.MeshLambertMaterial({
            color: 0xb4c6fc,
            flatShading: true,
        })
    );
    cargoBase.position.x = -15;
    cargoBase.position.z = 22;
    cargoBase.castShadow = true;
    cargoBase.receiveShadow = true;
    truck.add(cargoBase);

    // Techo del remolque
    const cargoRoof = new THREE.Mesh(
        new THREE.BoxGeometry(68, 33, 5),
        new THREE.MeshLambertMaterial({
            color: 0x9bb0e8,
            flatShading: true,
        })
    );
    cargoRoof.position.x = -15;
    cargoRoof.position.z = 36;
    cargoRoof.castShadow = true;
    truck.add(cargoRoof);

    // Puertas traseras del remolque
    const door1 = new THREE.Mesh(
        new THREE.BoxGeometry(3, 16, 24),
        new THREE.MeshLambertMaterial({
            color: 0x8a9ed6,
            flatShading: true,
        })
    );
    door1.position.x = -50;
    door1.position.y = 8;
    door1.position.z = 22;
    truck.add(door1);

    const door2 = new THREE.Mesh(
        new THREE.BoxGeometry(3, 16, 24),
        new THREE.MeshLambertMaterial({
            color: 0x8a9ed6,
            flatShading: true,
        })
    );
    door2.position.x = -50;
    door2.position.y = -8;
    door2.position.z = 22;
    truck.add(door2);

    // Cabina base
    const cabinBase = new THREE.Mesh(
        new THREE.BoxGeometry(28, 30, 20),
        new THREE.MeshLambertMaterial({
            color,
            flatShading: true
        })
    );
    cabinBase.position.x = 35;
    cabinBase.position.z = 18;
    cabinBase.castShadow = true;
    cabinBase.receiveShadow = true;
    truck.add(cabinBase);

    // Parte superior de la cabina
    const cabinTop = new THREE.Mesh(
        new THREE.BoxGeometry(24, 26, 15),
        new THREE.MeshLambertMaterial({
            color,
            flatShading: true
        })
    );
    cabinTop.position.x = 35;
    cabinTop.position.z = 32;
    cabinTop.castShadow = true;
    cabinTop.receiveShadow = true;
    truck.add(cabinTop);

    // Capó/frente del camión
    const hood = new THREE.Mesh(
        new THREE.BoxGeometry(12, 28, 16),
        new THREE.MeshLambertMaterial({
            color,
            flatShading: true
        })
    );
    hood.position.x = 47;
    hood.position.z = 20;
    hood.castShadow = true;
    hood.receiveShadow = true;
    truck.add(hood);

    // Parabrisas (más grande y visible)
    const windshield = new THREE.Mesh(
        new THREE.BoxGeometry(4, 24, 14),
        new THREE.MeshLambertMaterial({
            color: 0x5a8fc4,
            flatShading: true,
            transparent: true,
            opacity: 0.5
        })
    );
    windshield.position.x = 46;
    windshield.position.z = 32;
    truck.add(windshield);

    // Parachoques delantero
    const frontBumper = new THREE.Mesh(
        new THREE.BoxGeometry(5, 32, 6),
        new THREE.MeshLambertMaterial({
            color: 0x2a2a2a,
            flatShading: true,
        })
    );
    frontBumper.position.x = 55;
    frontBumper.position.z = 9;
    truck.add(frontBumper);

    // Faros delanteros
    const headlightMaterial = new THREE.MeshLambertMaterial({
        color: 0xffff88,
        flatShading: true,
        emissive: 0xffff88,
        emissiveIntensity: 0.3
    });

    const headlight1 = new THREE.Mesh(
        new THREE.BoxGeometry(2, 5, 5),
        headlightMaterial
    );
    headlight1.position.x = 54;
    headlight1.position.y = 11;
    headlight1.position.z = 16;
    truck.add(headlight1);

    const headlight2 = new THREE.Mesh(
        new THREE.BoxGeometry(2, 5, 5),
        headlightMaterial
    );
    headlight2.position.x = 54;
    headlight2.position.y = -11;
    headlight2.position.z = 16;
    truck.add(headlight2);

    // Luces en el techo de la cabina
    const roofLight1 = new THREE.Mesh(
        new THREE.BoxGeometry(4, 3, 2),
        new THREE.MeshLambertMaterial({
            color: 0xff8800,
            flatShading: true,
            emissive: 0xff8800,
            emissiveIntensity: 0.2
        })
    );
    roofLight1.position.x = 38;
    roofLight1.position.y = 8;
    roofLight1.position.z = 40;
    truck.add(roofLight1);

    const roofLight2 = new THREE.Mesh(
        new THREE.BoxGeometry(4, 3, 2),
        new THREE.MeshLambertMaterial({
            color: 0xff8800,
            flatShading: true,
            emissive: 0xff8800,
            emissiveIntensity: 0.2
        })
    );
    roofLight2.position.x = 38;
    roofLight2.position.y = -8;
    roofLight2.position.z = 40;
    truck.add(roofLight2);

    // Escape
    const exhaust = new THREE.Mesh(
        new THREE.CylinderGeometry(2, 2, 20, 6),
        new THREE.MeshLambertMaterial({
            color: 0x3a3a3a,
            flatShading: true,
        })
    );
    exhaust.position.x = 30;
    exhaust.position.y = 14;
    exhaust.position.z = 30;
    truck.add(exhaust);

    // Espejos retrovisores
    const mirror1 = new THREE.Mesh(
        new THREE.BoxGeometry(4, 2, 5),
        new THREE.MeshLambertMaterial({
            color: 0x2a2a2a,
            flatShading: true,
        })
    );
    mirror1.position.x = 36;
    mirror1.position.y = 17;
    mirror1.position.z = 34;
    truck.add(mirror1);

    const mirror2 = new THREE.Mesh(
        new THREE.BoxGeometry(4, 2, 5),
        new THREE.MeshLambertMaterial({
            color: 0x2a2a2a,
            flatShading: true,
        })
    );
    mirror2.position.x = 36;
    mirror2.position.y = -17;
    mirror2.position.z = 34;
    truck.add(mirror2);

    const frontWheel = Wheel(37);
    truck.add(frontWheel);

    const middleWheel = Wheel(5);
    truck.add(middleWheel);

    const backWheel = Wheel(-35);
    truck.add(backWheel);

    return truck;
}
