import * as THREE from "three";
import { minTileIndex, maxTileIndex } from "../constants";

export function generateRows(amount) {
    const rows = [];
    let lastRowType = null;
    let lastWaterDirection = null; // true = derecha, false = izquierda

    for (let i = 0; i < amount; i++) {
        let allowedTypes = ["car", "truck", "forest", "water"];

        // --- APLICACIÓN DE REGLAS ---

        // Regla 1: Si la última fila fue una carretera, la siguiente NO PUEDE ser agua.
        // Forzamos un búfer de césped o permitimos otra carretera.
        if (lastRowType === 'car' || lastRowType === 'truck') {
            allowedTypes = ["car", "truck", "forest"];
        }

        // Regla 2: Si la última fila fue agua, la siguiente NO PUEDE ser una carretera.
        // Debe ser obligatoriamente césped o más agua.
        else if (lastRowType === 'water') {
            allowedTypes = ["forest", "water"];
        }

        const newType = randomElement(allowedTypes);
        let rowData;

        // --- LÓGICA DE GENERACIÓN BASADA EN EL TIPO ---

        if (newType === "water") {
            // Si generamos agua, le pasamos la dirección del último río para que la invierta.
            const waterGen = generateWaterLaneMetadata(lastWaterDirection);
            rowData = waterGen.metadata;
            lastWaterDirection = waterGen.newDirection; // Actualizamos la memoria de dirección.
        } else {
            // Si la nueva fila NO es agua, reiniciamos la memoria de dirección del río.
            lastWaterDirection = null;

            // Generación estándar para los otros tipos de fila.
            if (newType === "car") rowData = generateCarLaneMetadata();
            if (newType === "truck") rowData = generateTruckLaneMetadata();
            if (newType === "forest") rowData = generateForesMetadata();
        }

        rows.push(rowData);
        lastRowType = newType; // Actualizamos la memoria del tipo para la siguiente iteración.
    }
    return rows;
}

function randomElement(array) {
    return array[Math.floor(Math.random() * array.length)];
}

function generateForesMetadata() {
    const occupiedTiles = new Set();
    const trees = Array.from({ length: 4 }, () => {
        let tileIndex;
        do {
            tileIndex = THREE.MathUtils.randInt(minTileIndex, maxTileIndex);
        } while (occupiedTiles.has(tileIndex));
        occupiedTiles.add(tileIndex);

        const height = randomElement([20, 45, 60]);

        return { tileIndex, height };
    });

    return { type: "forest", trees };
}
function generateCarLaneMetadata() {
    const direction = randomElement([true, false]);
    const speed = randomElement([125, 156, 188]);

    const occupiedTiles = new Set();

    const vehicles = Array.from({ length: 3 }, () => {
        let initialTileIndex;
        do {
            initialTileIndex = THREE.MathUtils.randInt(
                minTileIndex,
                maxTileIndex
            );
        } while (occupiedTiles.has(initialTileIndex));
        occupiedTiles.add(initialTileIndex - 1);
        occupiedTiles.add(initialTileIndex);
        occupiedTiles.add(initialTileIndex + 1);

        const color = randomElement([0xa52523, 0xbdb638, 0x78b14b]);

        return { initialTileIndex, color };
    });

    return { type: "car", direction, speed, vehicles };
}
function generateTruckLaneMetadata() {
    const direction = randomElement([true, false]);
    const speed = randomElement([125, 156, 188]);

    const occupiedTiles = new Set();

    const vehicles = Array.from({ length: 2 }, () => {
        let initialTileIndex;
        do {
            initialTileIndex = THREE.MathUtils.randInt(
                minTileIndex,
                maxTileIndex
            );
        } while (occupiedTiles.has(initialTileIndex));
        occupiedTiles.add(initialTileIndex - 2);
        occupiedTiles.add(initialTileIndex - 1);
        occupiedTiles.add(initialTileIndex);
        occupiedTiles.add(initialTileIndex + 1);
        occupiedTiles.add(initialTileIndex + 2);

        const color = randomElement([0xa52523, 0xbdb638, 0x78b14b]);

        return { initialTileIndex, color };
    });

    return { type: "truck", direction, speed, vehicles };
}
function generateWaterLaneMetadata(lastDirection) {
    let newDirection;

    // Si hay una dirección anterior (no es el primer río del bloque), la invertimos.
    if (lastDirection !== null) {
        newDirection = !lastDirection;
    } else {
        // Si es el primer río, la dirección es aleatoria.
        newDirection = randomElement([true, false]);
    }

    const speed = randomElement([80, 100, 120]);
    const occupiedTiles = new Set();
    const vehicles = Array.from({ length: 2 }, () => {
        let initialTileIndex;
        do {
            initialTileIndex = THREE.MathUtils.randInt(minTileIndex, maxTileIndex);
        } while (
            occupiedTiles.has(initialTileIndex - 2) ||
            occupiedTiles.has(initialTileIndex - 1) ||
            occupiedTiles.has(initialTileIndex) ||
            occupiedTiles.has(initialTileIndex + 1) ||
            occupiedTiles.has(initialTileIndex + 2)
        );
        occupiedTiles.add(initialTileIndex - 2);
        occupiedTiles.add(initialTileIndex - 1);
        occupiedTiles.add(initialTileIndex);
        occupiedTiles.add(initialTileIndex + 1);
        occupiedTiles.add(initialTileIndex + 2);
        return { initialTileIndex };
    });

    return {
        metadata: { type: "water", direction: newDirection, speed, vehicles },
        newDirection: newDirection
    };
}