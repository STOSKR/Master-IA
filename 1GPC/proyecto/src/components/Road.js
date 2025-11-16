import * as THREE from "three";
import { tilesPerRow, tileSize } from "../constants";

export function Road(rowIndex) {
    const road = new THREE.Group();
    road.position.y = rowIndex * tileSize;

    // Base de la carretera con color mejorado
    const foundation = new THREE.Mesh(
        new THREE.BoxGeometry(tilesPerRow * tileSize, tileSize, 2),
        new THREE.MeshLambertMaterial({
            color: 0x4a4e69,
            flatShading: true
        })
    );
    foundation.position.z = 1;
    foundation.receiveShadow = true;
    road.add(foundation);

    // Líneas divisorias amarillas (discontinuas)
    const lineCount = Math.floor(tilesPerRow / 2);
    for (let i = 0; i < lineCount; i++) {
        if (i % 2 === 0) { // Líneas discontinuas
            const line = new THREE.Mesh(
                new THREE.BoxGeometry(tileSize * 0.8, 4, 0.3),
                new THREE.MeshLambertMaterial({
                    color: 0xffd700,
                    flatShading: true
                })
            );
            line.position.x = (i - lineCount / 2) * tileSize;
            line.position.z = 2.2;
            road.add(line);
        }
    }

    // Bordes de la carretera (líneas blancas continuas)
    const edgeWidth = tilesPerRow * tileSize;

    const topEdge = new THREE.Mesh(
        new THREE.BoxGeometry(edgeWidth, 3, 0.3),
        new THREE.MeshLambertMaterial({
            color: 0xe0e0e0,
            flatShading: true
        })
    );
    topEdge.position.y = tileSize / 2 - 2;
    topEdge.position.z = 2.2;
    road.add(topEdge);

    const bottomEdge = new THREE.Mesh(
        new THREE.BoxGeometry(edgeWidth, 3, 0.3),
        new THREE.MeshLambertMaterial({
            color: 0xe0e0e0,
            flatShading: true
        })
    );
    bottomEdge.position.y = -tileSize / 2 + 2;
    bottomEdge.position.z = 2.2;
    road.add(bottomEdge);

    return road;
}