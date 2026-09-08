import json
import re
import subprocess
from pathlib import Path
p = Path(__file__).resolve().parents[1]
entries = json.loads((p/'script.json').read_text())
starts=[]
elapsed=0
for entry in entries:
    n=entry['slide_number']
    srt=(p/'audio'/f'slide-{n:02}.srt').read_text()
    assert '-->' in srt
    audio=p/'audio'/f'slide-{n:02}.mp3'
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(audio)]))
    segment=p/'video-work'/'segments'/f'slide-{n:02}.mp4'
    starts.append(elapsed)
    elapsed += float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(segment)])) if segment.exists() else duration + (0.25 if n < len(entries) else 0)
chapters=[(0,'开场'),(1,'理解差异'),(2,'对齐与泛化'),(4,'监测'),(5,'防御'),(6,'自我改进'),(7,'三个问题')]
intro='''中文标题：异质智能：如何守住人的选择权
English Title: An Alien Mind: Keeping Humans in Control
标签：人工智能，OpenAI，AI安全，对齐，递归自我改进

Source: https://openai.com/index/an-alien-mind/
Output: https://github.com/isomoes-video/ai-video/tree/main/an-alien-mind-zh

本片简要解读 Jakub Pachocki 的观点文章《An Alien Mind》，并用植物生长、订机票和文件整理等教学例子，帮助理解 AI 行为、安全监测与人的决策。片中的假设情境和三个收尾问题由本片补充，不是原文报告的实验。适合希望建立基本概念、再进一步阅读原文的观众。

'''
for index,title in chapters:
    secs=int(starts[index]); intro+=f'{secs//60:02}:{secs%60:02}  {title}\n'
assert len(re.findall(r'^\d{2}:\d{2}  ',intro,re.M))<=10
(p/'intro.txt').write_text(intro)
print(intro)
