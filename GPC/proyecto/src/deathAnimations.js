import * as THREE from "three";
import { player } from "./components/Player";

let animationFrame = 0;
let deathAnimationType = null;

export function playDeathAnimation(type) {
    deathAnimationType = type;
    animationFrame = 0;
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
    // El jugador vuela por el aire cuando es atropellado
    const maxFrames = 60;

    if (animationFrame < 20) {
        // Fase 1: Vuela hacia arriba y hacia atrás
        player.children[0].position.z += 2;
        player.children[0].position.x -= 1;
        player.children[0].rotation.x += 0.15;
        player.children[0].rotation.y += 0.1;
    } else if (animationFrame < maxFrames) {
        // Fase 2: Cae al suelo
        player.children[0].position.z -= 1.5;
        player.children[0].rotation.x += 0.1;
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
}
