import statistics

from src.data_loader import load_carbon_scenario

scenarios = ["low", "medium", "high"]

for scenario in scenarios:
    carbon_data = load_carbon_scenario(
        "data/carbon_scenarios.csv",
        scenario
    )

    intensities = list(carbon_data.values())

    mean = statistics.mean(intensities)
    standard_deviation = statistics.pstdev(intensities)

    print(f"{scenario.capitalize()} variability")
    print(f"Mean: {mean:.1f} gCO2e/kWh")
    print(
        f"Standard deviation: "
        f"{standard_deviation:.1f} gCO2e/kWh"
    )
    print("-" * 40)
