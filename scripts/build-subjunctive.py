# coding: utf-8
"""Rebuild the approved six subjunctive PDFs in GitHub Actions."""
from pathlib import Path
import base64, hashlib, io, lzma, tarfile, subprocess, sys
root = Path(__file__).resolve().parent
payload = ''.join((root / f'subj-payload-{i}.txt').read_text(encoding='ascii') for i in range(4))
assert len(payload) == 12295, f'Incomplete source archive: {len(payload)}'
assert hashlib.sha256(payload.encode('ascii')).hexdigest() == '94df36cb9896cef93f253cb882225e1dca69d266d6d328687d9555f1ceecbe7d'
raw = lzma.decompress(base64.b85decode(payload))
target = root / 'subj-build'
target.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as tar:
    for member in tar.getmembers():
        assert member.name in ('data.py','build.py')
        assert member.isfile()
        (target / member.name).write_bytes(tar.extractfile(member).read())
patch = lzma.decompress(base64.b85decode((root / 'patch-subjunctive-lesson4.b85').read_text(encoding='ascii'))).decode('utf-8')
data_file = target / 'data.py'
data_file.write_text(data_file.read_text(encoding='utf-8') + '\n' + patch, encoding='utf-8')
script = target / 'build.py'
body = script.read_text(encoding='utf-8')
body = body.replace('/mnt/data/subjunctive_final', '.')
comparison_note_start = "  if self.lesson['slug']=='クジラ構文・慣用表現応用':"
if comparison_note_start in body:
    i = body.index(comparison_note_start)
    j = body.index("  if self.lesson['slug']=='仮定法現在':", i)
    body = body[:i] + body[j:]

fonts = {
    'LiberationSerif-Regular.ttf': 'Liberation Serif:style=Regular',
    'LiberationSerif-Bold.ttf': 'Liberation Serif:style=Bold',
    'LiberationSans-Regular.ttf': 'Liberation Sans:style=Regular',
}
for basename, family in fonts.items():
    original = '/usr/share/fonts/truetype/liberation/' + basename
    actual = subprocess.check_output(['fc-match','-f','%{file}',family],text=True).strip()
    assert actual and Path(actual).is_file(), f'Missing {family}'
    body = body.replace(original, actual)
script.write_text(body,encoding='utf-8')
subprocess.run([sys.executable,str(script)],check=True)
