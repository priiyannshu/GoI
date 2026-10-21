import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { initServiceWorker } from './services/serviceWorkerRegistration';

import './styles/main.css';

const app = createApp(App);

const pinia = createPinia();
app.use(pinia);
app.use(router);

app.mount('#app');

// Register Workbox PWA service worker with auto-update
initServiceWorker();
