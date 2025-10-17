// src/components/Log.js

import * as THREE from "three";
import { tileSize } from "../constants";

export function Log(initialTileIndex, direction) {
    const log = new THREE.Group();
    log.position.x = initialTileIndex * tileSize;
    if (!direction) log.rotation.z = Math.PI;

    const main = new THREE.Mesh(
        // Más largo y un poco más bajo que un coche
        new THREE.BoxGeometry(100, 30, 20),
        new THREE.MeshLambertMaterial({ color: 0x7a4b28, flatShading: true })
    );
    // Lo hundimos un poco para que parezca que flota
    main.position.z = -5;
    main.castShadow = true;
    main.receiveShadow = true;
    log.add(main);

    return log;
}