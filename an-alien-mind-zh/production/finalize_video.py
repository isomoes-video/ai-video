# /// script
# dependencies = ["pillow>=11.1.0", "pypdfium2>=4.30.0"]
# ///
"""Round short holds up to full frames; normalize final audio/video start times."""
import importlib.util, json, math, subprocess
from pathlib import Path
p=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('combine',p.parents[1]/'scripts/combine_video.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
assets=c.build_slide_assets(8,p/'audio',p/'video-work/slides',p/'video-work/segments')
for asset in assets:
    source=c.probe_audio_duration(asset.audio_path)
    desired=source+(0.25 if asset.slide_number<8 else 0)
    data=probe(asset.segment_path)
    v=next(float(s['duration']) for s in data['streams'] if s['codec_type']=='video')
    a=next(float(s['duration']) for s in data['streams'] if s['codec_type']=='audio')
    if v<desired or v<a:
        total=math.ceil(desired*30)/30
        c.render_slide_segment(asset,source,total-source,True,30,'96k','burn')
c.combine_segments(p/'video-work/concat.txt',p/'video.mp4',True)
data=probe(p/'video.mp4')
target=math.ceil(float(data['format']['duration'])*30)/30
normalized=p/'video-work/normalized.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'video.mp4'),'-vf','setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.1','-af','asetpts=PTS-STARTPTS','-t',str(target),'-r','30','-c:v','libx264','-preset','medium','-tune','stillimage','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart',str(normalized)],check=True)
normalized.replace(p/'video.mp4')
print('Finalized',p/'video.mp4')
