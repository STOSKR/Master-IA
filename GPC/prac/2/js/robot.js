// Variables globales
var renderer, scene, camera;
var cameraControls;
var angulo = -0.01;

// Inicialización
init();
loadScene();
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
    let robot = new THREE.Object3D();

    // Base
    let baseMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000, wireframe: true });
    let base = new THREE.Mesh(new THREE.CylinderGeometry(50, 50, 15, 32), baseMaterial);
    base.position.y = 0;
    robot.add(base);

    // Brazo
    let brazo = new THREE.Object3D();

    let esparrago = new THREE.Mesh(new THREE.CylinderGeometry(20, 20, 18, 32), new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true }));
    esparrago.rotateOnAxis(new THREE.Vector3(0, 0, 1), Math.PI / 2);
    brazo.add(esparrago);

    let eje = new THREE.Mesh(new THREE.BoxGeometry(18, 120, 12), new THREE.MeshBasicMaterial({ color: 0x0000ff, wireframe: true }));
    eje.position.y = 60;
    brazo.add(eje);

    let rotula = new THREE.Mesh(new THREE.SphereGeometry(20, 32, 32), new THREE.MeshBasicMaterial({ color: 0xffff00, wireframe: true }));
    rotula.position.y = 120;
    brazo.add(rotula);

    // Antebrazo
    let antebrazo = new THREE.Object3D();
    antebrazo.position.y = 120;

    // Disco
    let disco = new THREE.Mesh(new THREE.CylinderGeometry(22, 22, 6, 32), new THREE.MeshBasicMaterial({ color: 0x00ffff, wireframe: true }));
    antebrazo.add(disco);

    // Nervios
    let nerviosMaterial = new THREE.MeshBasicMaterial({ color: 0xff00ff, wireframe: true });
    let distanciaNervios = 5;
    let posicionesNervios = [
        [distanciaNervios, 40, distanciaNervios],   // Nervio 1
        [-distanciaNervios, 40, distanciaNervios],  // Nervio 2
        [-distanciaNervios, 40, -distanciaNervios], // Nervio 3
        [distanciaNervios, 40, -distanciaNervios]   // Nervio 4
    ];
    for (let i = 0; i < posicionesNervios.length; i++) {
        let nervio = new THREE.Mesh(new THREE.BoxGeometry(4, 80, 4), nerviosMaterial);
        nervio.position.set(posicionesNervios[i][0], posicionesNervios[i][1], posicionesNervios[i][2]);
        antebrazo.add(nervio);
    }

    // Mano
    let manoObjeto = new THREE.Object3D();
    let mano = new THREE.Mesh(new THREE.CylinderGeometry(15, 15, 40, 32), new THREE.MeshBasicMaterial({ color: 0xff0000, wireframe: true }));
    mano.position.y = 80;
    mano.rotateOnAxis(new THREE.Vector3(0, 0, 1), Math.PI / 2);
    manoObjeto.add(mano);

    // Pinzas
    let pinzaMaterial = new THREE.MeshBasicMaterial({ color: 0xaaff00, wireframe: true });
    let pinza1 = new THREE.Mesh(new THREE.BoxGeometry(20, 19, 4), pinzaMaterial);
    pinza1.position.set(10, 80, 15);
    pinza1.rotateOnAxis(new THREE.Vector3(0, 1, 0), Math.PI / 2);

    manoObjeto.add(pinza1);


    // Dedo
    let dedoGeometry = new THREE.BufferGeometry();

    // Definir los vértices del dedo
    const verticesDedo = new Float32Array([
        // Parte trasera
        -2, 20, 0,  // Vértice 0
        2, 20, 0,  // Vértice 1
        2, 0, 0,   // Vértice 2
        -2, 0, 0,   // Vértice 3

        // Parte delantera
        -1, 15, 19, // Vértice 6
        1, 15, 19,  // Vértice 7
        1, 5, 19,   // Vértice 5
        -1, 5, 19,  // Vértice 4
    ]);

    // Definir los índices para las caras
    const indicesDedo = [
        // Cara trasera
        0, 1, 2,
        0, 2, 3,

        // Cara delantera
        4, 7, 6,
        6, 5, 4,

        // Conectar trasera y delantera
        0, 3, 7,    //izquierda
        7, 4, 0,    //izquierda
        0, 4, 1,    //superior
        1, 4, 5,    //superior
        2, 1, 6,    //derecha
        1, 5, 6,    //derecha
        3, 2, 7,    //inferior
        6, 3, 2,    //inferior
    ];

    // Añadir los vértices y los índices al objeto de geometría
    dedoGeometry.setAttribute('position', new THREE.BufferAttribute(verticesDedo, 3));
    dedoGeometry.setIndex(indicesDedo);

    // Calcular las normales para iluminación correcta
    dedoGeometry.computeVertexNormals();

    // Crear el material y el mesh del dedo
    let dedoMaterial = new THREE.MeshNormalMaterial();
    let dedo = new THREE.Mesh(dedoGeometry, dedoMaterial);

    // Posicionar el dedo y añadirlo a la pinza
    dedo.position.set(10, 70, 25); // Ajustar según la posición de la pinza
    manoObjeto.add(dedo);


    antebrazo.add(manoObjeto);
    brazo.add(antebrazo);
    robot.add(brazo);
    scene.add(robot);
}

function updateAspectRatio() {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
}

function update() {
    cameraControls.update();
}

function render() {
    requestAnimationFrame(render);
    update();
    renderer.render(scene, camera);
}