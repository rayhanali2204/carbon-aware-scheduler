import unittest

from src.emissions import calculate_job_emissions

class TestEmissions(unittest.TestCase):
    def test_baseline_emissions(self):
        emissions = calculate_job_emissions(
            1.0,
            [220, 250]
        )

        self.assertEqual(emissions, 470.0)

    def test_green_emissions(self):
        emissions = calculate_job_emissions(
            1.0,
            [100, 130]
        )

        self.assertEqual(emissions, 230.0)