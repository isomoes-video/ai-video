import json,re
from pathlib import Path
p=Path(__file__).resolve().parents[1]
slides=[
('一张图片之后', '<p class="kicker">安全事件解读 · 2026 年 9 月</p><h1>一张图片之后，<br>权限走了多远？</h1><p class="lead">OpenAI 论坛事件中的三道边界</p><div class="ribbon"><p>图片解析 → 登录身份 → 连接器权限</p></div><p class="source">依据 Hacktron 研究报告；结合公开安全公告与防御分析</p>'),
('先看发生了什么', '<h2>先看发生了什么</h2><div class="content"><div class="statement"><p class="tag">研究者报告</p><h3>论坛漏洞 + SSO 配置问题</h3><p>形成跨服务的账户访问路径</p></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:28px"><div class="card"><h3>演示的影响</h3><p>经员工 Codex 账户<br>创建内部仓库测试 PR</p></div><div class="card"><h3>证据的边界</h3><p>作者称未读取内部代码<br>潜在访问 ≠ 已证实泄露</p></div></div><p class="source">来源：Hacktron《Hacking OpenAI》；事件叙述为研究者披露</p></div>'),
('第一道边界：文件变成计算', '<h2>第一道边界：文件变成计算</h2><div class="content"><div class="flow"><div><h3>图片上传</h3><p>不可信输入</p></div><p>→</p><div><h3>格式转换</h3><p>ImageMagick</p></div><p>→</p><div><h3>底层解析</h3><p>libheif</p></div></div><div class="statement"><h3>风险藏在“自动处理”里</h3><p>解析器漏洞可能让数据处理变成代码执行</p></div><p class="source">Discourse 公告：GHSA-vhm9-85gw-x335 · CVE-2026-32882</p></div>'),
('第二道边界：登录不是万能钥匙', '<h2>第二道边界：登录不是万能钥匙</h2><div class="content"><p class="lead">以下为防御性类比，并非漏洞协议细节</p><div style="display:grid;grid-template-columns:1fr 1fr;gap:35px"><div class="card"><p class="tag">访客证</p><h3>允许进入论坛</h3><p>只服务于这个应用</p></div><div class="card accent"><p class="tag">机房钥匙</p><h3>访问另一套系统</h3><p>必须独立核验权限</p></div></div><p class="takeaway">共享身份，不应抹去应用之间的权限边界。</p></div>'),
('第三道边界：连接器扩大影响', '<h2>第三道边界：连接器扩大影响</h2><div class="content"><div class="flow"><div><h3>账户</h3><p>谁在请求？</p></div><p>→</p><div><h3>智能体</h3><p>执行什么？</p></div><p>→</p><div><h3>外部工具</h3><p>允许到哪里？</p></div></div><p class="lead">防御分析：影响范围取决于已经授予的权限</p><div class="ribbon"><p>按仓库授权 · 区分读写 · 可撤销 · 可审计</p></div></div>'),
('修复要落到正在运行的环境', '<h2>修复要落到正在运行的环境</h2><div class="content"><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px"><div class="card"><p class="number">01</p><h3>更新依赖</h3><p>核对安全公告<br>与发行版补丁</p></div><div class="card"><p class="number">02</p><h3>重建部署</h3><p>替换旧镜像<br>确认运行版本</p></div><div class="card"><p class="number">03</p><h3>隔离处理</h3><p>限制格式与资源<br>缩小进程权限</p></div></div><p class="takeaway">Discourse 公告要求重建，并增加图片处理沙箱。</p><p class="source">来源：Discourse 安全公告；ImageMagick 安全策略文档</p></div>'),
('AI 改变了成本，也改变了节奏', '<h2>AI 改变了成本，也改变了节奏</h2><div class="content"><div class="statement"><p class="tag">研究者观察</p><h3>模型帮助推进漏洞利用开发</h3><p>仍有专业人员提供方向与判断</p></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:28px"><div><h3>不能据此推断</h3><p>所有目标都同样容易<br>或所有步骤都能自主完成</p></div><div><h3>值得提前准备</h3><p>缩短补丁部署周期<br>关注解析器异常与权限使用</p></div></div></div>'),
('把每一次跨界都当成一次授权', '<p class="kicker">结语 · 防御分析</p><h1>把每一次跨界，<br>都当成一次授权。</h1><div class="content"><p class="lead">输入要隔离，身份要限域，工具要限权。</p><div class="ribbon"><p>从图片处理链开始，检查通向关键资源的整条路径。</p></div><p class="source">原文：hacktron.ai/blog/hacking-openai<br>补充：Discourse 安全公告 · ImageMagick 安全策略</p></div>')]
narr=[
'一张上传到论坛的图片，为什么会和内部代码仓库扯上关系？这期视频依据 Hacktron 的研究报告，梳理这条跨越图片处理、登录身份和工具权限的路径。接着，我们用几个防御性的例子，看看系统应该在哪里把它截断。',
'先把事实和影响分开。研究者报告，他们把论坛的图片解析漏洞与 OpenAI 的单点登录配置问题串联起来，通过员工的 Codex 账户创建了内部仓库测试 PR。作者称没有读取内部代码。因此，证明可以执行某个操作，并不等于证明所有资料都已泄露。',
'从入口看，图片其实需要被程序解析。Discourse 的安全公告确认，底层 libheif 漏洞可以经图片上传触发远程代码执行。可以把解析器想成拆包机器：外包装看起来只是图片，里面的结构仍然可能让机器出错。上传检查、格式转换和底层依赖，都属于同一条处理链。',
'拿到论坛环境之后，为什么还能继续跨越系统？报告指出，另一环是单点登录配置问题。这里用一个类比来理解防御原则，而不是还原漏洞细节。论坛访客证只应允许进入论坛，不能自动变成机房钥匙。一个应用受到影响时，其他应用仍然需要独立核验请求对应的身份和权限。',
'再往后，就是连接器带来的权限延伸。以下是我们的防御分析：智能体账户能够影响多少资源，取决于它连接了什么工具，以及工具授予了多少权限。例如，只读访问一个测试仓库，与能够修改整个组织，后果完全不同。按任务收窄授权、区分读写，并保留撤销和审计能力，可以减少账户失守后的影响。',
'因此，修复也要沿着整条路径走。Discourse 公告要求重建部署，让修补后的依赖进入运行环境，并增加图片处理沙箱。ImageMagick 的安全策略还可以限制格式、资源和处理能力。实际检查时，不要只确认补丁已经发布，还要确认线上进程使用了什么镜像，哪些格式仍可解析，以及处理失败后会留下什么记录。',
'这篇报告的另一个主题是 AI。作者描述了模型帮助推进漏洞利用开发，同时也强调专业人员的指导仍然重要。这样的案例不能直接变成所有模型、所有目标的能力排名。对防守方更有用的启发是：把修补和验证做得更快，并把图片处理异常与权限操作记录联系起来观察，而不是依赖攻击工作足够困难。',
'回到开头，真正需要关注的是，输入如何一步步触达关键资源。我们可以从一次图片上传开始，画出它经过的进程、身份系统和工具授权，再逐段确认隔离措施。输入要隔离，身份要限域，工具要限权。把每一次跨界都当成一次授权，才有机会在其中一环失守时，保住后面的系统。']
html=(p/'presentation.html').read_text().replace('lang="en"','lang="zh-CN"')
for i,(title,body) in enumerate(slides,1):
 id='title' if i==1 else f'slide-{i}'
 html=re.sub(r'<section id="'+id+r'"[^>]*>.*?</section>',f'<section id="{id}">{body}<p class="folio">安全边界 / {i:02d}</p></section>',html,flags=re.S)
html=html.replace('controls: true','controls: false').replace('progress: true','progress: false').replace("transition: 'slide'","transition: 'none'")
(p/'presentation.html').write_text(html)
(p/'script.json').write_text(json.dumps([dict(slide_number=i,narration=s) for i,s in enumerate(narr,1)],ensure_ascii=False,indent=2)+'\n')
(p/'sources.md').write_text('Source: https://www.hacktron.ai/blog/hacking-openai\n\nSupplement: https://github.com/discourse/discourse/security/advisories/GHSA-vhm9-85gw-x335\nSupplement: https://imagemagick.org/security-policy/\n\nAccessed: 2026-09-21. Incident and model capability claims are attributed to the researchers, not independently reproduced. Slides 4–5 and the closing recommendation are explanatory analogies and defensive analysis.\n')
