import json
from pathlib import Path
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent
model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4)
print('MODEL_READY', flush=True)
segments, info = model.transcribe(str(ROOT / 'MASTER_VOICE.mp3'), language='ru',
    word_timestamps=True, vad_filter=True, beam_size=3)
with (ROOT / 'transcript-segments.jsonl').open('w') as out:
    for segment in segments:
        row = {'start': segment.start, 'end': segment.end, 'text': segment.text,
            'words': [{'start': w.start, 'end': w.end, 'word': w.word} for w in segment.words or []]}
        out.write(json.dumps(row, ensure_ascii=False) + '\n')
        out.flush()
        print(round(segment.end, 1), segment.text[:90], flush=True)
print('TRANSCRIPTION_COMPLETE', flush=True)
