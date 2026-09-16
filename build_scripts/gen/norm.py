import re, unicodedata
_MAP = {'“': '"', '”': '"', '‘': "'", '’': "'", '–': '-', '—': '-', '−': '-',
        '‐': '-', '‑': '-', ' ': ' '}
_PUA = re.compile(r'[-﻿​]')
def norm(s):
    s = unicodedata.normalize('NFKC', s or '')
    for a, b in _MAP.items():
        s = s.replace(a, b)
    s = _PUA.sub('', s)
    return re.sub(r'\s+', ' ', s).strip()
