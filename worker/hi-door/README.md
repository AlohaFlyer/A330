# hi.ha330pilot.app no-code door

Cloudflare Worker `ha330-hi-door`. Typing `pilot@hawaiianair.com` at https://hi.ha330pilot.app/unlock sets a 30-day cookie; no one-time code. Serves the portal from this repo (raw.githubusercontent.com) and the manual indexes from R2 bucket `ha330-manuals` under `/_manuals/`. ha330pilot.app and manuals.ha330pilot.app stay behind Cloudflare Access (@alaskaair.com, one-time PIN).

Deploy: `npx wrangler@4 deploy` from this folder (Mac, wrangler logged in as ryanpettit@gmail.com). Logout: /logout. Change the address: edit ALLOWED in worker.js; bump TOKEN to force everyone to re-enter.

Security: anyone who knows the address gets in. Accepted by owner 2026-09-29.
