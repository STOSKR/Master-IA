import * as THREE from "three";
import { metadata as rows } from "./components/Map";
import { minTileIndex, maxTileIndex, tileSize } from "./constants";
import { player, position } from "./components/Player";
import { resetLogPosition } from "./animatePlayer";

const clock = new THREE.Clock();

export function animateVehicles() {
    const delta = clock.getDelta();

    // Animate cars and trucks
    rows.forEach((rowData, rowIndex) => {
        if (rowData.type === "car" || rowData.type === "truck" || rowData.type === "water") {
            const beginningOfRow = (minTileIndex - 2) * tileSize;
            const endOfRow = (maxTileIndex + 2) * tileSize;

            rowData.vehicles.forEach(({ ref }) => {
                if (!ref) throw Error("Vehicle reference is missing");

                if (rowData.direction) {
                    ref.position.x =
                        ref.position.x > endOfRow
                            ? beginningOfRow
                            : ref.position.x + rowData.speed * delta;
                } else {
                    ref.position.x =
                        ref.position.x < beginningOfRow
                            ? endOfRow
                            : ref.position.x - rowData.speed * delta;
                }

                // Si es un tronco y el jugador no está encima, que vuelva a flotar
                if (rowData.type === "water") {
                    const isPlayerOnThisLog = rowIndex === position.currentRow - 1 &&
                        Math.abs(player.position.x - ref.position.x) < tileSize / 2;

                    if (!isPlayerOnThisLog) {
                        resetLogPosition(ref);
                    }
                }
            });
        }
    });
}