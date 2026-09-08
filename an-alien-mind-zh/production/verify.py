import json, re, subprocess, struct
from pathlib import Path
p=Path(__file__).resolve().parents[1]
def probe(path): return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def secs(t):
 h,m,s,ms=map(int,re.split('[:,]',t));return h*3600+m*60+s+ms/1000
entries=json.loads((p/'script.json').read_text())
report={'slides':len(entries),'slide_checks':[]}
for e in entries:
 n=e['slide_number']; assert set(e)=={'slide_number','narration'}
 a=float(probe(p/'audio'/f'slide-{n:02}.mp3')['format']['duration'])
 d=probe(p/'video-work/segments'/f'slide-{n:02}.mp4')
 streams={s['codec_type']:s for s in d['streams']}
 v=float(streams['video']['duration']); sa=float(streams['audio']['duration'])
 assert v+0.00001>=sa,(n,v,sa)
 assert v+0.00001>=a+(0.25 if n<8 else 0),(n,v,a)
 srt=(p/'audio'/f'slide-{n:02}.srt').read_text()
 previous=0
 for start,end in re.findall(r'(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})',srt):
  b,t=secs(start),secs(end);assert b>=previous and t>b and t<=a+0.05;previous=t
 report['slide_checks'].append(dict(slide=n,narration_seconds=a,video_seconds=v,audio_seconds=sa,cues=srt.count('-->')))
d=probe(p/'video.mp4');s={x['codec_type']:x for x in d['streams']}
assert s['video']['codec_name']=='h264' and s['audio']['codec_name']=='aac'
assert (s['video']['width'],s['video']['height'])==(1920,1080)
assert s['video']['r_frame_rate']=='30/1'
assert float(s['video']['duration'])>=float(s['audio']['duration'])
assert abs(float(s['video']['start_time']))<0.001
assert float(d['format']['duration'])>=sum(x['narration_seconds'] for x in report['slide_checks'])+7*.25
atoms=[]
with (p/'video.mp4').open('rb') as f:
 while h:=f.read(8):
  size,typ=struct.unpack('>I4s',h);header=8
  if size==1:size=struct.unpack('>Q',f.read(8))[0];header=16
  atoms.append(typ.decode('ascii'))
  if size==0:break
  f.seek(size-header,1)
assert atoms.index('moov')<atoms.index('mdat')
report.update(duration_seconds=float(d['format']['duration']),width=1920,height=1080,fps=30,bytes=int(d['format']['size']),faststart=True,status='passed')
(p/'production/verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
