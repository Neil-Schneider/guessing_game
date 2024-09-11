"""Unit tests for the guessing game application.

Copyright (c) 2024 Neil Schneider
"""

import secrets

import pytest
import streamlit as st

import guessinggame

# Constants
MAX_GUESS_NUMBER = 10


# Mocking Streamlit's session state
class MockSessionState:
    """Mock session state for testing Streamlit applications."""

    def __init__(self) -> None:
        """Initialize the mock session state."""
        self.number_to_guess: int = secrets.randbelow(MAX_GUESS_NUMBER) + 1
        self.score: int = 0

    def __setattr__(self, key: str, value: any) -> None:
        """Set an attribute in the mock session state."""
        self.__dict__[key] = value

    def __getattr__(self, item: str) -> any:
        """Get an attribute from the mock session state."""
        return self.__dict__.get(item, None)


@pytest.fixture()
def session_state(monkeypatch: pytest.MonkeyPatch) -> MockSessionState:
    """Fixture to provide a mock session state."""
    state = MockSessionState()
    monkeypatch.setattr(st, 'session_state', state)
    return state


def test_initial_state(session_state: MockSessionState) -> None:
    """Test the initial state of the session."""
    assert 1 <= session_state.number_to_guess <= MAX_GUESS_NUMBER
    assert session_state.score == 0


def test_correct_guess(session_state: MockSessionState, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test behavior when the correct guess is made."""
    number = session_state.number_to_guess
    monkeypatch.setattr(st, 'number_input', lambda *_args, **_kwargs: number)
    monkeypatch.setattr(st, 'button', lambda label: label == 'Submit Guess')

    guessinggame.st.button('Submit Guess')  # Simulate button press

    assert session_state.score == 1


def test_incorrect_guess(session_state: MockSessionState, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test behavior when an incorrect guess is made."""
    number = session_state.number_to_guess
    incorrect_guess = number + 1 if number < MAX_GUESS_NUMBER else number - 1
    monkeypatch.setattr(st, 'number_input', lambda *_args, **_kwargs: incorrect_guess)
    monkeypatch.setattr(st, 'button', lambda label: label == 'Submit Guess')

    guessinggame.st.button('Submit Guess')  # Simulate button press

    assert session_state.score == 0
    assert session_state.number_to_guess != number  # Check if the number to guess was reset


def test_reset_game(session_state: MockSessionState, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test resetting the game."""
    monkeypatch.setattr(st, 'button', lambda label: label == 'Reset Game')

    guessinggame.st.button('Reset Game')  # Simulate button press

    assert session_state.score == 0
    assert 1 <= session_state.number_to_guess <= MAX_GUESS_NUMBER
