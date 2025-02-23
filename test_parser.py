import pytest
from your_parser_module import parse, evaluate  # Replace with your actual module name

@pytest.mark.parametrize("expression, expected", [
    # Arithmetic Operators
    ("2 + 3", 5),
    ("10 - 4", 6),
    ("5 * 6", 30),
    ("20 / 4", 5),
    ("(5 + 3) * 2 - 4 / 2", 14),
    ("-5 + 2", -3),
    ("3 + 2 * 4", 11),
    ("-6 / 2", -3),

    # Logical Operators
    ("3 < 5 and 4 > 2", True),
    ("5 > 10 or 2 < 3", True),
    ("not 4 > 3", False),
    ("3 == 3 and 4 != 2", True),
    ("5 <= 10 or 8 >= 20", True),
    ("not (4 > 5 and 3 < 1)", True),
    ("3 == 3 and 4 == 4", True),
    ("5 < 2 or 7 > 10", False),

    # Bitwise Operators
    ("3 & 1", 1),
    ("3 | 1", 3),
    ("3 ^ 1", 2),
    ("~5", -6),
    ("5 << 2", 20),
    ("8 >> 2", 2),
    ("1024 & 512", 0),
    ("-5 << 2", -20),
    ("-5 >> 2", -2),

    # Conditional Expressions (If Statements)
    ("if 5 < 10 then 1 else 0 end", 1),
    ("if 5 < 10 then if 2 < 3 then 1 else 0 end else 0 end", 1),
    ("if 0 < 1 then 1 else 0 end", 1),
    ("if 2 < 3 then if 4 > 5 then 0 else 1 end else 2 end", 1),
    ("if 5 == 5 then 10 end", 10),

    # Edge Cases
    ("0 + 0", 0),
    ("5 * 0", 0),
    ("9999999 * 1234567", 12345668765463),
    ("0.0001 * 0.0002", 0.00000002),
    ("1 << 10", 1024)
])
def test_parser(expression, expected):
    parsed_expr = parse(expression)
    result = evaluate(parsed_expr)
    assert result == expected

@pytest.mark.parametrize("expression", [
    "5 / 0",  # Division by zero
    "3 + 'a'",  # Invalid operation: string + number
    "if 5 == 5 then 'hello' + 5 end"  # String + Number inside if
])
def test_invalid_cases(expression):
    with pytest.raises(Exception):  # Expecting an exception
        parsed_expr = parse(expression)
        evaluate(parsed_expr)
