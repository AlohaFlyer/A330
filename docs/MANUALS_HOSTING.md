# Manuals hosting: R2 bucket behind Cloudflare Access

The Manuals page (`/manuals/index.html`, built by `build_scripts/page_manuals.py`) is served from
the public site at https://ha330pilot.app/manuals/. The manual text is NOT in the repo. Every
index fetch goes to `MANUALS_BASE = 'https://manuals.ha330pilot.app'` with
`fetch(url, {credentials: 'include', mode: 'cors'})`. Only `manuals/prompt.json` stays on the
public site (it holds the answer style, no manual text).

## R2

- Bucket: `ha330-manuals`
- Custom domain: `manuals.ha330pilot.app`
- Object keys, all at the bucket root, as produced by `build_scripts/build_manuals_index.py`:
  every file under `manuals/` except `index.html` and `prompt.json`, plus `login.html`. That is
  `manifest.json`, `<key>.json` for the 11 manuals, the FCOM parts `A330P_FCOM.<part>.json`
  (33 files), the MEL parts `A330_MEL.<part>.json` (6 files), `login.html` and `r2_cors.json`
  (harmless if uploaded). `manuals/manifest.json` lists every index file with its byte size.
- CORS policy on the bucket: `manuals/r2_cors.json` (AllowedOrigins https://ha330pilot.app,
  methods GET and HEAD, AllowedHeaders *, MaxAgeSeconds 86400).
- Re-upload the whole set after each rebuild; the page re-reads on every load (no SW cache).

## Cloudflare Access

- Application: self-hosted, hostname `manuals.ha330pilot.app`, path `/` (whole host).
- Policy: Allow, include "Emails ending in" `@alaskaair.com`, login method One-time PIN only.
- Session duration as preferred (24 h is enough for a duty day).
- CORS settings on the application: allowed origin `https://ha330pilot.app`, allow credentials
  ON, allowed methods GET HEAD OPTIONS, allowed headers `*`. Without "allow credentials" the
  browser drops the Access cookie on the cross-origin fetch and every request looks signed out.

## Sign-in flow

1. On load the page fetches `MANUALS_BASE/manifest.json`. An unauthenticated request is answered
   by Access with a redirect to its login page, which the browser surfaces as a CORS TypeError
   or a redirected response. Either way the page shows, in the status area, "Company email
   sign-in required for the manuals" and a "Sign in with @alaskaair.com" button.
2. The button navigates (same tab) to `MANUALS_BASE/login.html?back=<current page url>`.
   Access intercepts, runs the one-time-PIN login, and then serves `login.html`.
3. `login.html` reads `back`, accepts only `https://ha330pilot.app/...` (or localhost for
   testing), and `location.replace`s it; default `https://ha330pilot.app/manuals/`. It needs no
   other asset.
4. Back on the page the probe succeeds and searches run. A failed index fetch later (session
   expired) shows the same prompt again.

## Offline

The service worker cannot cache cross-origin credentialed JSON, so the manuals search needs a
connection. `build_offline_manifest.py` must not list `manuals/*.json` (they are not in the
repo anyway); the page tells the user when it is offline.

## Local testing

`?base=<url>` replaces `MANUALS_BASE` for that page load, e.g.
`http://127.0.0.1:8765/manuals/?base=http://127.0.0.1:8765/manuals`. `build_scripts/test_manuals_headless.py`
serves the repo with `python3 -m http.server` and uses that override; it also checks that
without the override the sign-in prompt appears and that `login.html` bounces to `back`.

## 2026-09-16 change: page served from the manuals origin
R2 cannot send Access-Control-Allow-Credentials and answered credentialed cross-origin GETs from
ha330pilot.app with 503, so the full Manuals page now lives in the bucket as `index.html`
(built to `manuals/app.html`; upload that file to R2 as `index.html` after every build) and is
opened at https://manuals.ha330pilot.app/index.html. GitHub Pages `manuals/index.html` is a
bounce that forwards ?s= / ?q= and carries the Ask Pualani provider, key and model in the URL
fragment (#ps=, never sent to a server). Access: team ha330pilot, app "ha330pilot manuals",
One-time PIN only, emails ending @alaskaair.com, 1 month session. Access CORS handling is
bypassed (same-origin now).

## 2026-09-16 later: whole portal behind Access
ha330pilot.app DNS records (4 A + www CNAME) are proxied through Cloudflare; the Access app
"A330 Study Portal" covers ha330pilot.app and manuals.ha330pilot.app with one policy (emails
ending @alaskaair.com, One-time PIN only, 1 month session). One code at the home page also
opens the manuals (SSO within the identity session). Login page branded (name, icon from the
public GitHub raw URL, header, footer, #F4F1F9). The OTP email itself is Cloudflare's fixed
template and cannot be branded. Free plan: 50 unique users per month across the whole portal.

## 2026-09-16 later: service worker and Access callback
sw.js v5 never intercepts /cdn-cgi/ (the Access login callback and logout), passes navigations
through with their original redirect mode, and returns redirected or opaqueredirect responses
untouched without caching them. The older worker answered the Access callback URL from cache
with the home page, which showed "This site can't be reached" after entering the code.
The leftover "Cloudflare" identity provider was deleted; One-time PIN is the only IdP.
