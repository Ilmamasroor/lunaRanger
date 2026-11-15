# Architecture & API Contract

**Source:** Notion — [Architecture & API Contract](https://app.notion.com/p/4109fd4012aa81b4878ee5242a1dd9e1)  
**Notion status:** Draft · Last reviewed 11 November 2026  
**Repository copy:** Documentation mirror; this file does not approve the design.

## Architecture status

The proposed MVP architecture supersedes the earlier Spring Boot boundary proposal. No Spring Boot runtime is required for the current MVP. The cross-layer contracts still require team alignment.

## Ownership boundaries

| Layer | Responsibility | Must not do |
|---|---|---|
| Python data pipeline | Ingest, clean, normalize, map and validate research data; preserve provenance; generate configuration and test fixtures | Run live gameplay or mutate runtime inventory |
| TypeScript simulation engine | Own live mission state, commands, validation, resource calculations and outcomes | Delegate authoritative decisions to UI or Unity |
| React + TypeScript | Own navigation, HUD, player input, mission screens, loading/error states and fallback | Duplicate authoritative resource calculations |
| Unity WebGL | Render the lunar environment, camera, hotspots and visual feedback | Decide resource changes, crew safety or mission success |

NASA data availability and completeness must not be assumed. The application should run with mock/configuration data while source datasets are unavailable.

## Data flow

1. Python ingests NASA/research sources or mock data.
2. The pipeline cleans, transforms, validates fields, types, units and ranges, and maps source fields to the common schema.
3. It emits versioned configuration and provenance-aware parameter records.
4. TypeScript validates the configuration and runs the authoritative simulation.
5. React sends player intent to the engine and renders returned state.
6. Unity receives authoritative snapshots/visual commands and renders them.
7. Mission outcomes feed the debrief and learning experience.

## Configuration provenance

Parameters should retain their value, unit, source/reference, dataset version, classification, validation status and caveats where applicable. Classifications are research data, engineering inference, gameplay assumption, or TBD. Illustrative values in the Notion design are not approved gameplay parameters.

## Design constraints

- Keep source-specific parsing outside the TypeScript engine.
- Python reference models are independent validation tools, not a second gameplay engine.
- React renders engine state rather than recalculating it.
- Unity is a visualization/interaction surface, not a second simulation authority.
- Preserve mock-data operation and a usable 2D fallback.
- Do not silently convert missing or unknown values into invented defaults.

## Review gates

This document remains **Draft** in Notion. Confirm data, simulation and Unity contracts with the team before treating this architecture as a frozen interface.

## Related records

- [Simulation design v0.2 — Needs Review](https://app.notion.com/p/4109fd4012aa8112960ce4e2027cf210)
- [React ↔ Unity contract v0.1 — Draft](https://app.notion.com/p/4189fd4012aa81b1b245ec85201dfb95)
- [Python → TypeScript contract v0.1 — Draft](https://app.notion.com/p/4189fd4012aa81e182dff3d2240f922c)
