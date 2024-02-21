import pandas as pd


class PointsTableSimulator:

    def __init__(
        self,
        tournament_schedule: pd.DataFrame,
        points_for_a_win: int,
        points_for_a_no_result: int = 1,
        points_for_a_draw: int = 1,
        tournament_schedule_away_team_column_name: str = "away",
        tournament_schedule_home_team_column_name: str = "home",
        tournament_schedule_match_number_column_name: str = "match_number",
        tournament_schedule_winning_team_column_name: str = "winner",
    ) -> None:
        """
        Initializes PointsTableSimulator object with provided parameters.

        Args:
            tournament_schedule (pd.DataFrame): DataFrame containing the schedule of the tournament matches.
            points_for_a_win (int): Points awarded for a win.
            points_for_no_result (int, optional): Points awarded for a match with no result. Default is 1.
            points_for_a_draw (int, optional): Points awarded for a draw. Default is 1.
            tournament_schedule_away_team_column_name (str, optional): Name of the column in the schedule DataFrame
                containing the away team names. Default is "away".
            tournament_schedule_home_team_column_name (str, optional): Name of the column in the schedule DataFrame
                containing the home team names. Default is "home".
            tournament_schedule_match_number_column_name (str, optional): Name of the column in the schedule DataFrame
                containing the match numbers. Default is "match_number".
            tournament_schedule_winning_team_column_name (str, optional): Name of the column in the schedule DataFrame
                containing the winning team names. Default is "winner".
        """
        self.tournament_schedule: pd.DataFrame = tournament_schedule
        self.points_for_a_draw: int = points_for_a_draw
        self.points_for_a_no_result: int = points_for_a_no_result
        self.points_for_a_win: int = points_for_a_win
        self.tournament_schedule_away_team_column_name: str = tournament_schedule_away_team_column_name
        self.tournament_schedule_home_team_column_name: str = tournament_schedule_home_team_column_name
        self.tournament_schedule_match_number_column_name: str = tournament_schedule_match_number_column_name
        self.tournament_schedule_winning_team_column_name: str = tournament_schedule_winning_team_column_name
