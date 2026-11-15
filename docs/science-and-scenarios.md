# Science, Parameters & Emergency Scenarios

This page summarizes the review constraints recorded in the team's Notion science documents. It is not a replacement for the source research papers or a scientific approval.

## Scientific Research — Lunar Environment & Survival Systems

**Source:** [Notion research record](https://app.notion.com/p/4109fd4012aa819daf82f8f8306ef451)  
**Status:** Needs Review · Last reviewed 6 November 2026

The research report covers oxygen and air quality, water consumption and recycling, lunar radiation hazards and protection, and lunar power generation/storage.

Review cautions:
- Keep oxygen supply distinct from CO₂ removal.
- The 98% ISS water-recovery milestone is system-level; it is not a universal recovery rate for every stream or a guaranteed lunar-habitat rate.
- Chang'e-4 silicon absorbed dose is not a human effective dose.
- NASA's 40 kW fission figure is a development target, not an operational lunar installation.
- Water-recovery arithmetic must remain explicitly illustrative, not a prediction of lunar make-up water.

## Simulation Parameter Sheet v1.2

**Source:** [Notion parameter sheet](https://app.notion.com/p/4109fd4012aa819ba783f63edf6d2ba0)  
**Status:** Needs Review · Last reviewed 6 November 2026

The source records research references, derived calculations, engineering inferences, modelling decisions and gameplay assumptions separately. It keeps several parameters unresolved, including EVA oxygen rate, human lunar effective dose, SPE warning time, shielding requirement, solar output, battery capacity, habitat demand and opening reserves.

The documented mock crew-demand values (oxygen 0.9 kg/person/day, water 5.0 kg/person/day, food 3000 kcal/person/day and CO₂ 1.1 kg/person/day) are explicitly mock gameplay assumptions, not validated science or a complete resource model. Do not infer opening reserves, battery duration, solar generation, habitat loads or safety thresholds from them.

## Resource Dependency Matrix v1.1

**Source:** [Notion dependency matrix](https://app.notion.com/p/4109fd4012aa8185a224e2ae18faa595)  
**Status:** Needs Review; Notion contains the older v1.1 copy, not the reported v1.3.1 revised source.

Do not implement a quantitative water or power dependency graph from this older copy. The revised matrix file was not available for synchronization. Open questions include potable/usable store boundaries, crew urine and humidity streams, wastewater processing, electrolysis feed, Sabatier output, crop gross water throughput versus net store debit, losses, power generation/storage/load assumptions and conditional battery outcomes.

## Emergency Scenarios v1.1 / revision history

**Source:** [Notion emergency scenarios](https://app.notion.com/p/4109fd4012aa81fda2ade6a2804d0e0a)  
**Status:** Needs Review.

Three proposed scenarios:
1. Reduced solar generation.
2. Water-recycling malfunction.
3. Solar-particle-event shelter decision.

These are proposals, not fully parameterized approved simulation rules. Solar degradation percentages, event triggers and SPE detection/advance warning are gameplay assumptions. Power and water outcomes remain conditional on unresolved models. The TypeScript engine's generic scenario registry and oxygen-generator workflow do not prove that these three science scenarios are implemented.

## Evidence labels

Use these labels consistently:
- **Research data:** directly supported by a cited source.
- **Engineering inference:** reasoned interpretation/calculation, with method and caveats.
- **Gameplay assumption:** chosen for playability; never present as a measured lunar fact.
- **TBD / pending review:** unresolved; block dependent scenarios rather than inventing defaults.

## Review policy

Keep the original Notion statuses unchanged. This repository mirror is informative and does not convert any Draft or Needs Review record into an Approved specification.
