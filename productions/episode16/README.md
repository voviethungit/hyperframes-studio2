# OLD CHANNEL 16

Channel: Скучная история для сна
Episode: Как люди стирали одежду без стиральных машин 200 лет назад

The six uploaded narration chunks are ordered 00–05. `MASTER_VOICE.mp3` is a packet-preserving FFmpeg concat with no gain, pitch, speed or silence processing. Measured duration:3548.551837 seconds. `audio-assembly-qa.json` records packet sequence verification. Sources remain in `assets/source-audio/` in the delivery copy.

`OLD_CHANNEL_16_FINAL.mp4` is only created after verification. Consult `OLD_CHANNEL_16_QA_REPORT.txt` and `export-verification.json` for measured results and limits. The film uses123 semantic paragraph scenes with absolute audio-derived frame boundaries at30fps. Timing uses multilingual Whisper ASR anchors and interpolation against the supplied script; it is not word-perfect forced alignment.

Verified delivery:59:08.566667,106457 frames,1920x1080, constant30fps,H.264/yuv420p and mono44.1kHzAAC. Size331858020 bytes. Original narration level retained at−21.7LUFS, true peak−1.2dBTP.

## Edit and render

The editable application is at `../../remotion-studio`, composition `OldChannel16`. Install with `npm ci`, then run `npm run dev`. The project uses system Chromium at `/usr/bin/chromium` in this environment.

A conventional complete native render is:

```bash
npx remotion render src/index.ts OldChannel16 out/OLD_CHANNEL_16_FINAL.mp4 --browser-executable=/usr/bin/chromium --codec=h264 --pixel-format=yuv420p --audio-codec=aac
```

Run this from `remotion-studio`. The production export uses `render_cached.py`: capture the first90 native Remotion frames of each scene, encode them, then repeat the mathematically constant final state through the remaining scene frames at CFR30. Static, pull, pan and push end frames were checked against native Remotion output pixel-for-pixel. Video segments are joined without re-encoding, then the entire unchanged MP3 is encoded once continuously to AAC. This prevents repeated lossy audio conversion and retains every narration pause. Camera changes happen over the first3seconds, followed by quiet holds. No human movement is synthesized.

`assets/scenes` contains all accepted artwork plus the actual generation prompts in adjacent JSON files. `all-image-prompts.json`, `production-plan.json`, the CSV manifest, `DESIGN.md` and `assets/references` preserve the production plan and appearance references. Contact sheets and `image-review.json` preserve the visual review record. Original rejected variants were retained in the working production folder; they are excluded from the final film.

Image generation was genuinely performed through the available image-generation tool. Requested native resolution was2560x1440; actual returns are approximately1672px wide and are scaled/cropped to1080p in Remotion. This limit is disclosed in the QA report. No stock photo substitutes, placeholder art, commercial music or added character speech were used.

A clean decode and sampled PCM comparisons are technical evidence, not a claim that a human listened to every second or that an external historian certified every object. See the NOT VERIFIED entries in the QA report.
