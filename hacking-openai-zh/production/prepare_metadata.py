import json,re,subprocess,math
from pathlib import Path
w=Path(__file__).resolve().parents[1]
def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]))
def millis(s):
    h,m,t=s.replace(',', '.').split(':');return round((int(h)*3600+int(m)*60+float(t))*1000)
def stamp(n):
    h,n=divmod(n,3600000);m,n=divmod(n,60000);s,n=divmod(n,1000);return f'{h:02}:{m:02}:{s:02},{n:03}'
def weight(s):return sum(0.5 if ord(c)<128 else 1 for c in s)
entries=json.loads((w/'script.json').read_text())
starts=[];cursor=0
for item in entries:
    n=item['slide_number'];p=w/'audio'/f'slide-{n:02}.srt'
    original=w/'production'/f'original-slide-{n:02}.srt'
    if not original.exists():original.write_text(p.read_text())
    parts=re.split(r'\n\s*\n',original.read_text().strip());new=[];alltext=''
    for part in parts:
        lines=part.splitlines();a,b=lines[1].split(' --> ');a,b=millis(a),millis(b);txt=''.join(lines[2:]);alltext+=txt
        tokens=re.findall(r'[A-Za-z0-9]+(?:[.\-][A-Za-z0-9]+)*|.',txt)
        chunks=[];current=''
        for token in tokens:
            if weight(current+token)>26 and current:
                chunks.append(current);current=''
            current+=token
            if token in '，。？！；：' and weight(current)>=8:
                chunks.append(current);current=''
        if current:chunks.append(current)
        total=sum(weight(x) for x in chunks);acc=0
        for chunk in chunks:
            begin=a+round((b-a)*acc/total);acc+=weight(chunk);end=a+round((b-a)*acc/total)
            new.append(f'{len(new)+1}\n{stamp(begin)} --> {stamp(end)}\n{chunk}\n')
    assert re.sub(r'\s','',alltext)==re.sub(r'\s','',item['narration']),f'Text mismatch {n}'
    p.write_text('\n'.join(new))
    starts.append(cursor)
    segment=w/'video-work'/'segments'/f'slide-{n:02}.mp4'
    audio=float(probe(w/'audio'/f'slide-{n:02}.mp3')['format']['duration'])
    if segment.exists():cursor+=float(probe(segment)['format']['duration'])
    else:cursor+=math.ceil((audio+(0.25 if n<len(entries) else 0))*30)/30
summary='本片依据 Hacktron 的公开研究报告，概述 OpenAI 论坛事件，并结合 Discourse 安全公告解释图片解析风险与修补要求。视频通过防御性类比，分析单点登录、智能体连接器和跨系统授权的边界，区分研究者演示的访问能力与尚未证实的潜在影响，最后提出隔离输入、收窄权限和验证实际部署的检查思路。'
lines=['中文标题：OpenAI 安全事件：一张图片之后','English Title: The OpenAI Security Incident: Beyond an Image Upload','标签：OpenAI，网络安全，单点登录，AI安全，软件供应链','', 'Source: https://www.hacktron.ai/blog/hacking-openai','Output: https://github.com/isomoes-video/ai-video/tree/main/hacking-openai-zh','',summary,'']
for n,title in [(1,'开场'),(2,'事件'),(3,'图片'),(4,'身份'),(5,'权限'),(6,'修复'),(7,'AI'),(8,'结语')]:
    t=int(starts[n-1]);lines.append(f'{t//60:02}:{t%60:02}  {title}')
(w/'intro.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps({'slides':len(entries),'estimated_duration':cursor,'starts':starts},ensure_ascii=False))
