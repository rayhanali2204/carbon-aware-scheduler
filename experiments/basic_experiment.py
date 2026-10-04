from datetime import datetime, timedelta

from src.models import Job
from src.data_loader import load_carbon_data
from src.scheduler import schedule_baseline, schedule_green
from src.emissions import calculate_job_emissions

carbon_data = load_carbon_data("data/carbon_intensity.csv")

job = Job(
    duration_hours=2,
    earliest_start=datetime(2026,1,1,9,0),
    deadline=datetime(2026,1,1,15,0),
    power_kw=1.0
)

baseline_start = schedule_baseline(job)
green_start = schedule_green(job, carbon_data)

baseline_intensities = []
green_intensities = []

for hour in range(job.duration_hours):
    baseline_time = baseline_start + timedelta(hours=hour)
    green_time = green_start + timedelta(hours=hour)

    baseline_intensities.append(carbon_data[baseline_time])
    green_intensities.append(carbon_data[green_time])

baseline_emissions = calculate_job_emissions(job.power_kw, baseline_intensities)
green_emissions = calculate_job_emissions(job.power_kw, green_intensities)

carbon_saved = baseline_emissions - green_emissions

savings_percent = (
    carbon_saved / baseline_emissions * 100
)

print("Carbon-Aware Scheduling Simulation")
print()

print("Job")
print(f"Duration: {job.duration_hours} hours")
print(f"Power: {job.power_kw} kW")
print(f"Earliest start: {job.earliest_start}")
print(f"Deadline: {job.deadline}")
print()

print("Baseline")
print(f"Start: {baseline_start}")
print(f"Emissions: {baseline_emissions:.1f} gCO2e")
print()

print("Carbon-aware")
print(f"Start: {green_start}")
print(f"Emissions: {green_emissions:.1f} gCO2e")
print()

print(f"Carbon saved: {carbon_saved:.1f} gCO2e")
print(f"Carbon savings: {savings_percent:.1f}%")

    

