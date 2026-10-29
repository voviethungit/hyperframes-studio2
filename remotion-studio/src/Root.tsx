import { MyComposition } from "./Composition";
import {Composition} from 'remotion';
import {Episode16} from './Episode16';
import episode16 from './Episode16Data.json';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <MyComposition />
      <Composition id="OldChannel16" component={Episode16} durationInFrames={episode16.total_frames} fps={30} width={1920} height={1080} />
    </>
  );
};
