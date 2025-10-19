// src/components/Log.js

import * as THREE from "three";
import { tileSize } from "../constants";

export function Log(initialTileIndex, direction) {
    const log = new THREE.Group();
    log.position.x = initialTileIndex * tileSize;
    if (!direction) log.rotation.z = Math.PI;

    // Tronco principal (más cilíndrico con geometría)
    const main = new THREE.Mesh(
        new THREE.BoxGeometry(100, 30, 20),
        new THREE.MeshLambertMaterial({
            color: 0x8b5a2b,
            flatShading: true
        })
    );
    main.position.z = -5; // Más bajo para que el jugador esté encima
    main.castShadow = true;
    main.receiveShadow = true;
    log.add(main);

    // Parte superior del tronco (más clara)
    const topPart = new THREE.Mesh(
        new THREE.BoxGeometry(98, 28, 8),
        new THREE.MeshLambertMaterial({
            color: 0xa0724e,
            flatShading: true
        })
    );
    topPart.position.z = 6; // Ajustado proporcionalmente
    topPart.castShadow = true;
    topPart.receiveShadow = true;
    log.add(topPart);

    // Anillos de crecimiento en los extremos
    const ringMaterial = new THREE.MeshLambertMaterial({
        color: 0x6b4423,
        flatShading: true
    });

    // Anillo frontal
    const frontRing = new THREE.Mesh(
        new THREE.CylinderGeometry(12, 12, 3, 8),
        ringMaterial
    );
    frontRing.rotation.z = Math.PI / 2;
    frontRing.position.x = 52;
    frontRing.position.z = -5; // Ajustado
    frontRing.castShadow = true;
    log.add(frontRing);

    // Anillo trasero
    const backRing = new THREE.Mesh(
        new THREE.CylinderGeometry(12, 12, 3, 8),
        ringMaterial
    );
    backRing.rotation.z = Math.PI / 2;
    backRing.position.x = -52;
    backRing.position.z = -5; // Ajustado
    backRing.castShadow = true;
    log.add(backRing);

    // Añadir nudos en el tronco
    const knotCount = Math.floor(Math.random() * 3) + 2;
    for (let i = 0; i < knotCount; i++) {
        const knot = new THREE.Mesh(
            new THREE.BoxGeometry(6, 4, 4),
            new THREE.MeshLambertMaterial({
                color: 0x5c3d24,
                flatShading: true
            })
        );
        knot.position.x = (Math.random() - 0.5) * 80;
        knot.position.y = (Math.random() - 0.5) * 20;
        knot.position.z = 2; // Ajustado
        knot.rotation.z = Math.random() * Math.PI;
        log.add(knot);
    }

    // Corteza texturizada en los lados
    const barkDetail1 = new THREE.Mesh(
        new THREE.BoxGeometry(95, 2, 15),
        new THREE.MeshLambertMaterial({
            color: 0x6b4423,
            flatShading: true
        })
    );
    barkDetail1.position.y = 14;
    barkDetail1.position.z = -3; // Ajustado
    log.add(barkDetail1);

    const barkDetail2 = new THREE.Mesh(
        new THREE.BoxGeometry(95, 2, 15),
        new THREE.MeshLambertMaterial({
            color: 0x6b4423,
            flatShading: true
        })
    );
    barkDetail2.position.y = -14;
    barkDetail2.position.z = -3; // Ajustado
    log.add(barkDetail2);

    return log;
}