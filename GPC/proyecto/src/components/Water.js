// src/components/Water.js

import * as THREE from "three";
import { tilesPerRow, tileSize } from "../constants";

export function Water(rowIndex) {
    const water = new THREE.Group();
    water.position.y = rowIndex * tileSize;

    const foundation = new THREE.Mesh(
        new THREE.PlaneGeometry(tilesPerRow * tileSize, tileSize),
        // Un color azul para el agua
        new THREE.MeshLambertMaterial({ color: 0x5190ED })
    );
    foundation.receiveShadow = true;
    water.add(foundation);

    return water;
}