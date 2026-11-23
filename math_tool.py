def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    result = a + b
    print("[TOOL EXECUTED] add_numbers")
    return result

def subtract_numbers(a: float, b: float) -> float:
    """Subtract b from a and return the result."""
    result = a - b
    print("[TOOL EXECUTED] subtract_numbers")
    return result

if __name__ == "__main__":
    print("Addition: ", add_numbers(25, 17))
    print("Subtraction: ", subtract_numbers(25, 17))