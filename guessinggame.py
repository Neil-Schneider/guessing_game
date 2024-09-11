"""A simple guessing game implemented using Streamlit.

Copyright (c) 2024 Neil Schneider
"""

import secrets

import streamlit as st

# Initialize session state variables
if 'number_to_guess' not in st.session_state:
    st.session_state.number_to_guess = secrets.randbelow(10) + 1
if 'score' not in st.session_state:
    st.session_state.score = 0


def reset_game() -> None:
    """Reset the game by selecting a new random number."""
    st.session_state.number_to_guess = secrets.randbelow(10) + 1


# Streamlit app layout
st.title('Guessing Game')
st.write('I have selected a number between 1 and 10. Can you guess it?')

# User input for guessing the number
user_guess = st.number_input('Enter your guess:', min_value=1, max_value=10, step=1, format='%d')

# Button to submit the guess
if st.button('Submit Guess'):
    if user_guess == st.session_state.number_to_guess:
        st.success('Congratulations! You guessed the correct number.')
        st.session_state.score += 1
        reset_game()
    else:
        st.error(
            f"Sorry, that's not correct. The correct number was {st.session_state.number_to_guess}. "
            'Try again!',
        )
        reset_game()

# Display the score
st.write(f'Your score: {st.session_state.score}')

# Button to reset the game manually
if st.button('Reset Game'):
    reset_game()
    st.session_state.score = 0
    st.success('The game has been reset. Try guessing the new number!')
