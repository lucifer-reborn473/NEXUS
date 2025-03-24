import pytest
from depreciated.calci import *


def test_basic_expression():
    expr = "var integer x= (2+ 1)"
    val = e(parse(expr))
    assert val == "Context(variables={'x': VariableInfo(value=3, dtype='integer', redundant=None)})"

# if __name__ == "__main__":
#     pytest.main()
e(parse("display (2 + 3)"))  
e(parse("display (10 - 4)"))  
e(parse("display (5 * 6)"))  
e(parse("display (20 / 4)"))  
e(parse("display ((5 + 3) * 2 - 4 / 2)"))  
e(parse("display (-5 + 2)"))  
e(parse("display (3 * (4 + 2) / 3 - 1)"))  
e(parse("display (3 + 2 * 4)"))  
e(parse("display (-6 / 2)"))  

# Logical Operators
e(parse("display (3 < 5 and 4 > 2)"))  
e(parse("display (5 > 10 or 2 < 3)"))  
e(parse("display (not 4 > 3)"))  
e(parse("display (3 == 3 and 4 != 2)"))  
e(parse("display (5 <= 10 or 8 >= 20)"))  
e(parse("display (not (4 > 5 and 3 < 1))"))  
e(parse("display (3 == 3 and 4 == 4)"))  
e(parse("display (5 < 2 or 7 > 10)"))  

# Bitwise Operators
e(parse("display (3 & 1)"))  
e(parse("display (3 | 1)"))  
e(parse("display (3 ^ 1)"))  
e(parse("display (~5)"))  
e(parse("display (5 << 2)"))  
e(parse("display (8 >> 2)"))  
e(parse("display (1024 & 512)"))  
e(parse("display (-5 << 2)"))  
e(parse("display (-5 >> 2)"))  

# Variable Definitions
e(parse("display ('hello world')"))  
e(parse("display ('a' + 'b')"))  
e(parse("display ('num' + 5)"))  # Should throw error
e(parse("display ('5')"))  

# Conditional Expressions (If Statements)
e(parse("display (if 5 < 10 then 1 else 0 end)"))
e(parse("display (if 5 < 10 then if 2 < 3 then 1 else 0 end else 0 end)"))
e(parse("display (if 0 < 1 then 1 else 0 end)"))
e(parse("display (if 2 < 3 then if 4 > 5 then 0 else 1 end else 2 end)"))
e(parse("display (if 5 == 5 then 10 end)"))

# Recursive Functions (Factorial Simulation)
expr = """
if 5 == 0 then 1 
else 5 * (if 4 == 0 then 1 else 4 * (if 3 == 0 then 1 else 3 * (if 2 == 0 then 1 else 2 * (if 1 == 0 then 1 else 1)))) end
"""
e(parse(expr))

# Edge Cases
e(parse("display (5 / 0)"))  # Division by zero
e(parse("display (3 + 'a')"))  # Invalid operation
e(parse("display (9999999 * 1234567)"))  # Large numbers
e(parse("display (0.0001 * 0.0002)"))  # Small numbers
e(parse("display (1 << 1024)"))  # Extremely large shift
e(parse("display (5 == 5 and 'a' == 'a')"))  # Comparison with string
print(parse(expr))
e(parse(expr))