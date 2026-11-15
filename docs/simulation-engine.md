# Simulation Design & TypeScript Engine Specification

**Source:** Notion — [Simulation Design & TypeScript Engine Specification v0.2](https://app.notion.com/p/4109fd4012aa8112960ce4e2027cf210)  
**Notion status:** Needs Review · Last reviewed 11 November 2026  
**Specification version:** v0.2

> This is a working engineering specification, not an approved scientific or operational model. Water allocation, numeric parameters and cross-layer contracts remain open review gates.

## Runtime boundaries

- Python prepares and validates data and exports versioned JSON configuration and test fixtures.
- TypeScript owns live calculations, commands, mission state and outcomes.
- React collects player decisions and renders returned state.
- Unity WebGL visualizes authoritative state through the React–Unity bridge.
- The mission should run with mock configuration before external event data is available.

## Resource model

The engine's documented resource inventory uses:
- `oxygenKg`
- `carbonDioxideKg`
- `waterKg`
- `foodKcal`
- `energyWh`

The engine documentation describes resource accounting in terms of opening inventory, production, recovery, consumption, removal, loss, closing inventory and deficits. Capacity and requirement flows are not direct inventory changes.

## Mission-cycle model

The design describes seven simulated operational-day cycles. These are gameplay cycles, not a claim that each cycle represents a real lunar day/night period. Deterministic behavior is an intended property of the simulation.

## Validation principles

- Required configuration values must be present and structurally valid.
- A parameter marked TBD or pending review must not be treated as an approved scientific input.
- A mock value passing structural validation is still a mock value.
- Do not invent water-store boundaries, power budgets, battery survival, radiation thresholds or other unresolved parameters.

## Known review gates

The Notion specification explicitly leaves water allocation, numeric parameters and cross-layer contracts open. Review the linked parameter and dependency documents before using values in a quantitative scenario.

## Related records

- [Architecture & API Contract — Draft](https://app.notion.com/p/4109fd4012aa81b4878ee5242a1dd9e1)
- [Simulation Parameter Sheet — Needs Review](https://app.notion.com/p/4109fd4012aa819ba783f63edf6d2ba0)
- [Resource Dependency Matrix — Needs Review](https://app.notion.com/p/4109fd4012aa8185a224e2ae18faa595)
