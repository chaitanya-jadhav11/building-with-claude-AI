"""
Module for calculating mathematical constants and values.
"""

from decimal import Decimal, getcontext


def calculate_pi_to_5th_digit():
    """
    Calculate pi to the 5th decimal digit using the Machin formula.
    
    The Machin formula is: pi/4 = 4*arctan(1/5) - arctan(1/239)
    
    Returns:
        float: Pi rounded to 5 decimal places (3.14159)
    """
    # Set precision high enough for accurate calculation
    getcontext().prec = 50
    
    # Calculate pi using the Machin formula
    # pi = 16*arctan(1/5) - 4*arctan(1/239)
    pi = 4 * (4 * arctan_taylor(Decimal(1) / Decimal(5)) 
              - arctan_taylor(Decimal(1) / Decimal(239)))
    
    return float(pi)


def arctan_taylor(x):
    """
    Calculate arctan(x) using Taylor series expansion.
    
    arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ...
    
    Args:
        x: Decimal number to calculate arctan for
        
    Returns:
        Decimal: The arctan value
    """
    power = x
    result = power
    i = 1
    
    # Iterate until convergence
    while True:
        i += 2
        power *= -x * x
        term = power / i
        
        if abs(term) < Decimal(10) ** -(getcontext().prec - 5):
            break
            
        result += term
    
    return result


if __name__ == "__main__":
    pi_value = calculate_pi_to_5th_digit()
    print(f"Pi to 5th digit: {pi_value}")
    print(f"Formatted: {pi_value:.5f}")
