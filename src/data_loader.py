import csv
from datetime import datetime


def load_carbon_data(file_path: str) -> dict[datetime, float]:
    carbon_data = {}

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            timestamp = datetime.strptime(
                row["timestamp"],
                "%Y-%m-%d %H:%M"
            )

            carbon_intensity = float(row["carbon_intensity"])

            carbon_data[timestamp] = carbon_intensity

    return carbon_data
           