# Simulation Parameter Sheet

**Project:** Junior Astronaut Mission Trainer — Lunar Survival Simulation
**Team:** Neural Knights
**Owner:** Fatima Khan
**Date:** 8 November 2026
**Source research:** *JUNIOR ASTRONAUT MISSION TRAINER — Scientific Research & Simulation Logic* (5 Nov 2026)
**Companion files:** `food-system-research.md` · `resource-dependency-matrix.md` · `emergency-scenarios.md`

---

## 1. Purpose

This sheet translates the science in the research document into a single, developer-facing list of simulation parameters. The development team should be able to build resource-balance rules from this sheet alone, without re-reading the full 18-page research paper.

Two rules apply throughout:

1. **No invented science.** Every numerical value is either (a) traced to a cited source in the research paper or (b) explicitly labelled as a gameplay or engineering assumption. No empty cell is filled with a guess.
2. **"To be defined" is a valid answer.** When a value is not yet known, the cell says so and states what the team must research or decide next.

---

## 2. How to Read This Sheet

Each parameter carries three labels in addition to its value and unit.

### 2.1 Classification — what kind of value it is

| Label | Meaning |
|---|---|
| **Research reference** | Value taken from a cited scientific source |
| **Derived calculation** | Arithmetic on a research reference (e.g., per-person × crew of 4; stoichiometric ratios) |
| **Engineering inference** | A reasonable engineering deduction from established principles — more grounded than a gameplay assumption, but not a measured or modelled research value (e.g., a load-shedding priority scheme, a power-budget estimate from assumed loads) |
| **Requires research** | A credible external source must be found before use |
| **Requires modelling decision** | A game-design choice the team must make; no single scientific answer exists |
| **Gameplay assumption** | Engineering placeholder agreed by the team; not a scientific fact |

### 2.2 Origin type — where the value came from

| Label | Meaning |
|---|---|
| **Measured** | Directly measured by an instrument or experiment |
| **Modelled** | Output of a scientific model (e.g., NASA mass-balance model) |
| **Proposed** | A development target, not yet a deployed system |
| **Derived** | Calculated by arithmetic from one of the above |
| **Engineering inference** | Deduced from engineering principles rather than measured or modelled |
| **Assumed** | Gameplay or mission-design assumption by the dev team |
| **To be defined** | Not yet assigned |

**How §2.1 and §2.2 relate:** §2.1 describes the *role* of the value in the project (research fact? calculation? decision to make?); §2.2 describes the *provenance* of the number (measured? modelled? deduced?). A value can be a "Research reference" in classification and "Modelled" in origin (e.g., NASA mass-balance values), or a "Derived calculation" in classification and "Engineering inference" in origin (e.g., the stoichiometric electrolysis feed, which is arithmetic on chemistry but not a NASA-measured figure).

### 2.3 v1-safe? — may it be used in the first simulation?

| Label | Meaning |
|---|---|
| **Yes** | Usable as-is |
| **Yes, with caveat** | Usable only under the stated conditions |
| **No** | Must not be used until a source or decision is provided |

---

## 3. Master Parameter Table

> Format follows the task spec: **Parameter · Value · Unit · Source · Classification**.
> Per-parameter detail (what it represents, origin, v1-safe, caveats) follows in §4.

### 3.1 Oxygen & Air Quality

| Parameter | Value | Unit | Source / Qualification | Classification |
|---|---|---|---|---|
| Sleeping O₂ consumption | 0.37 | g/min/person | NASA 2019 mass-balance study | Research reference |
| Nominal-activity O₂ consumption | 0.59 | g/min/person | NASA 2019 mass-balance study | Research reference |
| Aerobic-exercise O₂ consumption | up to 3.99 | g/min/person | NASA 2019 mass-balance study (NOT an EVA rate) | Research reference |
| Daily O₂ requirement per astronaut | ~0.89 | kg/person/day | NASA reference astronaut model (82 kg astronaut, incl. 90 min exercise) | Research reference |
| Daily CO₂ production per astronaut | ~1.08 | kg/person/day | NASA reference astronaut model | Research reference |
| Daily O₂ requirement (4 crew) | 3.56 | kg/day | Derived: 0.89 × 4 | Derived calculation |
| Daily CO₂ production (4 crew) | 4.32 | kg/day | Derived: 1.08 × 4 | Derived calculation |
| 30-day O₂ requirement (4 crew) | 106.8 | kg | Derived: 3.56 × 30 | Derived calculation |
| 30-day CO₂ production (4 crew) | 129.6 | kg | Derived: 4.32 × 30 | Derived calculation |
| EVA O₂ consumption rate | To be defined | g/min or kg/hour | Requires EVA-specific source; the 3.99 g/min aerobic value MUST NOT be reused as an EVA rate | Requires research |
| Emergency O₂ reserve (initial stock) | To be defined | kg | Engineering decision: backup O₂ available at mission start | Gameplay assumption |

### 3.2 Water

| Parameter | Value | Unit | Source / Qualification | Classification |
|---|---|---|---|---|
| Daily water requirement per astronaut | ~5.03 | kg/person/day (≈ L/person/day) | NASA 2019 mass-balance study; this is a modelled total requirement, not automatically a potable-tank withdrawal | Research reference |
| Daily water requirement (4 crew) | 20.12 | kg/day (≈ L/day) | Derived: 5.03 × 4; not automatically a potable-tank withdrawal | Derived calculation |
| 30-day water requirement (4 crew) | 603.6 | kg (≈ L) | Derived: 20.12 × 30; not a net make-up-water or tank-sizing value | Derived calculation |
| Humidity-condensate recovery | ~99 | % | NASA 2019 model (per-stream model figure) | Research reference |
| Urine-water recovery | ~85 | % | NASA 2019 model (per-stream model figure) | Research reference |
| Overall ISS water-recovery milestone | ~98 | % | NASA 2023 ISS milestone (system-level achievement, not per-stream) | Research reference |
| ISS water-recovery rate before Brine Processor Assembly (BPA) | ~93–94 | % | NASA 2023 ISS milestone article: "before the implementation of the Brine Processor Assembly (BPA), the total water recovery was between 93–94 %" | Research reference |
| Gameplay water-recovery rate | To be defined | % | Team modelling decision; do NOT default to 98 % as a guaranteed per-subsystem rate | Requires modelling decision |
| Failed-brine-processor fallback rate (inferred) | ~93–94 | % | NASA documents 93–94 % as the historical ISS water-recovery rate before BPA was added (NASA 2023). Treating this as the post-BPA-failure fallback rate is an engineering inference, not a direct NASA statement. | Engineering inference |
| Initial stored water (mission start) | To be defined | kg / L | Engineering decision | Gameplay assumption |

### 3.3 Radiation

| Parameter | Value | Unit | Source / Qualification | Classification |
|---|---|---|---|---|
| Chang'e-4 absorbed dose rate in silicon | 13.2 ± 1 | μGy/hour | Science Advances 2020 (measured in silicon — NOT a human-tissue dose) | Research reference |
| Chang'e-4 derived GCR dose-equivalent rate | 57.1 ± 10.6 | μSv/hour | Science Advances 2020 (derived value, not a universal effective dose) | Research reference |
| Human effective dose on the lunar surface | To be defined | mSv/day | Requires a dose model accounting for radiation type and biological effect; the 1.369 mSv/day figure MUST NOT be reused | Requires research |
| SPE / solar-storm warning time | To be defined | minutes | No universal 15–120 min value is supported by the listed sources | Requires research |
| Shielding-thickness requirement | To be defined | g/cm² | Mission-specific; no universal 20 g/cm² value is supported | Requires research |
| Shelter protection factor | To be defined | ratio or % reduction | Engineering decision: how much a shelter reduces exposure during an SPE | Gameplay assumption |

### 3.4 Power

| Parameter | Value | Unit | Source / Qualification | Classification |
|---|---|---|---|---|
| Fission surface-power target | ≥ 40 | kW (continuous) | NASA development target — **proposed/future technology, NOT deployed; out of scope for the initial mission (v1)** | Research reference (proposed) |
| Fission operating design goal | ~10 | years | NASA development target — proposed, not operating | Research reference (proposed) |
| Fission daily energy (mathematical example) | 960 | kWh/day | Derived example: 40 kW × 24 h — illustrative; **assumes fission is deployed, which it is not in v1** | Derived calculation |
| **v1 power model** | Solar + battery only | qualitative | **v1 habitat runs on solar panels + battery storage only. Fission is a future-technology unlock beyond v1.** The simulation MUST NOT imply that battery or backup sources can support the lunar night until habitat demand (TBD), usable battery capacity (TBD), battery efficiency (TBD), and solar generation (TBD) are all specified. | Gameplay assumption |
| Solar-power generation capacity | To be defined | kW | Location-specific (equator vs South Pole); requires panel-area and efficiency assumptions | Requires research |
| Battery storage capacity | To be defined | kWh | Engineering decision: depends on habitat demand and dark-period length | Gameplay assumption |
| Habitat average power demand | To be defined | kW | Requires summing the demand of all modelled subsystems | Requires research |
| Lunar daytime length (near equator) | ~14 | Earth days | NASA Moon Fact Sheet (NSSDCA) — synodic day 29.53 d ⇒ ~14.75 d daylight | Research reference |
| Lunar nighttime length (near equator) | ~14 | Earth days | NASA Moon Fact Sheet (NSSDCA) — synodic day 29.53 d ⇒ ~14.75 d darkness | Research reference |
| Lunar South Pole lighting | Variable (some areas near-continuous sunlight; nearby terrain in shadow) | qualitative | NASA lunar South Pole reference | Research reference |
| Power-priority tiers (Critical / Important / Reducible) | 3-tier scheme | qualitative | Proposed in research paper §5.5 — a gameplay scheme, NOT a NASA operating procedure | Gameplay assumption |

### 3.5 Crew & Mission

| Parameter | Value | Unit | Source / Qualification | Classification |
|---|---|---|---|---|
| Crew size | 4 | astronauts | Mission spec (fixed by the simulation brief) | Gameplay assumption |
| Mission duration (reference) | 30 | days | Reference used for 30-day calculations; final duration to be set by team | Requires modelling decision |
| Initial stored oxygen (mission start) | To be defined | kg | Engineering decision | Gameplay assumption |
| Activity schedule (sleep / nominal / exercise minutes per astronaut per day) | To be defined | minutes/day | Required only if the team chooses activity-based O₂ calculation | Requires modelling decision |

### 3.6 Food (full detail in `food-system-research.md`)

| Parameter | Value | Unit | Source / Qualification | Classification |
|---|---|---|---|---|
| Packaged food per astronaut | 2.39 | kg/person/day | Ewert 2019 (NASA, NTRS 20190027563) citing NASA Life Support Baseline Values and Assumptions Document (BVAD), Table 4-53 — the table is in the BVAD, which Ewert discusses; it is not a table within the Ewert paper itself | Research reference |
| Packaged food (4 crew) | 9.56 | kg/day | Derived: 2.39 × 4 | Derived calculation |
| 30-day packaged food (4 crew) | 286.8 | kg | Derived: 9.56 × 30 | Derived calculation |
| Energy requirement per astronaut | ~2,500–3,500 | kcal/person/day | NASA STEMonstration: Nutrition (2018); Science Friday interview with NASA ISS food systems manager (2022) | Research reference |
| Stored-food shelf life (vitamin B1) | ~1 year before inadequate | years | Cooper et al. 2017 (NPJ Microgravity, PMC5466603) | Research reference |
| Stored-food shelf life (vitamin C) | ~3 years before inadequate | years | Cooper et al. 2017 (NPJ Microgravity, PMC5466603) | Research reference |
| Stored-food target for beyond-LEO | up to 5 | years | Cooper et al. 2017 (NPJ Microgravity, PMC5466603) | Research reference |
| Crop growth time — microgreens | 7–14 | days | Horticulture reference (typical cycle); NASA is researching microgreens as a candidate crop | Research reference (horticulture) |
| Crop growth time — lettuce | 28–33 | days | Wheeler 1996 (NASA BPC); NASA OSDR OSD-269 (VEG-03A) | Research reference |
| Crop growth time — dwarf wheat | ~35–86 | days | NASA Growing Plants in Space (5 wk ISS); Wheeler 1996 (NASA BPC, 64–86 d) | Research reference |
| Crop growth time — soybean | 90–97 | days | Wheeler 1996 (NASA BPC) | Research reference |
| Plant area for food (vegetarian) | 40–50 | m²/person | Wheeler (NASA) bioregenerative life-support research | Research reference |
| Plant area for O₂/CO₂ removal | 20–25 | m²/person | Wheeler (NASA) bioregenerative life-support research | Research reference |
| Plant area for food (4 crew) | 160–200 | m² | Derived: 40–50 × 4 | Derived calculation |
| Veggie ISS chamber power | To be defined | W | The cited NASA Veggie page (2014) does not state a wattage; the ~70 W figure reported elsewhere (ISS National Lab / Sierra Space facility pages) requires a direct URL to be properly cited | Requires research |
| Fertilizer required (no recycling) | up to 90 | kg/person/year | Wheeler 2020 (NASA, NTRS 20200002230) | Research reference |
| Stored-food vs grown-food ratio | To be defined | ratio | Team decision; `food-system-research.md` §4.5 gives recommended ranges by mission length | Requires modelling decision |
| Crop water use — lettuce | ~2 | L/m²/d | Wheeler 2020 (NASA TM-2020-5008832, Table 2) — BPC measured | Research reference |
| Crop water use — wheat | ~5 | L/m²/d | Wheeler 2020 (NASA TM-2020-5008832, Table 2) — BPC measured | Research reference |
| Crop water use — soybean | ~5 | L/m²/d | Wheeler 2020 (NASA TM-2020-5008832, Table 2) — BPC measured | Research reference |
| Crop water use — potato | TBD — value reported in Wheeler 2020 p. 9 Table 2 but not extracted; no estimate assumed | L/m²/d | Wheeler 2020, p. 9, Table 2 | Requires research (source located) |
| Crop water demand (formula) | rate × area × 1 kg/L | kg/day | Derived from Wheeler 2020 L/m²/d values | Derived calculation |
| Crop electricity requirement (full-scale) | To be defined | kW | Illustrative estimate 18–36 kW for a 180 m² setup (`food-system-research.md` §5.4); final value depends on crop mix and PPFD choice — NOT a NASA lunar-system spec | Gameplay assumption (once chosen) |
| Initial stored food (mission start) | To be defined | kg | Engineering decision | Gameplay assumption |

---

## 4. Per-Parameter Detail

For every parameter in §3: what it represents · origin type · whether it is safe for v1 · caveats and next steps.

### 4.1 Oxygen & Air Quality

| Parameter | What it represents | Origin | v1 Safe? | Caveat / Next step |
|---|---|---|---|---|
| Sleeping O₂ — 0.37 g/min/person | O₂ used by one astronaut while sleeping | Modelled | Yes | Use only when modelling sleep periods; multiply by minutes in sleep. |
| Nominal O₂ — 0.59 g/min/person | O₂ used during normal waking activity | Modelled | Yes | Use for the bulk of the crew day. |
| Aerobic-exercise O₂ — up to 3.99 g/min/person | Peak O₂ used during aerobic exercise | Modelled | Yes, with caveat | Applies only to scheduled exercise windows. **MUST NOT be used as an EVA O₂ rate.** |
| Daily O₂ — ~0.89 kg/person/day | Planning daily total per astronaut | Modelled | Yes | Reference astronaut is 82 kg with 90 min daily exercise. Different crew profiles will shift this. |
| Daily CO₂ — ~1.08 kg/person/day | CO₂ exhaled per astronaut per day | Modelled | Yes | CO₂ removal is a SEPARATE system from O₂ generation; do not couple them. |
| 4-crew daily O₂ — 3.56 kg/day | Crew-level daily O₂ demand | Derived | Yes | Recalculate if crew size changes. |
| 4-crew daily CO₂ — 4.32 kg/day | Crew-level daily CO₂ load | Derived | Yes | Drives the CO₂-removal sizing. |
| 30-day O₂ — 106.8 kg | Total O₂ needed for a 30-day mission | Derived | Yes, with caveat | Assumes constant crew and no recovery losses; real mission needs more. |
| 30-day CO₂ — 129.6 kg | Total CO₂ produced in 30 days | Derived | Yes, with caveat | Drives sizing of CO₂-removal capacity. |
| EVA O₂ rate | O₂ consumed per astronaut during a spacewalk | To be defined | **No** | Find an EVA-specific NASA source before modelling spacewalks. |
| Emergency O₂ reserve | Backup O₂ available at mission start | To be defined | **No** | Dev team must pick an opening stock. Suggest a value and label it as a gameplay assumption. |

### 4.2 Water

| Parameter | What it represents | Origin | v1 Safe? | Caveat / Next step |
|---|---|---|---|---|
| Daily water requirement — ~5.03 kg/person/day | Modelled total water requirement in the reference-astronaut balance | Modelled | Yes, with caveat | This is not automatically the amount withdrawn from a potable tank. Define the habitat water-store boundary and identify the component streams before calculating tank withdrawal. |
| 4-crew daily water requirement — 20.12 kg/day | Crew-level daily water requirement | Derived | Yes, with caveat | ≈ 20.12 L/day using 1 kg ≈ 1 L; not automatically a daily potable-store debit. |
| 30-day water — 603.6 kg | Total water for 30-day mission, pre-recovery | Derived | Yes, with caveat | Real make-up water depends on recovery rate. |
| Humidity-condensate recovery — ~99 % | Recovery of water from crew humidity stream | Modelled | Yes, with caveat | Per-stream model figure; do not automatically apply this rate to crop transpiration or a lunar habitat. |
| Urine-water recovery — ~85 % | Recovery of water from urine | Modelled | Yes, with caveat | Per-stream model figure. |
| Overall ISS water-recovery milestone — ~98 % | Whole-system recovery achieved on the ISS | Measured | Yes, with caveat | System-level milestone, NOT a guaranteed per-subsystem rate. Do not use as the gameplay default for every stream. |
| Gameplay water-recovery rate | The single % the simulation uses | To be defined | **No** | Team must decide: single overall rate, or per-stream. If single, justify the chosen number. |
| Failed-brine-processor fallback — ~93–94 % (inferred) | Recovery rate if BPA fails | Measured (ISS, pre-BPA) — inference for post-failure | Yes, with caveat | NASA documented 93–94 % as the ISS recovery rate before BPA was added (NASA 2023). Using this as the post-BPA-failure rate is an engineering inference, not a direct NASA statement. Other component failures require a modelling decision. |
| Initial stored water | Water available at mission start | To be defined | **No** | Dev team must pick an opening reserve and label it as a gameplay assumption. |

### 4.3 Radiation

| Parameter | What it represents | Origin | v1 Safe? | Caveat / Next step |
|---|---|---|---|---|
| Chang'e-4 absorbed dose — 13.2 ± 1 μGy/hour | Energy absorbed in SILICON on the lunar surface | Measured | Yes, with caveat | Silicon measurement, not human tissue. **MUST NOT be converted to a human dose by changing the unit.** |
| Chang'e-4 GCR dose-equivalent — 57.1 ± 10.6 μSv/hour | Derived biological-equivalent rate for GCR | Derived | Yes, with caveat | Derived value, not a universal effective dose. Use as a reference only. |
| Human effective dose on lunar surface | Daily dose a human actually receives | To be defined | **No** | Requires a dose model (radiation type × biological effectiveness). The 1.369 mSv/day figure MUST NOT be reused. |
| SPE warning time | How long the crew has to reach shelter | To be defined | **No** | No universal 15–120 min value is supported. Either find a source or label as a gameplay assumption. |
| Shielding-thickness requirement | Regolith or material thickness needed | To be defined | **No** | Mission-specific; depends on material, density, duration. No universal 20 g/cm² value. |
| Shelter protection factor | How much the shelter cuts exposure | To be defined | **No** | Dev team must decide and label as a gameplay assumption. |

### 4.4 Power

| Parameter | What it represents | Origin | v1 Safe? | Caveat / Next step |
|---|---|---|---|---|
| Fission target — ≥ 40 kW | Continuous electrical power NASA is developing | Proposed | Yes, with caveat — **reference only; out of scope for v1** | Development target, not deployed. **v1 habitat uses solar + battery only; fission is a future-technology unlock.** |
| Fission design life — ~10 years | Operating design goal | Proposed | Yes, with caveat — **reference only; out of scope for v1** | Same caveat: proposed, not operating. |
| Fission daily energy — 960 kWh/day | What 40 kW × 24 h would yield | Derived | Yes, with caveat — **assumes fission deployed, which it is not in v1** | Mathematical example only; do NOT use for v1 power-budget calculations. |
| **v1 power model (solar + battery only)** | The power sources available in the v1 simulation | Assumed | Yes | **v1 runs on solar + battery only.** MUST NOT imply battery can support lunar night until habitat demand (TBD), usable capacity (TBD), efficiency (TBD), and solar generation (TBD) are all specified. These are engineering decisions requiring further specification. |
| Solar generation capacity | Power the solar array can produce | To be defined | **No** | Depends on location, panel area, efficiency, orientation. Find sources or label as a gameplay assumption. |
| Battery storage capacity | Energy the habitat can store | To be defined | **No** | Depends on demand and dark-period length. Dev team must decide and label as a gameplay assumption. |
| Habitat average power demand | Sum of all subsystem power draws | To be defined | **No** | Required before any battery-sizing calculation is meaningful. |
| Lunar daytime — ~14 Earth days | Length of the sunlit period near the equator | Measured | Yes | Source: NASA Moon Fact Sheet (NSSDCA). Major design driver for solar-only habitats. |
| Lunar nighttime — ~14 Earth days | Length of the dark period near the equator | Measured | Yes | Source: NASA Moon Fact Sheet (NSSDCA). This does not establish the battery capacity required; habitat demand, usable capacity, efficiency, and generation must be modelled. |
| South Pole lighting | Variable; some areas near-continuous sunlight | Measured | Yes | Use if the mission is set at the South Pole; changes the power model substantially. |
| Power-priority tiers | Critical / Important / Reducible classification of loads | Assumed | Yes, with caveat | A gameplay scheme proposed in the research paper, NOT a NASA operating procedure. Label as such. |

### 4.5 Crew & Mission

| Parameter | What it represents | Origin | v1 Safe? | Caveat / Next step |
|---|---|---|---|---|
| Crew size — 4 | Number of astronauts in the habitat | Assumed | Yes | Fixed by the simulation brief. |
| Mission duration — 30 days (reference) | Total simulated mission length | Assumed | Yes, with caveat | 30 days is used for derived totals. The team may pick 7 / 30 / longer; recalculate derived values accordingly. |
| Initial stored oxygen | O₂ available at mission start | To be defined | **No** | Dev team must pick and label as a gameplay assumption. |
| Activity schedule | Minutes per day each astronaut spends sleeping / nominal / exercising | To be defined | **No** | Only needed if the team uses activity-based O₂. Otherwise use the daily 0.89 kg planning value. |

### 4.6 Food

| Parameter | What it represents | Origin | v1 Safe? | Caveat / Next step |
|---|---|---|---|---|
| Packaged food — 2.39 kg/person/day | Daily food mass per astronaut (packaged) | Modelled | Yes | Same NASA mass-balance source as O₂ and water; consistent units. |
| 4-crew daily food — 9.56 kg/day | Crew-level daily food demand | Derived | Yes | Recalculate if crew size changes. |
| 30-day food — 286.8 kg | Total packaged food for 30-day mission | Derived | Yes, with caveat | Excludes any grown contribution; full vegetarian would reduce stored-food need. |
| Energy — 2,500–3,500 kcal/person/day | Astronaut daily energy need | Modelled | Yes, with caveat | NASA educational reference + Science Friday interview with NASA ISS food manager; range varies by mission and crew. |
| Vitamin B1 shelf life — ~1 year | Time before stored-food B1 degrades to inadequate | Measured | Yes, with caveat | Cooper 2017 NPJ Microgravity; room-temperature storage. |
| Vitamin C shelf life — ~3 years | Time before stored-food C degrades to inadequate | Measured | Yes, with caveat | Cooper 2017 NPJ Microgravity; room-temperature storage. |
| Beyond-LEO stored-food target — 5 years | Stored-food mission-duration target | Modelled | Yes, with caveat | Cooper 2017. |
| Microgreens growth — 7–14 days | Time from seed to harvest for microgreens | Modelled | Yes, with caveat | Horticulture reference, not a NASA lunar measurement. Use as order-of-magnitude only. |
| Lettuce growth — 28–33 days | Time from seed to first lettuce harvest | Measured | Yes | NASA BPC + Veggie ISS data; well-supported. |
| Dwarf wheat growth — ~35–86 days | Time from seed to wheat harvest | Measured | Yes | NASA BPC (64–86 d) + ISS Veggie (~35 d for dwarf variety). |
| Soybean growth — 90–97 days | Time from seed to soybean harvest | Measured | Yes | NASA BPC. |
| Plant area for food — 40–50 m²/person | Crop area needed for vegetarian diet per person | Modelled | Yes, with caveat | Wheeler NASA research; assumes vegetarian diet, controlled environment. |
| Plant area for O₂/CO₂ — 20–25 m²/person | Crop area for air revitalization per person | Modelled | Yes, with caveat | Wheeler NASA research. |
| 4-crew plant area for food — 160–200 m² | Total crop area for vegetarian food for 4 crew | Derived | Yes, with caveat | Derived from Wheeler's per-person estimate. |
| Veggie power | Power for small ISS crop chamber | To be defined | **No** | The cited NASA Veggie page (2014) does not state a wattage. A widely reported ~70 W figure (ISS National Lab / Sierra Space) requires a direct URL before use. |
| Fertilizer — up to 90 kg/person/year | Nutrient mass needed if not recycled | Modelled | Yes, with caveat | Wheeler 2020 NASA; emphasizes need for nutrient recycling. |
| Stored vs grown ratio | Split between stored and grown food | To be defined | **No** | Team modelling decision after selecting mission length. |
| Crop water — lettuce (~2 L/m²/d) | Daily water use per m² of lettuce crop | Measured (BPC) | Yes | Wheeler 2020, printed p. 9, Table 2. Gross BPC use; crop-humidity recovery in the habitat remains TBD. |
| Crop water — wheat (~5 L/m²/d) | Daily water use per m² of wheat crop | Measured (BPC) | Yes | Wheeler 2020, printed p. 9, Table 2. Gross BPC use; crop-humidity recovery in the habitat remains TBD. |
| Crop water — soybean (~5 L/m²/d) | Daily water use per m² of soybean crop | Measured (BPC) | Yes | Wheeler 2020, printed p. 9, Table 2. Gross BPC use; crop-humidity recovery in the habitat remains TBD. |
| Crop water — potato | Daily water demand per m² of potato crop | To be defined | **No** | Wheeler 2020, printed p. 9, Table 2; value not extracted. No estimate assumed. |
| Crop water demand (formula) | Total daily crop water = rate × area × 1 kg/L | Derived | Yes | Use Wheeler 2020 rates × chosen crop area. Feeds into water balance (Part C). |
| Crop electricity (full-scale) | Lighting + pumps + climate for crop system | To be defined | **No** | Illustrative estimate 18–36 kW for 180 m²; final depends on crop mix and PPFD choice. Label as gameplay assumption once chosen. |
| Initial stored food | Food available at mission start | To be defined | **No** | Dev team must pick and label as a gameplay assumption. |

---

## 5. Values Deliberately Excluded

The research paper (§8) lists values that MUST NOT be used as fixed scientific requirements in the simulation. They are excluded because the cited sources do not support them as universal lunar-mission facts.

| Excluded value | Reason |
|---|---|
| A universal 20 g/cm² lunar shielding requirement | Shielding depends on material, density, mission duration; no single universal figure. |
| A fixed human radiation dose of 1.369 mSv/day on the lunar surface | Requires a dose model; the Chang'e-4 silicon measurement MUST NOT be converted by unit-swapping. |
| A guaranteed 15–120-minute solar-storm warning time | No universal value supported by the listed sources. |
| A universal battery-storage requirement for the lunar night | Depends on habitat demand and dark-period length, which are location-specific. |
| A fixed oxygen-consumption rate specifically for a lunar spacewalk (EVA) | The 3.99 g/min aerobic-exercise value is NOT an EVA rate. An EVA-specific source is required. |

If any of these values are needed for gameplay, they MUST be entered in the sheet as **Gameplay assumption**, not as Research reference.

---

## 6. Open Decisions Required Before v1 Lock

The development team must resolve the following before the parameter set can be considered locked for v1.

| # | Decision | Affects | Owner |
|---|---|---|---|
| 1 | Mission location: equator or South Pole? | Solar generation, battery sizing, lighting model | Dev team + research |
| 2 | Mission duration: 7 / 30 / longer? | All storage calculations | Dev team |
| 3 | Activity schedule: single average O₂ rate, or activity-based? | Oxygen consumption model | Dev team |
| 4 | Water recovery: single overall rate, or per-stream (humidity / urine)? | Water balance, failure behaviour | Dev team |
| 5 | Radiation: background risk + occasional SPE only, or full dose model? | Radiation mechanic complexity | Dev team + research |
| 6 | Which systems have backup power, and which non-essential loads can be shed? | Emergency-scenario behaviour | Dev team |
| 7 | Initial reserves of O₂, water, food, battery charge at mission start | All resource loops | Dev team |
| 8 | EVA oxygen consumption rate (if EVAs are in v1) | EVA mechanic | Research |
| 9 | Food-system modelling decisions (crop mix, stored-vs-grown ratio, crop electricity value — see `food-system-research.md` §10) | Food, crop water, crop power | Dev team |
| 10 | Retrieve the potato water-use value from Wheeler 2020, printed p. 9, Table 2; use the existing L/m²/d rates for lettuce, wheat, and soybean | Crop water requirement | Research |

---

## 7. Source Index

Direct URLs for every source used in this sheet. The original research paper (§9) also lists these.

| # | Short name | URL | Used for |
|---|---|---|---|
| 1 | NASA — Astronaut Mass Balance for Long Duration Missions (Ewert & Stromgren, 2019) | https://ntrs.nasa.gov/citations/20190027563 | O₂ consumption (sleep / nominal / exercise / daily); CO₂ production; daily water; per-stream water outputs (Figure 1: urine 1.40, perspiration + respiration 3.04, feces 0.09 kg/p/d); per-stream recovery rates (page 6; Sabatier and oxygen-generation flows in Figure 6); packaged food 2.39 kg/p/d (citing NASA BVAD Table 4-53) |
| 2 | NASA — ISS Water Recovery Milestone (2023) | https://www.nasa.gov/missions/station/iss-research/nasa-achieves-water-recovery-milestone-on-international-space-station/ | Overall ~98 % system-level recovery milestone; pre-BPA water recovery rate was 93–94 % (documented in the same article) |
| 3 | Science Advances — First Measurements of the Radiation Dose on the Lunar Surface (2020) | https://pmc.ncbi.nlm.nih.gov/articles/PMC7518862/ | Chang'e-4 silicon absorbed dose; derived GCR dose-equivalent rate |
| 4 | NASA — Design for Ionizing Radiation Protection (OCHMO-TB-020) | https://www.nasa.gov/wp-content/uploads/2025/07/ochmo-tb-020-radiation-protection-rev-g.pdf | Radiation shielding and protection reference |
| 5 | NASA — Fission Surface Power | https://www.nasa.gov/exploration-systems-development-mission-directorate/fission-surface-power/ | ≥ 40 kW development target; ~10-year design life |
| 6 | NASA — Lunar South Pole Region (Moonbase Environment) | https://www.nasa.gov/reference/moonbase-environment/ | South Pole lighting and environment reference |
| 7 | NASA — Moon Fact Sheet (NSSDCA) | https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html | Lunar rotation period (27.32 d sidereal); length of day (29.53 d synodic) ⇒ ~14-day day/night cycle near equator |
| 8 | NASA — STEMonstration: Nutrition (2018) | https://www.nasa.gov/stem-content/stemonstrations-nutrition | Astronaut energy requirement (~2,500–3,500 kcal/person/day) |
| 9 | Cooper, Perchonok & Douglas — Space Food System Nutritional Quality over 3 Years (NPJ Microgravity, 2017) | https://pmc.ncbi.nlm.nih.gov/articles/PMC5466603/ | Vitamin B1 (~1 yr) and C (~3 yr) degradation; 5-year stored-food target for beyond-LEO |
| 10 | Wheeler, Mackowiak, Sager, Knott & Corey — NASA's Biomass Production Chamber (*Advances in Space Research*, 1996, 18(4/5): 215–224) | https://www.sciencedirect.com/science/article/pii/027311779500880N | Crop growth cycles (wheat 64–86 d; soybean 90–97 d; lettuce 28–30 d; potato) |
| 11 | Wheeler — NASA's Interests in Bioregenerative Life Support (2020) | https://ntrs.nasa.gov/api/citations/20200002230/downloads/20200002230.pdf | Fertilizer ~90 kg/person/year; plant area estimates |
| 12 | NASA — Growing Plants in Space | https://www.nasa.gov/exploration-research-and-technology/growing-plants-in-space | ISS crop examples; growth times (dwarf wheat 5 wk; Arabidopsis 6 wk); zinnia failure case |
| 13 | NASA — Veggie Plant Growth System Activated on ISS (2014) | https://www.nasa.gov/missions/station/veggie-plant-growth-system-activated-on-international-space-station | Veggie system description. The NASA page does not state a wattage; the ~70 W figure reported elsewhere requires a direct URL before use. |
| 14 | Fritsche — Space Crop Considerations for Human Exploration (NASA HRP, 2024) | https://ntrs.nasa.gov/api/citations/20250001897/downloads/20231215%20Space%20Crops%20HRP%20FINAL%20STRIVES%203.pdf | Leafy-greens growth model (28 d + 14 d cut-and-come-again) |
| 15 | NASA OSDR — OSD-269 (VEG-03A lettuce harvest data) | https://osdr.nasa.gov/bio/repo/data/studies/OSD-269 | VEG-03A lettuce harvested after 33 days + 3 weekly harvests |
| 16 | Horticulture references (supporting context only) | — | PPFD ranges by crop class; LED efficacy (~2.7 μmol/J); typical microgreens cycle (7–14 d). **NOT NASA lunar measurements; must not appear as fixed scientific values.** *(The previous 200–1,000 kg/kg transpiration range has been removed — use source #17 for crop water instead.)* |
| 17 | Wheeler, R. M. (2020) — NASA's Contributions to Vertical Farming (NASA TM-2020-5008832) | https://ntrs.nasa.gov/api/citations/20205008832/downloads/NASA%20TM-2020-5008832%20NASA's%20Contributions%20to%20Vertical%20Farming.pdf | **Crop water use rates** (printed p. 9, Table 2): lettuce ~2 L/m²/d; wheat ~5 L/m²/d; soybean ~5 L/m²/d. BPC measured. Potato value in Table 2 but not extracted. (Table 2 covers wheat, soybean, potato, lettuce — not tomato.) Also cites Wheeler 1996: 481 kg dry biomass, 94,700 kg condensed water across all BPC crops. |

---

## 8. Change Log

| Version | Date | Author | Notes |
|---|---|---|---|
| v1.3.2 | 2026-11-08 | Neural Knights | Verification pass against the cited NASA and peer-reviewed sources. (1) Corrected the 93 % water-recovery treatment: the NASA ISS Water Recovery Milestone article (2023) explicitly documents 93–94 % as the pre-BPA recovery rate. This is a verified NASA historical measurement; however, treating it as the guaranteed post-BPA-failure fallback rate is an engineering inference, not a direct NASA statement — classified accordingly. (2) Fixed a column-alignment error in the §4.2 failed-brine-processor row. (3) Marked the Veggie ~70 W figure as TBD: the cited NASA Veggie page (2014) does not state a wattage. (4) Removed personal-name attribution from the v1 power-model caveat. (5) No new values, calculations, or sources were introduced. |
| v1.3.1 | 2026-11-08 | Neural Knights | Clarified that 5.03 kg/person/day is a modelled water requirement, not a confirmed potable-store withdrawal; removed the unsupported potato estimate; corrected the crop-water and lunar-night power caveats; updated Ewert source locations. |
| v1.3 | 2026-11-05 | Neural Knights | Revised per follow-up engineering review: (1) §2.1 and §2.2 — added "Engineering inference" as a classification and origin type; added note explaining how the two tables relate (role vs provenance) to resolve the previous overlap. (2) §3.6 and §7 — corrected the packaged-food source attribution: the 2.39 kg value comes from NASA BVAD Table 4-53, which Ewert 2019 cites and discusses — it is not a table within the Ewert paper itself. (3) §7 source #1 — updated to include the per-stream water data from Ewert 2019 Figure 2 (urine 1.40 kg/p/d; perspiration + respiration 3.04 kg/p/d), correcting the earlier claim that per-stream data was unavailable. |
| v1.2 | 2026-11-05 | Neural Knights | Revised per engineering review: (1) §3.4 Power — clarified that the 40 kW fission target is **proposed/future technology, out of scope for v1**; added explicit "v1 power model" row stating the habitat runs on solar + battery only; added warning that battery cannot be assumed to support lunar night until demand, capacity, efficiency, and generation are all specified. (2) §3.6 and §4.6 Food — crop water rows now source-backed from Wheeler 2020 (NASA TM-2020-5008832, Table 2): lettuce ~2 L/m²/d, wheat ~5 L/m²/d, soybean ~5 L/m²/d; potato TBD (in source but not extracted); crop-water formula added. (3) §7 Source Index — added Wheeler 2020 as source #17; removed 200–1,000 kg/kg transpiration range from horticulture category #16. (4) Origin-type classifications tightened: fission rows now labelled "Research reference (proposed)" to distinguish from measured values. |
| v1.1 | 2026-11-05 | Neural Knights | Revised after team review: (1) merged `food-system-research.md` values into §3.6 and §4.6 — 13 food parameters now have research-backed values instead of "To be defined"; (2) added NASA Moon Fact Sheet as the traceable source for the ~14-day lunar day/night values; (3) expanded §7 Source Index with direct URLs and source numbers for all 16 sources, so developers can trace any value without leaving this sheet; (4) added NASA STEMonstration: Nutrition as source for the 2,500–3,500 kcal energy figure; (5) updated §6 to reflect that food research is complete and remaining food items are dev-team modelling decisions. |
| v1.0 | 2026-11-05 | Neural Knights | Initial parameter sheet derived from the research document. Food parameters are placeholders pending `food-system-research.md`. |
