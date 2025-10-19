import * as THREE from "three";
import { endsUpInValidPosition } from "../utilities/endsUpInValidPosition";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { metadata as rows, addRows } from "./Map";
import { gameState } from "../gameState";

export let player;

export async function createPlayer() {
    const playerContainer = new THREE.Group();
    const visualsGroup = new THREE.Group();

    const loader = new GLTFLoader();
    const gltf = await loader.loadAsync("/models/vaquero.glb");
    const playerModel = gltf.scene;

    playerModel.scale.set(8, 8, 8);

    playerModel.rotation.x = -Math.PI / 2;
    playerModel.rotation.z = Math.PI;

    playerModel.traverse(function (node) {
        if (node.isMesh) {
            node.castShadow = true;
            node.receiveShadow = true;
        }
    });
    visualsGroup.add(playerModel);
    playerContainer.add(visualsGroup);

    player = playerContainer;
    /*
    const body = new THREE.Mesh(
        new THREE.BoxGeometry(15, 15, 20),
        new THREE.MeshLambertMaterial({
            color: "white",
            flatShading: true,
        })
    );
    body.castShadow = true;
    body.receiveShadow = true;

    body.position.z = 10;
    player.add(body);
    const cap = new THREE.Mesh(
        new THREE.BoxGeometry(2, 4, 2),
        new THREE.MeshLambertMaterial({
            color: 0xf0619a,
            flatShading: true,
        })
    );
    cap.position.z = 21;
    cap.castShadow = true;
    cap.receiveShadow = true;
    player.add(cap);

    const playerContainer = new THREE.Group();
    playerContainer.add(player);
    */
    return player;
}

export const position = {
    currentRow: 0,
    currentTile: 0,
};

export const movesQueue = [];

export function clearMoveQueue() {
    movesQueue.length = 0;
}

export function initializePlayer() {
    player.position.x = 0;
    player.position.y = 0;

    // Resetear completamente el grupo visual (posición y rotación)
    player.children[0].position.x = 0;
    player.children[0].position.y = 0;
    player.children[0].position.z = 0;
    player.children[0].rotation.x = 0;
    player.children[0].rotation.y = 0;
    player.children[0].rotation.z = 0;

    position.currentRow = 0;
    position.currentTile = 0;

    clearMoveQueue();
} export function queueMove(direction) {
    if (!gameState.isActive) {
        clearMoveQueue();
        return;
    }

    const isValidMove = endsUpInValidPosition(
        {
            rowIndex: position.currentRow,
            tileIndex: position.currentTile,
        },
        [...movesQueue, direction]
    );

    if (!isValidMove) {
        movesQueue.push({ type: "jump", direction });
        return;
    }

    movesQueue.push(direction);
}

export function stepCompleted() {
    if (!gameState.isActive) {
        clearMoveQueue();
        return;
    }

    const move = movesQueue.shift();

    if (typeof move === 'object' && move.type === 'jump') {
        return;
    }

    const direction = move;

    if (direction === "forward") position.currentRow += 1;
    if (direction === "backward") position.currentRow -= 1;
    if (direction === "left") position.currentTile -= 1;
    if (direction === "right") position.currentTile += 1;

    if (position.currentRow > rows.length - 10) addRows();

    const scoreDOM = document.getElementById("score");
    if (gameState.isActive && position.currentRow > parseInt(scoreDOM.innerText)) {
        scoreDOM.innerText = position.currentRow.toString();
    }
}