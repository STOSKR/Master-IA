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
            const fadeZoneSize = tileSize * 1.5; // Zona donde se desvanecen

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

                // Calcular opacidad basada en la distancia a los bordes
                let opacity = 1;

                if (rowData.direction) {
                    // Vehículo yendo hacia la derecha
                    const distanceToEdge = endOfRow - ref.position.x;
                    if (distanceToEdge < fadeZoneSize) {
                        opacity = distanceToEdge / fadeZoneSize;
                    }
                    // Aparecer gradualmente desde el inicio
                    const distanceFromStart = ref.position.x - beginningOfRow;
                    if (distanceFromStart < fadeZoneSize) {
                        opacity = Math.min(opacity, distanceFromStart / fadeZoneSize);
                    }
                } else {
                    // Vehículo yendo hacia la izquierda
                    const distanceToEdge = ref.position.x - beginningOfRow;
                    if (distanceToEdge < fadeZoneSize) {
                        opacity = distanceToEdge / fadeZoneSize;
                    }
                    // Aparecer gradualmente desde el final
                    const distanceFromEnd = endOfRow - ref.position.x;
                    if (distanceFromEnd < fadeZoneSize) {
                        opacity = Math.min(opacity, distanceFromEnd / fadeZoneSize);
                    }
                }

                // Aplicar opacidad a todos los materiales del vehículo
                ref.traverse((child) => {
                    if (child.isMesh && child.material) {
                        if (!child.material.transparent) {
                            child.material.transparent = true;
                            child.userData.originalOpacity = child.material.opacity;
                        }
                        child.material.opacity = (child.userData.originalOpacity || 1) * opacity;
                    }
                });

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