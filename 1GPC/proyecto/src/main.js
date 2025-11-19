import * as THREE from "three";
import Stats from 'three/examples/jsm/libs/stats.module.js';
import { Renderer } from "./components/Renderer";
import { Camera } from "./components/Camera";
import { DirectionalLight } from "./components/DirectionalLight";
import { createPlayer, player, initializePlayer } from "./components/Player";
import { map, initializeMap } from "./components/Map";
import { animateVehicles } from "./animateVehicles";
import { animatePlayer, setParticleSystem } from "./animatePlayer";
import { hitTest, clearDeathTimeout } from "./hitTest";
import { setGameActive } from "./gameState";
import { updateDeathAnimation, resetDeathAnimation } from "./deathAnimations";
import ParticleSystem from "./particleSystem";
import WeatherSystem from "./weatherSystem";
import "./style.css";
import "./collectUserInput";

async function startGame() {
  // Manejar pantalla de inicio
  const startScreen = document.getElementById("start-screen");
  const startButton = document.getElementById("start-button");
  let gameStarted = false;

  function hideStartScreen() {
    if (startScreen) {
      startScreen.classList.add("hidden");
      gameStarted = true;
      initializeGame();
    }
  }

  // Click en el botón
  if (startButton) {
    startButton.addEventListener("click", hideStartScreen);
  }

  // Presionar Espacio
  window.addEventListener("keydown", (event) => {
    if (!gameStarted && event.code === "Space") {
      event.preventDefault();
      hideStartScreen();
    }
  });

  const stats = new Stats();
  stats.dom.style.position = 'absolute';
  stats.dom.style.top = '80px';
  stats.dom.style.left = '20px';
  document.body.appendChild(stats.dom);

  const scene = new THREE.Scene();

  // Skybox con gradiente de cielo
  const skyColor = new THREE.Color(0x87ceeb); // Celeste claro
  const horizonColor = new THREE.Color(0xffd89b); // Amarillo/naranja horizonte
  scene.background = skyColor;
  scene.fog = new THREE.Fog(horizonColor, 600, 1000); // Niebla más lejana

  await createPlayer();
  scene.add(player);
  scene.add(map);

  // Luz ambiental más cálida y suave
  const ambientLight = new THREE.AmbientLight(0xfff8dc, 0.6); // Tono cálido
  scene.add(ambientLight);

  const dirLight = DirectionalLight();
  dirLight.target = player;
  player.add(dirLight);

  // Luz hemisférica para simular luz del cielo
  const hemiLight = new THREE.HemisphereLight(0x87ceeb, 0xbaf455, 0.4);
  scene.add(hemiLight);

  // Sistemas de efectos
  const particleSystem = new ParticleSystem(scene);
  const weatherSystem = new WeatherSystem(scene);

  // Conectar el sistema de partículas con animatePlayer
  setParticleSystem(particleSystem);

  // Control manual de lluvia con botón y tecla F
  const rainToggleButton = document.getElementById('rain-toggle');

  function toggleRain() {
    const isRaining = weatherSystem.toggleRain();
    if (rainToggleButton) {
      if (isRaining) {
        rainToggleButton.classList.add('active');
      } else {
        rainToggleButton.classList.remove('active');
      }
    }
  }

  // Click en el botón
  if (rainToggleButton) {
    rainToggleButton.addEventListener('click', toggleRain);
  }

  // Tecla F para alternar lluvia
  window.addEventListener('keydown', (event) => {
    if (event.key.toLowerCase() === 'f') {
      event.preventDefault();
      toggleRain();
    }
  });

  const mainCamera = Camera();

  // --- CÁMARA DEL MINIMAPA (AJUSTADA) ---
  // 1. AJUSTA EL TAMAÑO DEL CUADRADO EN PANTALLA
  const minimapSize = 200; // Más pequeño

  const minimapCamera = new THREE.OrthographicCamera(
    window.innerWidth / -2,
    window.innerWidth / 2,
    window.innerHeight / 2,
    window.innerHeight / -2,
    1,
    1000
  );
  minimapCamera.up.set(0, 0, 1);
  // 2. AJUSTA EL NIVEL DE ZOOM
  minimapCamera.zoom = 3; // Mucho más zoom para que el contenido se vea más grande
  scene.add(minimapCamera);
  // --- FIN CÁMARA MINIMAPA ---

  const renderer = Renderer();
  renderer.setAnimationLoop(animate);

  const scoreDOM = document.getElementById("score");
  const resultDOM = document.getElementById("result-container");

  document.querySelector("#retry")?.addEventListener("click", initializeGame);

  window.addEventListener("keyup", (event) => {
    if (event.key.toLowerCase() === "r") {
      const resultDOM = document.getElementById("result-container");
      if (resultDOM && resultDOM.style.visibility === "visible") {
        initializeGame();
      }
    }
  });

  // No inicializar el juego automáticamente, esperar a que se presione el botón
  // initializeGame();

  function initializeGame() {
    clearDeathTimeout(); // Limpiar timeouts pendientes
    resetDeathAnimation(); // Resetear animaciones de muerte primero
    initializePlayer();
    initializeMap();
    setGameActive(true);
    if (scoreDOM) scoreDOM.innerText = "0";
    if (resultDOM) resultDOM.style.visibility = "hidden";
  }

  function handleResize() {
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Actualiza la cámara principal
    const size = 300;
    const viewRatio = window.innerWidth / window.innerHeight;
    const width = viewRatio < 1 ? size : size * viewRatio;
    const height = viewRatio < 1 ? size / viewRatio : size;
    mainCamera.left = width / -2;
    mainCamera.right = width / 2;
    mainCamera.top = height / 2;
    mainCamera.bottom = height / -2;
    mainCamera.updateProjectionMatrix();

    // Actualiza la cámara del minimapa para que no se deforme
    minimapCamera.left = window.innerWidth / -2;
    minimapCamera.right = window.innerWidth / 2;
    minimapCamera.top = window.innerHeight / 2;
    minimapCamera.bottom = window.innerHeight / -2;
    minimapCamera.updateProjectionMatrix();
  }
  window.addEventListener('resize', handleResize);
  handleResize();

  function animate() {
    if (!player) return;
    stats.update();

    // --- LÓGICA DE MOVIMIENTO DE CÁMARAS ---
    // 3. SE RESTAURA EL MOVIMIENTO DE LA CÁMARA PRINCIPAL
    mainCamera.position.x = player.position.x + 300;
    mainCamera.position.y = player.position.y - 300;
    mainCamera.lookAt(player.position);

    // Actualiza la cámara del minimapa para que siga al jugador desde arriba
    minimapCamera.position.set(player.position.x, player.position.y, 500);
    // --- FIN LÓGICA DE CÁMARAS ---

    animateVehicles();
    animatePlayer();
    updateDeathAnimation();
    hitTest();

    // Actualizar sistemas de efectos
    particleSystem.update();
    weatherSystem.update(player.position);

    // --- LÓGICA DE RENDERIZADO ---
    renderer.setScissorTest(true);

    // Renderiza la escena principal
    renderer.setScissor(0, 0, window.innerWidth, window.innerHeight);
    renderer.setViewport(0, 0, window.innerWidth, window.innerHeight);
    renderer.render(scene, mainCamera);

    // Renderiza el minimapa
    const margin = 10;
    renderer.setScissor(
      window.innerWidth - minimapSize - margin,
      window.innerHeight - minimapSize - margin,
      minimapSize,
      minimapSize
    );
    renderer.setViewport(
      window.innerWidth - minimapSize - margin,
      window.innerHeight - minimapSize - margin,
      minimapSize,
      minimapSize
    );
    renderer.render(scene, minimapCamera);

    renderer.setScissorTest(false);
  }
}

startGame();