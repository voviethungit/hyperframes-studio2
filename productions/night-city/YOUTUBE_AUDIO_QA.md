# Peak-limited YouTube delivery

Applies to OLD_CHANNEL_YOUTUBE_READY.mp4. The user authorized peak control after the original quality review.

PASS — True peak: -1.9 dBTP, measured after AAC encoding across the entire file. Original master: +2.3 dBTP; earlier MP4: +1.4 dBTP.
PASS — Integrated loudness: -20.4 LUFS, unchanged to 0.1 LU from the original. Loudness range remains 3.7 LU.
PASS — Original MASTER_VOICE.mp3 remains byte-identical and is retained separately.
PASS — Narration order, words, pauses and playback speed retained. Only excessive peaks are limited, with automatic make-up gain disabled and limiter latency compensated.
PASS — Video stream packet hash identical to the original verified video: no image re-encoding or editing.
PASS — 85828 video frames, constant 25 fps, 1920x1080; total duration 3433.12 seconds.
PASS — Five decoded waveform comparisons against the master exceed 0.97 correlation, including beginning and end.
PASS — Entire delivery audio decoded during EBU R128 measurement without errors.

Method: original MP3 decoded once, internally oversampled to 192 kHz, limited at -2 dBFS with 5 ms lookahead and 80 ms release, latency compensated, returned to 44.1 kHz and encoded to AAC at 192 kbps. The measured delivered true peak is the final safety check.

Remaining limitations: visual repetition and full-duration human listening/semantic signoff from QUALITY_REVIEW.md remain outstanding. Peak control prevents new overload but cannot reconstruct distortion already embedded in the original recording. This is technical delivery readiness, not a guarantee of perfect editorial or perceptual quality.
