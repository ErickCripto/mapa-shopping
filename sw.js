// Ao publicar versão nova, trocar o número abaixo.
const CACHE = "mapa-shopping-v19";
const FILES = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/apple-touch-icon.png", "mascote/bandi-oi.webp", "mascote/bandi-rota.webp", "mascote/bandi-ops.webp", "mascote/bandi-chegou.webp", "mascote/pixel/bandi-oi.webp", "mascote/pixel/bandi-rota.webp", "mascote/pixel/bandi-ops.webp", "mascote/pixel/bandi-chegou.webp", "mascote/pixel/bandi-pensando.webp", "mascote/pixel/bandi-apontar.webp", "mascote/pixel/bandi-triste.webp", "mascote/pixel/bandi-danca.webp"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES))); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(fetch(e.request).then(r => {
    if (r.ok && new URL(e.request.url).origin === location.origin) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); }
    return r;
  }).catch(() => caches.match(e.request).then(r => r || caches.match("index.html"))));
});
// Ao tocar num aviso (lembrete do estacionamento ou do encontro), abre o app.
self.addEventListener("notificationclick", e => {
  e.notification.close();
  e.waitUntil(clients.matchAll({type: "window", includeUncontrolled: true}).then(cs => {
    for (const c of cs) if ("focus" in c) return c.focus();
    return clients.openWindow("./");
  }));
});
