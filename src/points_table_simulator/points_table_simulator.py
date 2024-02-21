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
        self._validate_input_types(
            tournament_schedule,
            points_for_a_win,
            points_for_a_no_result,
            points_for_a_draw,
            tournament_schedule_away_team_column_name,
            tournament_schedule_home_team_column_name,
            tournament_schedule_match_number_column_name,
            tournament_schedule_winning_team_column_name
        )
        self.tournament_schedule: pd.DataFrame = tournament_schedule
        self.points_for_a_draw: int = points_for_a_draw
        self.points_for_a_no_result: int = points_for_a_no_result
        self.points_for_a_win: int = points_for_a_win
        self.tournament_schedule_away_team_column_name: str = tournament_schedule_away_team_column_name
        self.tournament_schedule_home_team_column_name: str = tournament_schedule_home_team_column_name
        self.tournament_schedule_match_number_column_name: str = tournament_schedule_match_number_column_name
        self.tournament_schedule_winning_team_column_name: str = tournament_schedule_winning_team_column_name
        self._validate_schedule_dataframe_columns()

    @staticmethod
    def _validate_input_types(
        tournament_schedule: pd.DataFrame,
        points_for_a_win: int,
        points_for_a_no_result: int,
        points_for_a_draw: int,
        tournament_schedule_away_team_column_name: str,
        tournament_schedule_home_team_column_name: str,
        tournament_schedule_match_number_column_name: str,
        tournament_schedule_winning_team_column_name: str
    ):
        """
        Validates the types of input arguments.

        Args:
            tournament_schedule (pd.DataFrame): DataFrame containing the schedule of the tournament matches.
            points_for_a_win (int): Points awarded for a win.
            points_for_no_result (int): Points awarded for a match with no result.
            points_for_a_draw (int): Points awarded for a draw.
            tournament_schedule_away_team_column_name (str): Name of the column in the schedule DataFrame
                containing the away team names.
            tournament_schedule_home_team_column_name (str): Name of the column in the schedule DataFrame
                containing the home team names.
            tournament_schedule_match_number_column_name (str): Name of the column in the schedule DataFrame
                containing the match numbers.
            tournament_schedule_winning_team_column_name (str): Name of the column in the schedule DataFrame
                containing the winning team names.

        Raises:
            TypeError: If any of the input arguments have incorrect types.
        """
        if not isinstance(tournament_schedule, pd.DataFrame):
            raise TypeError("tournament_schedule must be a pandas DataFrame")
        if not isinstance(points_for_a_win, int):
            raise TypeError("points_for_a_win must be an integer")
        if not isinstance(points_for_a_no_result, int):
            raise TypeError("points_for_a_no_result must be an integer")
        if not isinstance(points_for_a_draw, int):
            raise TypeError("points_for_a_draw must be an integer")
        if not isinstance(tournament_schedule_away_team_column_name, str):
            raise TypeError("tournament_schedule_away_team_column_name must be a string")
        if not isinstance(tournament_schedule_home_team_column_name, str):
            raise TypeError("tournament_schedule_home_team_column_name must be a string")
        if not isinstance(tournament_schedule_match_number_column_name, str):
            raise TypeError("tournament_schedule_match_number_column_name must be a string")
        if not isinstance(tournament_schedule_winning_team_column_name, str):
            raise TypeError("tournament_schedule_winning_team_column_name must be a string")

    def _validate_schedule_dataframe_columns(self):
        """
        Validates whether the provided column names are matching with the tournament_schedule DataFrame.

        Raises:
            ValueError: If any provided column name is missing from the columns of tournament_schedule dataframe.
        """
        schedule_dataframe_columns = self.tournament_schedule.columns
        if self.tournament_schedule_away_team_column_name not in schedule_dataframe_columns:
            raise ValueError(
                f"tournament_schedule_away_team_column_name '{self.tournament_schedule_away_team_column_name}' is not found in tournament_schedule columns"
            )
        if self.tournament_schedule_home_team_column_name not in schedule_dataframe_columns:
            raise ValueError(
                f"tournament_schedule_home_team_column_name '{self.tournament_schedule_home_team_column_name}' is not found in tournament_schedule columns"
            )
        if self.tournament_schedule_match_number_column_name not in schedule_dataframe_columns:
            raise ValueError(
                f"tournament_schedule_match_number_column_name '{self.tournament_schedule_match_number_column_name}' is not found in tournament_schedule columns"
            )
        if self.tournament_schedule_winning_team_column_name not in schedule_dataframe_columns:
            raise ValueError(
                f"tournament_schedule_winning_team_column_name '{self.tournament_schedule_winning_team_column_name}' is not found in tournament_schedule columns"
            )
