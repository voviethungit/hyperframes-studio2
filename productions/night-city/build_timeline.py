"""Align the supplied script to observed ASR words; apply authored semantic beats."""
import bisect, csv, difflib, json, math, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FPS = 25
def norm(s):
    return re.sub(r'[^\w]', '', s.lower().replace('ё', 'е'))
paragraphs = [p.strip() for p in (ROOT/'SCRIPT_RU.txt').read_text().split('\n\n') if p.strip()]
script_words, paragraph_offsets = [], []
for paragraph in paragraphs:
    paragraph_offsets.append(len(script_words))
    script_words.extend(norm(w) for w in re.findall(r'\w+', paragraph))
asr = [json.loads(line) for line in (ROOT/'transcript-segments.jsonl').read_text().splitlines()]
words = [w for s in asr for w in s['words'] if norm(w['word'])]
observed = [norm(w['word']) for w in words]
matches = difflib.SequenceMatcher(None, script_words, observed, autojunk=False)
anchors = {}
for block in matches.get_matching_blocks():
    for k in range(block.size):
        anchors[block.a+k] = words[block.b+k]['start']
coverage = len(anchors)/len(script_words)
assert coverage > .84, f'Low script/ASR exact word coverage: {coverage:.3f}'
keys = sorted(anchors)
def stamp(index):
    if index in anchors: return anchors[index]
    k = bisect.bisect_left(keys, index)
    if k == 0: return anchors[keys[0]]
    if k == len(keys): return words[-1]['end']
    a, b = keys[k-1], keys[k]
    return anchors[a] + (anchors[b]-anchors[a])*(index-a)/(b-a)
audio = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(ROOT/'MASTER_VOICE.mp3')]))
duration = float(audio['format']['duration'])
assert words[-1]['end'] >= duration-5, 'Transcript does not reach narration end'
total_frames = math.ceil(duration*FPS)
beats = [(int(line.split()[0]), line.split()[1]) for line in (ROOT/'scene-beats.txt').read_text().splitlines() if line.strip()]
assert beats[0][0] == 0 and all(a[0]<b[0] for a,b in zip(beats,beats[1:]))
raw = []
for i,(p,asset) in enumerate(beats):
    next_p = beats[i+1][0] if i+1<len(beats) else len(paragraphs)
    start = max(0,round(stamp(paragraph_offsets[p])*FPS)) if i else 0
    end = round(stamp(paragraph_offsets[next_p])*FPS) if next_p<len(paragraphs) else total_frames
    raw.append(dict(p0=p,p1=next_p,asset=asset,start_frame=start,end_frame=end))
# Merge very short list items into their enclosing semantic montage, rather than
# cutting at each one-word paragraph. Select the longest-supported subject.
scenes=[]; pending=[]
for item in raw:
    pending.append(item)
    frames=pending[-1]['end_frame']-pending[0]['start_frame']
    if frames < 125 and item is not raw[-1]: continue
    best=max(pending,key=lambda x:x['end_frame']-x['start_frame'])
    scene=dict(best)
    scene.update(p0=pending[0]['p0'],p1=pending[-1]['p1'],start_frame=pending[0]['start_frame'],end_frame=pending[-1]['end_frame'])
    if scenes and scene['asset']==scenes[-1]['asset'] and scene['end_frame']-scenes[-1]['start_frame']<750:
        scenes[-1].update(p1=scene['p1'],end_frame=scene['end_frame'])
    else: scenes.append(scene)
    pending=[]
inventory={x['id']:x for x in json.loads((ROOT/'asset-inventory.json').read_text())}
details=json.loads((ROOT/'asset-details.json').read_text())
for i,s in enumerate(scenes):
    s.update(number=i+1,start=s['start_frame']/FPS,end=s['end_frame']/FPS,
        duration=(s['end_frame']-s['start_frame'])/FPS,
        narration='\n\n'.join(paragraphs[s['p0']:s['p1']]),
        description=inventory[s['asset']]['description'],camera=['slow push in','slow pull back','gentle pan right','gentle pan left'][i%4])
    assert (ROOT/'assets'/(s['asset']+'.png')).is_file()
    assert s['end_frame']>s['start_frame']
    if i: assert s['start_frame']==scenes[i-1]['end_frame']
    s['transition']='gentle dissolve' if i and scenes[i-1]['asset']!=s['asset'] else 'continuous illustration'
assert scenes[0]['start_frame']==0 and scenes[-1]['end_frame']==total_frames
timeline=dict(fps=FPS,audio_duration=duration,total_frames=total_frames,
    alignment_exact_word_coverage=coverage,script_word_count=len(script_words),asr_word_count=len(words),scenes=scenes)
(ROOT/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2))
fields=['Scene number','Start time','End time','Duration','Exact Russian narration excerpt','English description of visual','Historical period','Location','Characters','Character identity notes','Wardrobe notes','Important props','Starting physical state','Action','Ending physical state','Camera framing','Camera movement','Generation asset ID','Continuity link to previous scene','Continuity link to next scene','Generation status','Regeneration count']
with (ROOT/'OLD_CHANNEL_SCENE_MANIFEST.csv').open('w',encoding='utf-8-sig',newline='') as out:
    writer=csv.writer(out,lineterminator='\n');writer.writerow(fields)
    for i,s in enumerate(scenes):
        era='present day' if s['asset']=='modern' else 'circa 1900' if s['asset']=='electric' else 'circa 1870' if s['asset']=='gas' else 'circa 1835'
        character,wardrobe,props,location=details[s['asset']]
        writer.writerow([s['number'],s['start'],s['end'],s['duration'],s['narration'],s['description'],era,location,character,'Reuse same image for recognizable recurring portrait; independent illustrative viewpoints between different images',wardrobe,props,'Illustrated state shown in the asset','Camera motion over a still illustration; narration unchanged','Same depicted physical state; no object animation','Wide/medium historical illustration',s['camera'],s['asset'],f'Scene {i}: illustrative view change; no implied physical-action cut' if i else 'Audio begins at 0',f'Scene {i+2}: illustrative view change' if i+1<len(scenes) else 'Original narration end','Generated illustration; camera rendering pending',0])
(ROOT/'alignment-summary.json').write_text(json.dumps({k:v for k,v in timeline.items() if k!='scenes'},indent=2))
print(json.dumps({k:v for k,v in timeline.items() if k!='scenes'},indent=2))
print('Scenes:',len(scenes),'Longest:',max(s['duration'] for s in scenes))
