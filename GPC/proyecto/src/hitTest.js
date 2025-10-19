import * as THREE from "three";
import { metadata as rows } from "./components/Map";
// 1. Importa movesQueue para saber si el jugador está saltando
import { player, position, clearMoveQueue, movesQueue } from "./components/Player";
import { setGameActive, gameState } from "./gameState";
import { playDeathAnimation } from "./deathAnimations";

const resultDOM = document.getElementById("result-container");
const finalScoreDOM = document.getElementById("final-score");

const playerBoundingBox = new THREE.Box3();
let deathTimeout = null;
let hasTriggeredDeath = false; // Bandera para evitar múltiples muertes
let waterCheckTimer = 0; // Temporizador para verificar agua
const WATER_CHECK_DELAY = 15; // frames antes de verificar muerte en agua (permite saltar)
let currentlyOnLog = false; // Estado actual de si está sobre un tronco

export function isPlayerOnLog() {
    return currentlyOnLog;
}

function showGameOver() {
    if (resultDOM && finalScoreDOM) {
        resultDOM.style.visibility = "visible";
        finalScoreDOM.innerText = position.currentRow.toString();
    }
    deathTimeout = null;
}

export function clearDeathTimeout() {
    if (deathTimeout) {
        clearTimeout(deathTimeout);
        deathTimeout = null;
    }
    hasTriggeredDeath = false; // Resetear la bandera
}

export function hitTest() {
    const row = rows[position.currentRow - 1];
    if (!row) return;

    // Si ya se disparó la muerte, no verificar más
    if (hasTriggeredDeath || !gameState.isActive) return;

    playerBoundingBox.setFromObject(player, true);

    if (row.type === "car" || row.type === "truck") {
        row.vehicles.forEach(({ ref }) => {
            if (!ref) throw Error("Vehicle reference is missing");

            const vehicleBoundingBox = new THREE.Box3().setFromObject(ref);

            if (playerBoundingBox.intersectsBox(vehicleBoundingBox)) {
                if (!resultDOM || !finalScoreDOM) return;

                hasTriggeredDeath = true;
                setGameActive(false);
                clearMoveQueue();

                // Determinar dirección del vehículo
                // row.direction: true = derecha, false = izquierda
                // Si va hacia la derecha (true), el jugador vuela hacia la izquierda (1)
                // Si va hacia la izquierda (false), el jugador vuela hacia la derecha (-1)
                const hitDirection = row.direction ? 1 : -1;

                // Reproducir animación de atropello con dirección
                playDeathAnimation("hit", hitDirection);

                // Mostrar resultado después de un delay para que se vea la animación
                clearDeathTimeout(); // Limpiar cualquier timeout previo
                deathTimeout = setTimeout(showGameOver, 1000);
            }
        });
    }

    if (row.type === "water") {
        const isOnLog = row.vehicles.some(({ ref }) => {
            if (!ref) return false;
            const logBoundingBox = new THREE.Box3().setFromObject(ref);
            return playerBoundingBox.intersectsBox(logBoundingBox);
        });

        // Actualizar estado de si está sobre un tronco
        currentlyOnLog = isOnLog;

        // Verificar muerte solo cuando no está en movimiento y no está sobre un tronco
        if (!isOnLog && movesQueue.length === 0 && !hasTriggeredDeath) {
            hasTriggeredDeath = true;
            setGameActive(false);
            clearMoveQueue();

            // Reproducir animación de ahogamiento
            playDeathAnimation("drown");

            // Mostrar resultado después de un delay para que se vea la animación
            clearDeathTimeout(); // Limpiar cualquier timeout previo
            deathTimeout = setTimeout(showGameOver, 1000);
        }
    } else {
        // Si no está en una fila de agua, no está sobre un tronco
        currentlyOnLog = false;
    }
}