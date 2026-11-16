# coding: utf-8
"""Reproduce four revised subjunctive worksheets: future, mixed and idioms."""
from pathlib import Path
import base64, hashlib, io, lzma, subprocess, sys, tarfile
root=Path(__file__).resolve().parent
payload=''.join((root/f'reorg-payload-{i}.txt').read_text(encoding='ascii') for i in range(4))
assert len(payload)==10130,(len(payload),'source incomplete')
assert hashlib.sha256(payload.encode('ascii')).hexdigest()=='395b29fb8b7be8230eabcde3e753a4dc99af934ff19f6c7879e93d684bd3274e'
raw=lzma.decompress(base64.b85decode(payload))
out=root/'reorg-source'
out.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as tar:
    for member in tar.getmembers():
        assert member.name in {'generator.py','lesson_data.py'} and member.isfile()
        (out/member.name).write_bytes(tar.extractfile(member).read())
p=out/'generator.py'
s=p.read_text(encoding='utf-8')
for suffix,family in [('LiberationSerif-Regular.ttf','Liberation Serif:style=Regular'),('LiberationSerif-Bold.ttf','Liberation Serif:style=Bold'),('LiberationSans-Regular.ttf','Liberation Sans:style=Regular')]:
    expected='/usr/share/fonts/truetype/liberation2/'+suffix
    actual=subprocess.check_output(['fc-match','-f','%{file}',family],text=True).strip()
    assert actual and Path(actual).exists(),family
    s=s.replace(expected,actual)
p.write_text(s,encoding='utf-8')
subprocess.run([sys.executable,str(p)],check=True)
