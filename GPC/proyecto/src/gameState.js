// Estado global del juego
export const gameState = {
    isActive: true
};

export function setGameActive(active) {
    gameState.isActive = active;
}
