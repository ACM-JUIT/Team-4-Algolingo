import { redirectIfAuthenticated } from '../core/auth.js';
import { mountAmbientWorld } from '../core/ambient.js';

async function bootstrap() {
  mountAmbientWorld({ world: 'auth' });
  await redirectIfAuthenticated('./dashboard.html');
}

bootstrap();
