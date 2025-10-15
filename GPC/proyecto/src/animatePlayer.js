import * as THREE from "three";
import {
    player,
    position,
    movesQueue,
    stepCompleted
} from "./components/Player";
import { tileSize } from "./constants";

const moveClock = new THREE.Clock(false);

export function animatePlayer() {
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
    player.children[0].position.z = Math.sin(progress * Math.PI) * 8;
}

function setRotation(progress) {
    const currentMove = movesQueue[0];
    const direction = typeof currentMove === 'object' ? currentMove.direction : currentMove;

    let endRotation = 0;
    if (direction === "forward") endRotation = 0;
    if (direction === "left") endRotation = Math.PI / 2;
    if (direction === "right") endRotation = -Math.PI / 2;
    if (direction === "backward") endRotation = Math.PI;

    player.children[0].rotation.z = THREE.MathUtils.lerp(
        player.children[0].rotation.z,
        endRotation,
        progress
    );
}