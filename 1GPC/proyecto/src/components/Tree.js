import * as THREE from "three";
import { tileSize } from "../constants";

export function Tree(tileIndex, height) {
    const tree = new THREE.Group();
    tree.position.x = tileIndex * tileSize;

    // Tronco principal
    const trunk = new THREE.Mesh(
        new THREE.BoxGeometry(15, 15, 20),
        new THREE.MeshLambertMaterial({
            color: 0x4d2926,
            flatShading: true,
        })
    );
    trunk.position.z = 10;
    trunk.castShadow = true;
    trunk.receiveShadow = true;
    tree.add(trunk);

    // Añadir textura al tronco con diferentes tonos
    const barkDetail1 = new THREE.Mesh(
        new THREE.BoxGeometry(16, 4, 6),
        new THREE.MeshLambertMaterial({
            color: 0x3d1f1c,
            flatShading: true,
        })
    );
    barkDetail1.position.z = 8;
    barkDetail1.position.y = 3;
    tree.add(barkDetail1);

    const barkDetail2 = new THREE.Mesh(
        new THREE.BoxGeometry(16, 4, 6),
        new THREE.MeshLambertMaterial({
            color: 0x3d1f1c,
            flatShading: true,
        })
    );
    barkDetail2.position.z = 16;
    barkDetail2.position.x = -3;
    tree.add(barkDetail2);

    const crown = new THREE.Mesh(
        new THREE.BoxGeometry(30, 30, height),
        new THREE.MeshLambertMaterial({
            color: 0x5a9216,
            flatShading: true,
        })
    );
    crown.position.z = height / 2 + 20;
    crown.castShadow = true;
    crown.receiveShadow = true;
    tree.add(crown);

    return tree;
}