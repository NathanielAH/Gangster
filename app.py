from flask import Flask, render_template, request, session, redirect, url_for
from game_logic import generate_secret_code, evaluate_guess

# Initialize the Flask application
app = Flask(__name__)

# Secret key for session management
app.secret_key = 'supersecretdevkey' # Keep this, or use a more secure key

# Game Parameters
CODE_LENGTH = 4
NUM_OPTIONS = 6  # Digits 0 to 5
MAX_ATTEMPTS = 10

@app.route('/', methods=['GET', 'POST'])
def home():
    message = None
    error_message = None
    game_over = False

    if request.method == 'GET':
        # --- Game Initialization (or continuation) ---
        if 'secret_code' not in session or 'attempts_remaining' not in session:
            session['secret_code'] = generate_secret_code(CODE_LENGTH, NUM_OPTIONS)
            session['attempts_remaining'] = MAX_ATTEMPTS
            session['history'] = [] # Stores list of dicts: {'guess': [], 'correct_position': #, 'correct_item_wrong_position': #}
            message = f"Welcome! Guess the {CODE_LENGTH}-digit code. Each digit is between 0 and {NUM_OPTIONS - 1}."
        
        # If game was over and user revisits, effectively start a new game by re-initializing
        if session.get('game_over_flag', False):
            session['secret_code'] = generate_secret_code(CODE_LENGTH, NUM_OPTIONS)
            session['attempts_remaining'] = MAX_ATTEMPTS
            session['history'] = []
            session['game_over_flag'] = False # Reset flag
            message = f"New Game Started! Guess the {CODE_LENGTH}-digit code. Each digit is between 0 and {NUM_OPTIONS - 1}."

    elif request.method == 'POST':
        # --- Guess Handling ---
        if 'secret_code' not in session or session.get('game_over_flag', False): # Prevent submissions if game not started or already over
            return redirect(url_for('home'))

        guess_str = request.form.get('guess', '')
        
        # Basic Input Validation
        if not guess_str.isdigit() or len(guess_str) != CODE_LENGTH:
            error_message = f"Invalid guess. Please enter exactly {CODE_LENGTH} digits."
        else:
            guess_list_int = [int(digit) for digit in guess_str]
            
            valid_guess = True
            for digit in guess_list_int:
                if not (0 <= digit < NUM_OPTIONS):
                    error_message = f"Invalid guess. Each digit must be between 0 and {NUM_OPTIONS - 1}."
                    valid_guess = False
                    break
            
            if valid_guess:
                session['attempts_remaining'] -= 1
                
                correct_position, correct_item_wrong_position = evaluate_guess(session['secret_code'], guess_list_int)
                
                current_guess_feedback = {
                    'guess': guess_str, # Store string version for easy display
                    'correct_position': correct_position,
                    'correct_item_wrong_position': correct_item_wrong_position
                }
                session['history'].append(current_guess_feedback)
                session.modified = True # Important when mutating session lists/dicts

                if correct_position == CODE_LENGTH:
                    message = f"Congratulations! You guessed the code {session['secret_code']} in {MAX_ATTEMPTS - session['attempts_remaining']} attempts!"
                    game_over = True
                    session['game_over_flag'] = True
                elif session['attempts_remaining'] <= 0:
                    message = f"Game Over! The secret code was {session['secret_code']}."
                    game_over = True
                    session['game_over_flag'] = True
                else:
                    message = f"Feedback: {correct_position} correct position, {correct_item_wrong_position} correct item (wrong position)."

    # --- Render Template ---
    # Ensure all variables passed to template are defined even if not used in all branches (e.g. for initial GET)
    return render_template('index.html', 
                           message=message,
                           error_message=error_message,
                           attempts_remaining=session.get('attempts_remaining'),
                           history=session.get('history'),
                           game_over=game_over)

if __name__ == '__main__':
    # Runs the app on a local development server.
    # Debug=True is helpful for development as it provides detailed error pages and auto-reloads on code changes.
    app.run(debug=True)
