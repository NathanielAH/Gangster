# Mastermind Codebreaker Game

## Description

Mastermind Codebreaker is a fun thinking game where you try to guess a secret code. The objective is to guess the secret sequence of numbers within a limited number of attempts. The code is generated randomly at the start of each game.

## How to Play

1.  The game will generate a secret code, which is a sequence of numbers. By default, this is **4 numbers long**, and each number can be **between 0 and 5** (inclusive).
2.  You will enter your guess as a sequence of numbers of the same length (e.g., `1234`).
3.  After each guess, you will receive feedback:
    *   **Correct item(s) in the correct position:** This tells you how many numbers in your guess are the correct value AND in the exact same position as in the secret code.
    *   **Correct item(s) in the wrong position:** This tells you how many numbers in your guess are correct values that exist in the secret code, BUT are in a different position than your guess. An item that is already counted for being in the correct position will not be counted again here.

4.  Use the feedback to deduce the secret code.
5.  You have a limited number of attempts (default is 10) to guess the code.

## How to Run the Game

1.  **Prerequisites:**
    *   You need to have Python installed on your system.

2.  **Running the game:**
    *   Open your terminal or command prompt.
    *   Navigate to the directory where you have saved the game files.
    *   Run the game using the following command:
        ```bash
        python main.py
        ```

## Files

*   `main.py`: This is the main application file. You run this file to play the game. It handles the game loop, user input, and displaying output.
*   `game_logic.py`: This file contains the core logic of the game, including:
    *   Generating the secret code.
    *   Evaluating the player's guess against the secret code.
*   `test_game_logic.py`: This file contains unit tests for the functions in `game_logic.py` to ensure they work correctly.

Happy guessing!
