"""
Custom Exceptions Module

This module defines custom exception classes used in the project.

Classes:
    InvalidScheduleDataError: Exception raised when the input schedule dataframe is invalid.
    NoQualifyingScenariosError: Exception raised when no qualifying scenarios are found for the given team.
    TournamentCompletionBelowCutoffError: Exception raised when the percentage of tournament completion is below the specified cutoff.
"""

class InvalidScheduleDataError(ValueError):
    """Exception raised when the input schedule dataframe is invalid."""

    def __init__(self, message="Invalid schedule data"):
        self.message = message
        super().__init__(self.message)


class NoQualifyingScenariosError(Exception):
    """Exception raised when no qualifying scenarios are found for the given team."""

    def __init__(self, message="No qualifying scenarios found"):
        self.message = message
        super().__init__(self.message)


class TournamentCompletionBelowCutoffError(Exception):
    """Exception raised when the percentage of tournament completion is below the specified cutoff."""

    def __init__(self, message="Percentage of tournament completion is below the specified cutoff."):
        self.message = message
        super().__init__(self.message)
