"""
Custom Exceptions Module

This module defines custom exception classes used in the project.

Classes:
    NoQualifyingScenariosError: Exception raised when no qualifying scenarios are found for the given team.
"""

class NoQualifyingScenariosError(Exception):
    """Exception raised when no qualifying scenarios are found for the given team."""

    def __init__(self, message="No qualifying scenarios found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
