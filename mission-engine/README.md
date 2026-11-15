# LunaRangers TypeScript Mission Engine

Authoritative state-machine and simulation engine for the **LunaRangers Junior Astronaut Mission Trainer**.

## Core Capabilities
- **Resource Simulation:** Continuous O2, CO2, Water, Food, and Energy delta modeling.
- **Hardened Mission Cycle Progression:** Strict boundary checks against negative cycles, fractional values, `NaN`, `Infinity`, and integer overflow.
- **Authoritative Action Dispatcher:** Validates all incoming actions from React HUD and Unity 3D clients with atomic state immutability.
- **EVA / Spacewalk Workflow:** Enforces crew readiness, habitat stability, resource thresholds, and radiation/solar hazard checks before clearing EVA.
- **Lunar Sample Collection & Safe Return:** Authoritative Day 6 workflow tracking sample acquisition, container storage, and safe astronaut return.
- **7-Day Mission Sequence:** One-day-at-a-time progression; current-day objective must be completed before advancing.
- **EVA Abort:** Explicit safe-return path that does not credit an unsecured sample.
- **Runtime Input Validation:** Checks configuration coefficients, efficiencies, crew count, and resource inventory before simulation.

## Quick Start
```bash
npm install
npm run typecheck
npm test
```
