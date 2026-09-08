"""Restore exact script spelling and segment cached provider word timestamps."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]

def norm(text):
    return ''.join(c.lower() for c in text if c.isalnum())

def stamp(ms):
    h,r=divmod(ms,3600000); m,r=divmod(r,60000); s,ms=divmod(r,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

for entry in json.loads((p/'script.json').read_text()):
    n=entry['slide_number']; original=entry['narration']
    sentences=json.loads((p/'production'/f'word-times-{n:02}.json').read_text())
    raw=[w for s in sentences for w in s['words']]
    assert norm(''.join(w['text'] for w in raw))==norm(original), f'Provider text mismatch, slide {n}'
    indices=[i for i,c in enumerate(original) if c.isalnum()]
    tokens=[]; pos=0
    for w in raw:
        length=len(norm(w['text']))
        if not length:
            if tokens: tokens[-1]['end']=max(tokens[-1]['end'],w['end_time'])
            continue
        first=indices[pos] if pos else 0
        pos+=length
        last=indices[pos] if pos<len(indices) else len(original)
        tokens.append(dict(text=original[first:last],start=w['begin_time'],end=w['end_time']))
    assert ''.join(w['text'] for w in tokens)==original
    groups=[]; group=[]
    for w in tokens:
        if group and len(''.join(x['text'] for x in group))+len(w['text'])>23:
            groups.append(group);group=[]
        group.append(w)
        if w['text'].rstrip()[-1] in '，。！？；：,.!?;:':
            groups.append(group);group=[]
    if group:groups.append(group)
    lines=[]
    for j,g in enumerate(groups,1):
        text=''.join(w['text'] for w in g).strip()
        assert any(c.isalnum() for c in text)
        lines.append(f'{j}\n{stamp(g[0]["start"])} --> {stamp(g[-1]["end"])}\n{text}\n')
    assert norm(''.join(''.join(w['text'] for w in g) for g in groups))==norm(original)
    (p/'audio'/f'slide-{n:02}.srt').write_text('\n'.join(lines))
    print(f'Slide {n}: {len(groups)} cues, exact script spelling restored')
