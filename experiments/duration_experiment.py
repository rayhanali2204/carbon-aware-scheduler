import csv
from datetime import datetime, timedelta

from src.models import Job
from src.data_loader import load_carbon_data
from src.scheduler import schedule_baseline, schedule_green
from src.emissions import calculate_job_emissions


carbon_data = load_carbon_data(
    "data/duration_carbon_intensity.csv"
)

earliest_start = datetime(2026, 1, 1, 9)
power_kw = 1.0
flexibility_hours = 6

duration_levels = [1, 2, 4]

results = []


for duration in duration_levels:
    deadline = earliest_start + timedelta(
        hours=duration + flexibility_hours
    )

    job = Job(
        duration_hours=duration,
        earliest_start=earliest_start,
        deadline=deadline,
        power_kw=power_kw
    )

    baseline_start = schedule_baseline(job)
    green_start = schedule_green(job, carbon_data)

    baseline_intensities = []
    green_intensities = []

    for hour in range(duration):
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
        "duration_hours": duration,
        "flexibility_hours": flexibility_hours,
        "baseline_start": baseline_start,
        "green_start": green_start,
        "baseline_emissions_gco2e": baseline_emissions,
        "green_emissions_gco2e": green_emissions,
        "carbon_saved_gco2e": carbon_saved,
        "savings_percent": savings_percent
    })

    print(
        f"Duration: {duration}h | "
        f"Green start: {green_start.strftime('%H:%M')} | "
        f"Baseline: {baseline_emissions:.1f} gCO2e | "
        f"Green: {green_emissions:.1f} gCO2e | "
        f"Savings: {savings_percent:.1f}%"
    )

output_file = "results/duration_results.csv"

with open(output_file, "w", newline="") as file:
    fieldnames = [
        "duration_hours",
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