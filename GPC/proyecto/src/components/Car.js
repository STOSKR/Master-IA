import * as THREE from "three";
import { tileSize } from "../constants";
import { Wheel } from "./Wheel";

export function Car(initialTileIndex, direction, color) {
    const car = new THREE.Group();
    car.position.x = initialTileIndex * tileSize;
    if (!direction) car.rotation.z = Math.PI;

    // Cuerpo principal inferior
    const baseBody = new THREE.Mesh(
        new THREE.BoxGeometry(60, 30, 10),
        new THREE.MeshLambertMaterial({
            color,
            flatShading: true
        })
    );
    baseBody.position.z = 8;
    baseBody.castShadow = true;
    baseBody.receiveShadow = true;
    car.add(baseBody);

    // Cuerpo principal superior (más estrecho)
    const main = new THREE.Mesh(
        new THREE.BoxGeometry(55, 28, 8),
        new THREE.MeshLambertMaterial({
            color,
            flatShading: true
        })
    );
    main.position.z = 16;
    main.castShadow = true;
    main.receiveShadow = true;
    car.add(main);

    // Capó (parte delantera del coche)
    const hood = new THREE.Mesh(
        new THREE.BoxGeometry(20, 26, 6),
        new THREE.MeshLambertMaterial({
            color,
            flatShading: true
        })
    );
    hood.position.x = 20;
    hood.position.z = 19;
    hood.castShadow = true;
    hood.receiveShadow = true;
    car.add(hood);

    // Cabina con colores más vibrantes
    const cabin = new THREE.Mesh(
        new THREE.BoxGeometry(28, 24, 12),
        new THREE.MeshLambertMaterial({
            color: 0xd4e4f7, // Azul claro en vez de blanco puro
            flatShading: true,
        })
    );
    cabin.position.x = -8;
    cabin.position.z = 25.5;
    cabin.castShadow = true;
    cabin.receiveShadow = true;
    car.add(cabin);

    // Techo de la cabina
    const roof = new THREE.Mesh(
        new THREE.BoxGeometry(24, 20, 3),
        new THREE.MeshLambertMaterial({
            color: 0xb0c4de,
            flatShading: true,
        })
    );
    roof.position.x = -8;
    roof.position.z = 32;
    roof.castShadow = true;
    car.add(roof);

    // Detalles del coche: ventanas
    const windowMaterial = new THREE.MeshLambertMaterial({
        color: 0x1e3a5f,
        flatShading: true,
        transparent: true,
        opacity: 0.7
    });

    const frontWindow = new THREE.Mesh(
        new THREE.BoxGeometry(2, 20, 10),
        windowMaterial
    );
    frontWindow.position.x = 6;
    frontWindow.position.z = 25.5;
    car.add(frontWindow);

    const backWindow = new THREE.Mesh(
        new THREE.BoxGeometry(2, 20, 10),
        windowMaterial
    );
    backWindow.position.x = -22;
    backWindow.position.z = 25.5;
    car.add(backWindow);

    // Parachoques delantero
    const frontBumper = new THREE.Mesh(
        new THREE.BoxGeometry(4, 30, 4),
        new THREE.MeshLambertMaterial({
            color: 0x2a2a2a,
            flatShading: true,
        })
    );
    frontBumper.position.x = 32;
    frontBumper.position.z = 6;
    car.add(frontBumper);

    // Parachoques trasero
    const backBumper = new THREE.Mesh(
        new THREE.BoxGeometry(4, 30, 4),
        new THREE.MeshLambertMaterial({
            color: 0x2a2a2a,
            flatShading: true,
        })
    );
    backBumper.position.x = -32;
    backBumper.position.z = 6;
    car.add(backBumper);

    // Faros delanteros
    const headlightMaterial = new THREE.MeshLambertMaterial({
        color: 0xffff88,
        flatShading: true,
        emissive: 0xffff88,
        emissiveIntensity: 0.3
    });

    const headlight1 = new THREE.Mesh(
        new THREE.BoxGeometry(2, 4, 4),
        headlightMaterial
    );
    headlight1.position.x = 31;
    headlight1.position.y = 9;
    headlight1.position.z = 12;
    car.add(headlight1);

    const headlight2 = new THREE.Mesh(
        new THREE.BoxGeometry(2, 4, 4),
        headlightMaterial
    );
    headlight2.position.x = 31;
    headlight2.position.y = -9;
    headlight2.position.z = 12;
    car.add(headlight2);

    // Luces traseras
    const taillightMaterial = new THREE.MeshLambertMaterial({
        color: 0xff0000,
        flatShading: true,
        emissive: 0xff0000,
        emissiveIntensity: 0.2
    });

    const taillight1 = new THREE.Mesh(
        new THREE.BoxGeometry(2, 3, 3),
        taillightMaterial
    );
    taillight1.position.x = -31;
    taillight1.position.y = 10;
    taillight1.position.z = 12;
    car.add(taillight1);

    const taillight2 = new THREE.Mesh(
        new THREE.BoxGeometry(2, 3, 3),
        taillightMaterial
    );
    taillight2.position.x = -31;
    taillight2.position.y = -10;
    taillight2.position.z = 12;
    car.add(taillight2);

    // Espejos retrovisores
    const mirror1 = new THREE.Mesh(
        new THREE.BoxGeometry(3, 2, 4),
        new THREE.MeshLambertMaterial({
            color: 0x2a2a2a,
            flatShading: true,
        })
    );
    mirror1.position.x = 2;
    mirror1.position.y = 15;
    mirror1.position.z = 28;
    car.add(mirror1);

    const mirror2 = new THREE.Mesh(
        new THREE.BoxGeometry(3, 2, 4),
        new THREE.MeshLambertMaterial({
            color: 0x2a2a2a,
            flatShading: true,
        })
    );
    mirror2.position.x = 2;
    mirror2.position.y = -15;
    mirror2.position.z = 28;
    car.add(mirror2);

    const frontWheel = Wheel(18);
    car.add(frontWheel);

    const backWheel = Wheel(-18);
    car.add(backWheel);

    return car;
}