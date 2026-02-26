// This is the Service Worker
const CACHE_NAME = 'zenith-cache-v1';

// Install event
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installed');
    self.skipWaiting();
});

// Fetch event (required for PWA installability)
self.addEventListener('fetch', (event) => {
    // For now, just pass the request through to the network normally
    event.respondWith(fetch(event.request).catch(() => {
        return new Response('Network error or offline.');
    }));
});