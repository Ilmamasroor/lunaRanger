"""Scientific Reference Model for Crop Growth, Water Demand & Failure Cascades.

Corresponds to 'Python Reference Models' and 'Expected Calculations' in Diagram 1 & 2.
Models crop maturity progression and resource dependencies under normal & emergency conditions.
"""

from typing import Any, Dict, List


def simulate_crop_lifecycle(
    crop_params: Dict[str, Any],
    allocated_area_m2: float = 10.0,
    mission_days: int = 30,
    water_ration_factor: float = 1.0,
    lighting_failure_day: int = -1,
    lighting_outage_duration_days: int = 0
) -> Dict[str, Any]:
    """Calculate daily growth progression, water demand, and failure cascade outcomes."""
    first_harvest_days = int(crop_params.get("first_harvest_days", 30))
    water_rate = float(crop_params.get("water_use_rate_l_m2_d", 2.0))
    crop_id = crop_params.get("crop_id", "crop")

    daily_water_demand_kg = water_rate * allocated_area_m2
    # Effective water provided based on rationing
    actual_daily_water_kg = daily_water_demand_kg * water_ration_factor

    daily_timeline = []
    cumulative_growth_fraction = 0.0
    crop_status = "growing"
    consecutive_outage_days = 0
    total_yield_harvests = 0

    for day in range(1, mission_days + 1):
        # Check lighting availability
        lighting_active = True
        if lighting_failure_day > 0:
            if lighting_failure_day <= day < (lighting_failure_day + lighting_outage_duration_days):
                lighting_active = False

        if not lighting_active:
            consecutive_outage_days += 1
        else:
            consecutive_outage_days = 0

        # Assess biological failure conditions
        if consecutive_outage_days >= 3:
            crop_status = "failed_lighting_loss"
        elif water_ration_factor < 0.5:
            crop_status = "failed_water_stress"

        # Growth calculation
        daily_growth_increment = 0.0
        if crop_status == "growing":
            if lighting_active and water_ration_factor >= 0.8:
                daily_growth_increment = 1.0 / first_harvest_days
                cumulative_growth_fraction += daily_growth_increment
            elif lighting_active and 0.5 <= water_ration_factor < 0.8:
                # Reduced water slows growth by 50%
                daily_growth_increment = (1.0 / first_harvest_days) * 0.5
                cumulative_growth_fraction += daily_growth_increment

            if cumulative_growth_fraction >= 1.0:
                crop_status = "ready_for_harvest"
                total_yield_harvests += 1
                cumulative_growth_fraction = 1.0

        daily_timeline.append({
            "day": day,
            "lighting_active": lighting_active,
            "water_supplied_kg": round(actual_daily_water_kg, 2),
            "growth_progress_pct": round(cumulative_growth_fraction * 100.0, 1),
            "status": crop_status
        })

    return {
        "crop_id": crop_id,
        "allocated_area_m2": allocated_area_m2,
        "nominal_daily_water_kg": round(daily_water_demand_kg, 2),
        "total_water_consumed_kg": round(actual_daily_water_kg * mission_days, 2),
        "final_status": crop_status,
        "harvests_achieved": total_yield_harvests,
        "daily_timeline": daily_timeline
    }


if __name__ == "__main__":
    sample_lettuce = {
        "crop_id": "lettuce_veg03a",
        "first_harvest_days": 33,
        "water_use_rate_l_m2_d": 2.0
    }

    # Nominal run
    nom = simulate_crop_lifecycle(sample_lettuce, allocated_area_m2=10.0, mission_days=30)
    print(f"Nominal 30d Lettuce Progress: {nom['daily_timeline'][-1]['growth_progress_pct']}% (Status: {nom['final_status']})")

    # Water stress run (Scenario 2 cascade)
    stress = simulate_crop_lifecycle(sample_lettuce, allocated_area_m2=10.0, mission_days=30, water_ration_factor=0.4)
    print(f"Rationed Water Status: {stress['final_status']}")

    # Power outage run (Scenario 1 cascade: 4-day outage)
    outage = simulate_crop_lifecycle(sample_lettuce, allocated_area_m2=10.0, mission_days=30, lighting_failure_day=10, lighting_outage_duration_days=4)
    print(f"Power Outage Status: {outage['final_status']}")

