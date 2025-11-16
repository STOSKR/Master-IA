import * as THREE from "three";
import { player } from "./components/Player";

let animationFrame = 0;
let deathAnimationType = null;
let hitDirection = 1; // 1 = derecha (vuela hacia izquierda), -1 = izquierda (vuela hacia derecha)

export function playDeathAnimation(type, direction = 1) {
    deathAnimationType = type;
    animationFrame = 0;
    if (type === "hit") {
        hitDirection = direction;
    }
}

export function updateDeathAnimation() {
    if (!deathAnimationType) return;

    animationFrame++;

    if (deathAnimationType === "drown") {
        animateDrowning();
    } else if (deathAnimationType === "hit") {
        animateHit();
    }
}

function animateDrowning() {
    // El jugador se hunde en el agua
    const sinkSpeed = 0.5;
    const maxFrames = 60;

    if (animationFrame < maxFrames) {
        player.children[0].position.z -= sinkSpeed;

        // Rotación adicional para efecto de hundimiento
        player.children[0].rotation.x += 0.02;
        player.children[0].rotation.z += 0.03;

        // Crear burbujas ocasionalmente
        if (animationFrame % 5 === 0 && animationFrame < 40) {
            createBubble();
        }
    } else {
        deathAnimationType = null;
    }
}

function animateHit() {
    // El jugador sale volando dando vueltas cuando es atropellado
    const maxFrames = 70;

    if (animationFrame < 25) {
        // Fase 1: Vuela hacia arriba y en la dirección del impacto dando vueltas rápidas
        player.children[0].position.z += 2.5;
        player.children[0].position.x += 1.5 * hitDirection; // Vuela en la misma dirección del vehículo
        player.children[0].position.y -= 0.5;

        // Rotaciones múltiples para efecto de dar vueltas
        player.children[0].rotation.x += 0.25;
        player.children[0].rotation.y += 0.20 * hitDirection;
        player.children[0].rotation.z += 0.18 * hitDirection;
    } else if (animationFrame < maxFrames) {
        // Fase 2: Cae al suelo mientras sigue girando
        player.children[0].position.z -= 2;

        // Continuar moviéndose en la dirección del impacto
        player.children[0].position.x += 0.5 * hitDirection;

        // Continuar girando pero más lento
        player.children[0].rotation.x += 0.15;
        player.children[0].rotation.y += 0.10 * hitDirection;
        player.children[0].rotation.z += 0.08 * hitDirection;
    }

    if (animationFrame >= maxFrames) {
        deathAnimationType = null;
    }
}

function createBubble() {
    const bubble = new THREE.Mesh(
        new THREE.SphereGeometry(2, 6, 6),
        new THREE.MeshLambertMaterial({
            color: 0xadd8e6,
            transparent: true,
            opacity: 0.5,
            flatShading: true
        })
    );

    bubble.position.copy(player.position);
    bubble.position.z = player.children[0].position.z + 10;
    bubble.position.x += (Math.random() - 0.5) * 10;
    bubble.position.y += (Math.random() - 0.5) * 10;

    player.parent.add(bubble);

    // Animar la burbuja hacia arriba
    let bubbleFrame = 0;
    const bubbleInterval = setInterval(() => {
        bubbleFrame++;
        bubble.position.z += 1;
        bubble.scale.multiplyScalar(1.02);
        bubble.material.opacity -= 0.02;

        if (bubbleFrame > 30 || bubble.material.opacity <= 0) {
            clearInterval(bubbleInterval);
            player.parent.remove(bubble);
            bubble.geometry.dispose();
            bubble.material.dispose();
        }
    }, 16);
}

export function resetDeathAnimation() {
    deathAnimationType = null;
    animationFrame = 0;

    // Resetear posición y rotación del jugador que las animaciones pudieron modificar
    if (player && player.children[0]) {
        player.children[0].position.x = 0;
        player.children[0].position.y = 0;
        player.children[0].position.z = 0;
        player.children[0].rotation.x = 0;
        player.children[0].rotation.y = 0;
        player.children[0].rotation.z = 0;

        // Resetear también el modelo interno si existe
        if (player.children[0].children[0]) {
            player.children[0].children[0].position.z = 5; // Mantener la altura inicial del modelo
        }
    }
}
