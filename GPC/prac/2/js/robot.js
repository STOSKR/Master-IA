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
    robot.add(brazo);
    /*
        // Antebrazo
        let antebrazo = new THREE.Object3D();
    
        let disco = new THREE.Mesh(new THREE.CylinderGeometry(22, 22, 6, 32), new THREE.MeshBasicMaterial({ color: 0xffff00 }));
        disco.position.y = 80;
        antebrazo.add(disco);
    
        let nerviosMaterial = new THREE.MeshBasicMaterial({ color: 0xff00ff });
        for (let i = 0; i < 4; i++) {
            let nervio = new THREE.Mesh(new THREE.BoxGeometry(4, 80, 4), nerviosMaterial);
            nervio.position.set(15 * Math.cos((i * Math.PI) / 2), 120, 15 * Math.sin((i * Math.PI) / 2));
            antebrazo.add(nervio);
        }
    
        let mano = new THREE.Mesh(new THREE.CylinderGeometry(15, 15, 40, 32), new THREE.MeshBasicMaterial({ color: 0x00ffff }));
        mano.position.y = 160;
        antebrazo.add(mano);
    
        scene.add(antebrazo);
    
        // Pinza
        let clawMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
        let claw1 = new THREE.Mesh(new THREE.BoxGeometry(20, 38, 4), clawMaterial);
        claw1.position.set(10, 195, 0);
        scene.add(claw1);
    
        let claw2 = claw1.clone();
        claw2.position.set(-10, 195, 0);
        */
    scene.add(robot);
    // scene.add(claw2);
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