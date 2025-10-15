import * as THREE from "three";
import { endsUpInValidPosition } from "../utilities/endsUpInValidPosition";
import { metadata as rows, addRows } from "./Map";
import { gameState } from "../gameState";

export const player = Player();

function Player() {
    const player = new THREE.Group();
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

    return playerContainer;
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
    player.children[0].position.z = 0;

    // Initialize metadata
    position.currentRow = 0;
    position.currentTile = 0;

    // Clear the moves queue
    clearMoveQueue();
}

export function queueMove(direction) {
    // Si el juego no está activo, vacía la cola y no añadas nuevos movimientos
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
        // Guardar la dirección intentada junto con el salto
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

    // Si es un salto, no actualizar la posición
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