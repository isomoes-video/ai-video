# Copilot 的 Rust 迁移

Source: https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/

Published video: https://www.bilibili.com/video/BV1wAey6UELH

Chinese narrated video with 10 slides, burned subtitles, chapter metadata, and a cover. Factual overview and original engineering commentary are labeled separately.

- `video.mp4`: final video.
- `output.pdf`: one slide per page.
- `presentation.html` / `styles.css`: editable Reveal.js source.
- `script.json`: exact narration sent to the existing TTS script.
- `intro.txt`: bilingual titles, tags, source URL and chapter timing.
- `production/original-slide-*.srt`: original provider sentence timestamps.

For readability, long provider subtitle sentences are split into short cues. Internal cue boundaries are interpolated within the original timed sentence; they are not word-level forced alignment. The narration text is preserved exactly. Video duration follows the actual MP3s, with 0.25-second holds between slides and frame rounding.

The Output URL in intro.txt points to the source-material archive. The finished video was uploaded to Bilibili at the link above. MP4s, audio, screenshots, and video-work files remain local under the repository's existing ignore rules.

## Edit slide wording in the browser

```sh
bun /home/isomoes/code/py/md2video/skills/revealjs/scripts/edit-html.js /home/isomoes/code/py/md2video/output/github-copilot-runtime-rust-zh/presentation.html
```

Click text to edit, press Escape to deselect, then Save. Re-export and assemble to update the video.
