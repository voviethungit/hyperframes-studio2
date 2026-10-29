# Remotion development environment

Installed and validated with Node 24.19.0, system Chromium 154 and FFmpeg 7.1.5.
Remotion core, CLI, media, transitions and ESLint integration are all pinned to 4.0.539. React and React DOM are 19.2.3.

## Commands

Run from `/workspace/hyperframes-studio2/remotion-studio`:

```bash
npm ci --cache /workspace/.npm-cache --no-audit --no-fund
npm run dev
```

Studio uses port 3000. A local readiness request is `curl --fail http://127.0.0.1:3000/`; expect the Studio HTML page. Start it again in a future task because processes do not survive snapshots. Use the existing isolated checkout, without creating a Git worktree unless requested.

```bash
npm run lint
npm run build
npm run compositions
npm run render
ffprobe -v error -show_streams -show_format out/remotion-check.mp4
```

The sample `MyComp` is an environment check: 1920x1080, 25 fps, 75 frames, three seconds, animated title, an existing historical background and a quiet synthetic test tone. It is separate from the finished long-form film. Output is ignored by Git. The Chromium path is configured explicitly, so rendering requires no additional browser download.

The official Codex skill lives at `../.agents/skills/remotion-best-practices/SKILL.md` relative to this directory. `../skills-lock.json` records the upstream skill identity. New Codex sessions can discover the skill; the current session has read it directly.

## Provenance

- Skill source: https://github.com/remotion-dev/skills, inspected at commit `30d4553ecd46fbc5212fd0ff006ae43af522158b`; skill version 4.0.539.
- Blank scaffold source: https://github.com/remotion-dev/template-empty, commit `bad1be9984b08a9ee3f3eee1df98765caa04ca11`.
- Dependencies are restored through the committed npm lockfile. The template was copied without its Git metadata, so this workspace belongs to the existing repository.
