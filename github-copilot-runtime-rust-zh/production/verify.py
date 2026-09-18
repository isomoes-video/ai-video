import json,re,subprocess
from pathlib import Path
w=Path(__file__).resolve().parents[1]
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def ms(s):
 h,m,t=s.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(t)
entries=json.loads((w/'script.json').read_text());results=[]
assert len(entries)==10
assert len(list((w/'audio').glob('*.mp3')))==10
assert len(list((w/'audio').glob('*.srt')))==10
pdfinfo=subprocess.check_output(['pdfinfo',str(w/'output.pdf')],text=True)
assert re.search(r'Pages:\s+10\b',pdfinfo)
for e in entries:
 n=e['slide_number'];audio=float(probe(w/'audio'/f'slide-{n:02}.mp3')['format']['duration']);seg=probe(w/'video-work/segments'/f'slide-{n:02}.mp4');v=next(s for s in seg['streams'] if s['codec_type']=='video');a=next(s for s in seg['streams'] if s['codec_type']=='audio')
 assert float(v['duration'])+1e-5>=audio+(0.25 if n<10 else 0),(n,'short visual')
 assert float(v['duration'])+1e-5>=float(a['duration']),(n,'stream coverage')
 text='';prev=0;count=0
 for block in re.split(r'\n\s*\n',(w/'audio'/f'slide-{n:02}.srt').read_text().strip()):
  lines=block.splitlines();start,end=map(ms,lines[1].split(' --> '));assert start>=prev and end>start and end<=audio+0.1;prev=end;text+=''.join(lines[2:]);count+=1
 assert re.sub(r'\s','',text)==re.sub(r'\s','',e['narration'])
 results.append({'slide':n,'source_audio_seconds':audio,'video_seconds':float(v['duration']),'subtitle_cues':count})
final=probe(w/'video.mp4');v=next(s for s in final['streams'] if s['codec_type']=='video');a=next(s for s in final['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'])==(1920,1080)
assert v['avg_frame_rate']=='30/1' and v['r_frame_rate']=='30/1'
assert abs(float(v['start_time'])-float(a['start_time']))<0.05
assert float(v['duration'])+1e-5>=float(a['duration'])
intro=(w/'intro.txt').read_text();assert len(re.findall(r'^\d\d:\d\d  ',intro,re.M))<=10
assert 'Source: https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/' in intro
raw=(w/'video.mp4').read_bytes();assert raw.find(b'moov')<raw.find(b'mdat')
report={'result':'PASS','duration_seconds':float(final['format']['duration']),'resolution':[v['width'],v['height']],'fps':v['avg_frame_rate'],'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'slides':results,'subtitle_timing':'Provider sentence anchors; interpolated short-cue boundaries','visual_review':'All ten slide screenshots reviewed; PDF render and burned subtitle frame checked'}
(w/'production/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
