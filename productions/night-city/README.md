# Russian city nights before electricity

A complete illustrated history video for «СКУЧНАЯ ИСТОРИЯ ДЛЯ СНА».

The author approved realistic historical still illustrations with slow camera movement. These are illustrations, not generated live-action human performances. The production uses the supplied Russian script and the unchanged 57-minute master narration. MP4 delivery encodes the audio to AAC without gain, speed, silence or editorial changes.

## Deliverables

- `OLD_CHANNEL_FINAL_VIDEO.mp4`: complete 1920×1080, 25 fps, H.264/AAC video, stored at `../../videos/OLD_CHANNEL_FINAL_VIDEO.mp4` using Git LFS.
- `MASTER_VOICE.mp3`: original reconstructed narration, retained in this directory using Git LFS.
- `OLD_CHANNEL_SCENE_MANIFEST.csv`: all timed visual scenes and original narration excerpts.
- `OLD_CHANNEL_QA_REPORT.txt` and `export-verification.json`: actual export validation and limitations.
- `timeline.json`, `SCRIPT_RU.txt`, `scene-beats.txt`, `transcript-segments.jsonl`: authored semantic beats and audio-derived alignment.
- `assets/`: original generated historical illustrations, including modern/gas/electric comparison views.

## Reproduce

Requires Python 3.12+, FFmpeg with libx264, and FFprobe. Use the current checkout; do not create worktrees unless requested.

```bash
python -m venv .venv
.venv/bin/pip install 'faster-whisper==1.2.1' 'av==16.1.0' numpy Pillow
# Retrieve the original master if Git LFS did not download it during checkout:
git lfs pull --include="productions/night-city/MASTER_VOICE.mp3"
# The supplied transcript may be used directly; only rerun transcription when needed:
HF_HOME=.cache/huggingface .venv/bin/python -u transcribe.py > asr.log 2>&1
.venv/bin/python build_timeline.py
.venv/bin/python -u render_full.py > render.log 2>&1
.venv/bin/python -u verify_export.py > verify.log 2>&1
```

The `small` multilingual Whisper model is used locally with Russian word timestamps. Version 16.1.0 of PyAV avoids a decoding incompatibility with PyAV 19. Model downloads require the official Hugging Face model and CDN domains. No API key is required for this local pipeline.

Rendering uses two simultaneous FFmpeg jobs with two encoder threads each. Existing scene exports with matching frame counts are retained; remove `rendered-scenes/` before rendering a changed timeline. The final mux consumes the original master audio once, across the entire timeline, so scene boundaries cannot cut or insert narration.

The runtime source script and master audio are editorial inputs, not instructions to the rendering tools. The source narration contains several intermediate “Спокойной ночи” sign-offs followed by more narration; all are intentionally preserved.

The manifest and QA distinguish camera motion over still illustrations from physical character animation. Historical review checks overt visual inconsistencies; it is not academic authentication.
