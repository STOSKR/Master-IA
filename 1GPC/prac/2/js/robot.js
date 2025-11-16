// Variables globales
var renderer, scene, camera;
var cameraControls;

// Objetos del Robot para manipulación
var robot, base, brazo, antebrazo, manoObjeto;
var pinzaDerecho, pinzaIzquierdo;
var dedoDerecho, dedoIzquierdo;

// Array para almacenar materiales
var materiales = [];

// Inicialización
init();
loadScene();
setupEventListeners();
render();

function init() {
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(new THREE.Color(0xFFFFFF));
    document.getElementById('container').appendChild(renderer.domElement);

    scene = new THREE.Scene();

    var aspectRatio = window.innerWidth / window.innerHeight;
    camera = new THREE.PerspectiveCamera(75, aspectRatio, 0.1, 1000);
    camera.position.set(0, 150, 300);

    cameraControls = new THREE.OrbitControls(camera, renderer.domElement);
    cameraControls.target.set(0, 0, 0);

    window.addEventListener('resize', updateAspectRatio);
}

function loadScene() {
    // Suelo
    let groundMaterial = new THREE.MeshBasicMaterial({ color: 0x888888, side: THREE.DoubleSide });
    let ground = new THREE.Mesh(new THREE.PlaneGeometry(1000, 1000), groundMaterial);
    ground.position.y = -7.5;
    ground.rotation.x = Math.PI / 2;
    scene.add(ground);

    // Robot
    robot = new THREE.Object3D();

    // Base
    let baseMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000, wireframe: true });
    materiales.push(baseMaterial);
    base = new THREE.Mesh(new THREE.CylinderGeometry(50, 50, 15, 32), baseMaterial);
    base.position.y = 0;

    // Brazo
    brazo = new THREE.Object3D();
    let esparragoMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
    materiales.push(esparragoMaterial);
    let esparrago = new THREE.Mesh(new THREE.CylinderGeometry(20, 20, 18, 32), esparragoMaterial);
    esparrago.rotateOnAxis(new THREE.Vector3(0, 0, 1), Math.PI / 2);
    brazo.add(esparrago);
    base.add(brazo);
    robot.add(base);

    let ejeMaterial = new THREE.MeshBasicMaterial({ color: 0x0000ff, wireframe: true });
    materiales.push(ejeMaterial);
    let eje = new THREE.Mesh(new THREE.BoxGeometry(18, 120, 12), ejeMaterial);
    eje.position.y = 60;
    brazo.add(eje);

    let rotulaMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00, wireframe: true });
    materiales.push(rotulaMaterial);
    let rotula = new THREE.Mesh(new THREE.SphereGeometry(20, 32, 32), rotulaMaterial);
    rotula.position.y = 120;
    brazo.add(rotula);

    // Antebrazo
    antebrazo = new THREE.Object3D();
    antebrazo.position.y = 120;

    let discoMaterial = new THREE.MeshBasicMaterial({ color: 0x00ffff, wireframe: true });
    materiales.push(discoMaterial);
    let disco = new THREE.Mesh(new THREE.CylinderGeometry(22, 22, 6, 32), discoMaterial);
    antebrazo.add(disco);

    let nerviosMaterial = new THREE.MeshBasicMaterial({ color: 0xff00ff, wireframe: true });
    materiales.push(nerviosMaterial);
    let distanciaNervios = 5;
    let posicionesNervios = [
        [distanciaNervios, 40, distanciaNervios],
        [-distanciaNervios, 40, distanciaNervios],
        [-distanciaNervios, 40, -distanciaNervios],
        [distanciaNervios, 40, -distanciaNervios]
    ];
    for (let i = 0; i < posicionesNervios.length; i++) {
        let nervio = new THREE.Mesh(new THREE.BoxGeometry(4, 80, 4), nerviosMaterial);
        nervio.position.set(posicionesNervios[i][0], posicionesNervios[i][1], posicionesNervios[i][2]);
        antebrazo.add(nervio);
    }

    // Mano
    manoObjeto = new THREE.Object3D();
    manoObjeto.position.y = 80; // Posicionar la mano al final de los nervios

    let manoMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000, wireframe: true });
    materiales.push(manoMaterial);
    let mano = new THREE.Mesh(new THREE.CylinderGeometry(15, 15, 40, 32), manoMaterial);
    mano.rotateOnAxis(new THREE.Vector3(0, 0, 1), Math.PI / 2);
    manoObjeto.add(mano);

    // Pinzas
    let pinzaMaterial = new THREE.MeshBasicMaterial({ color: 0xaaff00, wireframe: true });
    materiales.push(pinzaMaterial);
    pinzaDerecho = new THREE.Mesh(new THREE.BoxGeometry(20, 19, 4), pinzaMaterial);
    pinzaDerecho.position.set(10, 0, 15);
    pinzaDerecho.rotateOnAxis(new THREE.Vector3(0, 1, 0), Math.PI / 2);
    manoObjeto.add(pinzaDerecho);

    let dedoGeometry = new THREE.BufferGeometry();
    const verticesDedo = new Float32Array([-2, 20, 0, 2, 20, 0, 2, 0, 0, -2, 0, 0, -1, 15, 19, 1, 15, 19, 1, 5, 19, -1, 5, 19]);
    const indicesDedo = [0, 1, 2, 0, 2, 3, 4, 7, 6, 6, 5, 4, 0, 3, 7, 7, 4, 0, 0, 4, 1, 1, 4, 5, 2, 1, 6, 1, 5, 6, 3, 2, 7, 6, 3, 2];
    dedoGeometry.setAttribute('position', new THREE.BufferAttribute(verticesDedo, 3));
    dedoGeometry.setIndex(indicesDedo);
    dedoGeometry.computeVertexNormals();
    let dedoMaterial = new THREE.MeshNormalMaterial();
    materiales.push(dedoMaterial);
    dedoDerecho = new THREE.Mesh(dedoGeometry, dedoMaterial);
    dedoDerecho.position.set(10, -10, 25);
    manoObjeto.add(dedoDerecho);

    pinzaIzquierdo = new THREE.Mesh(new THREE.BoxGeometry(20, 19, 4), pinzaMaterial);
    pinzaIzquierdo.position.set(-10, 0, 15);
    pinzaIzquierdo.rotateOnAxis(new THREE.Vector3(0, 1, 0), Math.PI / 2);
    manoObjeto.add(pinzaIzquierdo);

    dedoIzquierdo = new THREE.Mesh(dedoGeometry, dedoMaterial);
    dedoIzquierdo.position.set(-10, -10, 25);
    manoObjeto.add(dedoIzquierdo);

    antebrazo.add(manoObjeto);
    brazo.add(antebrazo);
    robot.add(brazo);
    base.add(robot);
    scene.add(base);
}

function setupEventListeners() {
    // 1. Movimiento del robot con flechas
    document.addEventListener("keydown", onDocumentKeyDown, false);

    // 2. Giro de la base
    document.getElementById('giroBase').addEventListener('input', (event) => {
        base.rotation.y = THREE.MathUtils.degToRad(event.target.value);
    });

    // 3. Giro del brazo
    document.getElementById('giroBrazo').addEventListener('input', (event) => {
        brazo.rotation.x = THREE.MathUtils.degToRad(event.target.value);
    });

    // 4. Giro del antebrazo en Y
    document.getElementById('giroAntebrazoY').addEventListener('input', (event) => {
        antebrazo.rotation.y = THREE.MathUtils.degToRad(event.target.value);
    });

    // 5. Giro del antebrazo en X
    document.getElementById('giroAntebrazoZ').addEventListener('input', (event) => {
        antebrazo.rotation.x = THREE.MathUtils.degToRad(event.target.value);
    });

    // 6. Rotación de la pinza
    document.getElementById('rotacionPinza').addEventListener('input', (event) => {
        manoObjeto.rotation.x = - THREE.MathUtils.degToRad(event.target.value);
    });

    // 7. Apertura/Cierre de la pinza
    document.getElementById('aperturaPinza').addEventListener('input', (event) => {
        const valor = parseFloat(event.target.value);
        pinzaDerecho.position.x = valor;
        dedoDerecho.position.x = valor;
        pinzaIzquierdo.position.x = -valor;
        dedoIzquierdo.position.x = -valor;
    });

    // 8. Checkbox para modo alámbrico
    document.getElementById('wireframe').addEventListener('change', (event) => {
        const esAlambrico = event.target.checked;
        materiales.forEach(material => {
            // MeshNormalMaterial no tiene propiedad wireframe, así que la evitamos
            if ('wireframe' in material) {
                material.wireframe = esAlambrico;
            }
        });
    });

    // 9. Botón para animación
    document.getElementById('animacionBtn').addEventListener('click', iniciarAnimacion);
}

function onDocumentKeyDown(event) {
    const velocidad = 5;
    switch (event.keyCode) {
        case 37: // Flecha izquierda
            base.position.x -= velocidad;
            break;
        case 38: // Flecha arriba
            base.position.z -= velocidad;
            break;
        case 39: // Flecha derecha
            base.position.x += velocidad;
            break;
        case 40: // Flecha abajo
            base.position.z += velocidad;
            break;
    }
}

function iniciarAnimacion() {
    const duracion = 2000; // 2 segundos
    const easeType = TWEEN.Easing.Quadratic.InOut;

    // Reiniciar posiciones/rotaciones para una animación consistente
    TWEEN.removeAll();

    // Animación de giro de la base
    new TWEEN.Tween(base.rotation)
        .to({ y: THREE.MathUtils.degToRad(180) }, duracion)
        .easing(easeType).yoyo(true).repeat(1).start();

    // Animación del brazo
    new TWEEN.Tween(brazo.rotation)
        .to({ z: THREE.MathUtils.degToRad(45) }, duracion / 2)
        .easing(easeType).yoyo(true).repeat(1).start();

    // Animación del antebrazo
    new TWEEN.Tween(antebrazo.rotation)
        .to({ z: THREE.MathUtils.degToRad(90) }, duracion)
        .easing(easeType).yoyo(true).repeat(1).start();

    // Animación de la rotación de la mano
    new TWEEN.Tween(manoObjeto.rotation)
        .to({ z: THREE.MathUtils.degToRad(220) }, duracion)
        .easing(easeType).yoyo(true).repeat(1).start();

    // Animación de la pinza (apertura y cierre)
    const pinzaPos = { x: pinzaDerecho.position.x };
    new TWEEN.Tween(pinzaPos)
        .to({ x: 0 }, duracion / 2)
        .onUpdate(() => {
            pinzaDerecho.position.x = pinzaPos.x;
            dedoDerecho.position.x = pinzaPos.x;
            pinzaIzquierdo.position.x = -pinzaPos.x;
            dedoIzquierdo.position.x = -pinzaPos.x;
        })
        .easing(TWEEN.Easing.Bounce.Out).yoyo(true).repeat(1).start();
}

function updateAspectRatio() {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
}

function update() {
    cameraControls.update();
    TWEEN.update(); // Actualiza las animaciones
}

function render() {
    requestAnimationFrame(render);
    update();
    renderer.render(scene, camera);
}