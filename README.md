# Web-Based Mastermind Codebreaker Game

## Description

Mastermind Codebreaker is a fun thinking game, now available as a web application! The objective is to guess a secret sequence of numbers within a limited number of attempts. The code is generated randomly at the start of each game and played directly in your web browser.

The core rules remain the same:
1.  The game generates a secret code (by default, 4 numbers long, each between 0 and 5).
2.  You enter your guess as a sequence of numbers.
3.  After each guess, you receive feedback:
    *   **Correct item(s) in the correct position:** How many numbers in your guess are the correct value AND in the exact same position.
    *   **Correct item(s) in the wrong position:** How many numbers in your guess are correct values present in the secret code, BUT in a different position. (Items counted for correct position are not re-counted here).
4.  Use this feedback to deduce the secret code within the allowed attempts (default is 10).

## Requirements

*   Python 3
*   Flask (`pip install Flask`)

## How to Run the Game

1.  **Ensure Python 3 and Pip are installed.**
2.  **Install Flask:**
    Open your terminal or command prompt and run:
    ```bash
    pip install Flask
    ```
3.  **Run the application:**
    Navigate to the directory where you have saved the game files and run:
    ```bash
    python app.py
    ```
4.  **Play in your browser:**
    Open a web browser and navigate to:
    ```
    http://127.0.0.1:5000/
    ```

## Files

*   `app.py`: The main Flask application file. You run this file to start the web server and play the game. It handles game routes, web interface logic, and session management.
*   `game_logic.py`: This file contains the core logic of the Mastermind game, including:
    *   Generating the secret code.
    *   Evaluating the player's guess against the secret code.
*   `test_game_logic.py`: This file contains unit tests for the functions in `game_logic.py` to ensure the core game mechanics work correctly.
*   `templates/index.html`: The HTML template that structures the game's user interface in the web browser.
*   `static/style.css`: The CSS file that provides styling for the game's web interface.

Happy guessing!
