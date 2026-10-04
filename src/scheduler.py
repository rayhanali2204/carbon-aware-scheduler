from datetime import datetime, timedelta

from src.models import Job
from src.emissions import calculate_job_emissions

def schedule_baseline(job: Job) -> datetime:
    return job.earliest_start

def schedule_green(
    job: Job,
    carbon_data: dict[datetime, float]
) -> datetime:

    current_start = job.earliest_start
    latest_start = job.deadline - timedelta(hours=job.duration_hours)

    best_start = None
    lowest_emissions = float("inf")

    while current_start <= latest_start:
        carbon_intensities = []

        for hour in range(job.duration_hours):
            timestamp = current_start + timedelta(hours=hour)

            if timestamp not in carbon_data:
                raise ValueError(
                    "Missing carbon-intensity data for "
                    f"{timestamp}"
                )
            
            carbon_intensities.append(carbon_data[timestamp])

        emissions = calculate_job_emissions(
            job.power_kw,
            carbon_intensities
        )

        if emissions < lowest_emissions:
            lowest_emissions = emissions
            best_start = current_start

        current_start += timedelta(hours=1)

    return best_start

