from unittest import TestCase
from race_result import RaceResult

class TestRaceResult(TestCase):
    def setUp(self):
        self.file = "sample_race.log"
        self.raceResult = RaceResult(self.file)

    def test__extract_log_data(self):
        self.assertEqual(len(self.raceResult._extract_log_data(self.file)), 23)

    def test_results_len(self):
        self.assertEqual(len(self.raceResult.get_results()), 6)

    def test_winner(self):
        self.assertEqual(self.raceResult.get_results()[0][1], '038')

    def test_winner_race_time(self):
        self.assertEqual(self.raceResult.get_results()[0][4], '04:11.578')

    def test_winner_best_lap(self):
        self.assertEqual(self.raceResult.get_results()[0][5], '01:02.769')

    def test_winner_avg_speed(self):
        self.assertEqual(self.raceResult.get_results()[0][6], '44.245')
