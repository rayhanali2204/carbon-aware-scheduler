import csv
from datetime import datetime, timedelta

from src.models import Job
from src.data_loader import load_carbon_scenario
from src.scheduler import schedule_baseline, schedule_green
from src.emissions import calculate_job_emissions


scenarios = ["low", "medium", "high"]
flexibility_levels = [0, 1, 3, 6]

earliest_start = datetime(2026, 1, 1, 9)
duration_hours = 2
power_kw = 1.0

results = []


for scenario in scenarios:
    carbon_data = load_carbon_scenario(
        "data/carbon_scenarios.csv",
        scenario
    )

    for flexibility in flexibility_levels:
        deadline = earliest_start + timedelta(
            hours=duration_hours + flexibility
        )

        job = Job(
            duration_hours=duration_hours,
            earliest_start=earliest_start,
            deadline=deadline,
            power_kw=power_kw
        )

        baseline_start = schedule_baseline(job)
        green_start = schedule_green(job, carbon_data)

        baseline_intensities = []
        green_intensities = []

        for hour in range(duration_hours):
            baseline_time = baseline_start + timedelta(hours=hour)
            green_time = green_start + timedelta(hours=hour)

            baseline_intensities.append(
                carbon_data[baseline_time]
            )

            green_intensities.append(
                carbon_data[green_time]
            )

        baseline_emissions = calculate_job_emissions(
            power_kw,
            baseline_intensities
        )

        green_emissions = calculate_job_emissions(
            power_kw,
            green_intensities
        )

        carbon_saved = baseline_emissions - green_emissions

        savings_percent = (
            carbon_saved / baseline_emissions
        ) * 100

        results.append({
            "scenario": scenario,
            "flexibility_hours": flexibility,
            "baseline_start": baseline_start,
            "green_start": green_start,
            "baseline_emissions_gco2e": baseline_emissions,
            "green_emissions_gco2e": green_emissions,
            "carbon_saved_gco2e": carbon_saved,
            "savings_percent": savings_percent
        })

        print(
            f"{scenario.capitalize()} | "
            f"Flexibility: {flexibility}h | "
            f"Green start: {green_start.strftime('%H:%M')} | "
            f"Savings: {savings_percent:.1f}%"
        )


output_file = "results/scenario_results.csv"

with open(output_file, "w", newline="") as file:
    fieldnames = [
        "scenario",
        "flexibility_hours",
        "baseline_start",
        "green_start",
        "baseline_emissions_gco2e",
        "green_emissions_gco2e",
        "carbon_saved_gco2e",
        "savings_percent"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)


print(f"\nResults saved to {output_file}")