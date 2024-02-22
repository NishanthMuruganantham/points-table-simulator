import unittest
import pandas as pd
from points_table_simulator.points_table_simulator import PointsTableSimulator


class TestPointsTableSimulator(unittest.TestCase):

    def setUp(self):
        # Create a sample tournament schedule DataFrame
        self.tournament_schedule = pd.DataFrame({
            'match_number': [1, 2, 3],
            'home': ['Team A', 'Team B', 'Team C'],
            'away': ['Team B', 'Team C', 'Team A'],
            'winner': ['Team A', 'Team C', None]  # None indicates no result
        })

        # Initialize PointsTableSimulator object with sample parameters
        self.points_table_simulator = PointsTableSimulator(
            tournament_schedule=self.tournament_schedule,
            points_for_a_win=3,
            points_for_a_no_result=1,
            points_for_a_draw=1
        )

    def test_initialization(self):
        self.assertIsInstance(self.points_table_simulator.tournament_schedule, pd.DataFrame)
        self.assertEqual(self.points_table_simulator.points_for_a_win, 3)
        self.assertEqual(self.points_table_simulator.points_for_a_no_result, 1)
        self.assertEqual(self.points_table_simulator.points_for_a_draw, 1)
        self.assertEqual(self.points_table_simulator.tournament_schedule_away_team_column_name, 'away')
        self.assertEqual(self.points_table_simulator.tournament_schedule_home_team_column_name, 'home')
        self.assertEqual(self.points_table_simulator.tournament_schedule_match_number_column_name, 'match_number')
        self.assertEqual(self.points_table_simulator.tournament_schedule_winning_team_column_name, 'winner')

    def test_input_types(self):
        # Test incorrect input types
        with self.assertRaises(TypeError):
            PointsTableSimulator(
                tournament_schedule='not_a_dataframe',
                points_for_a_win='not_an_integer',
                points_for_a_no_result='not_an_integer',
                points_for_a_draw='not_an_integer',
                tournament_schedule_away_team_column_name=123,
                tournament_schedule_home_team_column_name=123,
                tournament_schedule_match_number_column_name=123,
                tournament_schedule_winning_team_column_name=123
            )

    def test_schedule_dataframe_columns(self):
        # Test missing column names
        with self.assertRaises(ValueError):
            PointsTableSimulator(
                tournament_schedule=pd.DataFrame({
                    'home': ['Team A'],
                    'away': ['Team B'],
                    'winner': ['Team A']
                }),
                points_for_a_win=3
            )

    def test_current_points_table(self):
        simulator = PointsTableSimulator(self.tournament_schedule, 3)
        current_table = simulator.current_points_table
        
        self.assertIsInstance(current_table, pd.DataFrame)
        
        expected_columns = ['team', 'matches_played', 'matches_won', 'matches_lost', 'matches_drawn', 'matches_with_no_result', 'remaining_matches', 'points']
        self.assertListEqual(list(current_table.columns), expected_columns)
        
        self.assertEqual(current_table.loc[current_table['team'] == 'Team A', 'points'].iloc[0], 3)  # TeamA won 1 match
        self.assertEqual(current_table.loc[current_table['team'] == 'Team B', 'points'].iloc[0], 0)  # TeamB drew 1 match
