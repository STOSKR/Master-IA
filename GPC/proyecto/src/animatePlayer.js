import * as THREE from "three";
import {
    player,
    position,
    movesQueue,
    stepCompleted
} from "./components/Player";
import { tileSize } from "./constants";
import { metadata as rows } from "./components/Map";

const moveClock = new THREE.Clock(false);

export function animatePlayer() {
    const currentRow = rows[position.currentRow - 1];
    if (currentRow && currentRow.type === "water") {
        const playerBox = new THREE.Box3().setFromObject(player, true);
        let logPlayerIsOn = null;

        for (const log of currentRow.vehicles) {
            if (!log.ref) continue;
            const logBox = new THREE.Box3().setFromObject(log.ref);
            if (playerBox.intersectsBox(logBox)) {
                logPlayerIsOn = log.ref;
                break;
            }
        }

        if (logPlayerIsOn && !movesQueue.length) {
            player.position.x = logPlayerIsOn.position.x;
        }
    }

    if (!movesQueue.length) return;

    if (!moveClock.running) moveClock.start();

    const stepTime = 0.2; // Seconds it takes to take a step
    const progress = Math.min(1, moveClock.getElapsedTime() / stepTime);

    setPosition(progress);
    setRotation(progress);

    // Once a step has ended
    if (progress >= 1) {
        stepCompleted();
        moveClock.stop();
    }
}

function setPosition(progress) {
    const startX = position.currentTile * tileSize;
    const startY = position.currentRow * tileSize;
    let endX = startX;
    let endY = startY;

    const currentMove = movesQueue[0];
    const direction = typeof currentMove === 'object' ? currentMove.direction : currentMove;

    if (direction === "left") endX -= tileSize;
    if (direction === "right") endX += tileSize;
    if (direction === "forward") endY += tileSize;
    if (direction === "backward") endY -= tileSize;

    // Si es un salto, mantener la posición inicial
    if (typeof currentMove === 'object' && currentMove.type === 'jump') {
        endX = startX;
        endY = startY;
    }

    player.position.x = THREE.MathUtils.lerp(startX, endX, progress);
    player.position.y = THREE.MathUtils.lerp(startY, endY, progress);

    const visualsGroup = player.children[0];
    if (visualsGroup && visualsGroup.children[0]) {
        visualsGroup.children[0].position.z = Math.sin(progress * Math.PI) * 8;
    }
}

function setRotation(progress) {
    const currentMove = movesQueue[0];
    const direction = typeof currentMove === 'object' ? currentMove.direction : currentMove;

    let endRotation = 0;
    if (direction === "forward") endRotation = 0;
    if (direction === "left") endRotation = Math.PI / 2;
    if (direction === "right") endRotation = -Math.PI / 2;
    if (direction === "backward") endRotation = Math.PI;

    const visualsGroup = player.children[0];
    if (visualsGroup) {
        visualsGroup.rotation.z = THREE.MathUtils.lerp(
            visualsGroup.rotation.z,
            endRotation,
            progress
        );
    }
}