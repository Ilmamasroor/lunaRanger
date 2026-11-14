# Junior Astronaut Mission Trainer — Science & Data Layer Handoff

Welcome! This package contains the **authoritative scientific parameters, NASA telemetry, and emergency scenarios** for the **Junior Astronaut Mission Trainer** simulation engine.

---

## 🚀 Quick Start for TypeScript Developers

You have two simple ways to integrate this data into your simulation engine:

### Option 1: Direct JSON Import (Fastest & Simplest)
If your TypeScript app runs in the browser or is bundled with Vite / Webpack / Next.js:
1. Copy the files from `outputs/` directly into your project's `src/data/` or `assets/` folder:
   - `outputs/mission_config.json` -> Master Schema 1.1 parameters
   - `outputs/emergency_scenarios.json` -> NASA DONKI Solar Particle Event scenarios
2. Copy the benchmark test fixtures for your engine tests:
   - `tests/fixtures/expected_life_support_calculations.json`
   - `tests/fixtures/expected_radiation_calculations.json`

### Option 2: Live Local REST API Server
If you prefer fetching the configuration dynamically over HTTP:
```bash
python api_server.py
```
This runs a CORS-enabled server at `http://localhost:8000`:
- `GET http://localhost:8000/api/mission-config` -> Validated mission configuration (Schema 1.1)
- `GET http://localhost:8000/api/scenarios/emergency` -> Space weather emergency scenarios
- `GET http://localhost:8000/api/fixtures/life-support` -> Stoichiometric validation fixtures
- `GET http://localhost:8000/api/fixtures/radiation` -> Dosimetry validation fixtures

---

## 📦 Data Contract (Schema 1.1)

```typescript
export interface MissionParameter {
  parameter_id: string;
  resource: "oxygen" | "water" | "food" | "co2" | "power" | "radiation" | "crew" | "general";
  flow_type: "consumption" | "production" | "recovery" | "storage" | "environment" | "infrastructure" | "specification";
  value_per_person: number | null; // null if qualitative or TBD
  raw_value: string | null;        // exact string from NASA research document
  unit: string;
  period: { value: number; unit: string };
  data_status: "research_reference" | "derived" | "engineering_inference" | "gameplay_assumption" | "tbd";
  source: string | null;
  assumptions: string[];
  notes: string;
}

export interface MissionConfig {
  schema_version: "1.1";
  mission: { crew_size: number };
  parameters: MissionParameter[];
}
```

---

## 🔬 Scientific Summary (4 Astronauts, 30-Day Mission)

* **Daily O₂ Demand:** `0.89 kg/person/day` -> `3.56 kg/day` for 4 crew
* **Daily CO₂ Exhaled:** `1.08 kg/person/day` -> `4.32 kg/day` for 4 crew
* **Electrolysis Feed:** `~4.01 kg/day` water consumed to yield `3.56 kg/day` O₂ ($2\text{H}_2\text{O} \rightarrow 2\text{H}_2 + \text{O}_2$)
* **Daily Water Requirement:** `5.03 kg/person/day` -> `20.12 kg/day` for 4 crew
* **Packaged Food:** `2.39 kg/person/day` -> `9.56 kg/day` for 4 crew (`3000 kcal/person/day`)
* **Lunar Surface Radiation (GCR):** `1.37 mSv/day` unshielded (Chang'e-4 derived)
* **Solar Particle Events (SPE):** Up to `10,000 pfu` peak flux; shelter provides `90%` reduction.
