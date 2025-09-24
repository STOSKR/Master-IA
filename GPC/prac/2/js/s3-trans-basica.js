

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
  camera.position.set(5, 10, 20);

  cameraControls = new THREE.OrbitControls(camera, renderer.domElement);
  cameraControls.target.set(0, 0, 0);

  window.addEventListener('resize', updateAspectRatio);
}


function loadScene() {
  ancho = 5
  alto = 10
  caja1 = new THREE.Mesh(new THREE.BoxGeometry(ancho, alto, 0.1), new THREE.MeshNormalMaterial());
  scene.add(new THREE.AxesHelper(15));
  scene.add(caja1);

}


function updateAspectRatio() {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
}

var time = 0;
function update() {
  time += 0.01;
  // Cambios para actualizar la camara segun mvto del raton
  cameraControls.update();

  // Crear la matriz de rotación
  let Rz = new THREE.Matrix4();
  Rz.makeRotationZ(0);
  let Rx = new THREE.Matrix4();
  Rx.makeRotationX(0);
  let Ry = new THREE.Matrix4();
  Ry.makeRotationY(Math.sin(time) - 45);

  // Crear una matriz de traslación
  let T = new THREE.Matrix4();
  T.makeTranslation(ancho, 0, 0);

  let T2 = new THREE.Matrix4();
  T2.makeTranslation(0.5 * ancho, 0.5 * alto, 0);

  // Combinar todas las transformaciones: T * Rx * Rz
  let M = new THREE.Matrix4();

  M.multiply(T);
  M.multiply(Rx);
  M.multiply(Rz);

  M.multiply(Ry);
  M.multiply(T2);
  // M = T * Rx * Rz

  // Aplicar la transformación  al objeto
  caja1.matrix.identity();  // Limpiar la matriz actual
  caja1.applyMatrix4(M);    // Aplicar la matriz de transformación combinada
  caja1.matrixAutoUpdate = false;  // Desactivar la actualización automática de la matriz


}

function render() {
  requestAnimationFrame(render);
  update();
  renderer.render(scene, camera);
}