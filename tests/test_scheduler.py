import unittest
from datetime import datetime

from src.models import Job
from src.data_loader import load_carbon_data
from src.scheduler import schedule_baseline, schedule_green


class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.carbon_data = load_carbon_data(
            "data/carbon_intensity.csv"
        )

        self.job = Job(
            duration_hours=2,
            earliest_start=datetime(2026, 1, 1, 9),
            deadline=datetime(2026, 1, 1, 15),
            power_kw=1.0
        )

    def test_baseline_runs_as_soon_as_possible(self):
        start = schedule_baseline(self.job)

        self.assertEqual(
            start,
            datetime(2026, 1, 1, 9)
        )

    def test_green_scheduler_selects_lowest_carbon_window(self):
        start = schedule_green(
            self.job,
            self.carbon_data
        )

        self.assertEqual(
            start,
            datetime(2026, 1, 1, 13)
        )