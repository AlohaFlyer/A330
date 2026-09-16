/* ha330pilot.app unlock log collector (Google Apps Script web app).
   Separate from the as787pilot.app collector so the two portals never mix.
   Writes need no key. Reads need READ_KEY, which lives in Script Properties, never in this file.

   Deploy: script.google.com > New project > paste this > Project Settings > Script Properties:
   READ_KEY = <a long random string> ; SHEET_ID = <id of a new empty Google Sheet named
   "ha330pilot unlock log"> ; then Deploy > New deployment > Web app, Execute as Me, Who has
   access: Anyone. Copy the /exec URL into build_scripts/page_fixups.py (LOG_URL) and rebuild.
   Protocol (identical to the B787 collector, so portal-settings.js is unchanged):
     POST {rows:[{email,ts,tz}], ua}   -> {ok:true, added:n}      (dedupe on ts+email)
     POST {read:true, key}             -> {ok:true, total, people:[{email,count,first,last}]}
                                          or {ok:false, error:'bad key'} */
function props() { return PropertiesService.getScriptProperties(); }
function sheet() {
  var ss = SpreadsheetApp.openById(props().getProperty('SHEET_ID'));
  var sh = ss.getSheetByName('unlocks') || ss.insertSheet('unlocks');
  if (sh.getLastRow() === 0) sh.appendRow(['ts', 'email', 'tz', 'ua', 'portal']);
  return sh;
}
function doPost(e) {
  var out = ContentService.createTextOutput().setMimeType(ContentService.MimeType.JSON);
  var body = {};
  try { body = JSON.parse(e.postData.contents || '{}'); } catch (err) { return out.setContent(JSON.stringify({ ok: false, error: 'bad json' })); }
  var sh = sheet();
  if (body.read) {
    if (!body.key || body.key !== props().getProperty('READ_KEY')) return out.setContent(JSON.stringify({ ok: false, error: 'bad key' }));
    var rows = sh.getDataRange().getValues().slice(1), by = {};
    rows.forEach(function (r) {
      var em = String(r[1]).toLowerCase(), ts = String(r[0]);
      if (!by[em]) by[em] = { email: em, count: 0, first: ts, last: ts };
      by[em].count++; if (ts < by[em].first) by[em].first = ts; if (ts > by[em].last) by[em].last = ts;
    });
    var people = Object.keys(by).map(function (k) { return by[k]; }).sort(function (a, b) { return b.count - a.count; });
    return out.setContent(JSON.stringify({ ok: true, total: rows.length, people: people }));
  }
  var existing = {}, data = sh.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) existing[String(data[i][0]) + '|' + String(data[i][1]).toLowerCase()] = 1;
  var added = 0;
  (body.rows || []).forEach(function (r) {
    if (!r || !r.email || !r.ts) return;
    var k = String(r.ts) + '|' + String(r.email).toLowerCase();
    if (existing[k]) return;
    sh.appendRow([String(r.ts), String(r.email).toLowerCase(), String(r.tz || ''), String(body.ua || '').slice(0, 200), 'ha330']);
    existing[k] = 1; added++;
  });
  return out.setContent(JSON.stringify({ ok: true, added: added }));
}
function doGet() { return ContentService.createTextOutput('ha330pilot unlock log collector'); }
