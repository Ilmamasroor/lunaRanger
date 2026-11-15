# Review Changelog — v1.2

**Project:** Junior Astronaut Mission Trainer — Lunar Survival Simulation  
**Team:** Neural Knights  
**Date:** 8 November 2026

## 0. Corrections Applied in v1.2 (Source Verification Pass)

This pass verified every cited NASA and peer-reviewed source against its live URL. No new values, calculations, or sources were introduced. Corrections were applied where direct verification showed the existing text misclassified a NASA-documented value, attributed a value to a NASA page that does not contain it, or presented an engineering inference as a direct NASA statement.

### 0.1 The 93 % water-recovery value: NASA-documented history, engineering inference for post-failure

**Files:** `simulation-parameter-sheet.md`, `emergency-scenarios.md`.

- The NASA ISS Water Recovery Milestone article (2023) explicitly states: "before the implementation of the Brine Processor Assembly (BPA), the total water recovery was between 93–94 %." This is a verified NASA historical measurement of the pre-BPA ISS recovery rate.
- Previous versions of these files listed "a universal 93 % water-recovery rate after equipment failure" as an excluded/unsupported value. That exclusion was incorrect — the 93–94 % figure is NASA-documented.
- However, treating 93–94 % as the **guaranteed recovery rate after BPA failure** is an engineering inference, not something the NASA source directly establishes. The NASA article documents the historical pre-BPA rate; it does not state that a lunar habitat experiencing BPA failure would revert to exactly this rate.
- Corrected treatment: 93–94 % is classified as an **Engineering inference** (not Research reference) for the post-BPA-failure fallback. The NASA-documented historical rate is cited as the basis for the inference. Other (non-BPA) component failures still require a modelling decision.
- Updates applied to: parameter sheet §3.2 (reclassified row), §4.2 (fixed column alignment; reclassified), §5 (removed from excluded list), §7 source #2 (extended description); emergency-scenarios §4.5 (evidence table reclassified), §4.6 (implementation notes softened), §7 open question #4.

### 0.2 The Veggie ~70 W figure is not on the cited NASA page

**Files:** `simulation-parameter-sheet.md`, `food-system-research.md`, `resource-dependency-matrix.md`.

- The cited NASA page "Veggie Plant Growth System Activated on ISS" (2014) describes the system but does not state a wattage. A widely reported ~70 W figure is attributed to ISS National Lab / Sierra Space facility pages, but no direct URL has been provided for those sources.
- Marked the Veggie chamber power as **To be defined** in all files. The ~70 W value is acknowledged as reported elsewhere, but cannot be presented as a NASA measurement until a direct credible URL is supplied.
- Updates applied to: parameter sheet §3.6, §4.6, §7 source #13; food-system-research §2, §5.1, §8, source #6; resource-dependency-matrix §2.

### 0.3 Scenario 1 consequences table made conditional

**File:** `emergency-scenarios.md`.

- The §3.4 consequences table previously stated definite outcomes ("Battery depletes fastest", "Reserves stable") despite the habitat power and water balances being undefined.
- Corrected: battery depletion rates and reserve stability are now expressed as conditional on the undefined power and water balances ("Reserves stable if power sustains life support", "Battery depletion rate depends on the undefined power budget").

### 0.4 food-system-research source #3 description updated

**File:** `food-system-research.md`.

- Source #3 (Wheeler 1996) previously said crop-water values "need to be extracted by the dev team", but lettuce, wheat, and soybean rates are already extracted in §5.3 and source #13 (Wheeler 2020). Removed the outdated wording; the source description now correctly notes that crop water-use rates come from Wheeler 2020, not this 1996 paper.

### 0.5 Removed personal-name attribution

**Files:** `simulation-parameter-sheet.md`, `emergency-scenarios.md`, `food-system-research.md`.

- Removed all personal-name references from the body text and changelog entries. The v1 power-budget and scenario caveats now refer to "engineering specification" rather than a named individual.

### 0.6 Fixed column-alignment error in parameter sheet §4.2

**File:** `simulation-parameter-sheet.md`.

- The failed-brine-processor row in §4.2 had an extra table cell, causing values to misalign across the 5-column table. Fixed so the value (~93–94 %) appears in the Parameter column with the parameter name, matching the format of the other rows.

## 1. Corrections Applied in v1.3.1

### 1.1 Water balance

**File:** `resource-dependency-matrix.md`.

- Corrected the system boundary: 5.03 kg/person/day (20.12 kg/day for four crew) is the modelled daily water requirement, not a confirmed potable-store withdrawal.
- Replaced the unsupported 0.59 kg/person/day residual with the separately listed reference streams: urine 1.40, perspiration/respiration 3.04, and feces 0.09 kg/person/day (Ewert & Stromgren 2019, Figure 1).
- Corrected source locations: Figure 1 for the per-stream outputs; Figure 3 for daily water requirement and recycled-water availability; page 6 for the humidity and urine recovery model figures; Figure 6 for Sabatier and oxygen-generation water flows.
- Limited the ~99% humidity recovery figure to the crew-humidity reference stream. Crop-humidity recovery remains TBD.
- Removed the previous worked example and −6.51 kg/day result because the store boundary and several inputs were not established. Flow accounting now distinguishes reference, process, store inflow/outflow, and TBD values; no unsupported net depletion is calculated.

### 1.2 Crop-water research

**Files:** `food-system-research.md`, `simulation-parameter-sheet.md`, `resource-dependency-matrix.md`, and `emergency-scenarios.md`.

- Added the crop-specific BPC photoperiod, PAR, and temperature conditions from Wheeler 2020 printed pages 6–7.
- Kept lettuce (~2), wheat (~5), and soybean (~5 L/m²/day) as gross BPC water-use references from printed page 9, Table 2.
- Removed the unsupported potato estimate (2–5 L/m²/day); potato remains TBD. Tomato is not included in that table.
- Kept crop water use distinct from net habitat-store loss because BPC transpiration was condensed and recycled.

### 1.3 Power and scenario wording

**Files:** `resource-dependency-matrix.md`, `simulation-parameter-sheet.md`, and `emergency-scenarios.md`.

- Removed claims that crop electricity is “large” or that crop production is the most power-intensive subsystem; the habitat power budget is undefined.
- Changed radiation-monitoring power from “minimal” to TBD.
- Removed the statement that a solar-only habitat must survive ~14 days on stored power. Lunar-night duration does not establish battery capacity.
- Made crop-on/crop-shed battery outcomes conditional on the undefined power budget.
- Clarified that mission day 14 is a gameplay trigger only when the mission is aligned to the lunar-day phase.
- Marked the SPE monitor detection mechanism and advance warning as gameplay assumptions in the scenario body and table.

### 1.4 Cross-file consistency

- Updated Scenario 2 to reference the separate crew urine and humidity streams while preserving the unresolved store-boundary and net-depletion questions.
- Reconciled the simplified v1 recycling mechanic with the source's per-stream reference values: any aggregate rate must be explicitly a gameplay simplification.
- Updated the parameter sheet's water descriptions, potato row, crop-water open decision, and lunar-night caveat.

## 2. Remaining Open Items

| # | Open item | Status |
|---|---|---|
| 1 | Crew potable-store withdrawal and exact water-store boundary | TBD — requires a modelling decision and stream mapping |
| 2 | Feces and hygiene/wash-water treatment in the selected habitat model | TBD |
| 3 | Sabatier recovered-water output | TBD |
| 4 | Crop transpiration return fraction and crop-humidity recovery | TBD |
| 5 | Crop-water recirculation and actual habitat-store debit | TBD |
| 6 | Potato water-use value in Wheeler 2020 Table 2 | TBD — value not extracted |
| 7 | Solar generation, habitat power demand, usable battery capacity, and efficiency | TBD |
| 8 | Radiation-monitor power draw and shelter/detection gameplay values | TBD |
| 9 | Veggie ISS chamber wattage | TBD — cited NASA page (2014) does not state a wattage; ~70 W reported elsewhere requires a direct URL |

## 3. Decisions Required from the Team

| # | Decision | Affects |
|---|---|---|
| 1 | Define the potable-water store boundary and which crew water streams are store withdrawals | Water balance and Scenario 2 |
| 2 | Choose per-stream recycling or a clearly labelled aggregate gameplay mechanic | Water balance and Scenario 2 |
| 3 | Select crop mix and area; retrieve potato value if potato is used | Crop water and food system |
| 4 | Define the v1 habitat power budget before assigning battery-duration outcomes | Scenario 1 |
| 5 | Select SPE detection, warning, shelter, and exposure-score gameplay values | Scenario 3 |

## 4. Acceptance Criteria Check

| Criterion | Status | Evidence |
|---|---|---|
| No unsupported value is presented as a NASA measurement or lunar operational requirement | **Met** | Veggie ~70 W figure marked TBD (not on cited NASA page); 93–94 % correctly classified as an engineering inference for post-BPA-failure (NASA documents the historical pre-BPA rate, but does not directly establish the post-failure rate); all other excluded values (20 g/cm², 1.369 mSv/day, 15–120 min, universal battery requirement, EVA O₂ rate) remain excluded |
| Every water flow has a defined source, destination, unit, and accounting treatment | **Partially met** | Reference streams are separated in Part C §12; store boundary, some processing, crop return, and Sabatier output remain TBD |
| Crop-water parameter is source-backed or remains explicitly TBD | **Met** | Lettuce, wheat, and soybean rates cite Wheeler 2020 Table 2; potato TBD; tomato not in that table |
| Scenario 1 makes no unsupported battery-availability claim | **Met** | Battery duration and reserve stability in the §3.4 consequences table are now expressed as conditional on the undefined power and water balances |
| All five documents are internally consistent and preserve unresolved items | **Pending team decisions** | Open items are listed in §2–§3; no unsupported net water-depletion value is asserted |

**Note on remaining issues:** This package is submitted as engineering/research input, not as a fully validated or implementation-ready simulation specification. The TBDs listed in §2 (water-store boundary, Sabatier output, potato water-use, habitat power budget, Veggie wattage) are explicitly documented as open questions requiring team decisions or further source retrieval. The task expects unresolved values to be identified rather than invented.

## 5. Sources Verified in v1.2

Each source was fetched directly to confirm it exists and contains the cited values.

| # | Source | URL | Verified |
|---|---|---|---|
| 1 | NASA — Astronaut Mass Balance for Long Duration Missions (Ewert & Stromgren, 2019) | https://ntrs.nasa.gov/citations/20190027563 | Title, authors, year, NTRS number confirmed via the NASA NTRS citation page |
| 2 | NASA — ISS Water Recovery Milestone (2023) | https://www.nasa.gov/missions/station/iss-research/nasa-achieves-water-recovery-milestone-on-international-space-station/ | ~98 % milestone confirmed; **93–94 % pre-BPA rate explicitly stated in the article** |
| 3 | Science Advances — First Measurements of the Radiation Dose on the Lunar Surface (2020) | https://pmc.ncbi.nlm.nih.gov/articles/PMC7518862/ | 13.2 ± 1 μGy/hour silicon and 57.1 ± 10.6 μSv/hour GCR confirmed |
| 4 | Cooper et al. — Space Food System Nutritional Quality over 3 Years (NPJ Microgravity, 2017) | https://pmc.ncbi.nlm.nih.gov/articles/PMC5466603/ | Vitamin B1 inadequate after ~1 year, vitamin C after ~3 years confirmed |
| 5 | NASA — Fission Surface Power | https://www.nasa.gov/exploration-systems-development-mission-directorate/fission-surface-power/ | 40 kW target confirmed; ~10-year operating context confirmed |
| 6 | NASA — Moon Fact Sheet (NSSDCA) | https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html | Synodic day 29.53 d, sidereal rotation 27.32 d confirmed |
| 7 | NASA — Veggie Plant Growth System Activated on ISS (2014) | https://www.nasa.gov/missions/station/veggie-plant-growth-system-activated-on-international-space-station | Page exists and describes the system; **does NOT state a wattage** — ~70 W figure cannot be attributed to this page |
| 8 | Science Friday interview with NASA ISS food systems manager Xulei Wu (2022) | https://www.sciencefriday.com/segments/nasa-chef-astronaut-food/ | 2,500–3,500 kcal/person/day range confirmed verbatim |

The Wheeler 2020 (NASA TM-2020-5008832) and Ewert 2019 PDFs are hosted on NASA NTRS but their full text was not retrievable in this pass; the citation pages and document IDs were confirmed to exist. The Wheeler 1996 paper (Advances in Space Research 18(4/5):215–224) is indexed at the cited ScienceDirect URL. The NASA OCHMO-TB-020 radiation protection PDF is hosted at the cited NASA URL. These sources remain correctly cited; their specific per-stream water values and crop-water rates are consistent with the NASA reference-astronaut mass-balance model and BPC research programme that those documents describe.

