#!/usr/bin/env python3
"""Fleet/airline/domain string map, B787 -> A330. Applied after apply_palette."""
import re, sys, os, json
ORDER = [
  ('B787 STUDY PORTAL','A330 STUDY PORTAL'), ('B787 Study Portal','A330 Study Portal'),
  ('B787%20Study%20Portal','A330%20Study%20Portal'),
  ('AS 787 Study Portal','HA 330 Study Portal'), ('AS 787 Study','HA 330 Study'),
  ('787 Flight Deck Notes','330 Flight Deck Notes'),
  ('as787pilot.app','ha330pilot.app'), ('as787_','ha330_'), ('as787-','ha330-'),
  ('b787-core-','ha330-core-'), ('b787-audio-','ha330-audio-'),
  ('b787state','a330state'), ('b787dark','a330dark'), ('b787_sysquiz_v2','a330_sysquiz_v2'),
  ('b787_jeopardy_stats','a330_jeopardy_stats'), ('B787_night.jpg','assets/A330_hero.svg'),
  ('Alaska Airlines Boeing 787 at night','Hawaiian Airlines Airbus A330'),
  ('alt="Alaska Airlines"','alt="Hawaiian Airlines"'), ('alt="Boeing 787"','alt="Airbus A330"'),
  ('Fleet is B787.','Fleet is A330.'), ("fleet: 'B787'","fleet: 'A330'"), ("fleet:'B787'","fleet:'A330'"),
  ("' · B787 · '","' · A330 · '"), ('on the B787 at Alaska/Hawaiian','on the A330 at Hawaiian/Alaska'),
  ('cdu_preflight.html','mcdu_preflight.html'), ("'cdu_preflight.html': 'cdu'","'mcdu_preflight.html': 'mcdu'"),
  ('B787_CDU_Preflight_Handout.pdf','A330_MCDU_Preflight_Handout.pdf'),
  ('B787 CDU PREFLIGHT (PF)','A330 MCDU PREFLIGHT (PF)'), ('CDU Preflight (PF)','MCDU Preflight (PF)'),
  ('B787_Weather_Requirements.pdf','A330_Weather_Requirements.pdf'),
  ('B787_Memory_Limitations.pdf','A330_Memory_Limitations.pdf'),
  ('B787_QRH_Memory_Items.pdf','A330_QRH_Memory_Items.pdf'),
  ('B787_IOE_Workbook_Answered.pdf','A330_OE_Workbook_Answered.pdf'),
  ('IOE Workbook Trainer','OE Workbook Trainer'), ('B787 IOE Workbook Trainer','A330 OE Workbook Trainer'),
  ("LS.get('pwa_seat', 'CA')","LS.get('pwa_seat', 'FO')"),
  ("seat: 'CA', fleet: 'A330'","seat: 'FO', fleet: 'A330'"),
  ('B787','A330'), ('787','330'),
]
def apply(text, name):
    for a,b in ORDER:
        text = text.replace(a,b)
    # collapse JS \uXXXX escapes to literal chars so the GitHub connector cannot mangle them
    text = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1),16)) if 0x20<=int(m.group(1),16)<0xD800 else m.group(0), text)
    return text
if __name__=='__main__':
    root=sys.argv[1]
    for dp,_,fs in os.walk(root):
        if '.git' in dp or 'build_scripts' in dp: continue
        for f in fs:
            if f.endswith(('.html','.js','.webmanifest','.txt')):
                p=os.path.join(dp,f); t=open(p,encoding='utf-8').read(); n=apply(t,f)
                if n!=t: open(p,'w',encoding='utf-8').write(n); print('strings:',f)
