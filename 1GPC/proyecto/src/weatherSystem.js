import * as THREE from "three";

class WeatherSystem {
    constructor(scene) {
        this.scene = scene;
        this.rainParticles = [];
        this.isRaining = false;
        this.rainIntensity = 0;
        this.targetIntensity = 0;
        this.rainGroup = new THREE.Group();
        scene.add(this.rainGroup);
    }

    // Iniciar lluvia
    startRain(intensity = 0.5) {
        this.targetIntensity = Math.min(1, Math.max(0, intensity));
        this.isRaining = true;
    }

    // Detener lluvia
    stopRain() {
        this.targetIntensity = 0;
        setTimeout(() => {
            this.isRaining = false;
        }, 2000);
    }

    // Alternar lluvia
    toggleRain() {
        if (this.isRaining && this.targetIntensity > 0) {
            this.stopRain();
            return false;
        } else {
            this.startRain(0.6);
            return true;
        }
    }

    // Crear gotas de lluvia
    createRainDrops(playerPosition, count = 200) {
        const geometry = new THREE.BoxGeometry(1, 1, 8);

        for (let i = 0; i < count; i++) {
            const material = new THREE.MeshLambertMaterial({
                color: 0xaaddff,
                transparent: true,
                opacity: 0.8,
                flatShading: true
            });

            const drop = new THREE.Mesh(geometry, material);

            drop.position.x = playerPosition.x + (Math.random() - 0.5) * 800;
            drop.position.y = playerPosition.y + (Math.random() - 0.5) * 800;
            drop.position.z = 100 + Math.random() * 100;

            drop.userData.velocity = -5 - Math.random() * 3;
            drop.userData.startZ = drop.position.z;

            this.rainGroup.add(drop);
            this.rainParticles.push(drop);
        }
    }

    // Actualizar clima
    update(playerPosition) {
        // Suavizar transición de intensidad
        if (this.rainIntensity < this.targetIntensity) {
            this.rainIntensity = Math.min(
                this.targetIntensity,
                this.rainIntensity + 0.01
            );
        } else if (this.rainIntensity > this.targetIntensity) {
            this.rainIntensity = Math.max(
                this.targetIntensity,
                this.rainIntensity - 0.01
            );
        }

        // Gestionar cantidad de gotas
        if (this.isRaining || this.rainIntensity > 0) {
            const targetCount = Math.floor(500 * this.rainIntensity);

            // Añadir gotas si hace falta
            if (this.rainParticles.length < targetCount) {
                this.createRainDrops(playerPosition, targetCount - this.rainParticles.length);
            }

            // Actualizar gotas existentes
            for (let i = this.rainParticles.length - 1; i >= 0; i--) {
                const drop = this.rainParticles[i];

                drop.position.z += drop.userData.velocity * this.rainIntensity;

                // Ajustar opacidad basada en la intensidad de la lluvia
                drop.material.opacity = 0.8 * this.rainIntensity;

                // Resetear gota si toca el suelo
                if (drop.position.z < 0) {
                    if (this.rainIntensity > 0.1) {
                        drop.position.z = drop.userData.startZ;
                        drop.position.x = playerPosition.x + (Math.random() - 0.5) * 800;
                        drop.position.y = playerPosition.y + (Math.random() - 0.5) * 800;
                    } else {
                        // Remover gota si ya no llueve
                        this.rainGroup.remove(drop);
                        drop.geometry.dispose();
                        drop.material.dispose();
                        this.rainParticles.splice(i, 1);
                    }
                }
            }
        }
    }

    // Limpiar sistema de clima
    clear() {
        this.rainParticles.forEach(drop => {
            this.rainGroup.remove(drop);
            drop.geometry.dispose();
            drop.material.dispose();
        });
        this.rainParticles = [];
        this.scene.remove(this.rainGroup);
    }
}

export default WeatherSystem;
