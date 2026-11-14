"""Scientific Reference Model for Lunar Life-Support Mass Balance (Crew of 4).

Based on NASA 2019 Mass Balance Study (Ewert & Stromgren, NTRS 20190027563) and
NASA Life Support Baseline Values and Assumptions Document (BVAD).
"""

from typing import Any, Dict, List


# Daily reference rates per person (NASA Ewert 2019)
O2_CONSUMPTION_KG_PERSON_DAY = 0.89
CO2_PRODUCTION_KG_PERSON_DAY = 1.08
WATER_REQUIREMENT_KG_PERSON_DAY = 5.03
URINE_WATER_KG_PERSON_DAY = 1.40
HUMIDITY_WATER_KG_PERSON_DAY = 3.04
PACKAGED_FOOD_KG_PERSON_DAY = 2.39

# Stoichiometric electrolysis conversion: 2 H2O -> 2 H2 + O2 (36.03 / 31.998 = ~1.126 kg water per kg O2)
WATER_PER_KG_O2_STOICHIOMETRIC = 36.03 / 31.998  # ~1.126


def calculate_daily_crew_mass_balance(crew_size: int = 4) -> Dict[str, float]:
    """Calculate daily consumable demands and production rates for the crew."""
    o2_daily = O2_CONSUMPTION_KG_PERSON_DAY * crew_size
    co2_daily = CO2_PRODUCTION_KG_PERSON_DAY * crew_size
    water_req_daily = WATER_REQUIREMENT_KG_PERSON_DAY * crew_size
    urine_daily = URINE_WATER_KG_PERSON_DAY * crew_size
    humidity_daily = HUMIDITY_WATER_KG_PERSON_DAY * crew_size
    food_daily = PACKAGED_FOOD_KG_PERSON_DAY * crew_size
    electrolysis_feed_min = round(o2_daily * WATER_PER_KG_O2_STOICHIOMETRIC, 2)

    return {
        "crew_size": crew_size,
        "daily_o2_demand_kg": round(o2_daily, 2),
        "daily_co2_production_kg": round(co2_daily, 2),
        "daily_water_requirement_kg": round(water_req_daily, 2),
        "daily_urine_water_reference_kg": round(urine_daily, 2),
        "daily_humidity_water_reference_kg": round(humidity_daily, 2),
        "daily_packaged_food_kg": round(food_daily, 2),
        "daily_electrolysis_feed_min_kg": electrolysis_feed_min,
        "mission_30d_o2_demand_kg": round(o2_daily * 30.0, 1),
        "mission_30d_co2_production_kg": round(co2_daily * 30.0, 1),
        "mission_30d_packaged_food_kg": round(food_daily * 30.0, 1),
    }


def simulate_life_support_emergency_cascade(
    scenario_type: str,
    crew_size: int = 4,
    mission_days: int = 30,
    water_recycler_efficiency: float = 0.98,
    co2_scrubber_powered: bool = True,
    electrolysis_powered: bool = True
) -> Dict[str, Any]:
    """Simulate resource balance and failure cascades under emergency conditions."""
    base = calculate_daily_crew_mass_balance(crew_size)
    o2_daily = base["daily_o2_demand_kg"]
    co2_daily = base["daily_co2_production_kg"]
    electrolysis_feed = base["daily_electrolysis_feed_min_kg"]

    # Initial stocks for 30-day baseline simulation (reference reserves)
    stored_o2_kg = 50.0
    stored_water_kg = 200.0
    accumulated_co2_cabin_kg = 0.0

    timeline = []
    cascade_triggered = None

    for day in range(1, mission_days + 1):
        # 1. CO2 Scrubbing
        if co2_scrubber_powered:
            net_co2_change = 0.0  # scrubbed
        else:
            net_co2_change = co2_daily
            accumulated_co2_cabin_kg += co2_daily
            if accumulated_co2_cabin_kg > 10.0 and not cascade_triggered:
                cascade_triggered = "air_quality_emergency_high_co2"

        # 2. Oxygen Generation vs Reserve Debit
        if electrolysis_powered and stored_water_kg >= electrolysis_feed:
            stored_water_kg -= electrolysis_feed
            o2_generated = o2_daily
            o2_reserve_debit = 0.0
        else:
            o2_generated = 0.0
            o2_reserve_debit = o2_daily
            stored_o2_kg = max(0.0, stored_o2_kg - o2_reserve_debit)
            if stored_o2_kg <= 10.0 and not cascade_triggered:
                cascade_triggered = "critical_o2_depletion"

        # 3. Water Recycling balance
        # Recoverable stream = urine + humidity (17.76 kg for 4 crew)
        recoverable_stream = base["daily_urine_water_reference_kg"] + base["daily_humidity_water_reference_kg"]
        recovered_water = recoverable_stream * water_recycler_efficiency
        net_water_loss = recoverable_stream * (1.0 - water_recycler_efficiency)
        stored_water_kg = max(0.0, stored_water_kg - net_water_loss)

        if stored_water_kg < electrolysis_feed and electrolysis_powered:
            electrolysis_powered = False
            if not cascade_triggered:
                cascade_triggered = "water_shortage_halts_electrolysis"

        timeline.append({
            "day": day,
            "stored_o2_kg": round(stored_o2_kg, 2),
            "stored_water_kg": round(stored_water_kg, 2),
            "accumulated_co2_cabin_kg": round(accumulated_co2_cabin_kg, 2),
            "electrolysis_active": electrolysis_powered,
            "co2_scrubber_active": co2_scrubber_powered,
            "cascade_status": cascade_triggered or "nominal"
        })

    return {
        "scenario_type": scenario_type,
        "crew_size": crew_size,
        "final_stored_o2_kg": round(stored_o2_kg, 2),
        "final_stored_water_kg": round(stored_water_kg, 2),
        "final_cabin_co2_kg": round(accumulated_co2_cabin_kg, 2),
        "cascade_triggered": cascade_triggered,
        "timeline": timeline
    }


if __name__ == "__main__":
    balance = calculate_daily_crew_mass_balance(4)
    print("Crew of 4 Nominal Mass Balance:")
    for k, v in balance.items():
        print(f"  {k}: {v}")

    # Test Scenario 2 cascade: failed recycler (drop from 98% to 93% pre-BPA rate)
    res_water_fail = simulate_life_support_emergency_cascade("water_recycler_failure", water_recycler_efficiency=0.93)
    print("\nScenario 2 (Water Recycler Degradation to 93%) Outcome:")
    print("  Final Water Stored:", res_water_fail["final_stored_water_kg"], "kg")
    print("  Cascade Triggered:", res_water_fail["cascade_triggered"])

    # Test Scenario 1 cascade: complete power drop halts scrubbers and electrolysis
    res_power_fail = simulate_life_support_emergency_cascade("power_failure", co2_scrubber_powered=False, electrolysis_powered=False)
    print("\nScenario 1 (Unpowered Life Support) Outcome:")
    print("  Final Cabin CO2:", res_power_fail["final_cabin_co2_kg"], "kg")
    print("  Cascade Triggered:", res_power_fail["cascade_triggered"])

