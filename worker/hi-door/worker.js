// ha330-hi-door: no-code door into the A330 study portal for one shared address.
// Host: hi.ha330pilot.app (NOT covered by the Cloudflare Access app that guards
// ha330pilot.app and manuals.ha330pilot.app). Typing ALLOWED at /unlock sets a
// 30-day cookie; the Worker then serves portal files from the public GitHub repo
// and manual indexes from the R2 bucket (binding MANUALS) under /_manuals/.
// Security note: anyone who types ALLOWED gets in. Owner accepted this 2026-09-29.

const ALLOWED = 'pilot@hawaiianair.com';
const COOKIE = 'hi_door';
const TOKEN = 'ha330-hi-v1';            // opaque marker; the email itself is the only secret
const MAX_AGE = 60 * 60 * 24 * 30;      // 30 days
const ORIGIN = 'https://raw.githubusercontent.com/AlohaFlyer/A330/main';
const SELF = 'https://hi.ha330pilot.app';

const TYPES = {
  html: 'text/html; charset=utf-8', js: 'application/javascript; charset=utf-8',
  json: 'application/json; charset=utf-8', css: 'text/css; charset=utf-8',
  png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', svg: 'image/svg+xml',
  ico: 'image/x-icon', webmanifest: 'application/manifest+json', pdf: 'application/pdf',
  mp3: 'audio/mpeg', m4a: 'audio/mp4', txt: 'text/plain; charset=utf-8', woff2: 'font/woff2'
};
const TEXT = /^(html|js|json|css|webmanifest|svg|txt)$/;

function ext(p) { const m = p.match(/\.([a-z0-9]+)$/i); return m ? m[1].toLowerCase() : ''; }

function hasCookie(req) {
  const c = req.headers.get('cookie') || '';
  return c.split(';').some(s => s.trim() === COOKIE + '=' + TOKEN);
}

function page(title, body, status = 200, extra = {}) {
  const html = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>${title}</title><style>
body{margin:0;font-family:"Segoe UI",Arial,Helvetica,sans-serif;background:#F4F1F9;color:#463C8F;display:flex;min-height:100vh;align-items:center;justify-content:center;padding:16px}
.box{max-width:420px;width:100%;text-align:center}h1{font-size:20px;letter-spacing:1px}
input{width:100%;box-sizing:border-box;font-size:17px;padding:12px;border:2px solid #463C8F;border-radius:6px;margin:10px 0}
button{width:100%;font-size:17px;font-weight:700;padding:12px;border:0;border-radius:6px;background:#CE0C88;color:#fff}
.err{color:#C0392B;min-height:1.4em;margin-top:8px}</style></head><body><div class="box">${body}</div></body></html>`;
  return new Response(html, { status, headers: { 'content-type': TYPES.html, 'cache-control': 'no-store', ...extra } });
}

function unlockForm(msg = '') {
  return page('A330 Study Portal', `<h1>A330 STUDY PORTAL</h1>
<form method="POST" action="/unlock"><input name="email" type="email" inputmode="email" autocomplete="email"
spellcheck="false" placeholder="Email address" aria-label="Email address" required autofocus>
<button type="submit">Enter</button></form><div class="err">${msg}</div>`, msg ? 403 : 200);
}

function rewrite(text, path) {
  let t = text.split('https://manuals.ha330pilot.app').join(SELF + '/_manuals')
              .split('https://ha330pilot.app').join(SELF);
  if (path === '/_manuals/index.html') {
    t = t.replace("String(QS.base).replace(/\\/+$/, '') : ''", "String(QS.base).replace(/\\/+$/, '') : '/_manuals'");
  }
  if (path === '/index.html') {
    // Pre-seed the portal's own client gate so the menu opens without retyping.
    const seed = `<script>document.cookie='ha330_access=1; path=/; max-age=157680000; samesite=lax';try{localStorage.setItem('ha330_email','${ALLOWED}')}catch(e){}</script>`;
    t = t.replace('<div class="gate"', seed + '<div class="gate"');
  }
  return t;
}

async function serveManual(req, env, path) {
  let key = path.slice('/_manuals/'.length) || 'index.html';
  if (key.endsWith('/')) key += 'index.html';
  const obj = await env.MANUALS.get(key);
  if (!obj) return new Response('Not found', { status: 404 });
  const e = ext(key);
  const h = { 'content-type': TYPES[e] || 'application/octet-stream', 'cache-control': 'private, no-store' };
  if (TEXT.test(e)) return new Response(rewrite(await obj.text(), '/_manuals/' + key), { headers: h });
  return new Response(obj.body, { headers: h });
}

async function servePortal(req, path) {
  if (path.endsWith('/')) path += 'index.html';
  if (!ext(path)) path += '.html';
  const init = { cf: { cacheEverything: true, cacheTtl: 300 }, headers: {} };
  const range = req.headers.get('range');
  if (range) init.headers.range = range;
  const up = await fetch(ORIGIN + path.split('/').map(encodeURIComponent).join('/'), init);
  if (up.status === 404) return new Response('Not found', { status: 404, headers: { 'content-type': TYPES.txt } });
  const e = ext(path);
  const h = new Headers({ 'content-type': TYPES[e] || 'application/octet-stream', 'cache-control': 'private, max-age=0, must-revalidate' });
  for (const k of ['content-range', 'accept-ranges', 'etag']) { const v = up.headers.get(k); if (v) h.set(k, v); }
  if (TEXT.test(e) && up.ok) return new Response(rewrite(await up.text(), path), { status: up.status, headers: h });
  if (up.headers.get('content-length') && !TEXT.test(e)) h.set('content-length', up.headers.get('content-length'));
  return new Response(up.body, { status: up.status, headers: h });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const path = url.pathname;

    if (path === '/unlock') {
      if (req.method === 'POST') {
        const form = await req.formData();
        const email = String(form.get('email') || '').trim().toLowerCase();
        if (email !== ALLOWED) return unlockForm('That email is not enabled here.');
        return new Response(null, { status: 303, headers: {
          location: '/',
          'set-cookie': `${COOKIE}=${TOKEN}; Path=/; Max-Age=${MAX_AGE}; Secure; HttpOnly; SameSite=Lax`,
          'cache-control': 'no-store' } });
      }
      return hasCookie(req) ? Response.redirect(SELF + '/', 303) : unlockForm();
    }
    if (path === '/logout') {
      return new Response(null, { status: 303, headers: { location: '/unlock',
        'set-cookie': `${COOKIE}=; Path=/; Max-Age=0; Secure; HttpOnly; SameSite=Lax` } });
    }
    if (path === '/robots.txt') return new Response('User-agent: *\nDisallow: /\n', { headers: { 'content-type': TYPES.txt } });
    if (!hasCookie(req)) {
      if (req.method === 'GET' && (req.headers.get('accept') || '').includes('text/html')) return Response.redirect(SELF + '/unlock', 302);
      return new Response('Unauthorized', { status: 401 });
    }
    if (req.method !== 'GET' && req.method !== 'HEAD') return new Response('Method not allowed', { status: 405 });
    if (path === '/_manuals' ) return Response.redirect(SELF + '/_manuals/index.html', 302);
    if (path.startsWith('/_manuals/')) return serveManual(req, env, path);
    return servePortal(req, path);
  }
};
