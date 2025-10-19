// src/components/Water.js

import * as THREE from "three";
import { tilesPerRow, tileSize } from "../constants";

export function Water(rowIndex) {
    const water = new THREE.Group();
    water.position.y = rowIndex * tileSize;

    // Agua con efecto de profundidad
    const foundation = new THREE.Mesh(
        new THREE.BoxGeometry(tilesPerRow * tileSize, tileSize, 3),
        new THREE.MeshLambertMaterial({
            color: 0x4a90e2, // Azul más vibrante
            flatShading: true
        })
    );
    foundation.position.z = 0.5;
    foundation.receiveShadow = true;
    water.add(foundation);

    // Añadir "olas" o detalles visuales
    const waveCount = Math.floor(Math.random() * 4) + 2;
    for (let i = 0; i < waveCount; i++) {
        const wave = new THREE.Mesh(
            new THREE.BoxGeometry(
                Math.random() * 20 + 10,
                Math.random() * 20 + 10,
                0.5
            ),
            new THREE.MeshLambertMaterial({
                color: 0x6bb3f7,
                flatShading: true,
                transparent: true,
                opacity: 0.7
            })
        );
        wave.position.x = (Math.random() - 0.5) * tilesPerRow * tileSize * 0.8;
        wave.position.y = (Math.random() - 0.5) * tileSize * 0.5;
        wave.position.z = 1.2;
        wave.receiveShadow = true;
        water.add(wave);

        // Guardar referencia para animación
        wave.userData.initialZ = wave.position.z;
        wave.userData.waveSpeed = Math.random() * 0.5 + 0.5;
    }

    // Añadir piedras ocasionales
    if (Math.random() > 0.7) {
        const rockCount = Math.floor(Math.random() * 2) + 1;
        for (let i = 0; i < rockCount; i++) {
            const rock = createRock();
            rock.position.x = (Math.random() - 0.5) * tilesPerRow * tileSize * 0.7;
            rock.position.y = (Math.random() - 0.5) * tileSize * 0.5;
            rock.position.z = 1.5;
            water.add(rock);
        }
    }

    return water;
}

function createRock() {
    const rock = new THREE.Mesh(
        new THREE.DodecahedronGeometry(Math.random() * 3 + 2, 0),
        new THREE.MeshLambertMaterial({
            color: 0x708090,
            flatShading: true
        })
    );
    rock.castShadow = true;
    rock.receiveShadow = true;
    return rock;
}