const CACHE_NAME = 'cec-wam-v2-live';
const urlsToCache = [
  './',
  './index.html',
  './CEC_WAM_MASTER_LEDGER_LIVE.xlsx',
  'https://cdn.sheetjs.com/xlsx-latest/package/dist/xlsx.full.min.js',
  'https://img.icons8.com/color/96/000000/artificial-intelligence.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
