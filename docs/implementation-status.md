# Implementation Status & Documentation Readiness

This page separates repository observations from proposed capabilities and review-gated science.

## Verified repository configuration

The root `package.json` defines:
- `npm run dev` — Vite development server.
- `npm run build` — Vite production build.
- `npm run lint` — oxlint.
- `npm run preview` — Vite preview server.

There is no root `test` or `typecheck` script in the manifest reviewed for this documentation update.

The Unity staging script expects a Unity export directory containing a `Build/` folder with the loader, data, framework and WASM files (or Brotli-compressed non-loader assets). It writes staged assets to `public/Build/`, which is ignored by Git.

## Implemented versus proposed

| Area | Evidence/status |
|---|---|
| React/Vite application | Present in repository; build must be verified in CI or a clean environment |
| Unity WebGL campaign | Unity project and staging instructions are present; generated WebGL build is ignored and must be supplied/staged separately |
| TypeScript simulation engine | Engine source and package-level documentation are present; run its own package checks |
| 2D practice mode | Described in project and Unity integration notes |
| Python data pipeline | Architecture/documentation describes the pipeline; verify its current branch output and generated fixture before claiming end-to-end ingestion |
| Three science emergency scenarios | Notion explicitly says they are not all implemented merely because a generic scenario registry exists |
| React–Unity event contract | Draft; exact event names, payload schemas and lifecycle behavior require confirmation |
| Scientific parameter set | Needs Review; mock values are not validated science |

## Release checks still required

- [ ] Clean-clone `npm ci`.
- [ ] Root production build.
- [ ] Root lint.
- [ ] Engine-specific tests and typecheck.
- [ ] Unity WebGL export staging and browser smoke test.
- [ ] Confirm WebAssembly MIME type on deployment.
- [ ] Test 2D mode without WebGL.
- [ ] Verify Python-generated configuration against the actual TypeScript loader.
- [ ] Verify no secrets or local machine paths are committed.
- [ ] Verify public demo in a fresh browser session.
- [ ] Reconcile screenshots/demo recording with the code being submitted.

Do not claim these checks passed unless their results are attached to the relevant commit or release evidence.
