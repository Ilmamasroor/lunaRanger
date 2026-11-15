# Food System Research

**Project:** Junior Astronaut Mission Trainer — Lunar Survival Simulation
**Team:** Neural Knights
**Owner:** Fatima Khan
**Date:** 8 November 2026
**Companion files:** `simulation-parameter-sheet.md` · `resource-dependency-matrix.md` · `emergency-scenarios.md`
**Scope:** Food requirements for a four-person lunar crew, with credible NASA / peer-reviewed sources.

---

## 1. Purpose

The original research paper covers oxygen, water, radiation, and power, but it does **not** cover food. The development team asked for a focused food-system investigation so that food production can be included in the simulation.

This file answers five questions:

1. How much food does each astronaut need per day?
2. Stored food vs growing food — which, and how much of each?
3. How much water and electricity does crop production require?
4. Why do crops need time to grow (and how much time)?
5. What happens if the growing system fails?

Two rules apply throughout, mirroring the parameter sheet:

1. **No invented science.** Every numerical value is either (a) traced to a cited source or (b) explicitly labelled as a gameplay assumption.
2. **"To be defined" is a valid answer** when no source has been found yet.

---

## 2. Investigation Summary

| Question | Headline finding | Source |
|---|---|---|
| Daily food per astronaut | ~2.39 kg/person/day of packaged food (≈ 2,500–3,500 kcal/person/day) | Ewert 2019 (NASA) — same mass-balance study cited in the research paper |
| Stored vs grown | ISS uses 100 % stored food; for missions > 1 year, some vitamins in stored food degrade to inadequate levels → fresh crops can help supplement stored food | Cooper et al. 2017 (NPJ Microgravity); NASA Growing Plants in Space |
| Water & electricity for crops | Veggie ISS chamber wattage not stated on the cited NASA page (TBD); full-scale vegetarian food production needs ~40–50 m² of crop area per person (lighting power for that area is a team decision) | NASA ISS Veggie; Wheeler (NASA) |
| Crop growth time | Lettuce 28–33 days; dwarf wheat ~35–86 days; soybean 90–97 days; microgreens 7–14 days | Wheeler 1996 (NASA BPC); Fritsche 2024 (NASA HRP); NASA OSDR |
| Failure consequences | Real ISS precedent: overwatered zinnias → fungal infection → plants died. Backup stored food is mandatory for any crop-based mission | NASA Growing Plants in Space; Cooper et al. 2017 |

---

## 3. Daily Food Requirement per Astronaut

### 3.1 Mass

The NASA study *Astronaut Mass Balance for Long Duration Missions* (Ewert, 2019) — the same source already used in the research paper for oxygen and water — gives a planning value of **2.39 kg of individually packaged food delivered per person per day**.

This is the packaged mass; the edible portion is less, but the packaged value is the appropriate planning number for sizing stored-food supplies.

| Parameter | Value | Unit | Source |
|---|---|---|---|
| Packaged food per astronaut | 2.39 | kg/person/day | Ewert 2019 (NASA, NTRS 20190027563) |
| Packaged food for 4 crew | 9.56 | kg/day | Derived: 2.39 × 4 |
| 30-day packaged food for 4 crew | 286.8 | kg | Derived: 9.56 × 30 |

### 3.2 Energy

| Parameter | Value | Unit | Source |
|---|---|---|---|
| Energy requirement per astronaut | ~2,500–3,500 | kcal/person/day | NASA STEMonstration: Nutrition (2018); Science Friday interview with NASA ISS food systems manager Xulei Wu (2022) |
| Energy requirement for 4 crew | ~10,000–14,000 | kcal/day | Derived: 2,500–3,500 × 4 |

Astronaut energy needs vary with body mass and activity (EVA days burn more than desk days). NASA's *STEMonstration: Nutrition* (2018) and Science Friday's 2022 interview with NASA ISS food systems manager Xulei Wu both place the range at roughly 2,500–3,500 kcal/person/day. The 2.39 kg packaged figure is the mass-balance planning value that already accounts for energy variation in the reference astronaut.

### 3.3 Simulation note

For v1, use the planning value of **2.39 kg/person/day** as the daily food-consumption rate. An activity-based food-consumption model is not needed for v1; the planning value already smooths over daily variation.

---

## 4. Stored Food vs Growing Food

### 4.1 Current practice

The International Space Station uses **100 % prepackaged food** shipped from Earth — freeze-dried, thermostabilized, and shelf-stable items (Cooper et al. 2017; NASA Growing Plants in Space). Fresh produce is occasionally delivered by cargo resupply but is consumed within days.

### 4.2 The shelf-life problem

Cooper, Perchonok & Douglas (2017), in a peer-reviewed *NPJ Microgravity* study, measured 24 micronutrients across 109 space foods stored for three years at room temperature. Key findings:

| Finding | Source |
|---|---|
| Potassium, calcium, vitamin D, vitamin K may be inadequate **even before storage** | Cooper et al. 2017 |
| Vitamins A, C, B1, B6 decrease during storage | Cooper et al. 2017 |
| **Vitamin B1 degrades to inadequate levels after ~1 year** | Cooper et al. 2017 |
| **Vitamin C degrades to inadequate levels after ~3 years** | Cooper et al. 2017 |
| Beyond-LEO missions need stored food to remain acceptable for **up to 5 years** without refrigeration | Cooper et al. 2017 |

**Implication:** Stored food alone is sufficient for short missions (ISS, 30-day lunar reference). For longer missions, fresh crops can help supplement stored food, particularly as some vitamins degrade during storage. Cooper et al. (2017) note that stored prepackaged food is *likely to continue to be the main source of nutrition* for future exploration missions, even when fresh crops are part of the plan — growing crops supplements rather than replaces stored food.

### 4.3 What fresh crops add

NASA's *Growing Plants in Space* overview states that vitamins in prepackaged form break down over time, and "freshly grown produce would provide nutrients in a long-lasting, easily absorbed form" — distinct from supplements, which cannot replicate the synergies of whole foods (Cooper et al. 2017).

### 4.4 NASA's long-term direction

NASA's Prototype Lunar/Mars Greenhouse project (University of Arizona / Kennedy Space Center, lead scientist Dr. Ray Wheeler) is designed to test a "continuous vegetarian diet" for astronauts on the Moon or Mars, using a closed-loop bioregenerative life-support system that provides food, air revitalization, water recycling, and waste recycling (University of Arizona SSEL).

### 4.5 Stored vs grown — recommended simulation split

| Mission length | Stored food | Grown food | Rationale |
|---|---|---|---|
| ≤ 30 days | 100 % | 0 % | Stored food alone is adequate; no time to grow a meaningful crop before mission end |
| ~6 months | ~90 % | ~10 % | Grown leafy greens as a nutrient supplement; bulk calories from stored |
| ≥ 1 year | ~70–80 % | ~20–30 % | Helps offset vitamin degradation (B1 after 1 yr; C after 3 yr) |

The exact split for a given mission is a **gameplay modelling decision** for the dev team — the research shows the principle (longer missions need more grown food) but does not dictate a single ratio.

---

## 5. Water and Electricity for Crop Production

### 5.1 What we know from NASA sources

| Parameter | Value | Unit | Source |
|---|---|---|---|
| Veggie ISS chamber power (lights, fans, control) | To be defined | W (total electrical) | NASA — Veggie Plant Growth System Activated on ISS (2014) does not state a wattage; the ~70 W figure reported by ISS National Lab / Sierra Space requires a direct URL to be properly cited |
| Plant area for O₂ / CO₂ removal for one person | 20–25 | m²/person | Wheeler (NASA) — bioregenerative life support presentations |
| Plant area for vegetarian food for one person | 40–50 | m²/person | Wheeler (NASA) — bioregenerative life support presentations |
| Fertilizer needed if not recycled | up to 90 | kg/person/year | Wheeler 2020 (NASA, NTRS 20200002230) |
| Plant area for vegetarian food for 4 crew (derived) | 160–200 | m² | Derived: 40–50 × 4 |
| Plant area for O₂/CO₂ for 4 crew (derived) | 80–100 | m² | Derived: 20–25 × 4 |

### 5.2 Lighting power — what the team must decide

NASA's research does not specify a single "right" lighting intensity for a lunar greenhouse; it depends on the crops chosen and the lighting technology. Reference values from horticulture and NASA's Biomass Production Chamber testing:

| Crop class | Typical PPFD (photosynthetic photon flux density) | Source |
|---|---|---|
| Low-light (lettuce, leafy greens) | 100–300 μmol/m²/s | Standard horticulture reference; NASA BPC used similar ranges for lettuce |
| Medium-light (tomato, pepper) | 300–600 μmol/m²/s | Standard horticulture reference; NASA chile-pepper experiment (PH-04) |
| High-light (wheat, soybean, rice) | 600–1,000 μmol/m²/s | Standard horticulture reference; NASA BPC used high-intensity lighting for wheat |

A modern LED fixture at ~2.7 μmol/J (horticulture-industry reference, not a NASA lunar specification) would draw roughly **200–350 W per m²** of crop canopy at the high-light end, or **~70–110 W per m²** at the low-light end. **Both the μmol/J figure and the W/m² figures are horticulture-industry references, not NASA lunar-system specifications.** The dev team must:

1. Choose a crop mix (e.g., leafy greens + dwarf wheat).
2. Choose a lighting intensity (PPFD) per crop class.
3. Multiply by the chosen crop area.
4. Sum to get total lighting power.

Until those choices are made, **"Crop electricity requirement" stays as To be defined** in the parameter sheet — labelled as a gameplay assumption once the team picks a number.

### 5.3 Water for crops — source-backed values from Wheeler 2020

**Source:** Wheeler, R. M. (2020). *NASA's Contributions to Vertical Farming*. NASA Technical Memorandum TM-2020-5008832, **printed p. 9, Table 2** for water-use rates and **printed pp. 6–7** for crop-specific growing conditions.
URL: https://ntrs.nasa.gov/api/citations/20205008832/downloads/NASA%20TM-2020-5008832%20NASA's%20Contributions%20to%20Vertical%20Farming.pdf

**Measured values (BPC, NFT hydroponics, controlled environment):**

| Crop | Average water use rate | Source location | Origin type |
|---|---|---|---|
| Lettuce | ~2 L/m²/d | Wheeler 2020, p. 9, Table 2 | Measured (BPC) |
| Wheat | ~5 L/m²/d | Wheeler 2020, p. 9, Table 2 | Measured (BPC) |
| Soybean | ~5 L/m²/d | Wheeler 2020, p. 9, Table 2 | Measured (BPC) |
| Potato | TBD — the value is reported in Wheeler 2020, p. 9, Table 2 (the table covers wheat, soybean, potato, and lettuce), but was not extracted for this brief. No estimate should be assumed. | Wheeler 2020, p. 9, Table 2 | Measured (BPC) — value to retrieve |

**Crop-specific growing conditions (Wheeler 2020, printed pp. 6–7):**

| Crop | Photoperiod | PAR (as printed in source) | Temperature | Source location |
|---|---|---:|---|---|
| Wheat | Constant light (24 h) or 20 h light / 4 h dark | 510–930 | 23°C or 20/16°C | Wheeler 2020, printed p. 6 |
| Soybean | 12 h light / 12 h dark or 10 h light / 14 h dark | 475–815 | 26/20°C | Wheeler 2020, printed p. 6 |
| Potato | 12 h light / 12 h dark; some later trials 16 h light / 8 h dark | 655–915 | 20/16°C; later 24/20°C then 20/16°C | Wheeler 2020, printed pp. 6–7 |
| Lettuce | 16 h light / 8 h dark | 280–335 (printed unit: μmol m⁻² d⁻¹) | 23°C | Wheeler 2020, printed p. 7 |

For wheat, soybean, and potato, PAR is reported in μmol m⁻² s⁻¹. The source prints the lettuce PAR unit as μmol m⁻² d⁻¹; that printed unit is retained here and is not silently corrected. These are BPC experimental conditions, not universal lunar crop requirements.

**Supporting context from Wheeler 1996:**

Wheeler, R. M., Mackowiak, C. L., Sager, J. C., Knott, W. M., & Corey, K. A. (1996). NASA's Biomass Production Chamber: a testbed for bioregenerative life support studies. ***Advances in Space Research*, 18(4/5), 215–224.**
DOI index: https://www.sciencedirect.com/science/article/pii/027311779500880N
*(Citation corrected in v1.3 — the previous version incorrectly cited this as Acta Astronautica 40(2–8): 1–11.)*

- Across all BPC crops tested (wheat, soybean, lettuce, potato): **481 kg dry plant biomass** produced, **94,700 kg condensed water** collected over the test programme.
- This confirms large water throughput — condensed water is mostly crop transpiration captured by the closed chamber's humidity-control system.

**Applicability to the simulation — important clarification:**

- The Wheeler 2020 rates describe **crop water use in the BPC system**, not net water lost from a habitat store. In the BPC, transpired water was **condensed and recycled** within the closed chamber. A lunar habitat with humidity-condensate recovery would similarly return most crop transpiration to the water loop (see the water balance in `resource-dependency-matrix.md` §12, flow 9).
- Therefore, crop water use (L/m²/d) is a **gross throughput** figure. The **net habitat water loss** from crops is much smaller — only the water incorporated into plant biomass and any unrecovered transpiration losses.
- BPC was an Earth-based closed chamber, not a lunar habitat. Values are measured Earth-side research references, not lunar operational measurements.
- Values are **per unit growing area per day** — scalable to whatever crop area the dev team chooses.
- Reasonable starting point for a lunar simulation; actual lunar system may differ due to gravity (1/6 g), atmosphere, and system design.

**Simulation formula:**
```
Crop water demand (kg/day) = water use rate (L/m²/d) × crop area (m²) × 1 kg/L
```

**Worked examples:**
- 10 m² lettuce → 2 × 10 = **20 kg/day** gross water demand (most returns as transpiration)
- 10 m² wheat → 5 × 10 = **50 kg/day** gross water demand (most returns as transpiration)
- 20 m² mixed (10 lettuce + 10 wheat) → 20 + 50 = **70 kg/day** gross water demand

**Note on the previous 200–1,000 kg/kg figure:** An earlier version of this section included a general horticulture reference of "200–1,000 kg water per kg dry biomass" as context. That figure has been **removed** per review instruction — it was a broad plant-physiology range, not a NASA measurement, and must NOT be used as a game parameter. The Wheeler 2020 L/m²/d values above are the correct source-backed figures to use.

### 5.4 Illustrative derived estimates for sizing — NOT NASA lunar-system specifications

The numbers below are **illustrative derived estimates**. They combine a research reference (Wheeler's plant-area estimate) with a chosen gameplay/design lighting intensity. They are **not** measurements or specifications from any NASA lunar-greenhouse system. They are included only to show the dev team the order of magnitude involved.

Assumptions:
- 4-person vegetarian food supply → 160–200 m² crop area (Wheeler, NASA — research reference)
- Mid-range 180 m² used for illustration
- LED power per m² chosen from horticulture-industry references (see §5.2)

| Scenario | Calculation | Result | Label |
|---|---|---|---|
| All-leafy-greens at ~100 W/m² LED | 180 m² × 100 W/m² | ~18 kW of lighting | Illustrative derived estimate |
| Mixed leafy + high-light at ~200 W/m² LED | 180 m² × 200 W/m² | ~36 kW of lighting | Illustrative derived estimate |
| Compare to fission surface-power target | 40 kW continuous | Lighting alone could consume most of the fission target | Comparison only |

**Gameplay implication:** A full vegetarian-grown food supply is power-intensive. **Feasibility cannot yet be assessed** — the v1 power budget is undefined (solar generation TBD, battery capacity TBD, total habitat demand TBD), and the fission 40 kW target is a proposed/future technology that is out of scope for v1 (Part A §3.4). Whether crop lighting at 18–36 kW is affordable depends entirely on those undefined values. The v1 power budget must be completed before deciding crop-area scale.

---

## 6. Why Crops Need Time to Grow

### 6.1 Each crop has a fixed biological growth cycle

Plants grow by photosynthesis and cell division, which have biological speed limits that no amount of power or water can shorten beyond a crop-specific minimum. The time from seed to first harvest is therefore a **hard constraint** the player must plan around.

### 6.2 NASA-measured growth cycles

From NASA's Biomass Production Chamber testing (Wheeler 1996, *Advances in Space Research* 18(4/5): 215–224) and ISS Veggie / Advanced Plant Habitat experiments:

| Crop | Days to first harvest | Source |
|---|---|---|
| Microgreens / sprouts | 7–14 | Horticulture reference (typical microgreens cycle); NASA is researching microgreens as a candidate crop (ARS/Wheeler) |
| Lettuce (BPC, controlled) | 28–30 | Wheeler 1996 (NASA BPC) |
| Lettuce (Veggie ISS, VEG-03A) | 33 + 3 weekly cut-and-come-again harvests | NASA OSDR OSD-269 |
| Leafy greens (general Veggie planning) | 28 + 14 days cut-and-come-again | Fritsche 2024 (NASA HRP, NTRS 20250001897) |
| Dwarf wheat (ISS Veggie / APH) | ~35 (5 weeks) | NASA Growing Plants in Space |
| Wheat (BPC, full-cycle) | 64–86 | Wheeler 1996 (NASA BPC) |
| Arabidopsis (research crop) | ~42 (6 weeks) | NASA Growing Plants in Space |
| Dwarf pak choi (ISS Veggie) | 64 (longest greens grown on station) | NASA Growing Plants in Space; Florida Master Gardeners report |
| Soybean (BPC, full-cycle) | 90–97 | Wheeler 1996 (NASA BPC) |

### 6.3 Why the time matters for the simulation

1. **A crop failure cannot be fixed in days.** If a lettuce crop dies on day 28, the player cannot regrow it before the next 28-day cycle completes. The crew must fall back on stored food.
2. **Cut-and-come-again extends harvest but does not speed initial growth.** Leafy greens can be harvested leaf-by-leaf for ~2 weeks after the first cut, but the initial 28-day wait still applies.
3. **A newly planted crop is a 1–3 month commitment.** Wheat and soybean tie up crop area, power, and water for months before any food is returned.

### 6.4 Recommended crop mix for the simulation

| Crop role | Suggested crop | First-harvest time | Why |
|---|---|---|---|
| Fast morale / nutrient boost | Microgreens | 7–14 days | Lowest time-investment; fresh vitamins |
| Steady fresh greens | Lettuce, dwarf pak choi | 28–33 days | Cut-and-come-again extends harvest |
| Calorie staple | Dwarf wheat | ~35–86 days | Realistic calorie source; longest wait |
| Protein / oil | Soybean | 90–97 days | Long commitment; high nutritional value |

---

## 7. What Happens If the Growing System Fails

### 7.1 Real-world precedent — the ISS zinnia failure

NASA's *Growing Plants in Space* page documents a real failure: zinnias grown in the Veggie chamber were **overwatered**, which led to **fungal growth** and **some plants dying**. Astronaut Scott Kelly nursed the surviving plants back to health. The failure was caused by a water-management error, not by an external hazard — illustrating that crop systems are sensitive to their own operation.

### 7.2 Failure modes the simulation should support

| Failure mode | Trigger | Effect | Recovery |
|---|---|---|---|
| Overwatering / fungal infection | Player sets water delivery too high | Crop dies over days; lost growth time | Reduce watering; replant |
| Lighting failure | Power diverted or lamp failure | Crop growth slows or stops | Restore power; resume growth |
| Pump / nutrient failure | Equipment fault or power loss | Crop starves; growth stops | Repair equipment |
| Contamination | Microbial intrusion | Crop unsafe to eat; discard | Sterilize system; replant |
| Total crop-area loss | Catastrophic chamber failure | All in-progress crops lost | Fall back to stored food only |

### 7.3 Mandatory backup: stored food

Because a crop failure cannot be fixed within the growth cycle, any mission that depends on grown food **must** carry enough stored food to cover the gap until the next harvest. Cooper et al. (2017) confirm that stored prepackaged food is "likely to continue to be the main source of nutrition for future exploration missions" — even when fresh crops are part of the plan.

### 7.4 Nutritional consequences of failure

If the growing system fails, the crew loses access to **fresh vitamins** that the stored food may already be short of (Cooper et al. 2017: potassium, calcium, vitamin D, vitamin K may be inadequate even before storage). On a long mission, this compounds over time:

| Mission time at which crop system fails | Nutritional consequence |
|---|---|
| Day 0–365 | Manageable — stored food still has most vitamins |
| Day 365+ | Stored food vitamin B1 may be inadequate (Cooper 2017) |
| Day 1095+ | Stored food vitamin C may also be inadequate (Cooper 2017) |

**Gameplay implication:** On a long mission, a crop failure isn't just a food-mass problem — it's a slow nutritional deficit that worsens over time.

---

## 8. Game-Design Parameters (forward reference to `simulation-parameter-sheet.md`)

These values update the food placeholder in §3.6 of the parameter sheet.

| Parameter | Value | Unit | Source / Qualification | Classification |
|---|---|---|---|---|
| Packaged food per astronaut | 2.39 | kg/person/day | Ewert 2019 (NASA, NTRS 20190027563) — same source as O₂ and water | Research reference |
| Packaged food (4 crew) | 9.56 | kg/day | Derived: 2.39 × 4 | Derived calculation |
| 30-day packaged food (4 crew) | 286.8 | kg | Derived: 9.56 × 30 | Derived calculation |
| Energy requirement per astronaut | ~2,500–3,500 | kcal/person/day | NASA STEMonstration: Nutrition (2018); Science Friday interview with NASA ISS food systems manager (2022) | Research reference |
| Stored-food shelf life (vitamin B1) | ~1 year before inadequate | years | Cooper et al. 2017 (NPJ Microgravity) | Research reference |
| Stored-food shelf life (vitamin C) | ~3 years before inadequate | years | Cooper et al. 2017 (NPJ Microgravity) | Research reference |
| Stored-food target for beyond-LEO | up to 5 | years | Cooper et al. 2017 (NPJ Microgravity) | Research reference |
| Crop growth time — microgreens | 7–14 | days | Horticulture reference (typical cycle); NASA is researching microgreens as a candidate crop | Research reference (horticulture) |
| Crop growth time — lettuce | 28–33 | days | Wheeler 1996 (NASA BPC); NASA OSDR OSD-269 | Research reference |
| Crop growth time — dwarf wheat | ~35–86 | days | NASA Growing Plants in Space; Wheeler 1996 (NASA BPC) | Research reference |
| Crop growth time — soybean | 90–97 | days | Wheeler 1996 (NASA BPC) | Research reference |
| Plant area for food (vegetarian) | 40–50 | m²/person | Wheeler (NASA) bioregenerative life-support research | Research reference |
| Plant area for O₂/CO₂ removal | 20–25 | m²/person | Wheeler (NASA) bioregenerative life-support research | Research reference |
| Plant area for food (4 crew) | 160–200 | m² | Derived: 40–50 × 4 | Derived calculation |
| Veggie ISS chamber power | To be defined | W | NASA Veggie page (2014) does not state a wattage; the ~70 W figure reported elsewhere (ISS National Lab / Sierra Space) requires a direct URL to be properly cited | Requires research |
| Fertilizer required (no recycling) | up to 90 | kg/person/year | Wheeler 2020 (NASA, NTRS 20200002230) | Research reference |
| Stored vs grown ratio | To be defined | ratio | Team decision; §4.5 gives recommended ranges by mission length | Requires modelling decision |
| Crop water use — lettuce | ~2 | L/m²/d | Wheeler 2020 (NASA TM-2020-5008832, Table 2) — BPC measured | Research reference |
| Crop water use — wheat | ~5 | L/m²/d | Wheeler 2020 (NASA TM-2020-5008832, Table 2) — BPC measured | Research reference |
| Crop water use — soybean | ~5 | L/m²/d | Wheeler 2020 (NASA TM-2020-5008832, Table 2) — BPC measured | Research reference |
| Crop water use — potato | TBD — value reported in Wheeler 2020 p. 9 Table 2 but not extracted; no estimate assumed | L/m²/d | Wheeler 2020, p. 9, Table 2 | Requires research (source located) |
| Crop water demand (formula) | rate × area × 1 kg/L | kg/day | Derived from Wheeler 2020 L/m²/d values | Derived calculation |
| Crop electricity requirement (full-scale) | To be defined | kW | Illustrative estimate 18–36 kW for a 180 m² setup (`food-system-research.md` §5.4); final value depends on crop mix and PPFD choice — NOT a NASA lunar-system spec | Gameplay assumption (once chosen) |
| Initial stored food (mission start) | To be defined | kg | Engineering decision | Gameplay assumption |

---

## 9. Sources

Sources include NASA, peer-reviewed research and supporting horticulture references. URLs verified 8 November 2026.

1. **NASA — Astronaut Mass Balance for Long Duration Missions (Ewert, 2019)**
   https://ntrs.nasa.gov/citations/20190027563
   Used for: packaged-food planning value of 2.39 kg/person/day. This is the same source the research paper uses for oxygen, CO₂, and water values, so units and methodology are consistent across sheets.

2. **Cooper, Perchonok & Douglas — Initial assessment of the nutritional quality of the space food system over three years of ambient storage (NPJ Microgravity, 2017)**
   https://pmc.ncbi.nlm.nih.gov/articles/PMC5466603/
   Used for: vitamin degradation rates (B1 ~1 year; C ~3 years); the 5-year stored-food target for beyond-LEO missions; the role of stored food as the main source of nutrition.

3. **Wheeler, Mackowiak, Sager, Knott & Corey — NASA's Biomass Production Chamber: a testbed for bioregenerative life support studies (*Advances in Space Research*, 1996, 18(4/5): 215–224)**
   https://www.sciencedirect.com/science/article/pii/027311779500880N
   Also indexed: https://pubmed.ncbi.nlm.nih.gov/11538800
   Used for: crop growth cycles (wheat 64–86 days; soybean 90–97 days; lettuce 28–30 days; potato); BPC potato yields; BPC biomass and condensed-water totals (481 kg dry biomass, 94,700 kg condensed water). Crop water-use rates (L/m²/d) are sourced from Wheeler 2020 (source #13 below), not this paper.

4. **Wheeler — NASA's Interests in Bioregenerative Life Support (NASA, 2020)**
   https://ntrs.nasa.gov/api/citations/20200002230/downloads/20200002230.pdf
   Used for: fertilizer requirement of up to 90 kg/person/year if nutrients are not recycled.

5. **NASA — Growing Plants in Space (NASA, updated Dec 2023)**
   https://www.nasa.gov/exploration-research-and-technology/growing-plants-in-space
   Used for: ISS crop examples (lettuce, Chinese cabbage, mizuna, kale, zinnia, dwarf wheat, chile peppers); growth times (Arabidopsis 6 weeks; dwarf wheat 5 weeks); the zinnia overwatering / fungal failure case as a real-world precedent.

6. **NASA — Veggie Plant Growth System Activated on International Space Station (NASA, May 2014)**
   https://www.nasa.gov/missions/station/veggie-plant-growth-system-activated-on-international-space-station
   Used for: Veggie system description. **The NASA page does not state a wattage.** A widely reported ~70 W figure (attributed to ISS National Lab / Sierra Space facility pages) requires a direct URL to be properly cited; until then, the Veggie chamber power remains TBD.

7. **Fritsche — Space Crop Considerations for Human Exploration (NASA Human Research Program, 2024)**
   https://ntrs.nasa.gov/api/citations/20250001897/downloads/20231215%20Space%20Crops%20HRP%20FINAL%20STRIVES%203.pdf
   Used for: leafy-greens growth model — 28 days to first harvest + 14 days cut-and-come-again.

8. **NASA OSDR — OSD-269 (VEG-03A lettuce harvest data)**
   https://osdr.nasa.gov/bio/repo/data/studies/OSD-269
   Used for: VEG-03A lettuce harvested after 33 days of growth, followed by 3 weekly harvests.

9. **Wheeler (NASA) — Plants for Bioregenerative Life Support Systems in Space (presentation, 2025)**
   https://www.thewaite.org/event/p4s-presents-dr-raymond-m-wheeler-plants-for-bioregenerative-life-support-systems-in-space
   Used for: plant-area estimates — 20–25 m²/person for O₂/CO₂ removal; 40–50 m²/person for vegetarian food.

10. **University of Arizona SSEL — Prototype Lunar/Mars Greenhouse**
    https://ssel.arizona.edu/missions/prototype-lunarmars-greenhouse
    Used for: closed-loop bioregenerative life-support concept; "continuous vegetarian diet" design goal.

11. **NASA — STEMonstration: Nutrition (2018)**
    https://www.nasa.gov/stem-content/stemonstrations-nutrition
    Used for: astronaut energy requirement (~2,500–3,500 kcal/person/day). Corroborated by Science Friday's 2022 interview with NASA ISS food systems manager Xulei Wu (https://www.sciencefriday.com/segments/nasa-chef-astronaut-food/).

12. **Horticulture references (supporting context only)**
    Used for: PPFD ranges by crop class (low / medium / high light); modern LED efficacy (~2.7 μmol/J); typical microgreens cycle (7–14 days). **None of these are NASA lunar measurements. They are included as context for design decisions only and must NOT appear in the simulation as fixed scientific values.**
    *(Note: the previous "200–1,000 kg water per kg dry biomass" transpiration range has been removed from this category per review instruction — it must not be used as a game parameter. Source-backed crop water values now come from Wheeler 2020, source #13 below.)*

13. **Wheeler, R. M. (2020). NASA's Contributions to Vertical Farming. NASA TM-2020-5008832.**
    https://ntrs.nasa.gov/api/citations/20205008832/downloads/NASA%20TM-2020-5008832%20NASA's%20Contributions%20to%20Vertical%20Farming.pdf
    Used for: **crop water use rates** — lettuce ~2 L/m²/d; wheat ~5 L/m²/d; soybean ~5 L/m²/d (**printed p. 9, Table 2**, "Rates of acid, stock solution, and water use for typical wheat, soybean, potato, and lettuce crops"). The potato value is in Table 2 but was not extracted for this brief. Also cites Wheeler 1996 (*Adv. Space Res.* 18(4/5): 215–224): 481 kg dry biomass, 94,700 kg condensed water across all BPC crops.

---

## 10. Open Questions

| # | Question | Owner |
|---|---|---|
| 1 | Retrieve the potato water-use value from Wheeler 2020 p. 9 Table 2 (lettuce/wheat/soybean already extracted; tomato is not in Table 2 — find a separate source if needed) | Research |
| 2 | Choose a crop mix for v1 (e.g., leafy greens + dwarf wheat, or microgreens + lettuce only) | Dev team |
| 3 | Choose a lighting intensity (PPFD) per crop class; calculate total lighting power | Dev team |
| 4 | Choose a stored-vs-grown ratio for the v1 mission length | Dev team |
| 5 | Decide whether crop failures in v1 are: (a) scripted scenario events, (b) random equipment failures, or (c) player-caused (overwatering, underpowering) | Dev team |
| 6 | Decide the initial stored-food stock at mission start | Dev team |
| 7 | Decide whether the simulation models crop nutritional content (vitamins) or only food mass | Dev team |

---

## 11. Change Log

| Version | Date | Author | Notes |
|---|---|---|---|
| v1.3.2 | 2026-11-08 | Neural Knights | Verification pass against the cited NASA sources. (1) Marked the Veggie ~70 W figure as TBD: the cited NASA Veggie page (2014) does not state a wattage, and the value reported elsewhere (ISS National Lab / Sierra Space) requires a direct URL to be properly cited. Updated §2 summary, §5.1, §8, and source #6. (2) Updated source #3 description: crop-water values are already extracted in §5.3 and source #13, so the outdated "to be extracted by the dev team" wording was removed. (3) Removed personal-name attribution from §5.4. (4) No new values, calculations, or sources were introduced. |
| v1.3.1 | 2026-11-08 | Neural Knights | Added crop-specific BPC photoperiod, PAR, and temperature conditions from Wheeler 2020 printed pp. 6–7; retained source-backed crop-water rates and clarified their gross-throughput scope. |
| v1.3 | 2026-11-05 | Neural Knights | Revised per follow-up engineering review: (1) §5.3 — added exact source location (Wheeler 2020, printed page 9, Table 2); added crop-specific growing conditions note (each crop had different light schedule, PAR, temperature — retrieve p. 9 for exact values); removed unsupported potato 2–5 L/m²/d estimate (now simply TBD); removed tomato from Table 2 list (source identifies wheat, soybean, potato, lettuce only); clarified rates are BPC gross water-use, not net habitat loss (transpired water was condensed and recycled in the BPC); corrected Wheeler 1996 citation to Advances in Space Research 18(4/5): 215–224 (was incorrectly Acta Astronautica 40(2–8): 1–11). (2) §5.4 — replaced the full-vegetarian infeasibility conclusion: feasibility cannot yet be assessed because the v1 power budget (solar, battery, demand) is undefined and fission is out of scope for v1. |
| v1.2 | 2026-11-05 | Neural Knights | Revised per engineering review: (1) §5.3 replaced — crop water now source-backed from Wheeler 2020 (NASA TM-2020-5008832, Table 2): lettuce ~2 L/m²/d, wheat ~5 L/m²/d, soybean ~5 L/m²/d; the 200–1,000 kg/kg horticulture figure removed entirely; simulation formula and worked examples added. (2) §5.4 — added engineering finding that 18–36 kW crop lighting exceeds the 40 kW fission target, so full vegetarian is not feasible with proposed power. (3) §8 — crop water rows now have real values instead of "To be defined". (4) §9 — added Wheeler 2020 as source #13; removed 200–1,000 kg/kg from horticulture category. (5) §10 — updated open question #1 to reflect that lettuce/wheat/soybean are extracted; potato/tomato still needed. |
| v1.1 | 2026-11-05 | Neural Knights | Revised after team review: (1) added NASA STEMonstration: Nutrition as source for the 2,500–3,500 kcal energy figure; (2) added explicit horticulture-reference disclaimers for microgreens, PPFD ranges, and LED efficacy; (3) re-labelled the 18–36 kW lighting estimates as illustrative derived estimates, not NASA lunar specs; (4) reinforced that the 200–1,000 kg/kg water figure is context only and MUST NOT be used as a simulation value; (5) softened the stored-food conclusion to match Cooper 2017 wording (crops supplement, do not replace, stored food); (6) corrected the source-list description to acknowledge horticulture references. |
| v1.0 | 2026-11-05 | Neural Knights | Initial food-system research. |
