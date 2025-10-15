import * as THREE from "three";
import { Renderer } from "./components/Renderer";
import { Camera } from "./components/Camera";
import { DirectionalLight } from "./components/DirectionalLight";
import { player, initializePlayer } from "./components/Player";
import { map, initializeMap } from "./components/Map";
import { animateVehicles } from "./animateVehicles";
import { animatePlayer } from "./animatePlayer";
import { hitTest } from "./hitTest";
import { setGameActive } from "./gameState";
import "./style.css";
import "./collectUserInput";

const scene = new THREE.Scene();
scene.add(player);
scene.add(map);

const ambientLight = new THREE.AmbientLight();
scene.add(ambientLight);

const dirLight = DirectionalLight();
dirLight.target = player;
player.add(dirLight);

const camera = Camera();
player.add(camera);

const scoreDOM = document.getElementById("score");
const resultDOM = document.getElementById("result-container");

document.querySelector("#retry")?.addEventListener("click", initializeGame);

// Reiniciar el juego al presionar la tecla "r"
window.addEventListener("keydown", (event) => {
  if (event.key.toLowerCase() === "r") {
    const resultDOM = document.getElementById("result-container");
    // Solo reiniciar si el menú de game over está visible
    if (resultDOM && resultDOM.style.visibility === "visible") {
      initializeGame();
    }
  }
});

initializeGame();

function initializeGame() {
  initializePlayer();
  initializeMap();
  setGameActive(true); // Reactivar el juego al reiniciar

  if (scoreDOM) scoreDOM.innerText = "0";
  if (resultDOM) resultDOM.style.visibility = "hidden";
}

const renderer = Renderer();
renderer.setAnimationLoop(animate);

function animate() {
  animateVehicles();
  animatePlayer();
  hitTest();
  renderer.render(scene, camera);
}