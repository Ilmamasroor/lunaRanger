# Unity WebGL in the React cockpit

Build the LunaRangers WebGL player from the Unity project with Editor 6000.2.7f2 and the LunaRangers template. Boot the DayOne scene, which contains the full campaign. From the repository root:

    npm ci
    node scripts/stage-unity.mjs <Unity export directory>
    npm run build

The staging script decodes the export's Brotli assets to standard static files in public/Build. Serve dist via HTTP with the application/wasm content type for .wasm. The 2D walkthrough is a separate practice mode.

Unity reports play state through lunarangers-campaign events. React adapts those events to Ilma's TypeScript mission engine for resource simulation, day progression, and sample return. Unity checks with the engine before opening the airlock on Days 1 and 6. The Day 5 cockpit exposes the engine denial during the replayed alert.

## Research sources

- The team data snapshot in src/data/pipeline-snapshot.json identifies the data pipeline commit. Its food, water, CO2, and O2 references are inputs to the daily resource simulation. The ISS water recovery milestone is used as a training coefficient. Starting inventories, energy rates, air scrubber efficiency, and clearance thresholds are game settings.
- NASA CCMC DONKI. An archived solar particle event from May 2024 triggers the Day 5 simulation alert. https://ccmc.gsfc.nasa.gov/tools/DONKI/
- NASA RadLab. The Day 5 briefing shows an archived ISS DosTel2 detector reading returned by the public RadLab API, alongside the published lunar detector measurement used as the pipeline's fallback. These are research references. https://visualization.osdr.nasa.gov/radlab/gui/data-api/
- NASA OSDR OSD-269. The Day 7 briefing links the ISS lettuce study as nutrition context. The study is a learning reference. https://osdr.nasa.gov/bio/repo/data/studies/OSD-269
