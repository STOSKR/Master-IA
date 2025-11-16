import * as THREE from "three";

export function DirectionalLight() {
    // Luz más cálida y suave (simulando luz del sol)
    const dirLight = new THREE.DirectionalLight(0xfff4e6, 0.8);
    dirLight.position.set(-100, -100, 200);
    dirLight.up.set(0, 0, 1);
    dirLight.castShadow = true;

    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;

    // Sombras más suaves
    dirLight.shadow.bias = -0.001;
    dirLight.shadow.radius = 2;

    dirLight.shadow.camera.up.set(0, 0, 1);
    dirLight.shadow.camera.left = -400;
    dirLight.shadow.camera.right = 400;
    dirLight.shadow.camera.top = 400;
    dirLight.shadow.camera.bottom = -400;
    dirLight.shadow.camera.near = 50;
    dirLight.shadow.camera.far = 400;

    return dirLight;
}