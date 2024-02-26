# pylint: disable = missing-module-docstring

import itertools
from typing import List, Tuple
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

    def simulate_the_qualification_scenarios(
        self, team_name: str, top_x_position_in_the_table: int, desired_number_of_scenarios: int = 3
    ) -> Tuple[List[pd.DataFrame], List[pd.DataFrame]]:

        list_of_points_tables_for_qualification_scenarios = []
        list_of_remaining_match_result_for_qualification_scenarios = []

        remaining_matches_in_the_schedule = self._find_remaining_matches_in_the_schedule()
        match_number_of_the_first_remaining_match = len(self.tournament_schedule) - len(remaining_matches_in_the_schedule) + 1
        list_of_possible_results_for_remaining_matches = list(itertools.product(*remaining_matches_in_the_schedule))

        initial_points_table = self.current_points_table

        for possible_results_for_remaining_matches in list_of_possible_results_for_remaining_matches:
            temporary_schedule_df = self.tournament_schedule.copy()
            updated_points_table = initial_points_table.copy()

            for match_number, possible_winning_team in enumerate(possible_results_for_remaining_matches):
                home_team, away_team = remaining_matches_in_the_schedule[match_number]
                temporary_schedule_df.loc[
                    match_number_of_the_first_remaining_match + match_number - 1, self.tournament_schedule_winning_team_column_name
                ] = possible_winning_team
                updated_points_table = self._update_points_table(
                    updated_points_table, home_team, away_team, possible_winning_team
                )

            updated_points_table.sort_values(by="points", ascending=False, inplace=True)
            updated_points_table.reset_index(drop=True, inplace=True)

            if team_name in updated_points_table["team"].values[:top_x_position_in_the_table]:
                list_of_points_tables_for_qualification_scenarios.append(updated_points_table)
                list_of_remaining_match_result_for_qualification_scenarios.append(temporary_schedule_df)

            if len(list_of_points_tables_for_qualification_scenarios) >= desired_number_of_scenarios:
                break

        return list_of_points_tables_for_qualification_scenarios, list_of_remaining_match_result_for_qualification_scenarios

    def _find_remaining_matches_in_the_schedule(self) -> List[Tuple[str]]:
        remaining_matches_df = self.tournament_schedule[
            self.tournament_schedule[self.tournament_schedule_winning_team_column_name].fillna("") == ""
        ]
        remaining_matches = list(remaining_matches_df.apply(
            lambda row: (row[self.tournament_schedule_home_team_column_name], row[self.tournament_schedule_away_team_column_name]),
            axis=1
        ))
        return remaining_matches

    def _update_points_table(
        self, points_table: pd.DataFrame, home_team: str, away_team: str, winning_team: str
    ) -> pd.DataFrame:
        points_table.loc[points_table["team"] == winning_team, "matches_won"] += 1
        points_table.loc[points_table['team'] == winning_team, 'points'] += self.points_for_a_win
        points_table.loc[points_table['team'] == home_team, 'matches_played'] += 1
        points_table.loc[points_table['team'] == away_team, 'matches_played'] += 1
        return points_table

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
