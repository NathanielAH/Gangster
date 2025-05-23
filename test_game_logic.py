import unittest
from game_logic import generate_secret_code, evaluate_guess

class TestGameLogic(unittest.TestCase):

    def test_generate_secret_code_length(self):
        """Test that generated code has the specified length."""
        self.assertEqual(len(generate_secret_code(length=5, num_options=6)), 5)
        self.assertEqual(len(generate_secret_code(length=3, num_options=3)), 3)
        self.assertEqual(len(generate_secret_code(length=1, num_options=1)), 1) # Edge case

    def test_generate_secret_code_options_range(self):
        """Test that items in generated code are within the specified num_options range."""
        length = 4
        num_options = 3  # Valid options: 0, 1, 2
        for _ in range(10): # Run multiple times to increase chance of catching errors
            code = generate_secret_code(length, num_options)
            self.assertEqual(len(code), length) # Also check length here
            for item in code:
                self.assertTrue(0 <= item < num_options, f"Item {item} out of range [0, {num_options-1}]")
        
        num_options_large = 10
        length_large = 10
        for _ in range(10):
            code = generate_secret_code(length_large, num_options_large)
            self.assertEqual(len(code), length_large)
            for item in code:
                self.assertTrue(0 <= item < num_options_large, f"Item {item} out of range [0, {num_options_large-1}]")

    def test_generate_secret_code_invalid_inputs(self):
        """Test that generate_secret_code raises ValueError for invalid inputs."""
        with self.assertRaises(ValueError):
            generate_secret_code(length=0, num_options=5)
        with self.assertRaises(ValueError):
            generate_secret_code(length=-1, num_options=5)
        with self.assertRaises(ValueError):
            generate_secret_code(length=4, num_options=0)
        with self.assertRaises(ValueError):
            generate_secret_code(length=4, num_options=-1)

    def test_evaluate_guess_no_matches(self):
        """Test evaluation when there are no matches."""
        secret_code = [1, 2, 3, 4]
        guess = [0, 0, 0, 0]
        self.assertEqual(evaluate_guess(secret_code, guess), (0, 0))

        secret_code = [1, 2, 3, 4]
        guess = [5, 6, 7, 8] # Different non-matching numbers
        self.assertEqual(evaluate_guess(secret_code, guess), (0, 0))

    def test_evaluate_guess_all_correct_position(self):
        """Test evaluation when all items are in the correct position."""
        secret_code = [1, 2, 3, 4]
        guess = [1, 2, 3, 4]
        self.assertEqual(evaluate_guess(secret_code, guess), (4, 0))

        secret_code = [0, 0, 0, 0]
        guess = [0, 0, 0, 0]
        self.assertEqual(evaluate_guess(secret_code, guess), (4, 0))

    def test_evaluate_guess_all_correct_item_wrong_position(self):
        """Test evaluation when all items are correct but in wrong positions."""
        secret_code = [1, 2, 3, 4]
        guess = [4, 3, 2, 1]
        self.assertEqual(evaluate_guess(secret_code, guess), (0, 4))

        secret_code = [1, 2, 1, 2]
        guess = [2, 1, 2, 1]
        self.assertEqual(evaluate_guess(secret_code, guess), (0, 4))

    def test_evaluate_guess_mixed_results(self):
        """Test evaluation with a mix of correct position and correct item/wrong position."""
        secret_code = [1, 2, 3, 4]
        guess = [1, 4, 2, 3]  # 1 correct_pos (1), 3 correct_item_wrong_pos (4,2,3)
        self.assertEqual(evaluate_guess(secret_code, guess), (1, 3))

        secret_code = [5, 0, 5, 0]
        guess = [5, 5, 0, 0] # First 5 is correct_pos. Second 0 is correct_pos.
                             # One 5 in guess is correct_item_wrong_pos. One 0 in guess is correct_item_wrong_pos.
        self.assertEqual(evaluate_guess(secret_code, guess), (2, 2))


    def test_evaluate_guess_duplicates_in_secret(self):
        """Test evaluation with duplicate items in the secret code."""
        secret_code = [1, 1, 2, 3]
        guess = [1, 4, 1, 1] 
        # Expected: (1,1)
        # First '1' in guess is correct_pos.
        # One of the remaining '1's in guess matches the second '1' in secret_code for correct_item_wrong_pos.
        self.assertEqual(evaluate_guess(secret_code, guess), (1, 1))
        
        secret_code = [1, 1, 1, 3]
        guess = [1, 1, 4, 1]
        # Expected: (2,1)
        # First two '1's in guess are correct_pos.
        # The third '1' in guess matches the third '1' in secret_code for correct_item_wrong_pos.
        self.assertEqual(evaluate_guess(secret_code, guess), (2, 1))

    def test_evaluate_guess_duplicates_in_guess(self):
        """Test evaluation with duplicate items in the guess."""
        secret_code = [1, 2, 3, 4]
        guess = [1, 1, 1, 1]  # First '1' is correct_pos. No other '1's in secret.
        self.assertEqual(evaluate_guess(secret_code, guess), (1, 0))

        secret_code = [1, 2, 1, 4]
        guess = [1, 1, 1, 1] # First '1' is correct_pos. One '1' from guess for second '1' in secret (correct_item_wrong_pos).
        self.assertEqual(evaluate_guess(secret_code, guess), (1, 1))


    def test_evaluate_guess_complex_duplicates(self):
        """Test more complex scenarios with duplicates."""
        secret_code = [0, 1, 0, 2]
        guess = [0, 0, 3, 4] 
        # Expected: (1,1)
        # First 0 in guess is correct_pos.
        # Second 0 in guess matches second 0 in secret_code (which is at index 2) for correct_item_wrong_pos.
        self.assertEqual(evaluate_guess(secret_code, guess), (1, 1))

        secret_code = [1, 1, 2, 2]
        guess = [1, 2, 1, 2]
        # Expected: (2,2)
        # First 1 in guess is correct_pos.
        # Second 2 in guess is correct_pos.
        # Second 1 in guess is correct_item_wrong_pos (matches second 1 in secret).
        # First 2 in guess is correct_item_wrong_pos (matches first 2 in secret).
        self.assertEqual(evaluate_guess(secret_code, guess), (2, 2))


    def test_evaluate_guess_no_double_counting(self):
        """Test that items are not double-counted."""
        secret_code = [1, 2, 3, 4]
        guess = [1, 1, 2, 2]
        # Expected: (1,1)
        # First '1' in guess is correct_pos.
        # One '2' from guess is correct_item_wrong_pos (matches '2' in secret).
        # The other '1' and '2' in guess have no corresponding match.
        self.assertEqual(evaluate_guess(secret_code, guess), (1, 1))

        secret_code = [1, 1, 1, 1]
        guess = [1, 2, 1, 2]
        # Expected: (2,0)
        # First '1' in guess is correct_pos.
        # Third '1' (at index 2) in guess is correct_pos.
        # The '2's do not match anything.
        self.assertEqual(evaluate_guess(secret_code, guess), (2, 0))
        
        secret_code = [1, 2, 3, 1]
        guess = [1, 1, 1, 1]
        # Expected: (2,0)
        # First '1' in guess is correct_pos (matches first '1' in secret).
        # Fourth '1' in guess is correct_pos (matches second '1' in secret at index 3).
        # The other two '1's in guess have no unmatched '1's in secret.
        self.assertEqual(evaluate_guess(secret_code, guess), (2, 0))

    def test_evaluate_guess_from_example(self):
        """Test based on a common Mastermind example."""
        # Example from a well-known source or common understanding
        secret_code = [1, 2, 3, 4] # Secret: Red, Green, Blue, Yellow
        guess = [1, 1, 2, 2]       # Guess: Red, Red, Green, Green
        # Expected: (1, 1)
        # One correct position (the first Red).
        # One correct color in wrong position (one Green in the guess matches Green in secret).
        # The second Red in guess has no match. The second Green in guess has no match (as the secret Green is already used for wrong position).
        self.assertEqual(evaluate_guess(secret_code, guess), (1, 1))

    def test_evaluate_guess_empty_lists(self):
        """Test evaluation with empty lists (should ideally be handled by length check)."""
        # Assuming game logic implies non-empty codes, but good to define behavior.
        # The current evaluate_guess raises ValueError if lengths differ.
        # If lengths are same and 0, it should be (0,0).
        secret_code = []
        guess = []
        self.assertEqual(evaluate_guess(secret_code, guess), (0, 0))

    def test_evaluate_guess_invalid_input_lengths(self):
        """Test that evaluate_guess raises ValueError for lists of different lengths."""
        with self.assertRaises(ValueError):
            evaluate_guess([1, 2, 3], [1, 2])
        with self.assertRaises(ValueError):
            evaluate_guess([1, 2], [1, 2, 3])

if __name__ == '__main__':
    unittest.main()
