import * as THREE from "three";
import {
    player,
    position,
    movesQueue,
    stepCompleted
} from "./components/Player";
import { tileSize } from "./constants";
import { metadata as rows } from "./components/Map";
import { isPlayerOnLog } from "./hitTest";

const moveClock = new THREE.Clock(false);
let particleSystemRef = null;
const LOG_HEIGHT_OFFSET = 6; // Altura adicional cuando está sobre un tronco

// Función para establecer la referencia al sistema de partículas
export function setParticleSystem(particleSystem) {
    particleSystemRef = particleSystem;
}

// Función de easing (ease in-out cubic)
function easeInOutCubic(t) {
    return t < 0.5
        ? 4 * t * t * t
        : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

export function animatePlayer() {
    const currentRow = rows[position.currentRow - 1];

    // Ajustar altura del jugador basada en si está sobre un tronco SOLO cuando está quieto
    const visualsGroup = player.children[0];
    if (visualsGroup && visualsGroup.children[0] && !moveClock.running) {
        const targetHeight = isPlayerOnLog() ? LOG_HEIGHT_OFFSET : 0;
        // Usar lerp suave solo cuando está completamente quieto
        visualsGroup.children[0].position.z = THREE.MathUtils.lerp(
            visualsGroup.children[0].position.z,
            targetHeight,
            0.2
        );
    }

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

            // Crear salpicaduras de agua cuando el jugador aterriza en el tronco
            if (particleSystemRef && moveClock.running && moveClock.getElapsedTime() > 0.18) {
                // Solo crear salpicaduras al final del salto
                const splashCreated = logPlayerIsOn.userData.splashCreated || false;
                if (!splashCreated) {
                    particleSystemRef.createWaterSplash(player.position);
                    logPlayerIsOn.userData.splashCreated = true;
                    setTimeout(() => {
                        logPlayerIsOn.userData.splashCreated = false;
                    }, 500);
                }
            }
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
        // Ajustar altura instantáneamente al aterrizar
        if (visualsGroup && visualsGroup.children[0]) {
            const targetHeight = isPlayerOnLog() ? LOG_HEIGHT_OFFSET : 0;
            visualsGroup.children[0].position.z = targetHeight;
        }

        // Crear partículas de polvo al aterrizar (si no es en agua)
        const currentRow = rows[position.currentRow - 1];
        if (particleSystemRef && currentRow && currentRow.type !== "water") {
            particleSystemRef.createDustParticles(player.position);
        }

        stepCompleted();
        moveClock.stop();
    }
}

// Función para animar el hundimiento del tronco
function animateLogSink(log) {
    const sinkAmount = 1.2; // Cuánto se hunde
    const sinkSpeed = 0.08;

    // Guardar la posición Z original si no existe
    if (log.userData.originalZ === undefined) {
        log.userData.originalZ = log.position.z || 0;
    }

    const targetZ = log.userData.originalZ - sinkAmount;

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
        // Calcular altura base del salto
        const jumpHeight = Math.sin(rawProgress * Math.PI) * 10;

        // Añadir altura del tronco si está sobre uno
        const logHeight = isPlayerOnLog() ? LOG_HEIGHT_OFFSET : 0;

        // Aplicar altura total
        visualsGroup.children[0].position.z = jumpHeight + logHeight;
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