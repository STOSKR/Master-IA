

// Variables globales que van siempre
var renderer, scene, camera;
var cameraControls;
var angulo = -0.01;

// 1-inicializa 
init();
// 2-Crea una escena
loadScene();
// 3-renderiza
render();

function init() {
  renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(new THREE.Color(0xFFFFFF));
  document.getElementById('container').appendChild(renderer.domElement);

  scene = new THREE.Scene();

  var aspectRatio = window.innerWidth / window.innerHeight;
  camera = new THREE.PerspectiveCamera(50, aspectRatio, 0.1, 100);
  camera.position.set(1, 1.5, 2);

  cameraControls = new THREE.OrbitControls(camera, renderer.domElement);
  cameraControls.target.set(0, 0, 0);

  window.addEventListener('resize', updateAspectRatio);
}


function loadScene() {
  // Añade el objeto grafico a la escena
  //let material = new THREE.MeshBasicMaterial({ color: 0x00ff00 }); // Verde

  /*let material = new THREE.MeshNormalMaterial();
  let cubo = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), material);
  scene.add(cubo);  */

  escalera = new THREE.Object3D();
  let material = new THREE.MeshNormalMaterial();

  for (let i = 0; i < 10; i++) {
    let escalon = new THREE.Mesh(new THREE.BoxGeometry(1, 0.1, 0.2), material);
    escalon.position.set(0, i * 0.05, i * 0.1);
    escalera.add(escalon);
  }

  /*planta = new THREE.Mesh(new THREE.BoxGeometry(2, 0.01, 2), material);
  planta.position.set(0, -0.05, -0.05);
  
  */
  let geometriaPiso = new THREE.PlaneGeometry(10, 10, 10, 10);
  let piso = new THREE.Mesh(geometriaPiso, material);
  piso.rotateOnAxis(new THREE.Vector3(1, 0, 0), -Math.PI / 2);
  scene.add(piso);
  /*
  escalera.add(planta);
  */
  scene.add(escalera);
}


function updateAspectRatio() {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
}

function update() {
  // Cambios para actualizar la camara segun mvto del raton
  cameraControls.update();
}

function render() {
  requestAnimationFrame(render);
  update();
  renderer.render(scene, camera);
}