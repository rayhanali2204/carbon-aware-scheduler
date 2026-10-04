def calculate_hourly_emissions(power_kw: float, carbon_intensity: float) -> float:
    energy_kwh = power_kw * 1
    emissions_gco2e = energy_kwh * carbon_intensity

    return emissions_gco2e

def calculate_job_emissions(
    power_kw: float,
    carbon_intensities: list[float]
) -> float:
    total_emissions = 0.0

    for carbon_intensity in carbon_intensities:
        total_emissions += calculate_hourly_emissions(
            power_kw,
            carbon_intensity
        )

    return total_emissions