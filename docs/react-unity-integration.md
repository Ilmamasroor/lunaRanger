# React ↔ Unity WebGL Integration Contract v0.1

**Source:** Notion — [React ↔ Unity WebGL Integration Contract v0.1](https://app.notion.com/p/4189fd4012aa81b1b245ec85201dfb95)  
**Notion status:** Draft · Last reviewed 14 November 2026

> Event names and payloads in the source contract are conceptual, not final. Confirm them against the current React and Unity source before relying on them.

## Ownership

- **React:** navigation, HUD, mission panels, player controls, accessibility and 2D fallback; forwards supported player intent to the TypeScript engine; renders authoritative results.
- **TypeScript engine:** mission state, action validation, resources, equipment outcomes, crew safety and progression. It alone decides whether an action succeeds.
- **Unity WebGL:** 3D rendering, camera, hotspots and visual feedback. It sends interaction intent and receives authoritative snapshots/visual commands; it does not mutate resource ledgers.

## Proposed message categories

1. Unity readiness and load failure.
2. Hotspot/module selection.
3. React-to-Unity visual command.
4. Authoritative state snapshot.
5. Visual interaction acknowledgement.
6. Diagnostic information for integration failures.

The Notion proposal suggests a versioned envelope with schema version, message ID, type and payload. It does not establish final event names or payload fields.

## Required contract decisions

- Stable hotspot/equipment IDs shared with the engine.
- Exact event names and payload schemas.
- Versioning and unknown-version behavior.
- Unity readiness handshake and loading timeout.
- Malformed/invalid payload handling.
- State revision to prevent stale updates.
- Listener cleanup across load/unload/reload.
- 2D fallback behavior when WebGL fails.
- No direct Unity mutation of authoritative resource state.

## Proposed vertical slice

The source proposes an oxygen-generator investigation/repair flow: Unity reports hotspot selection; React opens the equipment panel; the engine handles inspection, scenario activation, evidence, diagnosis and repair; React renders accepted/rejected outcomes; Unity updates visual indicators from the new authoritative state.

## Acceptance checklist

- [ ] Confirm stable IDs from actual Unity scenes and engine fixtures.
- [ ] Confirm exact event names and payloads with both developers.
- [ ] Test readiness handshake and timeout.
- [ ] Test hotspot selection and visual commands.
- [ ] Test authoritative snapshot updates.
- [ ] Test invalid IDs, malformed payloads and rejected actions.
- [ ] Test reload/unload without duplicate listeners.
- [ ] Test 2D fallback after WebGL load failure.
- [ ] Demonstrate the complete equipment investigation/repair interaction.

A previously demonstrated solar-array communication proof does not by itself establish that the complete mission interaction contract is integrated.
