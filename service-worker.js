// Basic service worker: caches app shell and API responses (sheet CSV)
const CACHE = 'cec-wam-cache-v1';
const APP_SHELL = [
  '/',
  '/index.html',
  '/app.js',
  '/manifest.json',
  'https://cdn.jsdelivr.net/npm/chart.js',
  'https://cdn.jsdelivr.net/npm/chart.js/dist/chart.min.js'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  // Let the sheet CSV requests fall back to cache-first
  if (e.request.method === 'GET' && url.searchParams.get('output') === 'csv') {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(networkRes => {
      caches.open(CACHE).then(c => c.put(e.request, networkRes.clone()));
      return networkRes.clone();
    })).catch(() => new Response('', {status: 504})));
    return;
  }

  // App shell: network-first then cache
  e.respondWith(
    fetch(e.request).catch(()=>caches.match(e.request))
  );
});
