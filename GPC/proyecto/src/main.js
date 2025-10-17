import * as THREE from "three";
import { Renderer } from "./components/Renderer";
import { Camera } from "./components/Camera";
import { DirectionalLight } from "./components/DirectionalLight";
import { createPlayer, player, initializePlayer } from "./components/Player";
import { map, initializeMap } from "./components/Map";
import { animateVehicles } from "./animateVehicles";
import { animatePlayer } from "./animatePlayer";
import { hitTest } from "./hitTest";
import { setGameActive } from "./gameState";
import "./style.css";
import "./collectUserInput";

async function startGame() {

  const scene = new THREE.Scene();

  await createPlayer();

  scene.add(player);
  scene.add(map);

  const ambientLight = new THREE.AmbientLight();
  scene.add(ambientLight);

  const dirLight = DirectionalLight();
  dirLight.target = player;
  player.add(dirLight);

  const camera = Camera();

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

  initializeGame();

  function initializeGame() {
    initializePlayer();
    initializeMap();
    setGameActive(true);

    if (scoreDOM) scoreDOM.innerText = "0";
    if (resultDOM) resultDOM.style.visibility = "hidden";
  }

  const renderer = Renderer();
  renderer.setAnimationLoop(animate);

  function handleResize() {
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const size = 300;
    const viewRatio = window.innerWidth / window.innerHeight;

    const width = viewRatio < 1 ? size : size * viewRatio;
    const height = viewRatio < 1 ? size / viewRatio : size;

    camera.left = width / -2;
    camera.right = width / 2;
    camera.top = height / 2;
    camera.bottom = height / -2;

    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', handleResize);
  handleResize();

  function animate() {
    if (!player) return;

    camera.position.x = player.position.x + 300;
    camera.position.y = player.position.y - 300;
    camera.lookAt(player.position);

    animateVehicles();
    animatePlayer();
    hitTest();
    renderer.render(scene, camera);
  }
}

startGame();