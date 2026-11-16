# -*- coding: utf-8 -*-
"""Reproducible audited PDF generation for six Japanese grammar worksheets."""
from pathlib import Path
import base64
import lzma
import hashlib
base = Path(__file__).resolve().parent
payload = b''.join((base / ('relative-payload-%d.txt' % i)).read_bytes() for i in range(3))
assert len(payload) == 12110, 'Generator data incomplete'
assert hashlib.sha256(payload).hexdigest() == 'eb12d5504ac649eb6ad0f873ed6d4064d57d690f64afebcf2f6522bfba7502a9', 'Generator data corrupted'
source = lzma.decompress(base64.b85decode(payload)).decode('utf-8')
exec(compile(source, str(base / 'build_source.py'), 'exec'), {'__name__': '__main__', '__file__': __file__})
