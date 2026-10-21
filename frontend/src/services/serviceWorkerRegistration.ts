import { registerSW } from 'virtual:pwa-register';

export function initServiceWorker() {
  if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
    // Proactively check for updates immediately on navigation
    navigator.serviceWorker.getRegistrations().then((registrations) => {
      for (const registration of registrations) {
        registration.update();
      }
    });

    const updateSW = registerSW({
      immediate: true,
      onNeedRefresh() {
        console.log('[PWA] New version available, automatically updating...');
        updateSW(true);
      },
      onOfflineReady() {
        console.log('[PWA] Application shell cached and ready for offline use.');
      },
      onRegistered(r) {
        console.log('[PWA] Service Worker registered with scope:', r?.scope);
      },
      onRegisterError(error) {
        console.error('[PWA] Service Worker registration failed:', error);
      },
    });
  }
}
