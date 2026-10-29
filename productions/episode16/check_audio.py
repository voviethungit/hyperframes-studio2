import json,subprocess,hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent
src=R/'MASTER_VOICE.mp3';dst=R/'OLD_CHANNEL_16_EXPORT_PENDING_QA.mp4'
assert hashlib.file_digest(src.open('rb'),'sha256').hexdigest()==(R/'master-sha256.txt').read_text().strip()
def read(p,t,d=4):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-t',str(d),'-vn','-ac','1','-ar','44100','-f','f32le','-']),dtype=np.float32)
checks=[]
for t in [0,598,1198,1798,2398,2998,3543]:
 a=read(src,t);b=read(dst,t);n=min(len(a),len(b));a=a[:n];b=b[:n]
 corr=float(np.corrcoef(a,b)[0,1]);gain=float(20*np.log10(np.sqrt(np.mean(b*b))/np.sqrt(np.mean(a*a))))
 checks.append({'time_seconds':t,'samples':n,'correlation':corr,'rms_difference_db':gain})
 assert corr>.98 and abs(gain)<.15,(t,corr,gain)
def count_samples(p):
 proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','44100','-f','s16le','-'],stdout=subprocess.PIPE)
 n=0
 while True:
  block=proc.stdout.read(1024*1024)
  if not block:break
  n+=len(block)
 assert proc.wait()==0
 return n//2
source_samples=count_samples(src);export_samples=count_samples(dst)
assert export_samples>=source_samples-44, (source_samples,export_samples)
assert export_samples-source_samples<2048, (source_samples,export_samples)
(R/'audio-sample-counts.json').write_text(json.dumps({'source_decoded_samples':source_samples,'export_decoded_samples':export_samples,'sample_rate':44100,'difference_samples':export_samples-source_samples,'status':'PASS','note':'AAC may have less than one codec frame of trailing padding; source duration remains authoritative'},indent=2))
(R/'audio-comparison.json').write_text(json.dumps({'status':'PASS','scope':'Decoded PCM comparisons at beginning, joins, and end; AAC is lossy, not bit identical','checks':checks},indent=2));print(json.dumps(checks))
