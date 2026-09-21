# OpenAI 安全事件：一张图片之后

Source: https://www.hacktron.ai/blog/hacking-openai

Chinese narrated explainer, 8 slides, 03:28, 1920×1080 at 30 fps. H.264 video and AAC narration, with burned-in Chinese subtitles. Published on Bilibili: https://www.bilibili.com/video/BV1YChi6BEAY

The repository ignores MP4 files, per-slide audio, screenshots, and video intermediates; these remain available in the local workspace.

- video.mp4: finished video
- presentation.html and styles.css: editable reveal.js deck
- output.pdf: one slide per page
- script.json: original Chinese narration
- audio/: MP3 and SRT for each slide
- intro.txt: titles, tags, exact source URL and chapters from rendered segment durations
- thumbnail.png: Qwen-generated cover, 2688×1536
- sources.md: references and attribution scope
- production/verification.json: timing and format checks

Subtitle cue boundaries are interpolated within provider timing anchors. Incident claims are attributed to Hacktron; the report was not independently reproduced. Analogies and defensive recommendations are labeled separately.

To edit slide wording in the browser, run from the md2video repository:

```sh
bun skills/revealjs/scripts/edit-html.js output/hacking-openai-zh/presentation.html
```

Click text, edit, press Escape, then Save. Updated narration requires regenerating audio and video.
