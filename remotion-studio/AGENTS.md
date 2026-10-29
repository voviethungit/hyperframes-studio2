# Remotion workspace

Read `../.agents/skills/remotion-best-practices/SKILL.md` before Remotion work and follow its relevant reference pages. The official skill is vendored at repository scope for Codex.

Work in this directory. Use `npm ci --cache /workspace/.npm-cache` to restore the exact dependency lock. `npm run dev` starts Studio on port 3000. `npm run lint` checks ESLint and TypeScript. `npm run build` bundles the project. `npm run render` exports the three-second environment check to `out/remotion-check.mp4` using `/usr/bin/chromium` and two render workers.

This is an isolated cloud task; use the current checkout. Create a worktree only if explicitly requested. Read `SETUP.md` for startup, readiness and source provenance. The historical production is in `../productions/night-city`.
