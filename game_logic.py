import random

def generate_secret_code(length=4, num_options=6):
    """
    Generates a secret code for the Mastermind game.

    Args:
        length: The length of the code (default 4).
        num_options: The number of unique items to choose from (e.g., 6 for 0-5) (default 6).

    Returns:
        A list of random integers representing the secret code.
    """
    if length <= 0:
        raise ValueError("Length must be a positive integer.")
    if num_options <= 0:
        raise ValueError("Number of options must be a positive integer.")
    
    secret_code = [random.randint(0, num_options - 1) for _ in range(length)]
    return secret_code

def evaluate_guess(secret_code, guess):
    """
    Evaluates a guess against the secret code in a Mastermind-like game.

    Args:
        secret_code: A list of integers representing the secret code.
        guess: A list of integers representing the player's guess.

    Returns:
        A tuple (correct_position, correct_item_wrong_position):
            correct_position: The number of items that are the correct value AND in the correct position.
            correct_item_wrong_position: The number of items that are the correct value BUT in the wrong position.
    """
    if len(secret_code) != len(guess):
        raise ValueError("Secret code and guess must have the same length.")

    correct_position = 0
    correct_item_wrong_position = 0

    secret_code_copy = list(secret_code)
    guess_copy = list(guess)
    
    # First, check for correct items in correct positions
    for i in range(len(secret_code_copy)):
        if guess_copy[i] == secret_code_copy[i]:
            correct_position += 1
            # Mark these as already counted so they don't get counted again
            secret_code_copy[i] = -1 
            guess_copy[i] = -2 # Use different markers to avoid collision if -1 is a valid code item

    # Next, check for correct items in wrong positions
    for i in range(len(guess_copy)):
        if guess_copy[i] != -2: # If this guess item wasn't a correct position match
            if guess_copy[i] in secret_code_copy:
                correct_item_wrong_position += 1
                # Mark the matched item in secret_code_copy as counted
                secret_code_copy[secret_code_copy.index(guess_copy[i])] = -1
                
    return (correct_position, correct_item_wrong_position)
