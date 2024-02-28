from unittest import TestCase
from unittest.mock import MagicMock
import pandas as pd
from points_table_simulator.exceptions import TournamentCompletionBelowCutoffError
from points_table_simulator.points_table_simulator import PointsTableSimulator


class ErrorTests(TestCase):

    def test_simulate_the_qualification_scenarios_function_with_completed_matches_below_cutoff_THEN_raise_TournamentCompletionBelowCutoffError(self):
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", None, None, None, None]  # Four matches remaining
        })
        simulator = PointsTableSimulator(tournament_schedule, points_for_a_win=3)

        with self.assertRaises(TournamentCompletionBelowCutoffError):
            simulator.simulate_the_qualification_scenarios("Team A", top_x_position_in_the_table=2)
