import * as THREE from "three";
import { tileSize } from "../constants";

export function Tree(tileIndex, height) {
    const tree = new THREE.Group();
    tree.position.x = tileIndex * tileSize;

    // Tronco con textura más detallada
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