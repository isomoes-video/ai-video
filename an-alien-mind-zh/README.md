# 异质智能：如何守住人的选择权

Source: https://openai.com/index/an-alien-mind/

Published video: https://www.bilibili.com/video/BV12Eb56tEjC

Chinese narrated overview with eight slides, short burned subtitles, a cover and chapter metadata. Teaching examples are labeled separately from the author's claims.

- `video.mp4`: final 1080p, 30 fps video.
- `output.pdf`: eight-page slide deck.
- `presentation.html` and `styles.css`: editable Reveal.js source.
- `script.json`: unchanged narration used by the speech service.
- `intro.txt`: bilingual titles, source link, tags and rendered chapter times.
- `thumbnail.png`: one Qwen-generated cover.
- `production/verification.json`: duration, subtitle and media validation.

## Edit slide wording in the browser

From the project root:

```sh
bun /home/isomoes/code/py/md2video/skills/revealjs/scripts/edit-html.js /home/isomoes/code/py/md2video/output/an-alien-mind-zh/presentation.html
```

Click text to edit, press Escape to deselect, then click Save. Stop the server with Ctrl+C. Re-export and render after edits to update the PDF and video.

## Reproduce audio and video

The helper imports the existing repository TTS engine and preserves provider word timestamps; it does not replace the engine. The formatter restores exact script spelling, which the provider may normalize in its timestamp output.

```sh
uv run output/an-alien-mind-zh/production/narrate.py --script output/an-alien-mind-zh/script.json --overwrite
python3 output/an-alien-mind-zh/production/reformat_srt.py
uv run scripts/combine_video.py --pdf output/an-alien-mind-zh/output.pdf --subtitles burn --overwrite
uv run output/an-alien-mind-zh/production/finalize_video.py
python3 output/an-alien-mind-zh/production/finish_metadata.py
python3 output/an-alien-mind-zh/production/verify.py
```

Finalization rounds short inter-slide holds up to a full 30 fps frame and normalizes stream starts. Source audio is retained in full.

The `Output:` link in `intro.txt` follows the repository's required archive convention. The finished video was uploaded to Bilibili at the link above.
