from dataclasses import dataclass
from datetime import datetime

@dataclass
class Job:
    duration_hours: int
    earliest_start: datetime
    deadline: datetime
    power_kw: float

    def __post_init__(self):
        if self.duration_hours <= 0:
            raise ValueError("Job duration must be greater than 0.")

        if self.power_kw <= 0:
            raise ValueError("Job power consumption must be greater than 0.")

        if self.deadline <= self.earliest_start:
            raise ValueError("Deadline must be after earliest start")

        available_hours = (self.deadline - self.earliest_start).total_seconds() / 3600

        if self.duration_hours > available_hours:
            raise ValueError(
                "Job duration does not fit within the scheduling window"
            )