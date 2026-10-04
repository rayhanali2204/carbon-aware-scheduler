import unittest
from datetime import datetime

from src.models import Job

class TestJob(unittest.TestCase):
    def test_valid_job(self):
        job = Job(duration_hours=2, 
                earliest_start=datetime(2026,1,1,9),
                deadline=datetime(2026,1,1,15),
                power_kw=1.0)

        self.assertEqual(job.duration_hours, 2)
        self.assertEqual(job.power_kw, 1.0)

    def test_job_cannot_exceed_scheduling_window(self):
        with self.assertRaises(ValueError):
            job = Job(duration_hours=5, 
                    earliest_start=datetime(2026,1,1,9),
                    deadline=datetime(2026,1,1,12),
                    power_kw=1.0)

    def test_duration_must_be_positive(self):
        with self.assertRaises(ValueError):
            Job(duration_hours=0, 
                earliest_start=datetime(2026,1,1,9),
                deadline=datetime(2026,1,1,15),
                power_kw=1.0)

    def test_power_must_be_positive(self):
        with self.assertRaises(ValueError):
            Job(duration_hours=2, 
                earliest_start=datetime(2026,1,1,9),
                deadline=datetime(2026,1,1,15),
                power_kw=0.0)
