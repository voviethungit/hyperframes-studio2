"""Create a delivery copy with peak limiting; preserve original narration master."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
video = ROOT/'OLD_CHANNEL_FINAL_VIDEO.mp4'
if not video.exists():
    video = ROOT.parents[1]/'videos/OLD_CHANNEL_FINAL_VIDEO.mp4'
master = ROOT/'MASTER_VOICE.mp3'
output = ROOT/'OLD_CHANNEL_YOUTUBE_READY.mp4'
assert video.is_file() and master.is_file()
subprocess.run([
    'ffmpeg', '-hide_banner', '-nostdin', '-y', '-v', 'warning',
    '-i', str(video), '-i', str(master), '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'copy', '-af',
    'aresample=192000,alimiter=limit=0.7943282347:attack=5:release=80:level=false:latency=true,aresample=44100',
    '-c:a', 'aac', '-b:a', '192k', '-t', '3433.090612',
    '-movflags', '+faststart', str(output)
], check=True)
print(output)
