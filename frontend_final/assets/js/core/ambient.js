import { createElementFromHtml } from './utils.js';

function randomRange(min, max) {
  return Math.random() * (max - min) + min;
}

export function mountAmbientWorld({ world = 'default' } = {}) {
  document.body.dataset.world = world;
  if (document.getElementById('cosmos-layer')) return;

  const layer = createElementFromHtml(`
    <div class="cosmos-layer" id="cosmos-layer" aria-hidden="true">
      <div class="cosmos-nebula"></div>
      <div class="cosmos-aurora"></div>
      <div class="cosmos-fog"></div>
      <div class="cosmos-lightbeam"></div>
      <div class="cosmos-stars" id="cosmos-stars"></div>
      <div class="cosmos-dust" id="cosmos-dust"></div>
    </div>
  `);
  document.body.prepend(layer);

  const starRoot = layer.querySelector('#cosmos-stars');
  const dustRoot = layer.querySelector('#cosmos-dust');

  for (let index = 0; index < 70; index += 1) {
    const star = document.createElement('span');
    star.className = 'ambient-star';
    const size = randomRange(1, 3.2);
    star.style.width = `${size}px`;
    star.style.height = `${size}px`;
    star.style.top = `${randomRange(0, 100)}%`;
    star.style.left = `${randomRange(0, 100)}%`;
    star.style.opacity = String(randomRange(0.25, 0.95));
    star.style.animation = `floatStar ${randomRange(12, 28)}s linear ${randomRange(-16, 0)}s infinite`;
    starRoot.appendChild(star);
  }

  for (let index = 0; index < 42; index += 1) {
    const dust = document.createElement('span');
    dust.className = 'ambient-dust';
    const size = randomRange(2, 6);
    dust.style.width = `${size}px`;
    dust.style.height = `${size}px`;
    dust.style.top = `${randomRange(0, 100)}%`;
    dust.style.left = `${randomRange(0, 100)}%`;
    dust.style.opacity = String(randomRange(0.08, 0.32));
    dust.style.animation = `floatDust ${randomRange(18, 34)}s ease-in-out ${randomRange(-18, 0)}s infinite`;
    dustRoot.appendChild(dust);
  }
}
