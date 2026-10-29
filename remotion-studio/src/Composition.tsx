import { Audio } from "@remotion/media";
import { AbsoluteFill, Composition, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export const MyComposition = () => {
  return (
    <Composition
      id="MyComp"
      component={MyComponent}
      durationInFrames={75}
      fps={25}
      width={1920}
      height={1080}
    />
  );
};

const StatusTitle = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return <div style={{ opacity: interpolate(frame, [0, fps], [0.2, 1], { extrapolateRight: "clamp" }), color: "#ffffff", fontFamily: "sans-serif", fontSize: 76, fontWeight: 700 }}>Remotion ready</div>;
};

export const MyComponent: React.FC = () => {
  return <AbsoluteFill style={{ backgroundColor: "#111b29" }}>
    <Img src={staticFile("check-background.png")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
    <AbsoluteFill style={{ backgroundColor: "rgba(17,27,41,0.45)", justifyContent: "center", alignItems: "center" }}><StatusTitle /></AbsoluteFill>
    <Audio src={staticFile("check-tone.wav")} />
  </AbsoluteFill>;
};
