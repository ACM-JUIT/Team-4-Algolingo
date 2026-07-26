import { mountAmbientWorld } from '../core/ambient.js';
import { qs } from '../core/utils.js';

mountAmbientWorld({ world: 'auth' });
const root = qs('#error-root');
if (root) {
  document.title = `${root.dataset.title} · AlgoLingo`;
}
