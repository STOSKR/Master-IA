import { queueMove } from "./components/Player";
import { gameState } from "./gameState";

document
    .getElementById("forward")
    ?.addEventListener("click", () => {
        if (gameState.isActive) queueMove("forward");
    });

document
    .getElementById("backward")
    ?.addEventListener("click", () => {
        if (gameState.isActive) queueMove("backward");
    });

document
    .getElementById("left")
    ?.addEventListener("click", () => {
        if (gameState.isActive) queueMove("left");
    });

document
    .getElementById("right")
    ?.addEventListener("click", () => {
        if (gameState.isActive) queueMove("right");
    });

window.addEventListener("keyup", (event) => {
    if (!gameState.isActive) return; // Ignorar eventos del teclado si el juego no está activo

    if (event.key === "ArrowUp") {
        event.preventDefault(); // Avoid scrolling the page
        queueMove("forward");
    } else if (event.key === "ArrowDown") {
        event.preventDefault(); // Avoid scrolling the page
        queueMove("backward");
    } else if (event.key === "ArrowLeft") {
        event.preventDefault(); // Avoid scrolling the page
        queueMove("left");
    } else if (event.key === "ArrowRight") {
        event.preventDefault(); // Avoid scrolling the page
        queueMove("right");
    }
});