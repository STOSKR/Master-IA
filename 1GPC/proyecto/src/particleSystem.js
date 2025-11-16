import * as THREE from "three";

// Sistema de gestión de partículas
class ParticleSystem {
    constructor(scene) {
        this.scene = scene;
        this.particles = [];
    }

    // Crear partículas de polvo cuando el jugador aterriza
    createDustParticles(position) {
        const particleCount = 8;
        const geometry = new THREE.BoxGeometry(2, 2, 2);

        for (let i = 0; i < particleCount; i++) {
            const material = new THREE.MeshLambertMaterial({
                color: 0xd4c4a8,
                transparent: true,
                opacity: 0.6,
                flatShading: true
            });

            const particle = new THREE.Mesh(geometry, material);
            particle.position.copy(position);
            particle.position.x += (Math.random() - 0.5) * 10;
            particle.position.y += (Math.random() - 0.5) * 10;
            particle.position.z += Math.random() * 3;

            // Velocidad de la partícula
            particle.userData.velocity = {
                x: (Math.random() - 0.5) * 0.5,
                y: (Math.random() - 0.5) * 0.5,
                z: Math.random() * 0.3 + 0.2
            };

            particle.userData.life = 30; // frames de vida
            particle.userData.type = 'dust';

            this.scene.add(particle);
            this.particles.push(particle);
        }
    }

    // Crear salpicaduras de agua
    createWaterSplash(position) {
        const particleCount = 12;
        const geometry = new THREE.BoxGeometry(1.5, 1.5, 1.5);

        for (let i = 0; i < particleCount; i++) {
            const material = new THREE.MeshLambertMaterial({
                color: 0x6bb3f7,
                transparent: true,
                opacity: 0.7,
                flatShading: true
            });

            const particle = new THREE.Mesh(geometry, material);
            particle.position.copy(position);
            particle.position.x += (Math.random() - 0.5) * 8;
            particle.position.y += (Math.random() - 0.5) * 8;
            particle.position.z = 2;

            // Velocidad de la partícula
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 1.5 + 0.5;
            particle.userData.velocity = {
                x: Math.cos(angle) * speed,
                y: Math.sin(angle) * speed,
                z: Math.random() * 2 + 1
            };

            particle.userData.life = 40; // frames de vida
            particle.userData.type = 'water';

            this.scene.add(particle);
            this.particles.push(particle);
        }
    }

    // Crear humo del escape de vehículos
    createExhaustSmoke(position, direction) {
        const geometry = new THREE.BoxGeometry(3, 3, 3);
        const material = new THREE.MeshLambertMaterial({
            color: 0x888888,
            transparent: true,
            opacity: 0.4,
            flatShading: true
        });

        const particle = new THREE.Mesh(geometry, material);
        particle.position.copy(position);
        particle.position.z += 5;

        // Velocidad basada en la dirección del vehículo
        particle.userData.velocity = {
            x: -direction * 0.2,
            y: 0,
            z: 0.1
        };

        particle.userData.life = 50;
        particle.userData.type = 'smoke';
        particle.userData.scale = 1;

        this.scene.add(particle);
        this.particles.push(particle);
    }

    // Actualizar todas las partículas
    update() {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const particle = this.particles[i];

            // Actualizar posición
            particle.position.x += particle.userData.velocity.x;
            particle.position.y += particle.userData.velocity.y;
            particle.position.z += particle.userData.velocity.z;

            // Aplicar gravedad para agua y polvo
            if (particle.userData.type === 'water' || particle.userData.type === 'dust') {
                particle.userData.velocity.z -= 0.08; // Gravedad
            }

            // Expandir humo
            if (particle.userData.type === 'smoke') {
                particle.userData.scale += 0.02;
                particle.scale.set(
                    particle.userData.scale,
                    particle.userData.scale,
                    particle.userData.scale
                );
            }

            // Reducir vida y opacidad
            particle.userData.life--;
            particle.material.opacity *= 0.96;

            // Remover partículas muertas
            if (particle.userData.life <= 0 || particle.material.opacity < 0.01) {
                this.scene.remove(particle);
                particle.geometry.dispose();
                particle.material.dispose();
                this.particles.splice(i, 1);
            }
        }
    }

    // Limpiar todas las partículas
    clear() {
        this.particles.forEach(particle => {
            this.scene.remove(particle);
            particle.geometry.dispose();
            particle.material.dispose();
        });
        this.particles = [];
    }
}

export default ParticleSystem;
