"""Scientific Reference Model for Lunar Surface Radiation & SPE Shelter Calculations.

Corresponds to 'Python Reference Models' and 'Expected Calculations' in Diagram 1 & 2.
Calculates ground-truth reference values for astronaut exposure during solar storms.
"""

from typing import Any, Dict, List


# Research baseline from Science Advances 2020 (Chang'e-4 lunar surface measurement)
BACKGROUND_GCR_DOSE_EQUIVALENT_RATE_USV_HR = 57.1  # µSv/hr (~1.37 mSv/day)


def calculate_spe_dose_rate_usv_hr(flux_pfu: float, noaa_scale: str) -> float:
    """Calculate effective lunar surface SPE dose-equivalent rate (µSv/hr) from proton flux."""
    # Scale conversion based on standard NASA / NOAA proton event dose models
    scale_multipliers = {
        "S1": 150.0,    # ~0.15 mSv/hr
        "S2": 600.0,    # ~0.60 mSv/hr
        "S3": 2500.0,   # ~2.50 mSv/hr
        "S4": 10000.0,  # ~10.0 mSv/hr
        "S5": 50000.0   # ~50.0 mSv/hr
    }
    return scale_multipliers.get(noaa_scale, flux_pfu * 1.5)


def simulate_reference_radiation_profile(
    scenario: Dict[str, Any],
    decision: str = "shelter_immediate",
    delay_minutes: float = 0.0,
    background_rate_usv_hr: float = BACKGROUND_GCR_DOSE_EQUIVALENT_RATE_USV_HR
) -> Dict[str, Any]:
    """Calculate expected hourly radiation exposure profile for validation testing."""
    duration_hrs = float(scenario.get("duration_hours", 24.0))
    flux_pfu = float(scenario.get("peak_flux_pfu", 100.0))
    noaa_scale = scenario.get("noaa_scale", "S2")
    shelter_factor = float(scenario.get("shelter_protection_factor", 0.90))

    spe_peak_rate = calculate_spe_dose_rate_usv_hr(flux_pfu, noaa_scale)

    hourly_timeline = []
    cumulative_dose_usv = 0.0

    total_steps = int(duration_hrs)
    for step in range(total_steps):
        time_elapsed_minutes = step * 60.0

        # Determine whether crew is inside shelter
        if decision == "shelter_immediate":
            in_shelter = True
        elif decision == "no_shelter":
            in_shelter = False
        elif decision == "shelter_delayed":
            in_shelter = (time_elapsed_minutes >= delay_minutes)
        else:
            in_shelter = True

        # Compute effective dose rate for this hour
        # Triangular storm profile approximation (rising to peak at midpoint, decaying)
        progress = (step + 0.5) / total_steps
        if progress <= 0.5:
            storm_intensity = 2.0 * progress
        else:
            storm_intensity = 2.0 * (1.0 - progress)

        instant_spe_rate = spe_peak_rate * storm_intensity

        if in_shelter:
            effective_spe = instant_spe_rate * (1.0 - shelter_factor)
            effective_gcr = background_rate_usv_hr * (1.0 - (shelter_factor * 0.5))  # partial GCR shielding
        else:
            effective_spe = instant_spe_rate
            effective_gcr = background_rate_usv_hr

        total_rate = effective_gcr + effective_spe
        cumulative_dose_usv += total_rate

        hourly_timeline.append({
            "hour": step + 1,
            "in_shelter": in_shelter,
            "effective_dose_rate_usv_hr": round(total_rate, 2),
            "cumulative_dose_usv": round(cumulative_dose_usv, 2)
        })

    return {
        "scenario_id": scenario.get("scenario_id"),
        "decision": decision,
        "delay_minutes": delay_minutes,
        "duration_hours": duration_hrs,
        "total_cumulative_dose_usv": round(cumulative_dose_usv, 2),
        "total_cumulative_dose_msv": round(cumulative_dose_usv / 1000.0, 3),
        "hourly_timeline": hourly_timeline
    }


if __name__ == "__main__":
    sample_scenario = {
        "scenario_id": "test_spe_001",
        "noaa_scale": "S3",
        "peak_flux_pfu": 1000.0,
        "duration_hours": 24.0,
        "shelter_protection_factor": 0.90
    }

    res_shelter = simulate_reference_radiation_profile(sample_scenario, decision="shelter_immediate")
    res_delayed = simulate_reference_radiation_profile(sample_scenario, decision="shelter_delayed", delay_minutes=60.0)
    res_none = simulate_reference_radiation_profile(sample_scenario, decision="no_shelter")

    print(f"Immediate Shelter Dose: {res_shelter['total_cumulative_dose_msv']} mSv")
    print(f"Delayed (60m) Shelter Dose: {res_delayed['total_cumulative_dose_msv']} mSv")
    print(f"No Shelter Dose: {res_none['total_cumulative_dose_msv']} mSv")

