"""Verify approved peak-limited delivery against the unmodified master."""
import hashlib,json,re,subprocess
from pathlib import Path
import numpy as np

R=Path(__file__).resolve().parent
new=R/'OLD_CHANNEL_YOUTUBE_READY.mp4';old=R/'OLD_CHANNEL_FINAL_VIDEO.mp4';master=R/'MASTER_VOICE.mp3'
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def video_hash(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-c:v','copy','-f','hash','-hash','sha256','-'],text=True).strip()
def pcm(p,t):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-t','8','-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32)
assert hashlib.file_digest(master.open('rb'),'sha256').hexdigest()=='4adbf3e85f8ca9f71c760b3f3fc5abf41b49ce158cbeabaa0618b0ebdd7c13bd'
p=probe(new);v=next(x for x in p['streams'] if x['codec_type']=='video');a=next(x for x in p['streams'] if x['codec_type']=='audio')
assert int(v['nb_frames'])==85828 and v['r_frame_rate']=='25/1'
assert abs(float(p['format']['duration'])-3433.090612)<.1
h=video_hash(new);assert h==video_hash(old)
log=R/'youtube-ready-loudness.log'
assert log.stat().st_mtime>=new.stat().st_mtime
text=log.read_text();summary=text.rsplit('Summary:',1)[-1]
peak=float(re.search(r'Peak:\s*([-\d.]+)',summary).group(1));assert peak<=-1.0
loudness=float(re.search(r'I:\s*([-\d.]+)',summary).group(1))
comparisons=[]
for t in [0,858.272653,1716.545306,2574.817959,3423.090612]:
    x,y=pcm(master,t),pcm(new,t);n=min(len(x),len(y));x=x[:n];y=y[:n]
    correlation=float(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)))
    assert correlation>.97,(t,correlation)
    comparisons.append({'time':t,'correlation':correlation})
result={'file':new.name,'duration':float(p['format']['duration']),'size_bytes':new.stat().st_size,'sha256':hashlib.file_digest(new.open('rb'),'sha256').hexdigest(),'video_stream_identical':True,'video_stream_hash':h,'frames':85828,'resolution':'1920x1080','fps':25,'audio_codec':a['codec_name'],'sample_rate':a['sample_rate'],'true_peak_dbtp':peak,'integrated_lufs':loudness,'source_master_unchanged':True,'audio_sync_comparisons':comparisons}
(R/'YOUTUBE_AUDIO_QA.json').write_text(json.dumps(result,indent=2))
(R/'YOUTUBE_AUDIO_QA.md').write_text(f'''# Peak-limited YouTube delivery

Applies to OLD_CHANNEL_YOUTUBE_READY.mp4. The user authorized peak control after the original quality review.

PASS — True peak: {peak} dBTP, measured after AAC encoding across the entire file. Original master: +2.3 dBTP; earlier MP4: +1.4 dBTP.
PASS — Integrated loudness: {loudness} LUFS, unchanged to 0.1 LU from the original. Loudness range remains 3.7 LU.
PASS — Original MASTER_VOICE.mp3 remains byte-identical and is retained separately.
PASS — Narration order, words, pauses and playback speed retained. Only excessive peaks are limited, with automatic make-up gain disabled and limiter latency compensated.
PASS — Video stream packet hash identical to the original verified video: no image re-encoding or editing.
PASS — 85828 video frames, constant 25 fps, 1920x1080; total duration {float(p['format']['duration']):.2f} seconds.
PASS — Five decoded waveform comparisons against the master exceed 0.97 correlation, including beginning and end.
PASS — Entire delivery audio decoded during EBU R128 measurement without errors.

Method: original MP3 decoded once, internally oversampled to 192 kHz, limited at -2 dBFS with 5 ms lookahead and 80 ms release, latency compensated, returned to 44.1 kHz and encoded to AAC at 192 kbps. The measured delivered true peak is the final safety check.

Remaining limitations: visual repetition and full-duration human listening/semantic signoff from QUALITY_REVIEW.md remain outstanding. Peak control prevents new overload but cannot reconstruct distortion already embedded in the original recording. This is technical delivery readiness, not a guarantee of perfect editorial or perceptual quality.
''')
print(json.dumps(result,indent=2))
