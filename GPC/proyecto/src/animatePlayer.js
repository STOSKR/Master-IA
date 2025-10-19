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

// Función de easing (ease in-out cubic)
function easeInOutCubic(t) {
    return t < 0.5
        ? 4 * t * t * t
        : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

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
            position.currentTile = Math.round(player.position.x / tileSize);

            // Efecto de hundimiento del tronco
            animateLogSink(logPlayerIsOn);
        }
    }
    if (!movesQueue.length) return;

    if (!moveClock.running) moveClock.start();

    const stepTime = 0.2;
    const rawProgress = Math.min(1, moveClock.getElapsedTime() / stepTime);
    const progress = easeInOutCubic(rawProgress); // Aplicar easing

    setPosition(progress, rawProgress);
    setRotation(progress);

    if (rawProgress >= 1) {
        stepCompleted();
        moveClock.stop();
    }
}

// Función para animar el hundimiento del tronco
function animateLogSink(log) {
    const targetZ = -0.8; // Hundimiento objetivo
    const sinkSpeed = 0.1;

    // Guardar la posición Z original si no existe
    if (log.userData.originalZ === undefined) {
        log.userData.originalZ = log.position.z || 0;
    }

    // Animar hacia el hundimiento
    if (log.position.z > targetZ) {
        log.position.z = Math.max(targetZ, log.position.z - sinkSpeed);
    }
}

// Función para restaurar la posición del tronco (se llama cuando el jugador se va)
export function resetLogPosition(log) {
    if (log.userData.originalZ !== undefined) {
        const floatSpeed = 0.05;
        if (log.position.z < log.userData.originalZ) {
            log.position.z = Math.min(log.userData.originalZ, log.position.z + floatSpeed);
        }
    }
}

function setPosition(progress, rawProgress) {
    const startX = player.position.x;
    const startY = player.position.y;

    const currentMove = movesQueue[0];
    const direction = typeof currentMove === 'object' ? currentMove.direction : currentMove;

    let destinationTile = position.currentTile;
    let destinationRow = position.currentRow;

    if (direction === "left") destinationTile -= 1;
    if (direction === "right") destinationTile += 1;
    if (direction === "forward") destinationRow += 1;
    if (direction === "backward") destinationRow -= 1;

    let endX = destinationTile * tileSize;
    let endY = destinationRow * tileSize;

    if (typeof currentMove === 'object' && currentMove.type === 'jump') {
        endX = startX;
        endY = startY;
    }

    player.position.x = THREE.MathUtils.lerp(startX, endX, progress);
    player.position.y = THREE.MathUtils.lerp(startY, endY, progress);

    const visualsGroup = player.children[0];
    if (visualsGroup && visualsGroup.children[0]) {
        // Usar rawProgress para el salto para que sea más natural
        visualsGroup.children[0].position.z = Math.sin(rawProgress * Math.PI) * 10;
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