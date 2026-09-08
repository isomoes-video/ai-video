# /// script
# dependencies = ["dashscope>=1.24.6", "openai>=1.109.0"]
# ///
"""Use the repository TTS engine, formatting provider word times as short cues."""
import importlib.util
import json
from pathlib import Path

workspace = Path(__file__).resolve().parents[1]
repo = workspace.parents[1]
spec = importlib.util.spec_from_file_location('tts', repo / 'scripts/tts_from_script.py')
tts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tts)
slide_index = 0

def short_cues(sentences):
    global slide_index
    slide_index += 1
    (workspace / 'production' / f'word-times-{slide_index:02d}.json').write_text(json.dumps(sentences, ensure_ascii=False, indent=2))
    cues, group = [], []
    def flush():
        if not group:
            return
        text = ''.join(w['text'] for w in group).strip()
        start, end = group[0]['begin_time'], group[-1]['end_time']
        if text and end > start:
            cues.append(f'{len(cues)+1}\n{tts._ms_to_srt_timestamp(start)} --> {tts._ms_to_srt_timestamp(end)}\n{text}\n')
        group.clear()
    for sentence in sentences:
        for word in sentence.get('words', []):
            if not word.get('text'):
                continue
            if group and len(''.join(w['text'] for w in group)) + len(word['text']) > 22:
                flush()
            group.append(word)
            if word['text'][-1] in '，。！？；：,.!?;:':
                flush()
        flush()
    if not cues:
        raise ValueError('Provider did not return usable word timestamps')
    return '\n'.join(cues)

tts._words_to_srt = short_cues
raise SystemExit(tts.main())
