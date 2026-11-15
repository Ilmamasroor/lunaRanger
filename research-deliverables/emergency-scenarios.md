# Emergency Scenarios

**Project:** Junior Astronaut Mission Trainer — Lunar Survival Simulation
**Team:** Neural Knights
**Owner:** Fatima Khan
**Date:** 8 November 2026
**Companion files:** `simulation-parameter-sheet.md` · `food-system-research.md` · `resource-dependency-matrix.md`

---

## 1. Purpose

This file proposes three realistic gameplay scenarios for the lunar survival simulation. Each scenario stress-tests a specific part of the resource dependency matrix (Part C) and forces the player to make trade-offs between competing systems.

For each scenario:

- **Initial situation** — what triggers the emergency and the starting state.
- **Affected systems** — which systems are involved, mapped to dependency edges from Part C §4.
- **Player decisions** — two or more meaningful choices the player must make.
- **Resource consequences** — what happens to O₂, water, food, power, and crew as a result.
- **Scientific evidence vs gameplay assumptions** — every research value is traced to a source in Part A or B; every invented number is explicitly labelled as a gameplay assumption.

Two rules apply, mirroring the parameter sheet:

1. **No invented science.** Numerical values that come from research are cited; numerical values that are gameplay choices are labelled as such.
2. **Meaningful consequences.** Each scenario must force a trade-off where no option is obviously correct, and the consequences must persist (not resolve instantly).

---

## 2. Scenario at a Glance

| # | Scenario | Trigger | Edges stressed (Part C) | Loop stressed | Primary tension |
|---|---|---|---|---|---|
| 1 | Solar power generation decreases | Panel degradation or lunar night at equator | 5, 6, 7, 10, 16 (all power feeds) | Loop A (cascade) + Loop B (crop vs power) | Life-support power vs crop power |
| 2 | Water recycling equipment malfunctions | Component failure (brine processor / urine processor) | 3, 4, 7, 8, 11 (water + electrolysis + crops) | Loop A (water → O₂ cascade) | Crew water vs electrolysis vs crops |
| 3 | Solar particle event triggers shelter decision | Gameplay system announces SPE *(monitor detection mechanism and advance warning are gameplay assumptions — see §5.5)* | 14, 15, 16 (shelter + crew labour + monitoring) | Loop C (SPE pause) | Shelter safety vs productive time |

---

## 3. Scenario 1 — Solar Power Generation Decreases

### 3.1 Initial situation

The habitat's solar power generation drops suddenly. Two realistic triggers:

- **Trigger A — Dust accumulation or partial array failure.** A solar panel array degrades. Generation drops by a gameplay-defined percentage (e.g., 40 % reduction). This can happen at any point in the lunar day. *Note: the specific causes (lunar dust, micrometeoroid damage, tracking fault) are scenario triggers / design assumptions for gameplay, not exhaustively quantified in the companion research. The research paper §5.2 establishes that solar output depends on location, panel orientation, equipment efficiency, and environmental conditions, but does not give per-cause degradation rates.*
- **Trigger B — Lunar night at equator.** The habitat enters the ~14-day lunar night. A solar-only habitat loses all solar generation until sunrise. *(Research reference: NASA Moon Fact Sheet — synodic day 29.53 d ⇒ ~14.75 d daylight / ~14.75 d darkness.)*

In both cases, the habitat attempts to draw on battery storage. **Whether the battery can actually sustain life support through the event is NOT established** — it depends on habitat average power demand (TBD — Part A §3.4), usable battery capacity (TBD), battery efficiency (TBD), and the remaining solar generation (TBD for Trigger A; zero for Trigger B). Fission power (40 kW NASA target) is a proposed/future technology and is **out of scope for v1** (Part A §3.4). The scenario must NOT imply that battery or backup sources can support the lunar night until those four values are specified.

**Starting state at trigger:**
- Battery charge: TBD (gameplay assumption — dev team picks opening reserve)
- Crew of 4: O₂ requirement 3.56 kg/day · CO₂ production 4.32 kg/day · water requirement reference 20.12 kg/day (potable-store withdrawal TBD) · packaged food 9.56 kg/day
- Crop system: optionally running (illustrative 18–36 kW estimate for a 180 m² setup — Part B §5.4; not a validated habitat load)

### 3.2 Affected systems (mapped to Part C edges)

| Edge | Dependency affected | What happens |
|---|---|---|
| 5 | Power → Air (electrolysis) | O₂ generation at risk if power drops |
| 6 | Power → Air (CO₂ removal) | CO₂ removal at risk → CO₂ accumulates at 4.32 kg/day |
| 7 | Power → Water recycling | Water recovery at risk → reserves deplete faster |
| 10 | Power → Food / Crops | Crop lighting is a candidate for load-shedding; its relative size in the habitat power budget is unknown |
| 16 | Power → Radiation (monitoring) | Draw TBD; detection capability and warning are gameplay assumptions |

**Loops stressed:** Loop A (Power ↔ Water ↔ O₂ cascade) and Loop B (Power ↔ Crops ↔ Food).

### 3.3 Player decisions

**Decision 1 — Load-shedding priority.** The player must decide which systems get full power, which get reduced, and which get paused. Use the 3-tier priority scheme from Part A §3.4 (Critical / Important / Reducible — a gameplay scheme, NOT a NASA operating procedure):

| Tier | Systems | Action |
|---|---|---|
| Critical | O₂ generation, CO₂ removal, thermal control | Keep at full power |
| Important | Water recycling, essential lighting, radiation monitoring | Reduce if needed |
| Reducible | Crop lighting, non-essential experiments, some rover activities | Pause first |

The player chooses where to draw the line between Important and Reducible.

**Decision 2 — Crop power fate.** The crop system has an illustrative 18–36 kW estimate for a 180 m² setup (Part B §5.4); its relative size in the habitat power budget is unknown. The player must decide:

- **Option A — Keep crops on.** This adds the crop-system load to the demand on available power. Whether battery depletion is faster, and whether power is lost before sunrise or repair, depends on the undefined habitat power budget.
- **Option B — Shed crop power.** This removes the crop-system load from the demand on available power; whether that materially extends battery operation depends on the undefined habitat power budget. Risk: crop growth cycle lost (lettuce 28–33 d, dwarf wheat ~35–86 d — Part B §6.2). Crew falls back to stored food (9.56 kg/day packaged, Part A §3.6).
- **Option C — Partial crop power.** Reduce lighting intensity (lower PPFD). Crop response is a gameplay assumption; the dev team must define how PPFD maps to growth rate.

**Decision 3 — Repair vs wait (Trigger A only).** If the trigger is panel damage rather than lunar night:

- **Option A — Send crew on EVA to repair.** Costs crew time and EVA O₂ (TBD — Part A §3.1 notes EVA O₂ rate requires an EVA-specific source). Restores generation sooner.
- **Option B — Wait for replacement or sunrise.** No EVA risk, but the battery would need to last until then (whether it can is TBD — v1 power budget undefined).

### 3.4 Resource consequences

> **Calculation (plain English):** One astronaut requires ~0.89 kg of oxygen per day (NASA 2019 mass-balance). For four astronauts: 0.89 × 4 = **3.56 kg/day**. If O₂ generation stops, the habitat must supply ~3.56 kg from stored oxygen each day. The modelled daily water requirement is 5.03 × 4 = **20.12 kg/day**; this is not automatically the potable-store withdrawal. Packaged food demand is 2.39 × 4 = **9.56 kg/day**, and CO₂ is produced at 1.08 × 4 = **4.32 kg/day**.

| Player choice | O₂ | Water | Food / Crops | Power |
|---|---|---|---|---|
| Crops on, life support full | Reserves stable if power sustains life support | Reserves stable if power sustains recycling | Crops survive | Battery depletion rate depends on the undefined power budget |
| Crops shed, life support full | Reserves stable if power sustains life support | Reserves stable if power sustains recycling | Crops lost; fall back to stored food (286.8 kg for 30-day mission, Part A §3.6) | Battery depletion rate depends on the undefined power budget; shedding crops reduces demand |
| Crops partial | Reserves stable if power sustains life support | Reserves stable if power sustains recycling | Crops slow (gameplay assumption) | Battery depletion rate depends on the undefined power budget |
| Life support also reduced | O₂ generation drops → reserves deplete at up to 3.56 kg/day | Water recycling drops → recovered inflows reduced (net depletion depends on undefined store boundary — see Part C §12) | Crops likely shed | Battery extends further if the demand reduction exceeds the critical-load impact, but life-support risk rises |

**Cascade risk (Loop A):** If battery fully depletes, power-fed systems stop **in order of the load-shedding priority the player has set** — the player may have already paused some systems before total depletion. Systems still powered at depletion stop:
- If O₂ generation was still powered, it stops → O₂ reserves deplete at 3.56 kg/day
- If CO₂ removal was still powered, it stops → CO₂ accumulates at 4.32 kg/day
- If water recycling was still powered, it stops → recovered-water inflows are reduced. **Note:** 20.12 kg/day is the modelled crew water requirement, not the net storage depletion or confirmed tank withdrawal. Actual depletion depends on the defined store boundary and return/recovery flows (see Part C §12).
- If crop lighting was still powered, it stops → crops die over days (gameplay assumption)

### 3.5 Scientific evidence vs gameplay assumptions

| Item | Type | Source / classification |
|---|---|---|
| ~14-day lunar night at equator | Research reference | NASA Moon Fact Sheet (Part A §7 source #7) |
| Fission surface power 40 kW target | Research reference — proposed, not deployed | NASA Fission Surface Power (Part A §7 source #5) |
| Crew O₂ demand 3.56 kg/day | Research reference | NASA 2019 mass-balance (Part A §3.1) |
| Crew CO₂ production 4.32 kg/day | Research reference | NASA 2019 mass-balance (Part A §3.1) |
| Crew daily water requirement 20.12 kg/day (not confirmed tank withdrawal) | Research reference | NASA 2019 mass-balance (Part A §3.2); Part C §12 |
| Crew food demand 9.56 kg/day | Research reference | Ewert 2019 (Part A §3.6) |
| Crop growth times (28–33 d lettuce, 35–86 d wheat) | Research reference | Wheeler 1996 NASA BPC; NASA Growing Plants in Space (Part A §3.6) |
| Crop power 18–36 kW for full vegetarian | Derived illustrative estimate | Part B §5.4 — NOT a NASA lunar spec |
| Solar panel degradation percentage | Gameplay assumption | Dev team picks (e.g., 40 %) |
| Battery capacity | Gameplay assumption | TBD — Part A §3.4 |
| Repair time for EVA | Gameplay assumption | Dev team picks; EVA O₂ rate itself requires research (Part A §3.1) |
| 3-tier load-shed priority scheme | Gameplay assumption | Proposed in research paper §5.5; NOT a NASA operating procedure |
| How PPFD reduction maps to growth rate | Gameplay assumption | Dev team defines |

### 3.6 v1 implementation notes

- The scenario can be triggered at mission day 14 as a fixed gameplay setup, or randomly for replayability. Day 14 is not a universal lunar-night start; the trigger assumes the mission is aligned to the selected lunar-day phase.
- For v1, use a simplified binary crop decision (on/off) rather than partial PPFD.
- The 3-tier priority scheme can be a drag-and-drop UI: player assigns each system to a tier.

---

## 4. Scenario 2 — Water Recycling Equipment Malfunctions

### 4.1 Initial situation

A water-recycling component fails. Realistic candidates based on ISS precedent:

- **Brine processor failure** — the system that extracts remaining water from concentrated urine brine.
- **Urine processor failure** — the upstream urine-water recovery system.
- **Humidity condensate path blockage** — the path that collects moisture from cabin air.

The failure reduces the overall water-recovery rate. Water reserves begin depleting as the recycling system's recovery capability decreases. The actual daily depletion depends on the defined potable-store boundary, crew return streams, the recovery rate after failure (gameplay assumption), crop-water recirculation, Sabatier output, and other losses. The crew urine and humidity reference streams are now listed separately in Part C §12, but **net depletion still cannot be calculated** because store withdrawal and several return/loss flows remain TBD.

**Starting state at trigger:**
- Water storage: TBD (gameplay assumption — Part A §3.2 lists initial stored water as TBD)
- Crew daily water requirement reference: 20.12 kg/day; potable-store withdrawal TBD (Part C §12)
- Crew urine water reference: 5.60 kg/day; crew humidity water reference: 12.16 kg/day for four crew (Part C §12); recovered quantities depend on processing and the defined system boundary
- If electrolysis is running: ~4.0 kg/day stoichiometric minimum water feed for O₂ generation (Part C edge 8 — derived calculation)

### 4.2 Affected systems (mapped to Part C edges)

| Edge | Dependency affected | What happens |
|---|---|---|
| 3 | Crew → Water (wastewater return) | Wastewater still produced but recycling can't process it fully |
| 4 | Water → Crew (potable supply) | Reserves deplete; crew may face rationing |
| 7 | Power → Water recycling | The failed subsystem draws power but produces less |
| 8 | Water → Air (electrolysis feed) | If the water available for electrolysis falls below ~4.0 kg/day (the stoichiometric minimum for 3.56 kg/day O₂), O₂ generation must be reduced or stopped |
| 11 | Water → Food / Crops | Crop water may need to be rationed |

**Loop stressed:** Loop A (water → O₂ cascade). A water shortage becomes an O₂ shortage through electrolysis.

### 4.3 Player decisions

**Decision 1 — Repair vs conserve.**

- **Option A — Repair the failed component.** Costs crew time and possibly spare parts. Recovery rate restored once complete. Repair time is a gameplay assumption (dev team picks).
- **Option B — Conserve water instead.** No repair risk, but crew must reduce consumption and crops may be rationed. Risk: reserves deplete before repair becomes necessary anyway.

**Decision 2 — Water allocation.** If water is scarce, the player must ration among competing uses:

| Use | Daily demand | Consequence if reduced |
|---|---|---|
| Crew water requirement | 20.12 kg/day reference (Part A §3.2); potable-store withdrawal TBD (Part C §12) | Crew health emergency if cut too far |
| Electrolysis feed (for O₂) | ~4.0 kg/day stoichiometric minimum (Part C edge 8) — **this is a daily flow rate, not a storage threshold.** If the available daily water for electrolysis falls below ~4.0 kg/day, O₂ generation must be reduced or stopped. | O₂ generation drops; O₂ reserves deplete at up to 3.56 kg/day |
| Crop water | Lettuce ~2; wheat ~5; soybean ~5 L/m²/d; potato TBD (Wheeler 2020, Part B §5.3) | Crops fail; fall back to stored food |

The player chooses how to split a limited water budget across these three. There is no obviously correct split.

**Decision 3 — Emergency reserves.** Draw from emergency water reserves (TBD — Part A §3.2) to bridge the gap, or hold reserves in case the situation worsens.

**Decision 4 — Sabatier maximization.** Push the Sabatier reactor (edge 9) to recover more water from CO₂ + H₂. Recovery percentage is TBD (Part C edge 9 — depends on system and available H₂). This is a research gap, not a guaranteed fallback.

### 4.4 Resource consequences

> **Calculation (plain English):** Producing 32 kg of O₂ via electrolysis theoretically requires 36 kg of water (2 H₂O → 2 H₂ + O₂; 36 kg water → 32 kg O₂). Therefore, producing 3.56 kg/day of O₂ requires 3.56 × 36/32 = **~4.0 kg/day** of water. This is a theoretical minimum before system losses. If the water available for electrolysis falls below ~4.0 kg/day, O₂ generation must be reduced or stopped (assuming no alternative water supply).

| Player choice | Water | O₂ | Crops |
|---|---|---|---|
| Repair quickly, no rationing | Reserves may stabilise or recover after repair **if** the restored recovery rate is sufficient to meet ongoing demand | Stable | Stable |
| Conserve, ration crew only | Reserves deplete slower | Stable (electrolysis preserved) | Stable |
| Conserve, cut electrolysis feed | Reserves deplete slower | O₂ generation drops; reserves deplete at up to 3.56 kg/day | Stable |
| Conserve, cut crop water | Reserves deplete slower | Stable | Crops fail over days; fall back to stored food |
| Cut everything to minimum | Reserves last longest | O₂ generation drops | Crops fail |

**Cascade risk (Loop A):** If the water available for electrolysis falls below ~4.0 kg/day (the stoichiometric minimum for 3.56 kg/day O₂):
- O₂ generation must be reduced or stopped (edge 8 broken)
- O₂ reserves deplete at up to 3.56 kg/day (edge 2)
- Emergency O₂ reserves (TBD — Part A §3.1) must cover until water is restored

**Rationing caveat:** Reducing crew water requirement does not necessarily translate into an equivalent reduction in net water-store loss. The reference urine and humidity streams are listed in Part C §12, but the potable-store debit, stream treatment, and recovery boundary remain TBD. Any savings from rationing are gameplay assumptions until that balance is defined.

### 4.5 Scientific evidence vs gameplay assumptions

| Item | Type | Source / classification |
|---|---|---|
| Crew daily water requirement 20.12 kg/day (not confirmed tank withdrawal) | Research reference | NASA 2019 mass-balance (Part A §3.2); Part C §12 |
| Humidity condensate recovery ~99 % | Research reference — per-stream model figure | NASA 2019 (Part A §3.2) |
| Urine water recovery ~85 % | Research reference — per-stream model figure | NASA 2019 (Part A §3.2) |
| Overall ISS water-recovery milestone ~98 % | Research reference — system-level, not per-stream | NASA 2023 (Part A §3.2) |
| ISS water-recovery rate before Brine Processor Assembly (BPA) | Research reference — ~93–94 % (NASA-documented pre-BPA rate) | NASA 2023 (Part A §3.2): "before the implementation of the Brine Processor Assembly (BPA), the total water recovery was between 93–94 %" |
| Electrolysis water feed ~4.0 kg/day stoichiometric minimum | Derived calculation | Part C edge 8 (2 H₂O → 2 H₂ + O₂; 36 kg water → 32 kg O₂) |
| Crew O₂ demand 3.56 kg/day | Research reference | NASA 2019 (Part A §3.1) |
| **Which component fails** | Gameplay assumption | Dev team picks; ISS has multiple components |
| **Recovery rate after BPA failure** | Engineering inference | NASA documents 93–94 % as the historical ISS water-recovery rate before the Brine Processor Assembly was added (NASA 2023, Part A §3.2). Treating this as the guaranteed post-BPA-failure rate is an engineering inference, not a direct NASA statement. |
| **Recovery rate after other component failure** | Gameplay assumption | If a non-BPA component fails (urine processor, humidity condensate path), the resulting recovery rate requires a modelling decision. |
| Repair time | Gameplay assumption | Dev team picks |
| Emergency water reserve size | Gameplay assumption | TBD — Part A §3.2 |
| Sabatier recovery percentage | Requires research / gameplay assumption | Part C edge 9 — magnitude TBD |
| Crew potable-store withdrawal and net return balance | Requires modelling decision / research | Part C §12 — reference streams listed; store boundary and some stream treatment remain TBD |

### 4.6 v1 implementation notes

- The research reference separates crew humidity and urine streams and gives different model recovery rates. For v1, either retain those streams separately or explicitly document a simplified aggregate gameplay mechanic; do not present the aggregate as a NASA per-stream rate.
- The water → O₂ cascade (edge 8) is the key gameplay tension — make sure the player sees the O₂ impact of water rationing.
- If BPA fails, the NASA-documented pre-BPA recovery rate of 93–94 % (NASA ISS water recovery milestone, 2023) is a reasonable engineering inference for the post-failure rate, but this inference is not directly established by the NASA source. If a different component fails, the resulting recovery rate requires a modelling decision.

---

## 5. Scenario 3 — Solar Particle Event Triggers a Shelter Decision

### 5.1 Initial situation

For this scenario, the gameplay system announces an incoming solar particle event (SPE). The use of radiation monitors to detect the event, including the detection mechanism and advance warning, is a **gameplay assumption**; the cited sources do not establish a specific monitor capability or warning time. SPEs are periods when the Sun releases large numbers of energetic particles; radiation levels can rise significantly (research paper §4.1 — no specific multiplier given).

The crew must decide whether and when to move into the habitat's radiation shelter. The shelter reduces exposure during the event (research paper §4.4 — specific protection factor TBD).

**Starting state at trigger:**
- Background radiation: Chang'e-4 derived GCR dose-equivalent rate 57.1 ± 10.6 μSv/hour (Science Advances 2020 — Part A §3.3). **This is a derived value, not a universal human effective dose.**
- SPE incoming: intensity and duration unknown until the event arrives and passes.
- Warning time: TBD — **no universal 15–120 min value is supported by the cited sources** (Part A §5 excluded value).
- Crew of 4 may be mid-task: EVA, crop tending, equipment repair.

### 5.2 Affected systems (mapped to Part C edges)

| Edge | Dependency affected | What happens |
|---|---|---|
| 14 | Radiation Protection → Crew (shelter) | Shelter reduces exposure if crew enters; factor TBD |
| 15 | Crew → Food / Crops (labour) | Crop tending pauses while crew shelters |
| 16 | Power → Radiation (monitoring) | If the gameplay monitoring mechanic is enabled, the monitor requires power; its draw and detection capability are TBD / gameplay assumptions |

**Loop stressed:** Loop C (SPE → crew activity pause — a dependency chain, not a feedback loop). The shelter forces a pause in crew-labour activities.

**Note (from Part C §7 Loop C clarification):** Life-support equipment (O₂ generation, CO₂ removal, water recycling, crop lighting) continues operating automatically while the crew shelters. Only crew-labour activities (EVAs, manual crop tending, hands-on repairs) pause. This is a gameplay assumption about what the habitat automates.

### 5.3 Player decisions

**Decision 1 — When to shelter.**

- **Option A — Shelter immediately on warning.** Crew safest, but loses productive time if the SPE turns out to be weak or misses the habitat.
- **Option B — Finish a critical task first, then shelter.** Risk: crew exposure rises if the SPE arrives sooner or stronger than expected.
- **Option C — Send only some crew to shelter, keep others on task.** Risk calculation: fewer crew exposed, but those outside take the full exposure.

**Decision 2 — Shelter duration.**

- **Option A — Stay until SPE confirmed over.** Safest, but maximum lost productive time. Crop tending, EVAs, and hands-on repairs all pause (edge 15).
- **Option B — Exit early to resume activities.** Risk: residual radiation exposure; possible health damage.
- **Option C — Rotate crew in and out of shelter.** Spreads exposure across the crew. Gameplay assumption — the dev team must define whether this is allowed and how it affects individual exposure.

**Decision 3 — What to leave running.** Confirm that life-support continues automatically. Decide whether to:

- Keep crop lighting on (crops continue, uses power)
- Pause crop lighting (crops slow, saves power — gameplay assumption about whether this is safe)
- Pause non-essential experiments (saves power)

### 5.4 Resource consequences

> **Calculation (plain English):** Radiation exposure accumulates over time. Remaining outside the shelter increases accumulated exposure at the background + SPE rate; entering the shelter reduces the exposure rate according to the selected gameplay protection factor. The simulation must use a **separately defined gameplay accumulation rate** rather than treating the Chang'e-4 measurement (57.1 μSv/hour derived GCR dose-equivalent) as a human health-damage rate. Use an abstract **"exposure score"** per crew member, not a real-world dose in mSv.

| Player choice | Crew radiation exposure | Productive time | Crops | Power |
|---|---|---|---|---|
| Shelter immediately, stay until clear | Lowest exposure (shelter factor applied — TBD) | Maximum lost time | Stable if lighting kept on | Power change TBD — gameplay assumption (no EVAs / no manual ops may reduce demand slightly, but life-support draw is unchanged) |
| Delay shelter to finish task | Higher exposure proportional to delay | Less lost time | Stable if lighting kept on | Power change TBD — gameplay assumption |
| Exit early | Residual exposure risk | Less lost time | Stable if lighting kept on | Power change TBD — gameplay assumption |
| Rotate crew | Spread exposure across 4 astronauts | Some tasks continue with reduced crew | Stable | Power change TBD — gameplay assumption |

**Key point:** Unlike Scenarios 1 and 2, this scenario does NOT directly deplete O₂, water, or food reserves. The resource at stake is **crew health** (radiation exposure accumulation) and **productive time**. The life-support loop continues running automatically.

**Health damage threshold:** The simulation needs a threshold for when accumulated exposure causes crew health damage. **This MUST be labelled as a gameplay assumption, not a medical limit.** The Chang'e-4 measurement (13.2 ± 1 μGy/hour in silicon, or 57.1 ± 10.6 μSv/hour derived GCR dose-equivalent) is a research reference for the lunar radiation environment — it is NOT a human effective dose and MUST NOT be directly used as a health damage rate (Part A §5 excluded value: 1.369 mSv/day).

### 5.5 Scientific evidence vs gameplay assumptions

| Item | Type | Source / classification |
|---|---|---|
| SPEs exist and can raise radiation levels significantly | Research reference | Research paper §4.1 (NASA radiation protection references) |
| Chang'e-4 GCR dose-equivalent rate 57.1 ± 10.6 μSv/hour | Research reference — derived, not human effective dose | Science Advances 2020 (Part A §3.3) |
| Hydrogen-rich materials (water, polyethylene) useful for SPE shielding | Research reference | Research paper §4.3 (NASA OCHMO-TB-020) |
| SPE warning time | Gameplay assumption | **No universal 15–120 min value supported** (Part A §5 excluded). Dev team picks and labels. |
| Shelter protection factor (% reduction) | Gameplay assumption | TBD — Part A §3.3 |
| SPE intensity and duration | Gameplay assumption | Dev team picks per event |
| Health damage threshold | Gameplay assumption | **NOT a medical limit** — must be labelled clearly. The 1.369 mSv/day figure MUST NOT be used (Part A §5 excluded). |
| Which activities pause vs continue during shelter | Gameplay assumption | Part C §7 Loop C note: life-support continues automatically; only crew-labour pauses |
| Whether crew rotation is allowed | Gameplay assumption | Dev team decides |

### 5.6 v1 implementation notes

- For v1, model radiation as a single accumulating **abstract "exposure score"** per crew member — not a real-world dose in mSv. Background GCR adds exposure continuously at a gameplay-defined rate; an SPE adds exposure faster at a separate gameplay-defined rate; shelter applies a flat reduction factor (gameplay assumption).
- Do NOT convert the Chang'e-4 silicon measurement to a human dose by changing units. Use it as a reference for the lunar environment, then pick a gameplay damage rate and label it as such.
- Define **two separate gameplay rates**: (a) background accumulation rate (slow, continuous) and (b) SPE accumulation rate (fast, event-driven). The shelter protection factor reduces whichever rate is currently active.
- The warning time can be a fixed gameplay value (e.g., "30 minutes") or a random range. Label clearly as a gameplay assumption either way.
- The shelter decision is the core tension — make the trade-off between safety and productivity visible to the player.

---

## 6. Cross-Scenario Design Notes

### 6.1 Scenario stacking

The three scenarios are designed to be independent, but the dev team may stack them for added difficulty:

- **Scenario 1 + Scenario 3** — Solar power decrease during an SPE. Crew must shelter while power is already short. **Whether life-support can continue on battery during shelter depends on the undefined v1 power budget** (demand, capacity, efficiency, generation all TBD). Whether crop lighting is a write-off depends on the Scenario 1 load-shedding decision (§3.3 Decision 1) — if the player already shed crop power, crops are already at risk.
- **Scenario 2 + Scenario 1** — Water recycling failure during lunar night. No solar generation; **whether the battery can cover both life support and repair depends on the undefined power budget** — repair power demand and available battery capacity are both TBD (gameplay assumptions — Part A §3.4). This stacking scenario cannot be fully specified until those values are set.
- **All three** — Maximum stress test. Probably too hard for v1; save for later versions.

### 6.2 Persistent consequences

Each scenario's consequences should persist after the trigger resolves:

| Scenario | Persistent consequence |
|---|---|
| 1 | Lost crop growth cycle (depends on crop selected — 7–14 d microgreens, 28–33 d lettuce, 35–86 d dwarf wheat, 90–97 d soybean; see Part B §6.2); depleted battery reserves; possible EVA crew time lost |
| 2 | Depleted water reserves; possible O₂ reserve depletion; lost crop cycle if crop water was rationed |
| 3 | Accumulated crew radiation exposure (does not reset); lost productive time |

### 6.3 Win and lose conditions (suggested)

| Scenario | Win condition | Lose condition |
|---|---|---|
| 1 | Power restored (repair complete or sunrise) before life-support reserves deplete | Battery fully depletes and life-support stops → cascade |
| 2 | Water recycling repaired and reserves stabilise before electrolysis feed must be throttled | Available daily water for electrolysis falls below ~4.0 kg/day → O₂ generation reduced or stopped → O₂ cascade |
| 3 | SPE passes with crew exposure below the gameplay-defined health threshold | Crew exposure exceeds threshold → health damage (gameplay assumption) |

These win/lose conditions are **gameplay design suggestions**, not scientific thresholds.

---

## 7. Open Questions

| # | Question | Scenario | Owner |
|---|---|---|---|
| 1 | Pick battery capacity and opening charge | 1 | Dev team |
| 2 | Pick solar panel degradation percentage for Trigger A | 1 | Dev team |
| 3 | Pick repair time for EVA (and confirm EVA O₂ rate source) | 1 | Dev team + research |
| 4 | Pick water recovery rate after component failure (BPA failure has a NASA-documented 93–94 % pre-BPA rate that may serve as an engineering inference for the post-failure rate, not a direct NASA statement; other component failures require a modelling decision) | 2 | Dev team |
| 5 | Pick repair time for water recycling component | 2 | Dev team |
| 6 | Pick emergency water reserve size | 2 | Dev team |
| 7 | Pick Sabatier recovery percentage | 2 | Dev team |
| 8 | Pick SPE warning time (gameplay assumption — no universal source) | 3 | Dev team |
| 9 | Pick shelter protection factor | 3 | Dev team |
| 10 | Pick radiation health-damage threshold (gameplay assumption — NOT a medical limit) | 3 | Dev team |
| 11 | Pick SPE intensity and duration range | 3 | Dev team |
| 12 | Decide whether crew rotation in/out of shelter is allowed | 3 | Dev team |
| 13 | Confirm whether the shelter can accommodate all four crew members simultaneously (capacity assumption) | 3 | Dev team |

---

## 8. Change Log

| Version | Date | Author | Notes |
|---|---|---|---|
| v1.3.2 | 2026-11-08 | Neural Knights | Verification pass against the cited NASA sources. (1) Corrected the 93 % water-recovery treatment in Scenario 2: the NASA ISS Water Recovery Milestone article (2023) explicitly documents 93–94 % as the pre-BPA recovery rate. This is a verified NASA historical measurement; however, treating it as the guaranteed post-BPA-failure fallback rate is an engineering inference, not a direct NASA statement — reclassified accordingly in §4.5 and §4.6. (2) Added conditional wording to the Scenario 1 §3.4 consequences table — battery depletion rates and reserve stability are now expressed as conditional on the undefined power and water balances, not as definite outcomes. (3) Removed personal-name attribution from Scenario 1 §3.1 and the v1.2 changelog entry. (4) No new values, calculations, or sources were introduced. |
| v1.3.1 | 2026-11-08 | Neural Knights | Corrected remaining review issues: battery-duration outcomes made conditional; mission-day-14 trigger identified as a phase-aligned gameplay setup; Scenario 2 updated to reference separate crew urine/humidity streams and unresolved store-boundary items; crop-water references updated to Wheeler 2020; SPE monitor detection and warning identified as gameplay assumptions in the scenario body. |
| v1.3 | 2026-11-05 | Neural Knights | Revised per follow-up engineering review: (1) §2 — SPE detection mechanism and advance warning now labelled as gameplay assumptions in the summary table. (2) §3.2 — removed "largest single power draw" claim (unconfirmed; v1 power budget undefined); radiation-monitoring power changed from "minimal" to TBD. (3) §3.3 — Decision 2 "largest draw" claim qualified; Decision 3 battery-duration wording made conditional. (4) §3.4 — cascade risk reworded: systems stop in load-shedding order, not simultaneously. (5) §6.1 — battery-continuity claims made conditional on the undefined power budget. (6) §7 — added open question #13 on shelter capacity for all four crew. (7) Cross-referenced Part C §12 per-stream water balance from §3.4. |
| v1.2 | 2026-11-05 | Neural Knights | Revised per engineering review: (1) Scenario 1 §3.1 — removed the implication that battery can support the lunar night; explicitly states that whether battery sustains life support depends on TBD values (demand, capacity, efficiency, generation) and requires engineering specification; clarified fission is out of scope for v1. (2) Cross-referenced Part C §12 Water Balance Accounting from Scenario 2. (3) Confirmed all unvalidated values remain explicitly marked as gameplay assumptions. (4) Confirmed abstract radiation exposure score remains separate from real dose units (mSv). |
| v1.1 | 2026-11-05 | Neural Knights | Revised after team review: (1) Scenario 2 — separated gross supplied-water demand (20.12 kg/day) from net storage depletion (depends on TBD wastewater return); reworded electrolysis threshold from “water reserves below minimum” to “available daily water for electrolysis below ~4.0 kg/day” (flow rate, not storage threshold); reworded repair recovery to “may stabilise or recover if restored rate is sufficient”; added rationing caveat that savings are gameplay assumptions until water balance is established. (2) Scenario 3 — replaced mSv exposure counter with abstract “exposure score”; marked power “slight reduction” as TBD/gameplay assumption; added separate background and SPE accumulation rates. (3) Scenario 1 — labelled panel-degradation causes as scenario triggers / design assumptions. (4) All scenarios — added plain-English calculation callouts to §3.4, §4.4, §5.4. (5) §5.2 — reworded Loop C as dependency chain not feedback loop. (6) §6.1 — made crop-lighting write-off conditional on Scenario 1 load-shedding decision; marked battery/repair power as gameplay assumptions. (7) §6.2 — clarified crop cycle loss depends on crop selected. (8) §6.3 — fixed electrolysis threshold in win/lose conditions. |
| v1.0 | 2026-11-05 | Neural Knights | Initial emergency scenarios. Three scenarios proposed; each maps to Part C edges and loops; every research value traced to Part A or B; every gameplay assumption labelled. Cross-scenario notes cover stacking, persistent consequences, and win/lose conditions. |
