import * as THREE from "three";
import { tileSize } from "../constants";
import { Wheel } from "./Wheel";

export function Car(initialTileIndex, direction, color) {
    const car = new THREE.Group();
    car.position.x = initialTileIndex * tileSize;
    if (!direction) car.rotation.z = Math.PI;

    // Cuerpo principal con esquinas redondeadas (estilo low-poly)
    const main = new THREE.Mesh(
        new THREE.BoxGeometry(60, 30, 15),
        new THREE.MeshLambertMaterial({
            color,
            flatShading: true
        })
    );
    main.position.z = 12;
    main.castShadow = true;
    main.receiveShadow = true;
    car.add(main);

    // Cabina con colores más vibrantes
    const cabin = new THREE.Mesh(
        new THREE.BoxGeometry(33, 24, 12),
        new THREE.MeshLambertMaterial({
            color: 0xd4e4f7, // Azul claro en vez de blanco puro
            flatShading: true,
        })
    );
    cabin.position.x = -6;
    cabin.position.z = 25.5;
    cabin.castShadow = true;
    cabin.receiveShadow = true;
    car.add(cabin);

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
    frontWindow.position.x = 10;
    frontWindow.position.z = 25.5;
    car.add(frontWindow);

    // Faros delanteros
    const headlightMaterial = new THREE.MeshLambertMaterial({
        color: 0xffff88,
        flatShading: true,
        emissive: 0xffff88,
        emissiveIntensity: 0.3
    });

    const headlight1 = new THREE.Mesh(
        new THREE.BoxGeometry(2, 3, 3),
        headlightMaterial
    );
    headlight1.position.x = 30;
    headlight1.position.y = 8;
    headlight1.position.z = 12;
    car.add(headlight1);

    const headlight2 = new THREE.Mesh(
        new THREE.BoxGeometry(2, 3, 3),
        headlightMaterial
    );
    headlight2.position.x = 30;
    headlight2.position.y = -8;
    headlight2.position.z = 12;
    car.add(headlight2);

    const frontWheel = Wheel(18);
    car.add(frontWheel);

    const backWheel = Wheel(-18);
    car.add(backWheel);

    return car;
}