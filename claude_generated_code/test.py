"""
Test module for the pi calculation function.
"""

import unittest
from main import calculate_pi_to_5th_digit


class TestPiCalculation(unittest.TestCase):
    """Test cases for pi calculation."""
    
    def test_pi_value_approximately_correct(self):
        """Test that pi is calculated to approximately 3.14159."""
        pi = calculate_pi_to_5th_digit()
        
        # Pi should be approximately 3.14159
        self.assertAlmostEqual(pi, 3.14159, places=5)
    
    def test_pi_is_between_bounds(self):
        """Test that pi is within expected bounds."""
        pi = calculate_pi_to_5th_digit()
        
        # Pi is between 3 and 4
        self.assertGreater(pi, 3)
        self.assertLess(pi, 4)
    
    def test_pi_is_greater_than_3_141(self):
        """Test that pi is greater than 3.141."""
        pi = calculate_pi_to_5th_digit()
        
        self.assertGreater(pi, 3.141)
    
    def test_pi_is_less_than_3_142(self):
        """Test that pi is less than 3.142."""
        pi = calculate_pi_to_5th_digit()
        
        self.assertLess(pi, 3.142)
    
    def test_pi_matches_known_value(self):
        """Test that pi matches the known value to 5 decimal places."""
        pi = calculate_pi_to_5th_digit()
        
        # Known value of pi to 5 decimal places
        expected_pi = 3.14159
        
        self.assertEqual(round(pi, 5), expected_pi)
    
    def test_pi_returns_float(self):
        """Test that the function returns a float."""
        pi = calculate_pi_to_5th_digit()
        
        self.assertIsInstance(pi, float)
    
    def test_multiple_calls_return_same_value(self):
        """Test that multiple calls return the same value."""
        pi1 = calculate_pi_to_5th_digit()
        pi2 = calculate_pi_to_5th_digit()
        
        self.assertEqual(pi1, pi2)


if __name__ == "__main__":
    unittest.main()
