// src/components/Water.js

import * as THREE from "three";
import { tilesPerRow, tileSize } from "../constants";

export function Water(rowIndex) {
    const water = new THREE.Group();
    water.position.y = rowIndex * tileSize;

    // Fondo del río (muy profundo)
    const riverBed = new THREE.Mesh(
        new THREE.BoxGeometry(tilesPerRow * tileSize, tileSize, 5),
        new THREE.MeshLambertMaterial({
            color: 0x1a3d6b, // Azul muy oscuro para el fondo
            flatShading: true
        })
    );
    riverBed.position.z = -2;
    riverBed.receiveShadow = true;
    water.add(riverBed);

    // Agua con efecto de profundidad - capa media
    const deepWater = new THREE.Mesh(
        new THREE.BoxGeometry(tilesPerRow * tileSize, tileSize, 4),
        new THREE.MeshLambertMaterial({
            color: 0x2c5aa0, // Azul más oscuro para profundidad
            flatShading: true,
            transparent: true,
            opacity: 0.8
        })
    );
    deepWater.position.z = 0;
    deepWater.receiveShadow = true;
    water.add(deepWater);

    // Agua superficie
    const foundation = new THREE.Mesh(
        new THREE.BoxGeometry(tilesPerRow * tileSize, tileSize, 2),
        new THREE.MeshLambertMaterial({
            color: 0x4a90e2, // Azul más vibrante
            flatShading: true,
            transparent: true,
            opacity: 0.85
        })
    );
    foundation.position.z = 1.5;
    foundation.receiveShadow = true;
    water.add(foundation);

    // Añadir "olas" o detalles visuales con más variedad
    const waveCount = Math.floor(Math.random() * 5) + 3;
    for (let i = 0; i < waveCount; i++) {
        const waveSize = Math.random() * 25 + 15;
        const wave = new THREE.Mesh(
            new THREE.BoxGeometry(
                waveSize,
                waveSize,
                0.8
            ),
            new THREE.MeshLambertMaterial({
                color: 0x6bb3f7,
                flatShading: true,
                transparent: true,
                opacity: 0.6
            })
        );
        wave.position.x = (Math.random() - 0.5) * tilesPerRow * tileSize * 0.8;
        wave.position.y = (Math.random() - 0.5) * tileSize * 0.6;
        wave.position.z = 1.8;
        wave.receiveShadow = true;
        water.add(wave);

        // Guardar referencia para animación
        wave.userData.initialZ = wave.position.z;
        wave.userData.waveSpeed = Math.random() * 0.5 + 0.5;
        wave.userData.waveOffset = Math.random() * Math.PI * 2;
    }

    // Detalles de espuma en el agua
    const foamCount = Math.floor(Math.random() * 4) + 2;
    for (let i = 0; i < foamCount; i++) {
        const foam = new THREE.Mesh(
            new THREE.BoxGeometry(
                Math.random() * 8 + 5,
                Math.random() * 8 + 5,
                0.5
            ),
            new THREE.MeshLambertMaterial({
                color: 0xd4f1f9,
                flatShading: true,
                transparent: true,
                opacity: 0.8
            })
        );
        foam.position.x = (Math.random() - 0.5) * tilesPerRow * tileSize * 0.7;
        foam.position.y = (Math.random() - 0.5) * tileSize * 0.5;
        foam.position.z = 2;
        water.add(foam);

        // Guardar referencia para animación
        foam.userData.initialZ = foam.position.z;
        foam.userData.waveSpeed = Math.random() * 0.3 + 0.3;
        foam.userData.waveOffset = Math.random() * Math.PI * 2;
    }

    // Añadir piedras ocasionales
    if (Math.random() > 0.6) {
        const rockCount = Math.floor(Math.random() * 3) + 1;
        for (let i = 0; i < rockCount; i++) {
            const rock = createRock();
            rock.position.x = (Math.random() - 0.5) * tilesPerRow * tileSize * 0.7;
            rock.position.y = (Math.random() - 0.5) * tileSize * 0.5;
            rock.position.z = 2;
            water.add(rock);
        }
    }

    return water;
} function createRock() {
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