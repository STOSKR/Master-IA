import * as THREE from "three";
import { tilesPerRow, tileSize } from "../constants";

export function Grass(rowIndex) {
    const grass = new THREE.Group();
    grass.position.y = rowIndex * tileSize;

    // Base de césped con color más vibrante
    const foundation = new THREE.Mesh(
        new THREE.BoxGeometry(tilesPerRow * tileSize, tileSize, 3),
        new THREE.MeshLambertMaterial({
            color: 0x7ec850, // Verde más vibrante
            flatShading: true
        })
    );
    foundation.position.z = 1.5;
    foundation.receiveShadow = true;
    grass.add(foundation);

    // Añadir manchas de césped más oscuro para variedad
    const patchCount = Math.floor(Math.random() * 3) + 2;
    for (let i = 0; i < patchCount; i++) {
        const patch = new THREE.Mesh(
            new THREE.BoxGeometry(
                Math.random() * 15 + 10,
                Math.random() * 15 + 10,
                0.5
            ),
            new THREE.MeshLambertMaterial({
                color: 0x6db03f,
                flatShading: true
            })
        );
        patch.position.x = (Math.random() - 0.5) * tilesPerRow * tileSize * 0.8;
        patch.position.z = 3.8;
        patch.receiveShadow = true;
        grass.add(patch);
    }

    // Añadir flores decorativas ocasionalmente
    if (Math.random() > 0.6) {
        const flowerCount = Math.floor(Math.random() * 3) + 1;
        for (let i = 0; i < flowerCount; i++) {
            const flower = createFlower();
            flower.position.x = (Math.random() - 0.5) * tilesPerRow * tileSize * 0.7;
            flower.position.z = 4;
            grass.add(flower);
        }
    }

    return grass;
}

function createFlower() {
    const flower = new THREE.Group();

    // Tallo
    const stem = new THREE.Mesh(
        new THREE.BoxGeometry(1, 1, 4),
        new THREE.MeshLambertMaterial({
            color: 0x2d5016,
            flatShading: true
        })
    );
    stem.position.z = 2;
    flower.add(stem);

    // Pétalos
    const colors = [0xff69b4, 0xffff00, 0xff6347, 0x9370db, 0xffa500];
    const petalColor = colors[Math.floor(Math.random() * colors.length)];

    const petal = new THREE.Mesh(
        new THREE.BoxGeometry(3, 3, 1),
        new THREE.MeshLambertMaterial({
            color: petalColor,
            flatShading: true
        })
    );
    petal.position.z = 4;
    flower.add(petal);

    return flower;
}