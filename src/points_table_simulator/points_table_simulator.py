# pylint: disable = missing-module-docstring

from typing import List
import pandas as pd


class PointsTableSimulator:     # pylint: disable = too-many-instance-attributes

    """
    PointsTableSimulator

    A class for simulating and calculating points table for a tournament based on provided schedule and points system.

    Args:
        tournament_schedule (pd.DataFrame): DataFrame containing the schedule of the tournament matches.
        points_for_a_win (int): Points awarded for a win.
        points_for_a_no_result (int, optional): Points awarded for a match with no result. Default is 1.
        points_for_a_draw (int, optional): Points awarded for a draw. Default is 1.
        tournament_schedule_away_team_column_name (str, optional): Name of the column in the schedule DataFrame
            containing the away team names. Default is "away".
        tournament_schedule_home_team_column_name (str, optional): Name of the column in the schedule DataFrame
            containing the home team names. Default is "home".
        tournament_schedule_match_number_column_name (str, optional): Name of the column in the schedule DataFrame
            containing the match numbers. Default is "match_number".
        tournament_schedule_winning_team_column_name (str, optional): Name of the column in the schedule DataFrame
            containing the winning team names. Default is "winner".

    Attributes:
        tournament_schedule (pd.DataFrame): DataFrame containing the schedule of the tournament matches.
        points_for_a_win (int): Points awarded for a win.
        points_for_a_no_result (int): Points awarded for a match with no result.
        points_for_a_draw (int): Points awarded for a draw.
        tournament_schedule_away_team_column_name (str): Name of the column in the schedule DataFrame
            containing the away team names.
        tournament_schedule_home_team_column_name (str): Name of the column in the schedule DataFrame
            containing the home team names.
        tournament_schedule_match_number_column_name (str): Name of the column in the schedule DataFrame
            containing the match numbers.
        tournament_schedule_winning_team_column_name (str): Name of the column in the schedule DataFrame
            containing the winning team names.

    Methods:
        current_points_table(): Calculates the current points table based on the provided tournament schedule.

    """

    def __init__(       # pylint: disable = too-many-arguments
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
            tournament_schedule_away_team_column_name=tournament_schedule_away_team_column_name,
            tournament_schedule_home_team_column_name=tournament_schedule_home_team_column_name,
            tournament_schedule_match_number_column_name=tournament_schedule_match_number_column_name,
            tournament_schedule_winning_team_column_name=tournament_schedule_winning_team_column_name
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

    @property
    def current_points_table(self) -> pd.DataFrame:
        """
        Calculates the current points table based on the provided tournament schedule.

        Returns:
            pd.DataFrame: DataFrame containing the current points table with the following columns:
                - 'team': The name of the team.
                - 'matches_played': The total number of matches played by the team.
                - 'matches_won': The total number of matches won by the team.
                - 'matches_lost': The total number of matches lost by the team.
                - 'matches_drawn': The total number of matches drawn by the team.
                - 'matches_with_no_result': The total number of matches with no result for the team.
                - 'remaining_matches': The total number of remaining matches for the team.
                - 'points': The total points earned by the team based on wins, draws, and no results.
        """

        team_points_data: List = []

        teams: set = set(self.tournament_schedule[self.tournament_schedule_away_team_column_name].unique()).union(
            set(self.tournament_schedule[self.tournament_schedule_home_team_column_name].unique())
        )

        for team in teams:
            matches_played: int = len(self.tournament_schedule[
                (
                    (self.tournament_schedule[self.tournament_schedule_away_team_column_name] == team) |
                    (self.tournament_schedule[self.tournament_schedule_home_team_column_name] == team)
                ) &
                (
                    (self.tournament_schedule[self.tournament_schedule_winning_team_column_name].fillna("") != "")
                )
            ])

            matches_won: int = len(self.tournament_schedule[
                (self.tournament_schedule[self.tournament_schedule_winning_team_column_name] == team)
            ])

            matches_lost: int = len(self.tournament_schedule[
                (
                    (self.tournament_schedule[self.tournament_schedule_away_team_column_name] == team) |
                    (self.tournament_schedule[self.tournament_schedule_home_team_column_name] == team)
                ) &
                (
                    (self.tournament_schedule[self.tournament_schedule_winning_team_column_name] != team) &
                    (self.tournament_schedule[self.tournament_schedule_winning_team_column_name].fillna("") != "")
                )
            ])

            matches_drawn: int = len(self.tournament_schedule[
                ((self.tournament_schedule[self.tournament_schedule_away_team_column_name] == team) |
                (self.tournament_schedule[self.tournament_schedule_home_team_column_name] == team)) &
                (self.tournament_schedule[self.tournament_schedule_winning_team_column_name] == "Draw")
            ])

            matches_with_no_result: int = len(self.tournament_schedule[
                ((self.tournament_schedule[self.tournament_schedule_away_team_column_name] == team) |
                (self.tournament_schedule[self.tournament_schedule_home_team_column_name] == team)) &
                (self.tournament_schedule[self.tournament_schedule_winning_team_column_name] == "No Result")
            ])

            remaining_matches: int = len(self.tournament_schedule[
                (
                    (self.tournament_schedule[self.tournament_schedule_away_team_column_name] == team) |
                    (self.tournament_schedule[self.tournament_schedule_home_team_column_name] == team)
                ) &
                (
                    (self.tournament_schedule[self.tournament_schedule_winning_team_column_name].fillna("") == "")
                )
            ])

            points: int = (matches_won * self.points_for_a_win) + (matches_drawn * self.points_for_a_draw) + \
                (matches_with_no_result * self.points_for_a_no_result)

            team_points_data.append({
                "team": team,
                "matches_played": matches_played,
                "matches_won": matches_won,
                "matches_lost": matches_lost,
                "matches_drawn": matches_drawn,
                "matches_with_no_result": matches_with_no_result,
                "remaining_matches": remaining_matches,
                "points": points
            })

        current_points_table = pd.DataFrame(team_points_data)
        current_points_table.sort_values(by="points", ascending=False, inplace=True)
        current_points_table.reset_index(drop=True, inplace=True)

        return current_points_table

    @staticmethod
    def _validate_input_types(
        tournament_schedule: pd.DataFrame,
        points_for_a_win: int,
        points_for_a_no_result: int,
        points_for_a_draw: int,
        **kwargs
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
        for key, value in kwargs.items():
            if not isinstance(value, str):
                raise TypeError(f"{key} must be a string")

    def _validate_schedule_dataframe_columns(self):
        """
        Validates whether the provided column names are matching with the tournament_schedule DataFrame.

        Raises:
            ValueError: If any provided column name is missing from the columns of tournament_schedule dataframe.
        """
        schedule_dataframe_columns = self.tournament_schedule.columns
        if self.tournament_schedule_away_team_column_name not in schedule_dataframe_columns:
            raise ValueError(
                f"tournament_schedule_away_team_column_name '{self.tournament_schedule_away_team_column_name}' \
                    is not found in tournament_schedule columns"
            )
        if self.tournament_schedule_home_team_column_name not in schedule_dataframe_columns:
            raise ValueError(
                f"tournament_schedule_home_team_column_name '{self.tournament_schedule_home_team_column_name}' \
                    is not found in tournament_schedule columns"
            )
        if self.tournament_schedule_match_number_column_name not in schedule_dataframe_columns:
            raise ValueError(
                f"tournament_schedule_match_number_column_name '{self.tournament_schedule_match_number_column_name}' \
                    is not found in tournament_schedule columns"
            )
        if self.tournament_schedule_winning_team_column_name not in schedule_dataframe_columns:
            raise ValueError(
                f"tournament_schedule_winning_team_column_name '{self.tournament_schedule_winning_team_column_name}' \
                    is not found in tournament_schedule columns"
            )
