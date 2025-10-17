import * as THREE from "three";
import { metadata as rows } from "./components/Map";
// 1. Importa movesQueue para saber si el jugador está saltando
import { player, position, clearMoveQueue, movesQueue } from "./components/Player";
import { setGameActive } from "./gameState";

const resultDOM = document.getElementById("result-container");
const finalScoreDOM = document.getElementById("final-score");

const playerBoundingBox = new THREE.Box3();

export function hitTest() {
    const row = rows[position.currentRow - 1];
    if (!row) return;

    playerBoundingBox.setFromObject(player, true);

    if (row.type === "car" || row.type === "truck") {
        row.vehicles.forEach(({ ref }) => {
            if (!ref) throw Error("Vehicle reference is missing");

            const vehicleBoundingBox = new THREE.Box3().setFromObject(ref);

            if (playerBoundingBox.intersectsBox(vehicleBoundingBox)) {
                if (!resultDOM || !finalScoreDOM) return;

                setGameActive(false);
                clearMoveQueue();
                resultDOM.style.visibility = "visible";
                finalScoreDOM.innerText = position.currentRow.toString();
            }
        });
    }

    if (row.type === "water" && movesQueue.length === 0) {
        const isOnLog = row.vehicles.some(({ ref }) => {
            if (!ref) return false;
            const logBoundingBox = new THREE.Box3().setFromObject(ref);
            return playerBoundingBox.intersectsBox(logBoundingBox);
        });

        if (!isOnLog) {
            setGameActive(false);
            clearMoveQueue();
            resultDOM.style.visibility = "visible";
            finalScoreDOM.innerText = position.currentRow.toString();
        }
    }
}