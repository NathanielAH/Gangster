from game_logic import generate_secret_code, evaluate_guess

# Game Parameters
CODE_LENGTH = 4
NUM_OPTIONS = 6  # Digits 0 to 5
MAX_ATTEMPTS = 10

def play_game():
    """Runs the Mastermind game loop."""
    print(f"Welcome to Mastermind!")
    print(f"Try to guess the {CODE_LENGTH}-digit code. Each digit is between 0 and {NUM_OPTIONS - 1}.")
    print(f"You have {MAX_ATTEMPTS} attempts.")

    secret_code = generate_secret_code(CODE_LENGTH, NUM_OPTIONS)
    attempts = 0
    won = False

    while attempts < MAX_ATTEMPTS:
        attempts += 1
        print(f"\nAttempt {attempts}/{MAX_ATTEMPTS}")
        
        while True:
            try:
                guess_str = input(f"Enter your {CODE_LENGTH}-digit guess (e.g., {''.join(str(i) for i in range(CODE_LENGTH))}): ")
                if not guess_str.isdigit():
                    print("Invalid input. Please enter only digits.")
                    continue
                if len(guess_str) != CODE_LENGTH:
                    print(f"Invalid input. Guess must be {CODE_LENGTH} digits long.")
                    continue
                
                guess = [int(digit) for digit in guess_str]
                
                # Validate if digits are within the allowed range
                valid_guess = True
                for digit in guess:
                    if not (0 <= digit < NUM_OPTIONS):
                        print(f"Invalid input. Each digit must be between 0 and {NUM_OPTIONS - 1}.")
                        valid_guess = False
                        break
                if not valid_guess:
                    continue
                
                break # Valid input received
            except ValueError: # Should be caught by isdigit, but as a safeguard
                print("Invalid input. Please enter a sequence of digits.")
            except Exception as e: # Catch any other unexpected error during input
                print(f"An unexpected error occurred during input: {e}")


        correct_position, correct_item_wrong_position = evaluate_guess(secret_code, guess)

        print(f"Feedback: {correct_position} correct item(s) in the correct position.")
        print(f"          {correct_item_wrong_position} correct item(s) in the wrong position.")

        if correct_position == CODE_LENGTH:
            print(f"\nCongratulations! You guessed the code {secret_code} in {attempts} attempts!")
            won = True
            break
    
    if not won:
        print(f"\nGame Over! You ran out of attempts.")
        print(f"The secret code was: {secret_code}")

if __name__ == "__main__":
    play_game()
