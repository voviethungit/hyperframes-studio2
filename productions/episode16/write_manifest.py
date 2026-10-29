import csv,json
from pathlib import Path
R=Path(__file__).resolve().parent;T=json.loads((R/'timeline.json').read_text());plans=json.loads((R/'all-image-prompts.json').read_text());reviews=json.loads((R/'image-review.json').read_text()) if (R/'image-review.json').exists() else {}
details=json.loads((R/'production-plan.json').read_text())
fields=['scene','start_seconds','end_seconds','start_frame','end_frame','exact_Russian_narration','English_visual_description','historical_setting','season_time','character_reference','wardrobe_tools','physical_state_start','physical_state_end','camera','transition','image','standalone_prompt','generation_status','review_status']
with (R/'OLD_CHANNEL_16_SCENE_MANIFEST.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(fields)
 for s,plan in zip(T['scenes'],plans):
  p=R/'assets/scenes'/f"{s['id']:03d}.json";m=json.loads(p.read_text()) if p.exists() else {}
  w.writerow([s['id']+1,s['start']/30,s['end']/30,s['start'],s['end'],s['narration'],plan['action'],details[s['id']]['historical_setting'],details[s['id']]['season_time'],plan['reference'],'Specified explicitly in standalone image prompt','Single coherent depicted state; see action','Same physical state, camera may move; no simulated limb animation',s['motion'],s['transition'],s['image'],m.get('prompt',plan['prompt']),m.get('status','PENDING'),reviews.get(str(s['id']),{}).get('status','NOT VERIFIED')])
print('Complete time-aligned manifest written:',len(T['scenes']))
