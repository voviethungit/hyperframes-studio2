import {Audio} from '@remotion/media';
import {AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import data from './Episode16Data.json';

type ShotProps = {image: string; duration: number; motion: string; dissolve: boolean};
const Shot = ({image,duration,motion,dissolve}: ShotProps) => {
 const frame=useCurrentFrame();
 if(image==='episode16/scenes/116.png') return <AbsoluteFill style={{opacity:dissolve?interpolate(frame,[0,18],[0,1],{extrapolateRight:'clamp'}):1}}>
  <Img src={staticFile('episode16/scenes/027.png')} style={{position:'absolute',left:0,top:0,width:'50%',height:'100%',objectFit:'cover',objectPosition:'40% center'}} />
  <Img src={staticFile(image)} style={{position:'absolute',left:'50%',top:0,width:'50%',height:'100%',objectFit:'cover'}} />
 </AbsoluteFill>;
 return <AbsoluteFill style={{opacity: dissolve ? interpolate(frame,[0,18],[0,1],{extrapolateRight:'clamp'}) : 1}}>
  <Img src={staticFile(image)} style={{width:'100%',height:'100%',objectFit:'cover',scale:motion==='static' ? 1.035 : interpolate(frame,[0,Math.min(89,Math.max(1,duration-1))],motion==='pull' ? [1.055,1.035] : [1.035,1.055],{extrapolateRight:'clamp'}),translate:motion==='pan' ? `${interpolate(frame,[0,Math.min(89,Math.max(1,duration-1))],[-9,9],{extrapolateRight:'clamp'})}px 0px` : undefined}} />
 </AbsoluteFill>;
};

// This is an intentionally manifest-driven documentary template. Each entry
// keeps its absolute audio-derived frame boundary, rather than cumulative rounding.
export const Episode16 = () => <AbsoluteFill style={{backgroundColor:'#30291f'}}>
 {data.scenes.map((s,i)=><Sequence key={s.id} name={`Scene ${s.id+1}`} from={s.start} durationInFrames={Math.min(data.total_frames-s.start,s.duration+(i<data.scenes.length-1 && data.scenes[i+1].transition==='dissolve'?18:0))}>
  <Shot image={s.image} duration={s.duration} motion={s.motion} dissolve={s.transition==='dissolve'} />
 </Sequence>)}
 <Audio src={staticFile('episode16/MASTER_VOICE.mp3')} />
</AbsoluteFill>;
