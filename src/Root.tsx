import React from "react";
import { Composition, Folder } from "remotion";
import { Edit, calcEdit, type EditProps } from "./shared/Edit";
import { Outro, OUTRO } from "./shared/Outro";
import { FPS, H, HANDLE, W } from "./shared/style";
import tech from "../themes/tech.json";
import sports from "../themes/sports.json";
import history from "../themes/history.json";

// One folder per theme. A theme is a file in themes/ (song pool, grades, frame, handle, episodes);
// tools/reel.py new <theme> <ep> registers an episode there. A new theme: add its json here.
type Theme = { id: string; handle: string; outro?: boolean; look: { font?: string }; episodes: { id: string; ep: string }[] };
const THEMES = [tech, sports, history] as Theme[];

export const Root: React.FC = () => (
  <>
    {THEMES.map((t) => (
      <Folder key={t.id} name={t.id}>
        {t.episodes.map(({ id, ep }) => (
          <Composition
            key={id}
            id={id}
            component={Edit}
            width={W}
            height={H}
            fps={FPS}
            durationInFrames={FPS * 18}
            defaultProps={{ theme: t.id, ep, handle: t.handle, outro: t.outro, font: t.look.font } as EditProps}
            calculateMetadata={calcEdit}
          />
        ))}
      </Folder>
    ))}
    {/* the end card on its own, to preview or export (docs/endcard.gif) */}
    <Composition id="EndCard" component={Outro} width={W} height={H} fps={FPS} durationInFrames={OUTRO} defaultProps={{ handle: HANDLE }} />
  </>
);
